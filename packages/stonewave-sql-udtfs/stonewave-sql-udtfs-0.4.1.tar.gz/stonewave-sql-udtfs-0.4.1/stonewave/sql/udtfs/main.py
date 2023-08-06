import json
import os
import argparse
from re import sub
import sys
import pkgutil
import toml
from distutils.util import strtobool
from stonewave.sql.udtfs.function_executor import execute
from stonewave.sql.udtfs.constants import USER_DEFINED_TABLE_FUNCTIONS_PATH
from stonewave.sql.udtfs.logger import logger
import stonewave.sql.udtfs.functions as built_in_funcs
from wheel_filename import parse_wheel_filename
from stonewave.sql.udtfs.test_utility import check_expected_parameters_list
from stonewave.sql.udtfs.load_function import load_function_by_name
from stonewave.sql.udtfs.version import sql_udtfs_version


def _list_udtfs_from_path(path, udtfs_list):
    try:
        for importer, modname, _ in pkgutil.iter_modules(path):
            info_path = os.path.join(importer.path, modname, "infos.toml")
            if not os.path.exists(info_path):
                logger.error("can not load function information", function_name=modname, info_path=info_path)
                continue
            info_toml = toml.load(info_path)
            udtfs_list[modname] = info_toml["params"]
    except Exception as e:
        logger.error("load udtfs error", path=path, error=str(e))


def list_udtfs():
    if not os.path.exists(USER_DEFINED_TABLE_FUNCTIONS_PATH):
        os.mkdir(USER_DEFINED_TABLE_FUNCTIONS_PATH)
    udtfs_list = {}
    _list_udtfs_from_path(built_in_funcs.__path__, udtfs_list)
    _list_udtfs_from_path([USER_DEFINED_TABLE_FUNCTIONS_PATH], udtfs_list)
    return udtfs_list


def list_udtfs_cmd(args):
    udtfs_list = list_udtfs()
    if args.output_path:
        with open(args.output_path, "w") as f:
            f.write(json.dumps(udtfs_list, indent=4))
    else:
        print(json.dumps(udtfs_list, indent=4))


def _validate_function(func_name):
    sys.path.append("/tmp")
    func = load_function_by_name(func_name)
    if func is None:
        raise Exception("Can not find method implements for BaseFunction from stonewave.sql.udtfs.base_function")
    func_dir = func().__dir__()
    if "get_name" not in func_dir or "process" not in func_dir:
        raise Exception("Invalid function class, please implement get_name(self) and process(self, )")
    os.system("rm -rf /tmp/{}/**/__pycache__".format(func_name))


def register_udtf(func_name, func_path):
    if not os.path.exists(USER_DEFINED_TABLE_FUNCTIONS_PATH):
        os.mkdir(USER_DEFINED_TABLE_FUNCTIONS_PATH)
    pwf = parse_wheel_filename(os.path.basename(func_path))
    # install package to temperary directory
    os.system("pip install {} -t /tmp/{}".format(func_path, func_name))
    os.system("mv /tmp/{0}/{1}/* /tmp/{0} && rm -rf /tmp/{0}/{1}".format(func_name, pwf.project))
    info_path = os.path.join("/tmp", func_name, "infos.toml")
    if not os.path.exists(info_path):
        logger.error("can not load function information", function_name=func_name, info_path="infos.toml")
        print({"status": "Failed", "error": "please include infos.toml for function information"})
        return
    info_toml = toml.load(info_path)
    params = info_toml["params"]
    check_expected_parameters_list(params)
    _validate_function(func_name)
    os.system("mv /tmp/{0} {1}/{0}".format(func_name, USER_DEFINED_TABLE_FUNCTIONS_PATH))


def register_udtf_cmd(args):
    func_name = args.function_name
    func_path = args.function_path
    register_udtf(func_name, func_path)


def exec_udtf_cmd(args):
    execute(args.function_name, input, sys.stdout)


def remove_udtf(function_name):
    os.system("rm -rf {}/{}".format(USER_DEFINED_TABLE_FUNCTIONS_PATH, function_name))


def remove_udtf_cmd(args):
    remove_udtf(args.function_name)


def execute_command():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        Command sw_py_udtf
        Usage Examples:

        1) exec
        $ sw_py_udtf exec --function-name <name>
        Execute function, please integrate to stonewave service. Function name is required.
        2) list 
        $ sw_py_udtf list --output-path <path>
        List all accessiable python table functions. Output path is not required. If no
        output path, with list all table functions to stdout.
        3) register
        $ sw_py_udtf register --function-name <name> --function-path <path>
        Function name and function path are required. currently only support file system path
        for user defined table function python wheel package
        4) remove
        $ sw_py_udtf exec --function-name remove
        Remove table function. Function name is required
        """,
    )
    parser.add_argument("-V", "--version", action="version", version=sql_udtfs_version())
    subparsers = parser.add_subparsers()

    exec_subparser = subparsers.add_parser("exec")
    exec_subparser.add_argument(
        "-n",
        "--function-name",
        required=True,
        type=str,
        help="user defined table function name",
    )
    exec_subparser.set_defaults(callback=exec_udtf_cmd)

    list_subparser = subparsers.add_parser("list")
    list_subparser.add_argument(
        "-o",
        "--output-path",
        default="",
        type=str,
        help="output udtfs list to specific path",
    )
    list_subparser.set_defaults(callback=list_udtfs_cmd)

    register_subparser = subparsers.add_parser("register")
    register_subparser.add_argument(
        "-n",
        "--function-name",
        required=True,
        type=str,
        help="user defined table function name",
    )
    register_subparser.add_argument(
        "-p",
        "--function-path",
        required=True,
        type=str,
        help="user defined table function package path",
    )
    register_subparser.set_defaults(callback=register_udtf_cmd)

    remove_subparser = subparsers.add_parser("remove")
    remove_subparser.add_argument(
        "-n",
        "--function-name",
        required=True,
        type=str,
        help="user defined table function name",
    )
    remove_subparser.set_defaults(callback=remove_udtf_cmd)

    args = parser.parse_args()
    args.callback(args)
