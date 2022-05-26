'''
Refinement to the winning players
'''

import pandas as pd

players = pd.read_csv("C:/Users/alber/Desktop/Universita/Magistrale/Master-s-thesis-Moneyball-II/01_Datasets/Players Statistics/data_2/Final Datasets/Parametrized/Final_df_players_Parametrized.csv")
keepers = pd.read_csv("C:/Users/alber/Desktop/Universita/Magistrale/Master-s-thesis-Moneyball-II//01_Datasets/Players Statistics/data_2/Final Datasets/Parametrized/Final_df_keepers_Parametrized.csv")
winners = pd.read_csv('0_league_winners.csv')

player_tot = pd.concat([players[['Player_SN','Data_League','scouting_period', 'Position']], keepers[['Player_SN','Data_League','scouting_period', 'Position']]], ignore_index = True)

total2 = pd.merge(winners, player_tot, left_on = ['Player', 'League', 'Season'], right_on = ['Player_SN','Data_League','scouting_period'])
total2 = total2[['Player', 'League', 'Season', 'Position']]

total2 = total2.drop_duplicates()

new_roles = ['Centre-Back', 'Full-Back', 'Midfielder', 'Striker', 'Winger', 'Goalkeeper']

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
                   'Second Striker' : new_roles[3],
                   'Goalkeeper' : new_roles[5]}

total2['Gen_Pos'] = total2['Position'].map(role_dictionary)
total2 = total2.drop(['Position'], axis = 1)

total2.to_csv('1_league_winners_ref.csv', index = False, encoding='utf-8-sig')