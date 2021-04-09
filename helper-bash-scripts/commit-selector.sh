for lang_dir in */ ; do
    cd "./$lang_dir"
    for project_dir in */ ; do
        cd "./$project_dir"
        hash=$(git rev-parse --short HEAD)
        # will echo in the format:
        # lang/project/hash
        echo "$lang_dir$project_dir$hash"
        cd ..
    done
    cd ..
done