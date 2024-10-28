
import os
import requests
import time

# Your personal access token
token = 'token'

# Set up the headers
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def check_rate_limit():
    rate_limit_url = 'https://api.github.com/rate_limit'
    response = requests.get(rate_limit_url, headers=headers)
    rate_limit = response.json()
    remaining = rate_limit['rate']['remaining']
    reset_time = rate_limit['rate']['reset']
    return remaining, reset_time

def get_java_files_from_repo(repo_name):
    java_files = []
    repo_url = f'https://api.github.com/repos/{repo_name}/contents'
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 403:
        remaining, reset_time = check_rate_limit()
        if remaining == 0:
            wait_time = reset_time - time.time()
            print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
            time.sleep(wait_time)
            response = requests.get(repo_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch contents for {repo_name}: {response.status_code}")
        return java_files

    contents = response.json()
    if not isinstance(contents, list):
        print(f"Unexpected response format for {repo_name}: {contents}")
        return java_files

    def get_java_files(content, base_path=""):
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'file' and item.get('name', '').endswith('.java'):
                    file_path = os.path.join(base_path, item['name'])
                    java_files.append(file_path)
                    print(f"Found Java file: {file_path}")
                elif item.get('type') == 'dir':
                    dir_response = requests.get(item['url'], headers=headers)
                    if dir_response.status_code != 200:
                        print(f"Failed to fetch directory contents for {item['url']}: {dir_response.status_code}")
                        continue
                    dir_contents = dir_response.json()
                    if not isinstance(dir_contents, list):
                        print(f"Unexpected directory response format: {dir_contents}")
                        continue
                    get_java_files(dir_contents, os.path.join(base_path, item['name']))
            else:
                print(f"Unexpected item format: {item}")

    get_java_files(contents)
    return java_files

with open('java_repos.txt', 'r', encoding='utf-8') as file:
    repos = [line.strip() for line in file]

if not repos:
    print("No repositories found in java_repos.txt")

with open('java_files_from_repo2.txt', 'w', encoding='utf-8') as file:
    count = 0
    total_java_files = 0
    for repo in repos:
        count += 1
        print(f"Processing repository {count}/{len(repos)}: {repo}")
        java_files = get_java_files_from_repo(repo)
        if not java_files:
            print(f"No Java files found in repository: {repo}")
        for java_file in java_files:
            file.write(f"{repo},{java_file}\n")
            total_java_files += 1

print(f"Total Java files from repositories: {total_java_files}")