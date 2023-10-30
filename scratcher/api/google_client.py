from __future__ import print_function

import sys

sys.path.append("../")

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

from config import constants

DEFAULT_FORM = {
    "title": "アンケート調査",
    "item": {
        "title": "これらの動作は同じパターンで実装可能だと思いますか？",
        "questionItem": {
            "question": {
                "required": True,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [
                        {"value": "そう思う"},
                        {"value": "ややそう思う"},
                        {"value": "ややそう思わない"},
                        {"value": "そう思わない"},
                    ],
                },
            }
        },
    },
}


def __access_service(secret_path):
    SCOPES = constants.FORM_SCOPES
    DISCOVERY_DOC = constants.FORM_DISCOVERY_DOC

    store = file.Storage(constants.TOKEN_PATH)
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(secret_path, SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
    )

    return form_service


def create_form(secret_path, form=DEFAULT_FORM):
    """Props = {
        title : str,
        item: {
            title: str,
            questionItem: {
                question: dictionary
            }
        }
    }"""

    NEW_FORM = {
        "info": {
            "title": form["title"],
        }
    }

    NEW_QUESTION = {
        "requests": [{"createItem": {"item": {form["item"]}, "location": {"index": 0}}}]
    }

    form_service = __access_service(secret_path)

    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()

    # Adds the question to the form
    question_setting = (
        form_service.forms()
        .batchUpdate(formId=result["formId"], body=NEW_QUESTION)
        .execute()
    )

    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()
    print(get_result)


def get_form(secret_path, formId):
    form_service = __access_service(secret_path)
    return form_service.forms().get(formId.execute())
