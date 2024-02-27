import sys

sys.path.append("../")

import requests
from config import constants

API_BASE_URL = constants.SCRATCH_API_BASE_URL
BASE_URL = constants.SCRATCH_BASE_URL

# プロジェクトのリミックス元IDの取得
def get_remix_parent(id, deep=0):
    """Scratch作品のリミックス元IDを取得
    Args:
        id (int): プロジェクトID
        deep（int): リミックス元までに何回派生しているか

    Returns:
        str: Scratch作品のメタ情報を含んだJSON
    """
    try:
        response = requests.get(f"{API_BASE_URL}/projects/{id}")
    except Exception as e:
        print("トークン取得中にエラーが発生しました")
        print(e)

    meta = response.json()

    if meta["remix"]["parent"]:
        return get_remix_parent(meta["remix"]["parent"], deep + 1)
    else:
        if deep == 0:
            return None
        else:
            return {"parent_id": id, "deep": deep}


# プロジェクトのメタ情報取得
def get_meta(id):
    """Scartch作品のメタ情報を取得
    Args:
        id (int): プロジェクトID

    Returns:
        str: Scratch作品のメタ情報を含んだJSON
    """
    try:
        response = requests.get(f"{API_BASE_URL}/projects/{id}")
    except Exception as e:
        print("トークン取得中にエラーが発生しました")
        print(e)

    meta = response.json()

    if meta["id"]:
        return meta
    else:
        return False


# プロジェクト取得用のトークン取得
def get_token(id):
    """Scartch作品のJSON取得に必要なトークンを取得
    Args:
        id (int): プロジェクトID

    Returns:
        str: JSON取得に必要なトークン
    """
    try:
        response = requests.get(f"{API_BASE_URL}/projects/{id}")
    except Exception as e:
        print("トークン取得中にエラーが発生しました")
        print(e)

    project = response.json()

    if project["id"]:
        return project["project_token"]
    else:
        return False

# プロジェクトの説明文取得 
def get_description(id):
    """Scartch作品の説明文を取得
    Args:
        id (int): プロジェクトID

    Returns:
        str: 対象のScratch作品の説明文
    """
    try:
        response = requests.get(f"{API_BASE_URL}/projects/{id}")

        project = response.json()

        return project["instructions"]
    except Exception as e:
        print("トークン取得中にエラーが発生しました")
        print(e)


# プロジェクト取得
def get_project(id):
    """Scartch作品のJSONを取得
    Args:
        id (int): プロジェクトID

    Returns:
        dictionary: 対象のScratch作品のJSON
    """
    json_data = ""
    try:
        token = get_token(id)
        json_data = requests.get(f"{BASE_URL}/{id}?token={token}").json()
    except Exception as e:
        print("プロジェクト取得中にエラーが発生しました")
        print(e)

    if json_data:
        return json_data
    else:
        return False
