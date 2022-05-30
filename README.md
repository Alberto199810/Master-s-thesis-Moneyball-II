<p align="center">
  <a href="https://alberto-allegri-moneyball2.herokuapp.com/" target="_blank" rel="noopener noreferrer">
    <img width="500" src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/04_App/notebooks/pict2.png" alt="Thesis logo">
  </a>
</p>

# Statistics and Sport: The Moneyball idea applied to Football world

### Alberto Allegri, Bocconi University, Master's Thesis in Data Science & Business Analytics

**Tech Stack:**<br />
![R](https://img.shields.io/badge/r-%23276DC3.svg?style=for-the-badge&logo=r&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 [<img src='https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white'>](https://alberto-allegri-moneyball2.herokuapp.com/)

## Table of Contents
1. [General Info](#general-info)
2. [Methodology](#methodology)
3. [Repository Structure](#repository-structure)
4. [Results](#results)
5. [Credits](#credits)

## General Info

This repository contains the code for my Master's Thesis, where I try to replicate the moneyball idea (building a team capable of winning the league, but with a restricted budget) using both football statistics coming from [FBRef Scouting Reports](https://fbref.com/en/players/70d74ece/scout/365_euro/Karim-Benzema-Scouting-Report), [Transfermarkt](https://www.transfermarkt.com/) and [PlayeRank](https://github.com/mesosbrodleto/playerank) data together.

If you want a visualization of aggregated PlayeRank data, you can visit the app I built under this link: https://alberto-allegri-moneyball2.herokuapp.com/.


## Methodology

The idea behind the thesis is that we start from a dataset having as independent variables (our ```X```) all the statistics that you can find in the FBRef scouting report, and as dependent variable (our ```y```) the average PlayeRank score of a player for the entire season. The data I had was going from season 2017/2018 to season 2020/2021, for all the players that had a scouting report in FBRef in those season. For each and every single of these players, I had their average PlayeRank score, thanks to the data PlayeRank provided me. Unfortunately, the only dataset I can show you is the one with FBRef data, since PlayeRank data are protected by an NDA.

Thanks to the two obtained datasets (one for Goalkeepers, one for moving players, since variables in the scouting report are different between Goalkeepers and non-Goalkeepers), what I decided to do was the following:

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

Once the 7 different algorithms were applied, if a variable was selected by ```at least 5 out of 7``` algorithms, then it was included in my final choice (final choice can be seen at this [link](https://github.com/Alberto199810/Master-s-thesis-Moneyball-II/blob/main/02_Machine%20Learning/Variables%20per%20role.txt).

Finally, when the variables were selected, I collected the players that won the league from season 2017/2018 to season 2020/2021 in all the top-5 European Leagues (csv can be found at this [link](https://github.com/Alberto199810/Master-s-thesis-Moneyball-II/blob/main/03_Data%20Analytics/Winners/1_league_winners_ref.csv)). Then, I calculated the mean values of the important variables within each role, and, by using the [NORM](https://jermwatt.github.io/machine_learning_refined/notes/16_Linear_algebra/16_5_Norms.html#:~:text=A%20norm%20is%20a%20kind,living%20in%20the%20same%20space.) function, I calculated which observations in my dataset were the closest to the average statistics of the players who actually won the league. But, to this whole reasoning, I applied a restriction: the selected players had to have a Transfermarkt evaluation that was 1/x (X could be selected, basing on how much money we wanted to save) the average value of the players within a certain role in the winning team.

The final result is a full team that is actually costing way less the total cost of the winning team, but that actually had very close performances for the most important statistics to evaluate the total performance of a player in his role!

To retrieve the team for a precise league/season we just have to run low_cost_winners(season, league, factor_to_save).


## Repository Structure

Within the repository, you can see four main folders:
1. **01_Datasets**
2. **02_Machine Learning**
3. **03_Data Analytics**
4. **04_App**

### 01_Datasets
In this folder, you can find the scripts I wrote to build my final dataset. Moreover, in the section [Leagues Comparison](https://github.com/Alberto199810/Master-s-thesis-Moneyball-II/tree/main/01_Datasets/Leagues%20Comparison) you can see the code I applied to standardize statistics across leagues, producing the following map of European Leagues:

<p align="center">
<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/leghe_net.png" class="aligncenter" width="650">
</p>  
  
How was this computed? I took the data regarding all European matches in the last 12 years (from 2010 to 2022), and I generated a contact matrix, with this reasoning (example following):

Given four matches between a Serie A team and a Ligue 1 team with these results (Serie A 2-1 Ligue 1, Ligue 1 3-0 Serie A, Serie A 6-2 Ligue 1, Ligue 1 1-4 Serie A), the starting matrix would be:

|           | Serie A  | Ligue 1  | 
| :-------: | :-------:| :-------: |
| Serie A   |  0  |  3  |   
| Ligue 1   |  8  |  0  |  

Where C<sub>i,j</sub> is the difference with which league j has beaten league i in the matches that j won against i, while C<sub>j,i</sub> is the difference with which league i has beaten league j in the matches that i won against j. Then, to standardize everything and make it consistent, I divided both C<sub>i,j</sub> and C<sub>j,i</sub> by the total amount of matches they played one against the other. So the resulting matrix, in our case, would be:

|           | Serie A  | Ligue 1  | 
| :-------: | :-------:| :-------: |
| Serie A   |  0  |  0.75  |   
| Ligue 1   |  2  |  0  |

By doing like this, we could create a directed graph where the weight of the directed link from node i to node j was equal to C<sub>i,j</sub> (in our case, link **FROM** Ligue 1 **TO** Serie A had a weight of **2**, while link **FROM** Serie A **TO** Ligue 1 had a weight of **0.75**), meaning that a link of a certain weight from node i to node j is generated to represent by how many goals (on average) league i **loses against** league j. 

Finally, to represent everything, the node size in the plot is depending on the average degree of the in-edges. That's how I built the network, with node size representing how ```difficult``` (and for this reason *powerful*) a certain league is. Then, other calculation was applied to obtain 5 final ```difficulty coefficients```, represented in the following table:

|  League  | Difficulty Index | 
| :------------------: | :----------------:|
| La Liga   |  1  | 
| Premier League | 0.996 |     
| Fußball-Bundesliga | 0.931 |
|  Serie A | 0.904 |
|  Ligue 1 | 0.856 |
  
The rest of the scripts (the one in [Player Statistics](https://github.com/Alberto199810/Master-s-thesis-Moneyball-II/tree/main/01_Datasets/Players%20Statistics) folder) are related to building the dataset with the statistics coming both from FBRef and PlayeRank. Once this dataset was defined, I multiplied the FBRef statistics with the difficulty coefficients, to standardize statistics across leagues. 

### 02_Machine Learning
In this folder, you can find the script I built to obtain the chosen variables per each role, applying the 7 different variable selection algorithms.

### 03_Data Analytics
In this folder, you can find both the scripts I wrote to obtain the winners dataset and the jupyter notebook containing the function to get the most similar players to the ones that won the league. Moreover, we built a "Trade-off" value by dividing the Percentage of Money we're saving with the **similarity coefficient** (Similarity is measured as the *distance* from statistics of a player to the average statistics of league winners, computed with norm function) of the low-cost team. 

### 04_App
In this final folder, there is the script for building the app that can be found at this [link](https://alberto-allegri-moneyball2.herokuapp.com/). Code can be found in the notebook "bqplot.ipynb". Then, [voila](https://github.com/voila-dashboards/voila) and [Heroku](https://www.heroku.com/what) were used for the deploy.

This app was created just to have a first view of PlayeRank data, mixed with TransferMarkt valuation, and it will show you:

```
● A preview of PlayeRank data with a boxplot
● A scatterplot with PlayeRank score on the x-axis and TransferMarkt valuation on the y-axis, with size of 
  the scatter dependant on a "Likability" parameter (computed with PlayeRank index/TransferMarkt valuation)
● A pitch where the best 11 players by the likability parameter (divided by role) are represented.
```

Here, a preview with some screenshots of the three plots (various interactive filters can be applied to plots):

<p align="center">
<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/boxplot.png" class="aligncenter" width="750">
</p>
  
<p align="center">
<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/scatterplot.png" class="aligncenter" width="750">
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/Alberto199810/Master-s-thesis-Moneyball-II/main/11 lik.png" class="aligncenter" width="750">
</p>

## Results
The below tables details the similarity coefficient, the percentage savings and the trade off coefficient for the top 5 values obtained for trade off coefficient. Obviously, the higher is trade-off, the best is the combination of similarities of statistics and money we're saving. <br />

| Season       | League  | Similarity Coeff.  | Savings | Trade Off |
| :----------: | :----------:| :-----------------: | :-------: | :---------:|
| 2020-2021    | Serie A     | 4.424397	  |  74.68%   |	16.880303 |
| 2020-2021    | Ligue 1     | 4.480457	  |  75.25%   |	16.796812 |
| 2019-2020    | Serie A     | 5.254009	  |  80.59%	 |  15.338965 |
| 2020-2021    | Bundesliga  | 5.364341	  |  82.05%	 |  15.296018 |
| 2018-2019    | Ligue 1     | 5.763644	  |  84.11%	 |  14.59353  |

By looking at the resulting value, it seems that the best trade-off is found in Serie A 2020/2021, with a **4.424397** similarity coefficient and a **74.68%** save on the budget. Looking at absolute amounts, the built team costs **€152.941.662** (very close to the total value of Cagliari Calcio, the 12th team for total cost of the squad in [Serie A 2020/2021](https://www.gonfialarete.com/2020/10/07/serie-a-2020-2021-il-valore-delle-rose-napoli-sul-podio/)). 

If we look at two of the coefficients we have in our dataset (Likability of the signing and average PlayeRank index), we discover that the two teams are very similar in the total sum of the PlayeRank score (**2.96** for the low-cost players, **3.02** for the winners), but low-cost players have a way higher total likability (**957.38** vs **851.27**). In the following table, the low-cost team for Serie A, 2020/2021: <br />

|	Similarity   |	Player              	| Valuation     |	Position      |
| :------------: | :----------------------:| :--------------: | :--------------:|
|	4.293194     |	Claudio Bravo        |	€1.000.000    |	Goalkeeper    |
|	3.511304	    | Niklas Stark         |	€10.750.000  	| Centre-Back   |
|	3.824119	    | Amir Rrahmani        |	€13.333.333  	| Centre-Back   |
|	4.419091    	| Jordan Torunarigha   |	€11.333.333  	| Centre-Back   |
|	2.988132    	| Bruno Peres         	| €2.666.666	   | Full-Back     |
|	3.917845    	| Andrea Conti        	| €7.166.666	   | Full-Back     |
|	3.961353    	| Maxime Busi         	| €4.250.000	   | Full-Back     |   
|	5.423287	    | Óscar De Marcos      |	€2.333.333	   | Full-Back     |
|	3.433324	    | Roberto Gagliardini  |	€14.666.666  	| Midfielder    |
|	3.889508	    | Jasmin Kurtič	       | €2.833.333    | Midfielder    |
|	4.096985    	| Otávio              	| €7.000.000	   | Midfielder    |
|	5.068749    	| Marko Rog            |	€11.666.666  	| Midfielder    |
|	5.765697	    | Ivan Ilić	           | €5.333.333   	| Midfielder    |
|	6.038868	    | Danilo Cataldi       |	€2.900.000    |	Midfielder    |
|	3.687857	    | Patrik Schick	       | €24.333.333	  | Striker       |
|	5.250205	    | Saša Kalajdžić	      | €12.625.000	  | Striker       |
|	6.221749	    | Sehrou Guirassy	     | €13.000.000	  | Striker       |
|	3.847888	    | Karim Bellarabi	     | €5.750.000   	| Winger        |

## Credits
This repository is by Alberto Allegri (alberto.allegri@studbocconi.com) as part of the Master's Thesis in Data Science & Business Analytics at Boccony University, with the supervision of professor [Carlo Ambrogio Favero](https://didattica.unibocconi.eu/myigier/index.php?IdUte=48917&idr=1753&lingua=eng).
