'''
Scraping the players that won the leagues in their country
'''

import pandas as pd

seriea_links = ['https://fbref.com/en/squads/e0652b02/2017-2018/Juventus-Stats',
                'https://fbref.com/en/squads/e0652b02/2018-2019/Juventus-Stats',
                'https://fbref.com/en/squads/e0652b02/2019-2020/Juventus-Stats',
                'https://fbref.com/en/squads/d609edc0/2020-2021/Internazionale-Stats']
premierl_links = ['https://fbref.com/en/squads/b8fd03ef/2017-2018/Manchester-City-Stats',
                  'https://fbref.com/en/squads/b8fd03ef/2018-2019/Manchester-City-Stats',
                  'https://fbref.com/en/squads/822bd0ba/2019-2020/Liverpool-Stats',
                  'https://fbref.com/en/squads/b8fd03ef/2020-2021/Manchester-City-Stats']
laliga_links = ['https://fbref.com/en/squads/206d90db/2017-2018/Barcelona-Stats',
                'https://fbref.com/en/squads/206d90db/2018-2019/Barcelona-Stats',
                'https://fbref.com/en/squads/53a2f082/2019-2020/Real-Madrid-Stats',
                'https://fbref.com/en/squads/db3b9613/2020-2021/Atletico-Madrid-Stats']
ligueone_links = ['https://fbref.com/en/squads/e2d8892c/2017-2018/Paris-Saint-Germain-Stats',
                  'https://fbref.com/en/squads/e2d8892c/2018-2019/Paris-Saint-Germain-Stats',
                  'https://fbref.com/en/squads/e2d8892c/2019-2020/Paris-Saint-Germain-Stats',
                  'https://fbref.com/en/squads/cb188c0c/2020-2021/Lille-Stats'] 
bundes_links = ['https://fbref.com/en/squads/054efa67/2017-2018/Bayern-Munich-Stats',
                'https://fbref.com/en/squads/054efa67/2018-2019/Bayern-Munich-Stats',
                'https://fbref.com/en/squads/054efa67/2019-2020/Bayern-Munich-Stats',
                'https://fbref.com/en/squads/054efa67/2020-2021/Bayern-Munich-Stats']

team_diz = {
    'Serie A' : seriea_links,
    'Premier League' : premierl_links,
    'La Liga' : laliga_links,
    'Ligue 1' : ligueone_links, 
    'Bundesliga' : bundes_links
    }

def winning_team_function(link, league):
    teamdata = pd.read_html(link, header = 1)[0].dropna()
    teamdata['League'] = league
    teamdata['Season'] = link[37:46]
    return teamdata[['Player','League','Season']]


total = pd.DataFrame(columns=['Player', 'League', 'Season'])

for i in list(team_diz.keys()):
    for j in range(len(team_diz[i])):
        dat = winning_team_function(team_diz[i][j],i)
        total = pd.concat([total, dat], ignore_index=True)

total.to_csv('league_winners.csv', index = False, encoding='utf-8-sig')