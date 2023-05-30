import os
from datetime import datetime, timedelta
from github import Github

ACCESS_TOKEN = open("token.txt", "r").read().strip()
github = Github(ACCESS_TOKEN)

SECONDS_IN_A_DAY = 86400
MAX_REPO_SIZE = 5000


def get_query(start_time, end_time):
    start_time_str = start_time.strftime("%Y-%m-%d")
    end_time_str = end_time.strftime("%Y-%m-%d")

    return f"language:python created:{start_time_str}..{end_time_str}"


def clone_repositories(repositories):
    for index, repository in enumerate(repositories, 1):
        print(f"{index}/{repositories.totalCount}")
        if repository.size > MAX_REPO_SIZE:
            continue
        print(repository.clone_url)
        os.system(f"git clone {repository.clone_url} repos/{repository.owner.login}/{repository.name}")


def main():
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)

    for i in range(3):
        query = get_query(start_time, end_time)
        print(query)
        repositories = github.search_repositories(query)
        clone_repositories(repositories)
        start_time -= timedelta(days=1)
        end_time -= timedelta(days=1)


if __name__ == "__main__":
    main()
