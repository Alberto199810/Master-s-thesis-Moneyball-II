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

year = c(2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020)
contact_matrix = data.frame()

links = c("https://fbref.com/en/comps/8/history/UEFA-Champions-League-Seasons",
          "https://fbref.com/en/comps/19/history/UEFA-Europa-League-Seasons")

for (link in links){
  
  for (i in year){
    
    print(i)
    
    tryCatch({
      
      match_logs = data.frame(get_match_urls(country = "", gender = "M", season_end_year = i, tier = "", non_dom_league_url = link))
      for (j in 1:dim(match_logs)[1]){
        data_to_app = data.frame()
        match_data <- get_match_report(match_url = match_logs[j,])
        data_to_app = match_data[,c("Home_Team","Away_Team")]
        if ((match_data$Home_Score - match_data$Away_Score) > 0) {
          data_to_app$Winner = match_data$Home_Team
          data_to_app$DR = match_data$Home_Score - match_data$Away_Score
        } else if ((match_data$Home_Score - match_data$Away_Score) < 0) {
          data_to_app$Winner = match_data$Away_Team
          data_to_app$DR = match_data$Away_Score - match_data$Home_Score
        } else {
          next
        }
        contact_matrix = rbind(contact_matrix, data_to_app)
        closeAllConnections()
      }
      
    }, error = function(e){})
    
  } 
  
}

write.csv(contact_matrix,'data_matches.csv')