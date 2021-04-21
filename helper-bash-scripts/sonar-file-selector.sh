for lang_dir in */ ; do
    cd "./$lang_dir"
    for project_dir in */ ; do
        mkdir -p "../../../files/$lang_dir$project_dir"
        cp "./$project_dir/sonar-project.properties" "../../../files/$lang_dir$project_dir"
    done
    cd ..
done