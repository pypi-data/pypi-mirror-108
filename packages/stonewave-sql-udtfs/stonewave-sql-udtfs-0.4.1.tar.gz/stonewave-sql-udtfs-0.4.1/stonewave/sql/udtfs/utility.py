import pyarrow as pa


def get_arrow_data_type_from_value(value):
    if not value:
        return pa.utf8()
    else:
        # bool needs to be placed before int because isinstance(True, int) == True
        if isinstance(value, bool):
            return pa.bool_()
        elif isinstance(value, int):
            return pa.int64()
        elif isinstance(value, float):
            return pa.float64()
        # elif isinstance(value, decimal.Decimal):
        # return pa.decimal128(13)
        else:
            return pa.utf8()
