# Statistics and Sport: The Moneyball idea applied to Football world

### Alberto Allegri, Bocconi University, Master's Thesis in Data Science & Business Analytics

**Tech Stack:**<br />
![R](https://img.shields.io/badge/r-%23276DC3.svg?style=for-the-badge&logo=r&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 [<img src='https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white'>](https://alberto-allegri-moneyball2.herokuapp.com/)

## Table of Contents
1. [General Info](#general-info)
2. [Methodology](#methodology)
3. [File Structure](#file-structure)


## General Info

This repository contains the code for my Master's Thesis, where I try to replicate the moneyball idea (building a team capable of winning the league, but with a restricted budget) using both football statistics coming from [FBRef Scouting Reports](https://fbref.com/en/players/70d74ece/scout/365_euro/Karim-Benzema-Scouting-Report), [Transfermarkt](https://www.transfermarkt.com/) and [PlayeRank](https://github.com/mesosbrodleto/playerank) data together. 

## Methodology

The idea behind the thesis is that we start from a dataset having as independent variables (our ```X```) all the statistics that you can find in the FBRef scouting report, and as dependent variable (our ```y```) the average PlayeRank score of a player for the entire season. The data I had were going from season 2017/2018 to season 2020/2021, for all the players that had a scouting report in FBRef in those season. For each and every single of these players, I had their average PlayeRank score, thanks to the data PlayeRank provided me. Unfortunately, the only dataset I can show you is the one with FBRef data, since PlayeRank data are protected by an NDA.

Thanks to the two obtained datasets (one for Goalkeepers, one for moving players, since variables in the scouting report are different between Keepers and non-Keepers), what I decided to do was the following:
Firstly, I split the data in 6 different sets:
```
● Goalkeepers
● Centre-Backs
● Full-Backs
● Midfielders
● Wingers
● Strikers
```

Then, to each of these sets, we apply 7 different Variable Selection Algorithms to select which FBRef statistics are the most important to predict PlayeRank score:
```
● BorutaPy
● Recursive Feature Elimination
● Univariate Feature Selection
● Lasso Regression
● Feature Shuffling
● Feature Performance
● Target Mean Performance
```

Once the 7 different algorithms were applied, if a variable was selected by ```at least 5 out of 7``` algorithms, then it was included in my final choice.

Finally, when the variables were selected, I collected the players that won the league from season 2017/2018 to season 2020/2021 in all the top-5 European Leagues (csv can be found at this [link](https://github.com/Alberto199810/Master-s-thesis-Moneyball-II/blob/main/03_Data%20Analytics/Winners/1_league_winners_ref.csv)). Then, I calculated the mean values of the important variables within each role, and, by using the [NORM](https://jermwatt.github.io/machine_learning_refined/notes/16_Linear_algebra/16_5_Norms.html#:~:text=A%20norm%20is%20a%20kind,living%20in%20the%20same%20space.) function, I calculated which observations in my dataset where the closest to the average statistics of the players who actually won the league. But, to this whole reasoning, I applied a restriction: the selected players had to have a Transfermarkt evaluation that was 1/x (X could be selected, basing on how much money we wanted to save) the average value of the players within a certain role in the winning team.

The final result is a full team that is actually costing way less the total cost of the winning team, but that actually had very close performances for the most important statistics to evaluate the total performance of a player in his role!

To retrieve the team for a precise league/season we just have to run low_cost_winners(season, league, factor_to_save).

## File Structure

Within the repository, you can see three main folders:
1. **01_Datasets**
2. **02_Machine Learning**
3. **03_Data Analytics**

### 01_Datasets
In this folder, you can find the scripts I wrote to build my final dataset. Moreover, in the section [Leagues Comparison](https://github.com/Alberto199810/Master-s-thesis-Moneyball-II/tree/main/01_Datasets/Leagues%20Comparison) you can see the code I applied to standardize statistics across leagues (with a map of European Leagues)

<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/leghe_net.png" width="750">

Moreover, just to have a view of the data, I created an interactive app that can be found at this [link](https://alberto-allegri-moneyball2.herokuapp.com/) that will show you:
```
● A preview of PlayeRank data with a boxplot
● A scatterplot with PlayeRank score on the x-axis and TransferMarkt valuation on the y-axis, with size of the scatter dependant 
on a "Likability" parameter (computed with PlayeRank index/TransferMarkt valuation)
● A pitch where the best 11 players by the likability parameter (divided by role) are represented.
```

Here, a preview with some screenshots of the three plots:

<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/boxplot.png" width="750">

<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/scatterplot.png" width="750">

<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/11 lik.png" width="750">

### 02_Machine Learning
In this folder, you can find the script I built to obtain the chosen variables per each role, applying the 7 different variable selection algorithms.

### 03_Data Analytics
In this final folder, you can find both the scripts I wrote to obtain the winners dataset and the jupyter notebook containing the function to get the most similar players to the ones that won the league. Moreover, we built a "Trade-off" value by dividing the Percentage of Money we're saving with the similarity coefficient of the low-cost team. 


## Results
The below tables details the similarity coefficient, the percentage savings and the trade off coefficient for the top 5 values obtained for trade off coefficient. Obviously, the higher is trade-off, the best is the combination of similarities of statistics and money we're saving.

| Season       | League  | Similarity Coeff.  | Savings | Trade Off |
| :----------: | :----------:| :-----------------: | :----------: | :---------:|
| 2020-2021    | Serie A     | 4.424397	  |  74.685169   |	16.880303 |
| 2020-2021    | Ligue 1     | 4.480457	  |  75.257386   |	16.796812 |
| 2019-2020    | Serie A     | 5.254009	  |  80.591059	 |  15.338965 |
| 2020-2021    | Bundesliga  | 5.364341	  |  82.053054	 |  15.296018 |
| 2018-2019    | Ligue 1     | 5.763644	  |  84.111916	 |  14.59353  |
<br />
<br />
By looking at the resulting value, it seems that the best trade-off is found in Serie A 2020/2021, with a 4.424397 similarity coefficient and a 74.68% save on the budget. Looking at absolute amounts, the built team costs $152,941,662 (very close to the total value of Cagliari Calcio, the 12th team for total cost of the squad). 	
