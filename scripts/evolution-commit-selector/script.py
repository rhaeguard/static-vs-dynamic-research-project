from datetime import datetime

def do_months_differ(month_a, month_b):
    return month_a.split("-")[1] != month_b.split("-")[1]

def print_list(l):
    for ll in l:
        print(ll)

with open("commits") as file:
    lines = file.read().splitlines()
    commit_date_tuples = list(zip(map(lambda x: x.split(" ")[1], lines[0::2]), lines[1::2]))
    commit_date_tuples.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'))
    monthly_date_tuples = [commit_date_tuples[0]]
    last_date = commit_date_tuples[0][1]
    for commit, date in commit_date_tuples:
        if do_months_differ(last_date, date):
            monthly_date_tuples.append((commit, date))
        last_date = date
    
    tri_monthly_tuples = monthly_date_tuples[::3]
    for commit, date in tri_monthly_tuples:
        print(commit, date)