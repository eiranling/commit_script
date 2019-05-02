import requests
import re
from constants import *


def make_git_request(url, access_token, params=None):
    """Makes a request to the specified URL"""
    head = {
        "Private-Token": access_token
    }
    response = requests.get(url, params, headers=head)
    if response.status_code != 200:
        return None
    return response.json()


def calculate_addition_average(commits):
    additions = 0
    deletions = 0
    total = 0
    for commit in commits:
        additions += commit[STATS][ADDITIONS]
        deletions += commit[STATS][DELETIONS]
        total += commit[STATS][TOTAL]
    return {ADDITIONS: additions/len(commits), DELETIONS: deletions/len(commits), TOTAL:total/len(commits)}


def find_logical_changes(url, commits):
    for index in range(len(commits)):
        diffs = make_git_request("{0}/{1}/diff".format(url, commits[index]['id']), ACCESS_TOKEN)
        commits[index][DIFF] = strip_diffs(diffs)
        diff_sum = {ADDITIONS: 0, DELETIONS: 0}
        for diff in commits[index][DIFF]:
            diff_sum[ADDITIONS] += diff[ADDITIONS]
            diff_sum[DELETIONS] += diff[DELETIONS]

        commits[index][STATS][ADDITIONS] = diff_sum[ADDITIONS]
        commits[index][STATS][DELETIONS] = diff_sum[DELETIONS]
        commits[index][STATS][TOTAL] = diff_sum[ADDITIONS] + diff_sum[DELETIONS]
    return commits


def strip_diffs(diffs):
    for diff_index in range(len(diffs)):
        diffs[diff_index][ADDITIONS] = 0
        diffs[diff_index][DELETIONS] = 0
        diff_lines = diffs[diff_index][DIFF].split('\n')
        for line in diff_lines:
            if re.compile("^\\+(?!\\s*([{}();])\\s*)(\\s*(?!(//|#)).*)").match(line):
                diffs[diff_index][ADDITIONS] += 1
            if re.compile("^-(?!\\s*([{}();])\\s*)(\\s*(?!(//|#)).*)").match(line):
                diffs[diff_index][DELETIONS] += 1
    return diffs


if __name__ == "__main__":
    url = input("Enter the host URL: ")
    project = input("Enter the project id: ")
    commits = make_git_request("{0}/api/v4/projects/{1}/repository/commits".format(url, project), ACCESS_TOKEN, {
        "all": True,
        "with_stats": True
    })
    commits = find_logical_changes("{0}/api/v4/projects/{1}/repository/commits".format(url, project), commits)
    averages = calculate_addition_average(commits)
    print(AVERAGE_STRING_FORMAT.format(averages[ADDITIONS], averages[DELETIONS], averages[TOTAL]))



