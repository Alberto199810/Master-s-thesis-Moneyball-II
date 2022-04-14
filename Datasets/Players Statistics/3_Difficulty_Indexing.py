import pandas as pd

play = pd.read_csv("data_2/Final Datasets/Final_df_players.csv")
keep = pd.read_csv("data_2/Final Datasets/Final_df_keepers.csv")
dif_ind = pd.read_csv("../Leagues Comparison/Difficulty_Index.csv") 

dif_ind.League = dif_ind.League.apply(lambda x: x.replace("Fußball-Bundesliga","Bundesliga"))
diz_pos = {dif_ind.League[i]:dif_ind.Difficulty_Index[i] for i in range(len(dif_ind))}
diz_neg = {dif_ind.League[i]:1/dif_ind.Difficulty_Index[i] for i in range(len(dif_ind))}

def function_to_resize(dataset, columns_neg):
    dataset["Dif_Ind_Value_Pos"] = dataset['Data_League'].map(diz_pos)
    dataset["Dif_Ind_Value_Neg"] = dataset['Data_League'].map(diz_neg)
    
    not_to_resize = ['Player_SN','Player_LN','Player Valuation','scouting_period','Age',
                     'Height','Position','Foot','Data_League','longName','Dif_Ind_Value_Pos',
                     'Dif_Ind_Value_Neg']
    columns_to_resize = [e for e in list(dataset.columns) if e not in not_to_resize]
    
    columns_to_resize_neg = columns_neg
    
    columns_to_resize_pos = [e for e in list(columns_to_resize) if e not in columns_to_resize_neg]

    for i in columns_to_resize_pos:
        dataset[i] = dataset[i] * dataset["Dif_Ind_Value_Pos"]
    for i in columns_to_resize_neg:
        dataset[i] = dataset[i] * dataset["Dif_Ind_Value_Neg"]
        
    dataset = dataset.drop(["Dif_Ind_Value_Pos","Dif_Ind_Value_Neg","longName"], axis = 1)
    
    return dataset
    

columns_to_resize_neg_player = ['Yellow.Cards','Red.Cards','Passes.Offside',
                                'Passes.Out.of.Bounds','Passes.Intercepted',
                                'Passes.Blocked','Dribbled.Past','Errors',
                                'Miscontrols','Dispossessed', 'Second.Yellow.Card',
                                'Fouls.Committed','Offsides','Penalty.Kicks.Conceded',
                                'Own.Goals']

columns_to_resize_neg_keeper = ['Goals.Against','Penalty.Kicks.Missed',
                                'Free.Kick.Goals.Against','Corner.Kick.Goals.Against',
                                'Own.Goals.Scored.Against.Goalkeeper']

play = function_to_resize(play, columns_to_resize_neg_player)
keep = function_to_resize(keep, columns_to_resize_neg_keeper)
    
play.to_csv("data_2/Final Datasets/Parametrized/Final_df_players_Parametrized.csv", index = False, encoding='utf-8-sig')
keep.to_csv("data_2/Final Datasets/Parametrized/Final_df_keepers_Parametrized.csv", index = False, encoding='utf-8-sig')