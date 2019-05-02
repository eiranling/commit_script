# commit_script
Python script to analyze and provide statistics for commits in a repository.

This python script makes use of the Gitlab v4 API to calculate the average number of logical changes to files per commit.
Logical changes in this sense are changes that hold some logical significance. i.e. changes that are not simply blank lines or braces.
