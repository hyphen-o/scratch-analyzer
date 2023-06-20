import json
import requests
import csv
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

id = 270002293
csv_name = 'dataset_id.csv'
sprites = pd.read_csv(f'sprites.csv')

with open(f'out_csv/{csv_name}', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['project_id', 'sprite_name'])


def get_id(start_id, end_id):
    for i in range(start_id, end_id):
        time.sleep(0.01)
        try:
            url = requests.get(
                f'https://api.scratch.mit.edu/projects/{i}')
            project = json.loads(url.text)
            print(project['id'])
            if (project['id']):
                project_token = json.loads(url.text)['project_token']
                json_data = json.loads(requests.get(
                    f'https://projects.scratch.mit.edu/{i}?token={project_token}').text)
                print('go')
                for j in range(len(sprites.index)):
                    print(sprites.iloc[j][0])
                    if (json_data['targets'][1]['name'] == sprites.iloc[j][0]):
                        with open(f'out_csv/{csv_name}', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([i, sprites.iloc[j][0]])
                        print('Dataset_id: ' + str(project['id']))
                        break
                print(str(i) + ': not defaultsprite')

        except Exception as e:
            print(str(i) + ': none')


with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(get_id, 600000000, 700000000)
    executor.submit(get_id, 700000001, 799794842)
