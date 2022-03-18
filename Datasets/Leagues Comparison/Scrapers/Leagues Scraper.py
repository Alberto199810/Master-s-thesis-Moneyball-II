import pandas as pd
import numpy as np

all_comp = pd.read_html("https://github.com/JaseZiv/worldfootballR_data/blob/master/raw-data/all_leages_and_cups/all_competitions.csv")[0]

all_comp_l = all_comp[(all_comp['competition_type'].str.contains('Domestic Leagues')) &
                      (all_comp['season_end_year'] == 2022) &
                      (all_comp['gender'] == "M")]

all_comp_l = all_comp_l.reset_index()

links = [(all_comp_l['seasons_urls'][i],all_comp_l['competition_name'][i]) for i in range(len(all_comp_l))]
links = list(dict.fromkeys(links))

league_dat = pd.DataFrame(columns=['League', 'Club'])

for i in range(len(links)):
    print(i)
    league = pd.read_html(links[i][0])[0]
    for k in range(len(league)):
        league_dat = league_dat.append({'League': links[i][1],
                                        'Club' : league['Squad'][k]}, ignore_index=True)

league_dat = league_dat.dropna()

league_dat.to_csv('League_Clubs.csv', index = False, encoding='utf-8-sig')