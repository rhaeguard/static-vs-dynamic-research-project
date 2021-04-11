from datetime import datetime
from dataclasses import dataclass

@dataclass
class Project:
    lang: str
    name: str
    sonarqube_key: str

    def get_commits_file_location(self) -> str:
        return f"{self.get_folder_location()}/all_commits"
    
    def get_folder_location(self) -> str:
        return f"./{self.lang}/{self.name}"

projects = [
    # Project("kotlin", "ktor", "evolution-kotlin-ktor"),
    # Project("js", "express", "evolution-js-express"),
    # Project("scala", "dotty", "evolution-scala-dotty"),
    # Project("go", "etcd", "evolution-go-etcd"),
    # Project("python", "django", "evolution-python-django"),
    Project("ruby", "rails", "evolution-ruby-rails")
]

def months_differ(month_a, month_b):
    return month_a.split("-")[1] != month_b.split("-")[1]

def select_trimonthly_commits_and_dates():
    for project in projects:
        with open(project.get_commits_file_location()) as file:
            lines = file.read().splitlines()
            commit_date_tuples = list(zip(map(lambda x: x.split(" ")[1], lines[0::2]), lines[1::2]))
            commit_date_tuples.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'))
            monthly_date_tuples = [commit_date_tuples[0]]
            last_date = commit_date_tuples[0][1]
            for commit, date in commit_date_tuples:
                if months_differ(last_date, date):
                    monthly_date_tuples.append((commit, date))
                last_date = date
            
            tri_monthly_tuples = monthly_date_tuples[::3]
            with open(project.get_folder_location()+"/commits-and-dates", "w") as writer:
                for commit, date in tri_monthly_tuples:
                    writer.write(f"{commit} {date}\n")

if __name__ == "__main__":
    select_trimonthly_commits_and_dates()
