import json
import datetime
from functools import cmp_to_key
import os


def _format_epoch(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000000).strftime("%Y-%m-%d %H:%M:%S")


def _compare_slice(s1, s2):
    if s1["latest"] > s2["latest"] or s1["latest"] == s2["latest"] and s1["earliest"] > s2["earliest"]:
        return -1
    else:
        return 1


def _parse_slice_meta(slice_meta_file):
    with open(slice_meta_file, "r") as meta:
        slice_meta = meta.read()
        slices = json.loads(slice_meta)
        for slice in slices:
            slice["earliest"] = _format_epoch(slice["earliest_time"])
            slice["latest"] = _format_epoch(slice["latest_time"])
        return slices


def _add_slice_meta(all_metas, slice_meta_file, sub_dir=""):
    if os.path.exists(slice_meta_file):
        slices = _parse_slice_meta(slice_meta_file)
        if sub_dir:
            for slice in slices:
                slice["partition"] = sub_dir
        all_metas.extend(slices)


def load_stats(event_set_dir):
    sorted_slices = []
    if os.path.exists(event_set_dir):
        all_metas = []
        dirs = os.listdir(event_set_dir)
        for sub_dir in dirs:
            slice_meta_json = os.path.join(event_set_dir, sub_dir, "slice_meta.json")
            _add_slice_meta(all_metas, slice_meta_json, sub_dir)

        # the new version stores slice_meta.json in different location
        slice_meta_json = os.path.join(event_set_dir, "slice_meta.json")
        _add_slice_meta(all_metas, slice_meta_json)
        sorted_slices = sorted(all_metas, key=cmp_to_key(_compare_slice))
    return sorted_slices
