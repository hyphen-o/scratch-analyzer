import json
import requests

API_BASE_URL = "https://api.scratch.mit.edu"
BASE_URL = "https://projects.scratch.mit.edu"

# プロジェクト取得用のトークン取得
def get_token(id):
    try:
        url = requests.get(
            f'{API_BASE_URL}/projects/{id}'
        )
    except Exception as e:
        print("トークン取得中にエラーが発生しました")
        print(e)

    project = json.loads(url.text)

    if (project['id']):
        return json.loads(url.text)['project_token']
    else:
        return False

# プロジェクト取得
def get_project(id):
    json_data = ""
    try:
        token = get_token(id)
        json_data = json.loads(requests.get(
            f'{BASE_URL}/{id}?token={token}').text)
    except Exception as e:
        print("プロジェクト取得中にエラーが発生しました")
        print(e)

    if (json_data):
        return json_data
    else:
        return False
