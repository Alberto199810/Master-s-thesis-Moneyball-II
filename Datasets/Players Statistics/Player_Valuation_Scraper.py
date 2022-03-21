import pandas as pd
import requests, re, ast
import numpy as np
from datetime import datetime

data_play = pd.read_csv("data_2/Source Dataset/df_players.csv", encoding='latin-1')
data_keep = pd.read_csv("data_2/Source Dataset/df_keepers.csv", encoding='latin-1')

data_play = data_play.drop(['Unnamed: 0'], axis = 1)
data_keep = data_keep.drop(['Unnamed: 0'], axis = 1)

def player_val_scraper(dataset):
    
    dataset['link_TRM'] = dataset['link_TRM'].apply(lambda x : x.replace('profil', 'marktwertverlauf'))
    dataset['Player_Valuation'] = 0

    for i in range(len(dataset)):
        
        try:
            anno_iniz = dataset['scouting_period'][i][:4]
            anno_fine = dataset['scouting_period'][i][-4:]
            r = requests.get(dataset['link_TRM'][i], headers = {'User-Agent':'Mozilla/5.0'})
            p = re.compile(r"'data':(.*)}\],")
            s = p.findall(r.text)[0]
            s = s.encode().decode('unicode_escape')
            data = ast.literal_eval(s)
            ww = []
            for k in range(len(data)): 
                if datetime.strptime(data[k]['datum_mw'], "%b %d, %Y") >= datetime(int(anno_iniz), 7, 1, 0, 0) and datetime.strptime(data[k]['datum_mw'], "%b %d, %Y") <= datetime(int(anno_fine), 6, 30, 0, 0):
                    ww.append(data[k]['y'])
            if len(ww) != 0:
                dataset.loc[i,"Player_Valuation"] = np.mean(ww)
            else:
                dataset.loc[i,"Player_Valuation"] = data[-1]['y']
        
        except:
            pass
    
    return dataset
        
data_play = player_val_scraper(data_play)
data_keep = player_val_scraper(data_keep)

column_to_move = data_play.pop("Player_Valuation")
data_play.insert(2, "Player Valuation", column_to_move)
column_to_move = data_keep.pop("Player_Valuation")
data_keep.insert(2, "Player Valuation", column_to_move)

data_play = data_play.drop(['link_TRM'], axis = 1)
data_keep = data_keep.drop(['link_TRM'], axis = 1) 

data_play.to_csv("df_players.csv", index = False, encoding='utf-8-sig')
data_keep.to_csv("df_keepers.csv", index = False, encoding='utf-8-sig')
