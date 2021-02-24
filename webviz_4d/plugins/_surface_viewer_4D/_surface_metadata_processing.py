import json
import pandas as pd


def update_selections(selection_list: dict, metadata: pd.DataFrame):
    # print(json.dumps(selection_list, indent=4))
    # print(metadata["map_type"])
    print(selection_list["observed"])

    for maptype in ["observed", "simulated"]:
        df = metadata[metadata["map_type"] == maptype]
        selection_list[maptype].update({"interval": update_intervals(df)})
        selection_list[maptype].update({"name": update_names(df)})
        selection_list[maptype].update({"ensemble": update_ensemble(df)})
        selection_list[maptype].update({"attribute": update_attribute(df)})
        selection_list[maptype].update({"realization": update_realizations(df)})
    # print(json.dumps(selection_list, indent=4))
    return selection_list


def update_intervals(dframe):
    intervals = dframe[["data.time.t1", "data.time.t2"]].drop_duplicates()
    interval_list = [
        f"{t2[0:4]}-{t2[4:6]}-{t2[6:8]}-{t1[0:4]}-{t1[4:6]}-{t1[6:8]}"
        for t1, t2 in zip(
            list(intervals["data.time.t1"]), list(intervals["data.time.t2"])
        )
    ]
    return interval_list


def update_names(dframe):
    return list(dframe["data.name"].unique())


def update_ensemble(dframe):
    return list(dframe["fmu_id.ensemble"].unique())


def update_attribute(dframe):
    return list(dframe["data.content"].unique())


def update_realizations(dframe):
    return list(dframe["fmu_id.realization"].unique())