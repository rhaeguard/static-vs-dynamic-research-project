# Research Question 1 Replication Guide

For RQ1, we selected 60 projects across 6 languages (10 project per language). 

You can see the list of all those projects [here](./scripts/current-commit-hash-collection/RQ1_all_project_details.csv).

One of the most important parts in that sheet is the Last Commit Id part. That's the commit we scanned.

## Sonarqube Project Properties Files

For all the projects we have scanned, you can find the project properties files [here](./sonarqube/sonar-project-properties-files/rq1)

When replicating, those files need to be in their appropriate project folders.

## Scanning

To scan a project, just go to the folder of that project and run

```bash
sonar-scanner
```

## Collecting the data

You have to run [data-collector.py](./scripts/data-collection/data_collector.py) file to collect the necessary data.

You need to have 2 environment variables in place:
1. `SONAR_USER_PASS` - username and password for sonarqube separated by colon (:) (e.g. admin:admin123)
2. `SONAR_ENDPOINT` - sonarqube endpoint with the port (e.g. 127.0.0.1:9000)

## Plotting

[visualize.ipynb](./scripts/data-collection/visualize.ipynb) file visualizes the collected data.



