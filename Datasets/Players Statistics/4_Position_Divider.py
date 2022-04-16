import pandas as pd
import numpy as np

play = pd.read_csv("data_2/Final Datasets/Parametrized/Final_df_players_Parametrized.csv", encoding='latin-1')
keep = pd.read_csv("data_2/Final Datasets/Parametrized/Final_df_keepers_Parametrized.csv", encoding='latin-1')

posizioni = np.unique(play['Position'])

new_roles = ['Centre-Back', 'Full-Back', 'Midfielder', 'Striker', 'Winger']

role_dictionary = {'Attacking Midfield' : new_roles[2], 
                   'Central Midfield' : new_roles[2], 
                   'Centre-Back' : new_roles[0],
                   'Centre-Forward' : new_roles[3],
                   'Defensive Midfield' : new_roles[2], 
                   'Left Midfield' : new_roles[4],
                   'Left Winger' : new_roles[4], 
                   'Left-Back' : new_roles[1],  
                   'Right Midfield' : new_roles[4], 
                   'Right Winger' : new_roles[4],
                   'Right-Back' : new_roles[1], 
                   'Second Striker' : new_roles[3]}

play["Gen_Pos"] = play['Position'].map(role_dictionary)
Gen_Pos = play.pop('Gen_Pos')

play.insert(6, 'Gen_Pos', Gen_Pos)

def deleteCol(dataset):
    dataset = dataset.reset_index()
    dataset = dataset.drop(['index'], axis = 1)
    return dataset

def saveData(position, final_name):
    dataset = play[play['Gen_Pos'] == position]
    dataset = deleteCol(dataset)
    dataset.to_csv("data_2/Final Datasets/Roles Division/{fname}".format(fname = final_name), index = False, encoding='utf-8-sig')
    
nuovi_dati = [["Centre-Back", "1_Centre_Backs_Par.csv"],
              ["Full-Back", "2_Full_Backs_Par.csv"],
              ["Midfielder", "3_Midfielders_Par.csv"],
              ["Striker", "5_Strikers_Par.csv"],
              ["Winger", "4_Wingers_Par.csv"]]

keep.to_csv("data_2/Final Datasets/Roles Division/0_Keepers_Par.csv", index = False, encoding='utf-8-sig')
for i in nuovi_dati:
    saveData(i[0], i[1])