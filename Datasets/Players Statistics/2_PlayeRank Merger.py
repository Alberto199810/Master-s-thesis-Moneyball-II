import pandas as pd

df_players = pd.read_csv("data_2/Source Dataset/df_players.csv")
ranking = pd.read_csv("Esempio 2017-2018/ranking.csv")

### STEP 0: Useful functions
def resetdrop(data):
    dataset = data.reset_index()
    dataset = dataset.drop(['index'], axis = 1)
    return dataset

def movecol(data, column, position):
    column_to_move = data.pop(column)
    data.insert(position, column, column_to_move)
    return data

### STEP 1: Short Name merge
ranking['longName'] = ranking['longName'].apply(lambda x: " ".join(x.split()))

SN_Merge = pd.merge(df_players, ranking, left_on = ["Player_SN","scouting_period"], right_on = ["longName","scouting_period"])

### STEP 2: Long Name merge
'''
What I do now is taking the players from ranking that do not appear in the
first merged dataset, and now merging the missing ones with the Long Names and
no more with the short one
'''
miss1 = pd.DataFrame(ranking[~ranking['longName'].isin(SN_Merge['longName'])].dropna())
miss1 = resetdrop(miss1)

miss2 = pd.DataFrame(df_players[~df_players['Player_SN'].isin(SN_Merge['Player_SN'])])
miss2 = resetdrop(miss2)

LN_Merge = pd.merge(miss2, miss1, left_on = ["Player_LN","scouting_period"], right_on=["longName","scouting_period"])

### STEP 3: Put together the first two merged dataset
Tot_Merge = SN_Merge.append(LN_Merge, ignore_index=True)
Tot_Merge = resetdrop(Tot_Merge)

### STEP 4: Now, for the remaining ones, we merge on substrings
miss3 = pd.DataFrame(ranking[~ranking['longName'].isin(Tot_Merge['longName'])].dropna())
miss3 = resetdrop(miss3)

miss4 = pd.DataFrame(df_players[~df_players['Player_SN'].isin(Tot_Merge['Player_SN'])])
miss4 = resetdrop(miss4)

str_match = "({})".format("|".join(miss4.Player_SN))

Rem_Merge = pd.merge(miss3, miss4, left_on= [miss3.longName.str.extract(str_match)[0], "scouting_period"], right_on=["Player_SN","scouting_period"])

### STEP 5: Now let's put everything together
Final_Merge = Tot_Merge.append(Rem_Merge, ignore_index=True)

list_to_move = ['longName', 'ratings_mean']

Final_Merge = Final_Merge.drop([list_to_move[0]], axis = 1)
Final_Merge = movecol(Final_Merge, list_to_move[1], 2)

### FINAL STEP: Save the dataset
Final_Merge.to_csv("Final_Dataset.csv", index = False, encoding='utf-8-sig')