import pyarrow as pa
import os
import pandas as pd
from stonewave.sql.udtfs.base_function import BaseFunction, udtf
from stonewave.sql.udtfs.functions.slice_metas.slice_meta_loader import load_stats


class SliceMetasFunction(BaseFunction):
    def __init__(self):
        pass

    def get_name(self):
        return "slice_metas"

    def process(self, row_writer, row_idx, args):
        event_set = args[0]
        home = os.getenv("STONEWAVE_HOME")
        event_set_dir = os.path.join(home, "var", "event_sets", event_set)
        slice_metas = load_stats(event_set_dir)
        for slice_meta in slice_metas:
            slice_meta["event_set"] = event_set

        df = pd.DataFrame(slice_metas)
        table = pa.Table.from_pandas(df, preserve_index=False)
        batches = table.to_batches()
        row_writer.batch_iterator = iter(batches)
