import requests
from requests.auth import HTTPBasicAuth
import os
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd

credentials = os.getenv("SONAR_USER_PASS").split(":")

BASE_URL = "http://138.197.132.210:9000/api"

@dataclass
class EvolutionMetricResults:
    ncloc: List[int]
    sqale_debt_ratio: List[float]
    sqale_index: List[int]


def collect_data(project_key: str):
    url = BASE_URL + \
        f"/measures/search_history?component={project_key}&metrics=sqale_index,sqale_debt_ratio,ncloc&ps=1000"
    response = requests.get(url, auth=HTTPBasicAuth(*credentials))

    measures = response.json()["measures"]
    ncloc = []
    sqale_debt_ratio = []
    sqale_index = []
    for measure in measures:
        metric = measure["metric"]
        hist = measure["history"]
        if metric == "ncloc":
            ncloc = list(map(lambda x: int(x["value"]), hist))
        elif metric == "sqale_index":
            sqale_index = list(map(lambda x: int(x["value"]), hist))
        elif metric == "sqale_debt_ratio":
            sqale_debt_ratio = list(map(lambda x: float(x["value"]), hist))

    return EvolutionMetricResults(ncloc, sqale_debt_ratio, sqale_index)


read_from_csv = True

colummns = ["Number of Lines of Code", "Technical Debt Ratio", "Technical Debt"]

if read_from_csv:
    df = pd.read_csv("evolution-kotlin-ktor.csv")[colummns]
else:
    r = collect_data("evolution-kotlin-ktor")
    records = zip(r.ncloc, r.sqale_debt_ratio, r.sqale_index)

    df = pd.DataFrame.from_records(records, columns=colummns)
    df.to_csv("evolution-kotlin-ktor.csv")

df["Size Normalized Technical Debt"] = df["Technical Debt"] / df["Number of Lines of Code"]

print(df)
