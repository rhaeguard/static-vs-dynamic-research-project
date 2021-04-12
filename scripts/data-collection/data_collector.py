import requests
from requests.auth import HTTPBasicAuth
import os
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd

credentials = os.getenv("SONAR_USER_PASS").split(":")

BASE_URL = "http://138.197.132.210:9000/api"


@dataclass
class MetricResults:
    sqale_debt_ratio: float = -1
    ncloc: int = -1
    sqale_index: int = -1


@dataclass
class Project:
    key: str
    name: str
    lang: str
    metric_results: MetricResults = None

def project_to_tuple(p: Project):
    return (p.name, p.lang, p.metric_results.sqale_debt_ratio, p.metric_results.ncloc, p.metric_results.sqale_index)

def get_all_projects() -> Tuple[int, List[Project]]:
    """
        Returns (
            total: number,
            projects: List[Project]
        )
    """
    def create_project(p: dict):
        key, name = p['key'], p['name']
        lang = key.split("-")[0]
        return Project(key=key, name=name, lang=lang)

    url = BASE_URL + "/projects/search"
    response = requests.get(url, auth=HTTPBasicAuth(*credentials))
    response = response.json()

    total_project_count = response['paging']['total']
    projects = list(map(create_project, filter(lambda p: not p['key'].startswith("evolution-"), response['components'])))
    return total_project_count, projects


def set_metrics_of_project(project: Project):
    """
        Sets the metric values of ncloc and sqale_debt_ratio
    """
    url = BASE_URL + "/measures/component?metricKeys=sqale_debt_ratio,ncloc,sqale_index&component="+project.key
    response = requests.get(url, auth=HTTPBasicAuth(*credentials))
    response = response.json()
    measures = response["component"]["measures"]
    metric_results = MetricResults()
    for measure in measures:
        if measure["metric"] == "ncloc":
            metric_results.ncloc = int(measure["value"])
        elif measure["metric"] == "sqale_index":
            metric_results.sqale_index = int(measure["value"])
        elif measure["metric"] == "sqale_debt_ratio":
            metric_results.sqale_debt_ratio = round(
                float(measure["value"]), ndigits=2)
    project.metric_results = metric_results


def populate_all():
    total, projects = get_all_projects()
    for project in projects:
        set_metrics_of_project(project)

    # print("Total : %d projects" % total)
    # print("="*70)
    # print("%-40s %-10s %-8s %-8s" % ("Name", "Language", "TD Score", "NCLOC"))
    # for p in projects:
        # print("%-40s %-10s %6.2f %8d %8d" % project_to_tuple(p))
    return projects

columns=["Project Name", "Project Language", "Technical Debt Ratio", "Number of Lines of Code", "Technical Debt"]

def create_pandas_db():
    projects = populate_all()
    projects = list(map(project_to_tuple, projects))
    df = pd.DataFrame.from_records(projects, columns =columns)
    df.to_csv('data_dump.csv')
    return df

def read_db_from_dump():
    return pd.read_csv("data_dump.csv")[columns]

if __name__ == "__main__":
    read_from_dump = True
    if read_from_dump:
        df = read_db_from_dump()
    else:
        df = create_pandas_db()
    df = df.sort_values(by="Project Language")
    print(df)
