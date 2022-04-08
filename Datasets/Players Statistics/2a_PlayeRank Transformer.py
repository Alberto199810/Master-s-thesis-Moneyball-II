import pandas as pd
import datetime

#Import data shared by PlayeRank  
df = pd.read_json("data_2/Source Dataset/playerank_export.json")

#Get rid of hour and minute of the game, we're only interested in Year/Month/Day
df['timestamp'] = df['timestamp'].apply(lambda x: x.date())

#Let's divide in four different datasets related to the seasons
df_2017_8 = df[(df['timestamp'] >= datetime.date(2017,7,1)) & (df['timestamp'] <= datetime.date(2018,6,30))]
df_2018_9 = df[(df['timestamp'] >= datetime.date(2018,7,1)) & (df['timestamp'] <= datetime.date(2019,6,30))]
df_2019_0 = df[(df['timestamp'] >= datetime.date(2019,7,1)) & (df['timestamp'] <= datetime.date(2020,8,25))]
df_2020_1 = df[(df['timestamp'] >= datetime.date(2020,8,26)) & (df['timestamp'] <= datetime.date(2021,6,30))]

#Pre-Processing of the dataset
def funzref(dataset, season):
    data = dataset.groupby(['player']).agg({'playerankIndex':'mean', 'player':'count'})
    data.columns = ['avg_playerankIndex', 'num_of_matches']
    data = data.reset_index()
    data = data[data['num_of_matches'] >= 10]
    data['player'] = data['player'].apply(lambda x: x.split(",")[0])
    data['player'] = pd.to_numeric(data['player'])
    data['scouting_period'] = season
    return data
    
df_2017_8 = funzref(df_2017_8, '2017-2018')
df_2018_9 = funzref(df_2018_9, '2018-2019')
df_2019_0 = funzref(df_2019_0, '2019-2020')
df_2020_1 = funzref(df_2020_1, '2020-2021')

#We import players.json in order to substitute Player Short Name with the Long one
df_pl = pd.read_json("data_2/Source Dataset/players.json")
df_pl['shortName'] = df_pl['shortName'].apply(lambda x: x.encode().decode('unicode_escape'))
df_pl['firstName'] = df_pl['firstName'].apply(lambda x: x.encode().decode('unicode_escape'))
df_pl['lastName'] = df_pl['lastName'].apply(lambda x: x.encode().decode('unicode_escape'))
df_pl['longName'] = df_pl[['firstName', 'lastName']].agg(' '.join, axis=1)
df_pl = df_pl[['longName','wyId']]

#Now we merge the datasets together
l = [df_2017_8, df_2018_9, df_2019_0, df_2020_1]

for i in range(len(l)):
    l[i] = pd.merge(l[i], df_pl[['longName','wyId']], left_on = "player", right_on = "wyId")
    l[i] = l[i][['longName', 'avg_playerankIndex', 'scouting_period']]

ranking = pd.concat(l, ignore_index = True)
ranking['longName'] = ranking['longName'].apply(lambda x: " ".join(x.split()))

#And now we save it in .csv format
ranking.to_csv("data_2/Source Dataset/ranking.csv",index = False, encoding='utf-8-sig')