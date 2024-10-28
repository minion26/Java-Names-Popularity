import requests
import time

# Your personal access token
token = 'token'

# Set up the headers
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}


# Function to get Java repositories
def get_java_repos():
    repos = []
    page = 1
    while page <= 34:
        response = requests.get(
            f'https://api.github.com/search/repositories?q=language:Java&sort=stars&order=desc&page={page}&per_page=30',
            headers=headers
        )
        data = response.json()

        if response.status_code == 403:
            reset_time = int(response.headers.get('X-RateLimit-Reset'))
            current_time = time.time()
            sleep_time = max(reset_time - current_time, 0)  # Ensure sleep_time is non-negative
            print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            continue

        if 'items' not in data:
            print(f"Error: {data}")
            break

        repos.extend(data['items'])
        page += 1

    return repos


java_repos = get_java_repos()

# Save repo names to a file
with open('java_repos.txt', 'w', encoding='utf-8') as file:
    for repo in java_repos:
        file.write(f"{repo['full_name']}\n")

print(f"Total Java repositories: {len(java_repos)}")
