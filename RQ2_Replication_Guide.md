# Research Question 2 Replication Guide

For RQ2, we selected 12 projects across 6 languages (2 project per language). 

All of those projects are shown in the following table:

|Language|Project           |Github                                      |Last Commit Id|
|--------|------------------|--------------------------------------------|--------------|
|kotlin  |ktor              |https://github.com/ktorio/ktor              |e425a2885     |
|kotlin  |kotlinx.coroutines|https://github.com/Kotlin/kotlinx.coroutines|b7e08b8f      |
|scala   |finagle           |https://github.com/twitter/finagle          |e02495aa6     |
|scala   |dotty             |https://github.com/lampepfl/dotty           |b44cafa3cf    |
|go      |etcd              |https://github.com/etcd-io/etcd             |7f97dfd45     |
|go      |moby              |https://github.com/moby/moby                |68bec0fcf7    |
|js      |express           |https://github.com/expressjs/express        |50893685      |
|js      |vue               |https://github.com/vuejs/vue                |0948d999      |
|ruby    |rails             |https://github.com/rails/rails              |2b1b75e9ff    |
|ruby    |vagrant           |https://github.com/hashicorp/vagrant        |22795b161     |
|python  |scikit-learn      |https://github.com/scikit-learn/scikit-learn|b1d686d07     |
|python  |django            |https://github.com/django/django            |e4430f22c8    |


One of the most important parts in that sheet is the Last Commit Id part. That's the commit we scanned.

## Sonarqube Project Properties Files

For all the projects we have scanned, you can find the project properties files [here](./sonarqube/sonar-project-properties-files/rq1)

When replicating, those files need to be in their appropriate project folders.

## Commit selection

We selected commits on Tri-Monthly basis. So, to do that: 

1. Extract all the commits from a repo with their dates with the following command and saved the information to a file called _all\_commits_:
```bash
git rev-list --pretty='format:%ad' --date=short HEAD > all_commits
```
2. Put that file under its project's folder [here](./scripts/evolution-commit-selector).
3. Do (1 and 2) for all the projects
4. Run the [script.py](./scripts/evolution-commit-selector/script.py) file. It will generate a _commits-and-dates_ file for each project.
5. For each project, copy its commits-and-dates file and [commit.sh](./scripts/evolution-commit-selector/commit.sh) file to that project's original folder; and run the scan using sonar-scanner (don't forget to add the correct sonar-project.properties file too)

## Data Collection

To collect the scanned data, just run [script.py](./scripts/evolution-data-collection/script.py) file.

To visualize the changes, just run [visualize.ipynb](./scripts/evolution-data-collection/visualize.ipynb) file.

## Running tests

We made use of [Mann-Kendall Tests code](https://github.com/digeo/evolution-of-td-in-apache/blob/master/perform_mktests.py) from _The Evolution of Technical Debt in the Apache Ecosystem_ paper repository.

