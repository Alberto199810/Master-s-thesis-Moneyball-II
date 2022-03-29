#Let's initialize our script
rm(list=ls()) 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
  
#Library for scraping data from FBref.com
#devtools::install_github("JaseZiv/worldfootballR")
  
listofpackages <- c("worldfootballR", "dplyr", "devtools", "dplyr", "httr", "stringr", "plyr")
  
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
    pos = unlist(c(mapped_players[i,"TmPos"]))
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
    
    #Let's initialize our dataframes
    players_data = data.frame() 
    player_data_mom = data.frame()
    
    #And now let's scrape all available years for each player
    for (i in unique(new_player_FB$scouting_period)){
      player_data_mom = subset(new_player_FB, scouting_period == i)
      player_data_mom = data.frame(t(player_data_mom))
      names(player_data_mom) = c(player_data_mom["Statistic",])
      player_data_mom = data.frame(player_data_mom["Per90",])
      player_data_mom$scouting_period = i
      players_data = rbind.fill(players_data, player_data_mom)
    }
    
    #Take the tail of the dataframe, and then exclude "Last 365 Days" report
    players_data = tail(players_data, n = length(unique(new_player_FB$scouting_period)))   
    players_data = subset(players_data, scouting_period != "Last 365 Days")
    
    #Insert Trasnfermarket link, it will be useful when we'll have to scrape valuation
    players_data$link_TRM = player_TRM

    #Now let's add some other important columns
    if (is.na(new_player_TRM$date_of_birth) == TRUE) {
      year_born = 2022-as.integer(new_player_TRM$age)
      players_data$Age = (as.integer(substr(players_data[,'scouting_period'],6,9))) - (2022-as.integer(new_player_TRM$age))
    } else {
      players_data$Age = as.integer(ceiling(difftime(paste(substr(players_data[,'scouting_period'],6,9), "-6-10", sep=""), new_player_TRM$date_of_birth, units = "days")/365))
    }
    players_data$Height = new_player_TRM$height #Height
    players_data$Player_SN = unique(new_player_FB$Player)
    if ('name_in_home_country' %in% names(new_player_TRM) == TRUE) {
      players_data$Player_LN = new_player_TRM$name_in_home_country
    } else {
      players_data$Player_LN = unique(new_player_FB$Player)
    }
    players_data$Position = pos #Position in the field
    players_data$Foot = new_player_TRM$foot #Preferred foot

    #To add the league
    players_data$Data_League = substr(players_data$scouting_period,11,nchar(players_data$scouting_period))
    players_data$scouting_period = substr(players_data$scouting_period,1,9)

    #Append the dataframes basing on position)
    if (isTRUE(dim(players_data)[2] >= 30) == TRUE){
      if (isTRUE(players_data$Position[1] =="Goalkeeper") == TRUE){
        df_keepers = rbind.fill(df_keepers, players_data)
      } else {
        df_players = rbind(df_players, players_data)
      }
    } else {next}
  }, error = function(e){})
}

#Rename rows
rownames(df_players) = 1:nrow(df_players)
#Rearrange the dataset
df_players <- df_players %>% relocate(Player_SN,
                                      Player_LN,
                                      link_TRM,
                                      scouting_period,
                                      Age,
                                      Height,
                                      Position,
                                      Foot,
                                      Data_League,
                                      .before = Goals)

#Rename rows
rownames(df_keepers) = 1:nrow(df_keepers)
#Rearrange the dataset
df_keepers <- df_keepers %>% relocate(Player_SN,
                                      Player_LN,
                                      link_TRM,
                                      scouting_period,
                                      Age,
                                      Height,
                                      Position,
                                      Foot,
                                      Data_League,
                                      .before = Goals.Against)

#Saving the two datasets
write.csv(df_players,'df_players.csv')
write.csv(df_keepers,'df_keepers.csv')