import json
from sumo.wrapper import CallSumoApi
import pandas as pd


class SumoConnection:
    def __init__(self, env="fmu"):
        self.api = CallSumoApi(env=env)
        self.api.get_bearer_token()
        self._data = [
            result["_source"]
            for result in self.api.searchroot("*").get("hits").get("hits")
        ]

    @property
    def ensembles_with_4d(self):
        print(self.api.search(query="*", select="4d"))

    def _get_case(self, ensemble: dict):
        for case in self._data:
            if case["fmu_ensemble_id"] == ensemble["id"]:
                return (
                    self.api.search(f"fmu_ensemble_id:{ensemble['id']}")
                    .get("hits")
                    .get("hits")
                )
        raise KeyError(f"Case not found")

    def get_surface_attributes_in_ensemble(self, ensemble: dict):
        surface_attrs = []
        # print(self._get_case(ensemble))
        df = pd.DataFrame(columns=[])
        data = []
        for obj in self._get_case(ensemble):
            content = obj.get("_source")

            # print(obj.get("data_type"))
            # print(content.get("4d"))
            if content.get("data_type") == "surface" and content.get("4d"):
                data.append(
                    {
                        "fmu_id.realization": content.get("realization").get("id"),
                        "fmu_id.ensemble": content.get("fmu_ensemble_id"),
                        "map_type": "observed"
                        if content.get("4d").get("is_observation")
                        else "simulated",
                        "data.name": content.get("name"),
                        "data.content": content.get("4d").get("attribute"),
                        "data.time.t1": content.get("time").get("t1"),
                        "data.time.t2": content.get("time").get("t2"),
                        "statistics": "",
                        "filename": content.get("_sumo").get("blob_url"),
                    }
                )
            # surface_attrs.append(obj.get("_source"))
        return pd.DataFrame(data)

    def get_realizations_for_attribute(self, ensemble: str, attribute: str):
        pass

    def get_attributes_for_time_interval(self, ensemble: str, t1: str, t2: str):
        pass

    def get_attributes_with_date_difference(self, ensemble: str) -> list:
        data = (
            self.api.search(f"fmu_ensemble_id:{ensemble['id']}").get("hits").get("hits")
        )
        objs = []
        for obj in data:
            if (
                not obj["_source"].get("content")
                or obj["_source"].get("data_type") != "surface"
            ):
                continue
            if obj["_source"].get("content") not in objs:
                objs.append(obj["_source"].get("content"))
        return objs

    def get_names_for_attribute(self, ensemble_name: str, attribute: str) -> list:
        pass

    def get_dates_for_attribute(self, ensemble_name: str, attribute: str) -> list:
        pass


conn = SumoConnection()
print(conn.ensembles_with_4d)
# data = []
for ens in conn.ensembles:
    data.append(conn.get_surface_attributes_in_ensemble(ensemble=ens))
# print(pd.concat(data))
# pd.concat(data).to_csv("data.csv", index=False)
# # data.append(conn.get_surface_attributes_in_ensemble(ensemble=ens))
# with open("output2.json", "w") as f:
#     json.dump(conn._data, f)