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


colummns = ["Language", "Project", "Number of Lines of Code", "Technical Debt Ratio", "Technical Debt", "Date"]

project_keys = [
    "evolution-kotlin-ktor",
    "evolution-js-express"
]
dfs = []
for key in project_keys:
    r = collect_data(key)
    lng = key.split("-")[1]
    proj = key.split("-")[2]

    lang = len(r.ncloc) * [lng]
    project = len(r.ncloc) * [proj]

    commits = []
    with open(f"../evolution-commit-selector/{lng}/{proj}/commits-and-dates") as f:
        for ll in f:
            commits.append(ll.split()[1])

    records = zip(lang, project, r.ncloc, r.sqale_debt_ratio, r.sqale_index, commits)
    
    df = pd.DataFrame.from_records(records, columns=colummns)
    dfs.append(df)

df = pd.concat(dfs)

df["Size Normalized Technical Debt"] = df["Technical Debt"] / df["Number of Lines of Code"]

df.to_csv("data.csv")

print(df)
