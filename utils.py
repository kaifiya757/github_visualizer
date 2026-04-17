import requests

def get_user(username):
    url = f"https://api.github.com/users/{username}"
    return requests.get(url).json()

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    return requests.get(url).json()