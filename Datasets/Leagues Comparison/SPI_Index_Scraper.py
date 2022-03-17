import pandas as pd
import numpy as np

second_ranking = pd.read_html('https://www.globalfootballrankings.com/')[0]

second_ranking = second_ranking[['League','Average SPI']]

second_ranking['League'] = ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1', 
                            'Liga Portuguesa', 'Eredivisie', 'Brasileiro Série A',
                            'Mexican Primera Division Torneo Clausura', 'Russian League', 
                            'English League Championship', 'Austrian Bundesliga','Belgian League', 
                            'Turkish League', 'Swiss Super League', 'Denmark League', 'MLS', 
                            'Argentina Primera Division', 'Scottish Premiership', 
                            'Japanese J League' , 'German 2. Bundesliga', 'Greece League', 
                            'Norway League', 'Italy Serie B','Spanish Segunda Division', 
                            'French Ligue 2','Sweden League', 'Chinese Super League',
                            'Australian A-League', 'English League One','United Soccer League', 
                            'South African ABSA Premier League', 'English League Two']

lista_SPI = [i for i in second_ranking['Average SPI']]
lista_SPI.append(0)

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

scaled_SPI = NormalizeData(lista_SPI)
second_ranking['Average SPI'] = scaled_SPI[:-1]

second_ranking.to_csv('SPI_Index.csv')