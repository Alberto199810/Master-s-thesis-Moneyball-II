#clear the environment 
rm(list=ls()) 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

#Library for scraping data from FBref.com
#devtools::install_github("JaseZiv/worldfootballR")

listofpackages <- c("worldfootballR", "dplyr", "devtools", "dplyr", "httr", "stringr")

for (j in listofpackages){
  if(sum(installed.packages()[, 1] == j) == 0) {
    install.packages(j)
  }
  library(j, character.only = T)
}

#Saving as a dataframe the data regarding FBref & Transfermarkt links for every player
mapped_players <- player_dictionary_mapping()

#Taking list of players
players = mapped_players[,"PlayerFBref"]
numb = dim(players)[1]

#Initializing our dataframes
df_players = data.frame()
df_keepers = data.frame()

for (i in (1:numb)){
  tryCatch({
    
    print(i)
    
    #First Step, select the player and store FBref and TRM links
    player_FB = unlist(c(mapped_players[i,"UrlFBref"]))
    player_TRM = unlist(c(mapped_players[i,"UrlTmarkt"]))
    
    #Now scrape both from FBref and Transfermarkt
    new_player_FB = data.frame()
    new_player_TRM = data.frame()
    new_player_FB = fb_player_scouting_report(player_url = player_FB, pos_versus = "primary")
    new_player_TRM = tm_player_bio(player_url = player_TRM)
    
    #Skip players that do not have scouting report, to fasten the scraping
    if (isTRUE(dim(new_player_FB)[1] == 0) == TRUE){
      next}
    
    #Select FBref data for the last 365 days, or, if missing, the most recent one
    players_data = subset(new_player_FB, scouting_period == "Last 365 Days" | scouting_period == new_player_FB[1,"scouting_period"])
    #Save scouting period, will be useful later
    scout_per = unique(players_data$scouting_period)
    
    #Transpose the dataframe
    players_data = data.frame(t(players_data))
    
    #Put the Statistic row as header
    names(players_data) = c(players_data["Statistic",])
    
    #Select the statistics
    players_data = data.frame(players_data["Per90",])
    
    #Change index
    rownames(players_data) <- unlist(c(mapped_players[i,"PlayerFBref"]))
    
    #Add various columns
    players_data$scouting_period = scout_per #Scouting period
    players_data$Player_valuation = as.integer(unlist(c(new_player_TRM[,"player_valuation"]))) #Valuation
    
    #Skip players that do not have valuation
    if (isTRUE(is.na(players_data$Player_valuation)) == TRUE){
      next}
    
    players_data$Age = new_player_TRM$age #Age
    players_data$Height = new_player_TRM$height #Height
    players_data$Position = unlist(c(mapped_players[i,"TmPos"])) #Position in the field
    players_data$Foot = new_player_TRM$foot #Preferred foot
    contr_left = as.Date(new_player_TRM$contract_expires) - as.Date("2022-03-03")
    players_data$Y_Contract_Left = as.numeric(contr_left, units="days")/365 #Year of contract left
    players_data$Actual_Club = new_player_TRM$current_club #Actual club (for season 2021/2022)
    
    #To add the league
    player_stats = fb_player_season_stats(player_FB, stat_type = "playing_time")
    if (players_data$scouting_period == "Last 365 Days"){
      player_stats = subset(player_stats, Season == "2021-2022" | Season == "2022" | Season == "2021")
    } else {
      player_stats = subset(player_stats, Season == substring(unique(players_data$scouting_period),1,9))
    }
    camp = c()
    for (i in player_stats$Comp){
      x = substring(i,1,1)
      if (isTRUE(!is.na(as.numeric(x)) == TRUE)){
        camp = c(camp, i)
        } else {next}
    }
    campionato = unlist(c(camp))
    campionato = campionato[campionato != "1. Champions Lg" & 
                            campionato != "2. Europa Lg" & 
                            campionato != "3. Conf Lg" &
                            campionato != "3. 3. Liga"]
    campionato = tail(campionato, n=1)
    players_data$Data_League = substring(campionato,4,nchar(campionato)) 
    #Here, we basically appended a column related to the LEAGUE from which data are scraped.
    #Indeed, there were some cases where the player at the end of season 2020/2021 changed club,
    #But data for season 2021/2022 weren't available. So to have more data, we took the data
    #of season 2020/2021, but the league was different from the CURRENT LEAGUE. For this reason,
    #In this column we put the LEAGUE name where the data took place.
    
    #Append the dataframes basing on position)
    if (isTRUE(dim(players_data)[2] >= 30) == TRUE){
      if (isTRUE(players_data$Position=="Goalkeeper") == TRUE){
        df_keepers = rbind(df_keepers, players_data)
        } else {
        df_players = rbind(df_players, players_data)
        }
    } else {next}
  }, error = function(e){})
}

#Making Index the first column (Player Name)
df_players = cbind(Player_Names = rownames(df_players), df_players)
#Delete column of scouting period, it's useless
df_players$scouting_period <- NULL
#Rename rows
rownames(df_players) = 1:nrow(df_players)
#Rearrange the dataset
df_players <- df_players %>% relocate(Player_valuation,
                                      Age,
                                      Height,
                                      Position,
                                      Foot,
                                      Y_Contract_Left,
                                      Actual_Club,
                                      Data_League,
                                      .before = Goals)

#Making Index the first column (Keeper Name)
df_keepers = cbind(Keeper_Names = rownames(df_keepers), df_keepers)
#Delete column of scouting period, it's useless
df_keepers$scouting_period <- NULL
#Rename rows
rownames(df_keepers) = 1:nrow(df_keepers)
#Rearrange the dataset
df_keepers <- df_keepers %>% relocate(Player_valuation,
                                      Age,
                                      Height,
                                      Position,
                                      Foot,
                                      Y_Contract_Left,
                                      Actual_Club,
                                      Data_League,
                                      .before = Goals.Against)

#Saving the two datasets
write.csv(df_players,'df_players.csv')
write.csv(df_keepers,'df_keepers.csv')