import requests


def make_git_request(url, access_token):
    """Makes a request to the specified URL"""
    head = {
        "Private-Token": access_token
    }
    requests.get(url).headers(head)
    

if __name__ == "__main__":
    url = input("Enter the host URL: ")

