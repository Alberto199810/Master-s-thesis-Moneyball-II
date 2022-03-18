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

Centre_Backs = play[play['Gen_Pos'] == "Centre-Back"]
Centre_Backs.to_csv("Centre_Backs.csv")

Full_Backs = play[play['Gen_Pos'] == "Full-Back"]
Full_Backs.to_csv("Full_Backs.csv")

Midfielders = play[play['Gen_Pos'] == "Midfielder"]
Midfielders.to_csv("Midfielders.csv")

Strikers = play[play['Gen_Pos'] == "Striker"]
Strikers.to_csv("Strikers.csv")

Wingers = play[play['Gen_Pos'] == "Winger"]
Wingers.to_csv("Wingers.csv")
