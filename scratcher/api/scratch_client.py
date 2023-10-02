import json
import requests

API_BASE_URL = "https://api.scratch.mit.edu"
BASE_URL = "https://projects.scratch.mit.edu"

# プロジェクト取得用のトークン取得
def get_token(id):
    try:
        response = requests.get(
            f'{API_BASE_URL}/projects/{id}'
        )
    except Exception as e:
        print("トークン取得中にエラーが発生しました")
        print(e)

    # TODO：response.json()で受け取れる
    project = response.json()

    if (project['id']):
        return project['project_token']
    else:
        return False

def get_description(id):
    try:
        response = requests.get(
            f'{API_BASE_URL}/projects/{id}'
        )

        return response["instructions"]
    except Exception as e:
        print("トークン取得中にエラーが発生しました")
        print(e)

# プロジェクト取得
def get_project(id):
    json_data = ""
    try:
        token = get_token(id)
        json_data = requests.get(
            f'{BASE_URL}/{id}?token={token}').json()
    except Exception as e:
        print("プロジェクト取得中にエラーが発生しました")
        print(e)

    if (json_data):
        return json_data
    else:
        return False
