# How to scan a new repository for evolution thingy?

1. Clone the repo to somewhere
2. Run `helper-bash-scripts/all-commits-and-dates.sh` command in the folder
3. Take the `all_commits` file from the repo and put it in `evolution-commit-selector` folder, inside of a folder that is of the form `$language/$repo_name`
4. Add the project info to `projects` list in `scripts.py` file.
5. Run the `script.py` file. It will generate the `commits-and-dates` file in the appropriate folders
6. Copy `commits-and-dates` file and `commit.sh` file into the repo's directory
7. Run the shell script...and wait till it finishes
8. Add the project key to the `project_keys` dict in `evolution-data-collection/script.py` file.
9. Run the script file.
10. Go to `visualize` notebook and add the project name to `projects` list, and run the whole notebook. It should produce the charts for evolution thingy.
