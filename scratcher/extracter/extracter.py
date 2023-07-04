
import sys
sys.path.append('../')

import json
import requests
import csv
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from scratcher.api import scratch_client

id1 = 271005087
id2 = 500946724
csv_name = 'dataset_id.csv'
sprites = pd.read_csv(f'sprites.csv')


def get_id(start_id, end_id):
    for id in range(start_id, end_id):
        time.sleep(0.01)
        try:
            
            project_token = scratch_client.get_token(id)
            if(project_token):
                data = scratch_client.get_project(id, project_token)
                print('go')
                for j in range(len(sprites.index)):
                    if (data['targets'][1]['name'] == sprites.iloc[j][0]):
                        with open(f'out_csv/{csv_name}', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([i, sprites.iloc[j][0]])
                        print('Dataset_id: ' + str(project['id']))
                        break
                print(str(id) + ': not defaultsprite')

        except Exception as e:
            print(str(i) + ': none')


with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(get_id, id1, 500000000)
    executor.submit(get_id, id2, 799794842)
