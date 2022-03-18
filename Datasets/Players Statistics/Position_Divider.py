import pandas as pd
import numpy as np

play = pd.read_csv("data_2/df_players.csv", encoding='latin-1')

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

def deleteCol(dataset, coln):
    dataset = dataset.reset_index()
    dataset = dataset.drop(['index', coln], axis = 1)
    return dataset

def saveData(position, final_name):
    dataset = play[play['Gen_Pos'] == position]
    dataset = deleteCol(dataset, 'Unnamed: 0')
    dataset.to_csv(final_name, index = False, encoding='latin-1')
    
nuovi_dati = [["Centre-Back", "Centre_Backs.csv"],
              ["Full-Back", "Full_Backs.csv"],
              ["Midfielder", "Midfielders.csv"],
              ["Striker", "Strikers.csv"],
              ["Winger", "Wingers.csv"]]

for i in nuovi_dati:
    saveData(i[0], i[1])
