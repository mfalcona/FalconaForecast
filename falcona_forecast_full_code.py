# falcona forecast full code
# contains integrated code from ff_data_coll, ff_model_top5, and results_collector for each top 5 league
# this code will automatically populate predictions, past results, and updated calendar for each league
# will also update all trends, power ratings, etc

# licensed for use by Matt Falcona or with expressed, written consent by Matt Falcona
# 11/21/21

# current season results collector

"""
Created on Sun Oct 24 2021

@author: matthewfalcona
"""

# use this code to retrieve current season results and future schedule for the top 5 leagues
# will feed into ML model, post-game win expectancy model, and results tracker

# imports

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
from datetime import date

curr_date = date.today()
curr_date = pd.to_datetime(curr_date)

"""
# scraping Scores and Fixtures site
ita_url = "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures"
#ita_url = "https://fbref.com/en/comps/11/11611/schedule/2022-2023-Serie-A-Scores-and-Fixtures"
ita_page = requests.get(ita_url)
ita_soup = BeautifulSoup(ita_page.content, 'html.parser')
ita_stats = ['date','home_team','home_xg','score','away_xg','away_team']
ita_stats_list = [[td.getText() for td in ita_soup.find_all('td', {'data-stat': stat})] for stat in ita_stats]
seriea_sched = pd.DataFrame(ita_stats_list).T

# building schedule df
seriea_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
seriea_sched['Date'] = pd.to_datetime(seriea_sched['Date'])
seriea_sched[['League','Season']] = ['Serie A','2022-23']

# dropping xG and Score from schedule df
seriea_sched = seriea_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]

# defining results df
seriea_results = seriea_sched[seriea_sched['Date'] < curr_date]

# dropping xg and score from schedule df
seriea_sched = seriea_sched.drop(['HxG','Score','AxG'], axis = 1)

# building results df
# seriea_results[['Hscore','Ascore']] = seriea_results['Score'].str.split('-', 1, expand=True)
seriea_results = seriea_results.replace('',np.nan,regex=True)
seriea_results = seriea_results.dropna()
seriea_results['Hscore'] = seriea_results['Score'].str[:1].astype(int)
seriea_results['Ascore'] = seriea_results['Score'].str[-1:].astype(int)
seriea_results = seriea_results.drop('Score',axis = 1)
seriea_results['Total'] = seriea_results['Hscore'] + seriea_results['Ascore']
seriea_results['Act_Diff'] = seriea_results['Hscore'] - seriea_results['Ascore']
seriea_results['HxG'] = seriea_results['HxG'].replace('',0,regex=True)
seriea_results['AxG'] = seriea_results['AxG'].replace('',0,regex=True)
seriea_results['HxG'] = seriea_results['HxG'].astype(float)
seriea_results['AxG'] = seriea_results['AxG'].astype(float)
seriea_results['xG_Diff'] = seriea_results['HxG'] - seriea_results['AxG']
seriea_results['Result'] = np.select(condlist=[seriea_results['Act_Diff'] > 0, seriea_results['Act_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
seriea_results['xResult'] = np.select(condlist=[seriea_results['xG_Diff'] > 0, seriea_results['xG_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
seriea_results['Act_vs_Exp_Result'] = np.select(condlist=[seriea_results['Result'] == seriea_results['xResult']], choicelist = ['Same'], default = 'Diff')
seriea_results['xTotal'] = seriea_results['HxG'] + seriea_results['AxG']

col_order = ['Home','Away','League','Season','Date','Hscore','Ascore','Result','Total','HxG','AxG', 'xResult', 'xTotal','Act_Diff','xG_Diff','Act_vs_Exp_Result']

seriea_results = seriea_results[col_order]


###################################################################################################
# spain

spa_url = "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures"
#spa_url = "https://fbref.com/en/comps/12/11573/schedule/2022-2023-La-Liga-Scores-and-Fixtures"
spa_page = requests.get(spa_url)
spa_soup = BeautifulSoup(spa_page.content, 'html.parser')
spa_stats = ['date','home_team','home_xg','score','away_xg','away_team']
spa_stats_list = [[td.getText() for td in spa_soup.find_all('td', {'data-stat': stat})] for stat in spa_stats]
laliga_sched = pd.DataFrame(spa_stats_list).T

# building schedule df
laliga_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
laliga_sched['Date'] = pd.to_datetime(laliga_sched['Date'])
laliga_sched[['League','Season']] = ['La Liga','2022-23']

# dropping xG and Score from schedule df
laliga_sched = laliga_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]

# defining results df
laliga_results = laliga_sched[laliga_sched['Date'] < curr_date]

# dropping xg and score from schedule df
laliga_sched = laliga_sched.drop(['HxG','Score','AxG'], axis = 1)

# building results df
#laliga_results[['Hscore','Ascore']] = laliga_results['Score'].str.split('-', 1, expand=True)
laliga_results = laliga_results.replace('',np.nan,regex=True)
laliga_results = laliga_results.dropna()
laliga_results['Hscore'] = laliga_results['Score'].str[:1].astype(int)
laliga_results['Ascore'] = laliga_results['Score'].str[-1:].astype(int)
laliga_results = laliga_results.drop('Score',axis = 1)
laliga_results['Total'] = laliga_results['Hscore'] + laliga_results['Ascore']
laliga_results['Act_Diff'] = laliga_results['Hscore'] - laliga_results['Ascore']
laliga_results['HxG'] = laliga_results['HxG'].replace('',0,regex=True)
laliga_results['AxG'] = laliga_results['AxG'].replace('',0,regex=True)
laliga_results['HxG'] = laliga_results['HxG'].astype(float)
laliga_results['AxG'] = laliga_results['AxG'].astype(float)
laliga_results['xG_Diff'] = laliga_results['HxG'] - laliga_results['AxG']
laliga_results['Result'] = np.select(condlist=[laliga_results['Act_Diff'] > 0, laliga_results['Act_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
laliga_results['xResult'] = np.select(condlist=[laliga_results['xG_Diff'] > 0, laliga_results['xG_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
laliga_results['Act_vs_Exp_Result'] = np.select(condlist=[laliga_results['Result'] == laliga_results['xResult']], choicelist = ['Same'], default = 'Diff')
laliga_results['xTotal'] = laliga_results['HxG'] + laliga_results['AxG']

col_order = ['Home','Away','League','Season','Date','Hscore','Ascore','Result','Total','HxG','AxG', 'xResult', 'xTotal','Act_Diff','xG_Diff','Act_vs_Exp_Result']

laliga_results = laliga_results[col_order]


#########################################################################################
# france

fra_url = "https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures"
#fra_url = "https://fbref.com/en/comps/13/11585/schedule/2022-2023-Ligue-1-Scores-and-Fixtures"
fra_page = requests.get(fra_url)
fra_soup = BeautifulSoup(fra_page.content, 'html.parser')
fra_stats = ['date','home_team','home_xg','score','away_xg','away_team']
fra_stats_list = [[td.getText() for td in fra_soup.find_all('td', {'data-stat': stat})] for stat in fra_stats]
ligue1_sched = pd.DataFrame(fra_stats_list).T

# building schedule df
ligue1_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
ligue1_sched['Date'] = pd.to_datetime(ligue1_sched['Date'])
ligue1_sched[['League','Season']] = ['Ligue 1','2022-23']

# dropping xG and Score from schedule df
ligue1_sched = ligue1_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]

# defining results df
ligue1_results = ligue1_sched[ligue1_sched['Date'] < curr_date]

# dropping xg and score from schedule df
ligue1_sched = ligue1_sched.drop(['HxG','Score','AxG'], axis = 1)


# building results df
# ligue1_results[['Hscore','Ascore']] = ligue1_results['Score'].str.split('-', 1, expand=True)
ligue1_results = ligue1_results.replace('',np.nan,regex=True)
ligue1_results = ligue1_results.dropna()
ligue1_results['Hscore'] = ligue1_results['Score'].str[:1].astype(int)
ligue1_results['Ascore'] = ligue1_results['Score'].str[-1:].astype(int)
ligue1_results = ligue1_results.drop('Score',axis = 1)
ligue1_results['Total'] = ligue1_results['Hscore'] + ligue1_results['Ascore']
ligue1_results['Act_Diff'] = ligue1_results['Hscore'] - ligue1_results['Ascore']
ligue1_results['HxG'] = ligue1_results['HxG'].replace('',0,regex=True)
ligue1_results['AxG'] = ligue1_results['AxG'].replace('',0,regex=True)
ligue1_results['HxG'] = ligue1_results['HxG'].astype(float)
ligue1_results['AxG'] = ligue1_results['AxG'].astype(float)
ligue1_results['xG_Diff'] = ligue1_results['HxG'] - ligue1_results['AxG']
ligue1_results['Result'] = np.select(condlist=[ligue1_results['Act_Diff'] > 0, ligue1_results['Act_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
ligue1_results['xResult'] = np.select(condlist=[ligue1_results['xG_Diff'] > 0, ligue1_results['xG_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
ligue1_results['Act_vs_Exp_Result'] = np.select(condlist=[ligue1_results['Result'] == ligue1_results['xResult']], choicelist = ['Same'], default = 'Diff')
ligue1_results['xTotal'] = ligue1_results['HxG'] + ligue1_results['AxG']

col_order = ['Home','Away','League','Season','Date','Hscore','Ascore','Result','Total','HxG','AxG', 'xResult', 'xTotal','Act_Diff','xG_Diff','Act_vs_Exp_Result']

ligue1_results = ligue1_results[col_order]



#########################################################################################
# germany

ger_url = "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures"
#ger_url = "https://fbref.com/en/comps/20/11593/schedule/2022-2023-Bundesliga-Scores-and-Fixtures"
ger_page = requests.get(ger_url)
ger_soup = BeautifulSoup(ger_page.content, 'html.parser')
ger_stats = ['date','home_team','home_xg','score','away_xg','away_team']
ger_stats_list = [[td.getText() for td in ger_soup.find_all('td', {'data-stat': stat})] for stat in ger_stats]
bund_sched = pd.DataFrame(ger_stats_list).T

# building schedule df
bund_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
bund_sched['Date'] = pd.to_datetime(bund_sched['Date'])
bund_sched[['League','Season']] = ['Bundesliga','2022-23']

# dropping xG and Score from schedule df
bund_sched = bund_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]

# dropping xg and score from schedule df
bund_sched = bund_sched.drop(['HxG','Score','AxG'], axis = 1)


# defining results df
bund_results = bund_sched[bund_sched['Date'] < curr_date]


# building results df
#bund_results[['Hscore','Ascore']] = bund_results['Score'].str.split('-', 1, expand=True)
bund_results = bund_results.replace('',np.nan,regex=True)
bund_results = bund_results.dropna()
bund_results['Hscore'] = bund_results['Score'].str[:1].astype(int)
bund_results['Ascore'] = bund_results['Score'].str[-1:].astype(int)
bund_results = bund_results.drop('Score',axis = 1)
bund_results['Total'] = bund_results['Hscore'] + bund_results['Ascore']
bund_results['Act_Diff'] = bund_results['Hscore'] - bund_results['Ascore']
bund_results['HxG'] = bund_results['HxG'].replace('',0,regex=True)
bund_results['AxG'] = bund_results['AxG'].replace('',0,regex=True)
bund_results['HxG'] = bund_results['HxG'].astype(float)
bund_results['AxG'] = bund_results['AxG'].astype(float)
bund_results['xG_Diff'] = bund_results['HxG'] - bund_results['AxG']
bund_results['Result'] = np.select(condlist=[bund_results['Act_Diff'] > 0, bund_results['Act_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
bund_results['xResult'] = np.select(condlist=[bund_results['xG_Diff'] > 0, bund_results['xG_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
bund_results['Act_vs_Exp_Result'] = np.select(condlist=[bund_results['Result'] == bund_results['xResult']], choicelist = ['Same'], default = 'Diff')
bund_results['xTotal'] = bund_results['HxG'] + bund_results['AxG']


col_order = ['Home','Away','League','Season','Date','Hscore','Ascore','Result','Total','HxG','AxG', 'xResult', 'xTotal','Act_Diff','xG_Diff','Act_vs_Exp_Result']

bund_results = bund_results[col_order]

bund_results.to_csv('/Users/matthewfalcona/FalconaForecast/data/buli_results_2022_08_25.csv')


bund_results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/buli_results_2022_08_25.csv')

######################################################################################
# england

eng_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
#eng_url = "https://fbref.com/en/comps/9/11566/schedule/2022-2023-Premier-League-Scores-and-Fixtures"
eng_page = requests.get(eng_url)
eng_soup = BeautifulSoup(eng_page.content, 'html.parser')
eng_stats = ['date','home_team','home_xg','score','away_xg','away_team']
eng_stats_list = [[td.getText() for td in eng_soup.find_all('td', {'data-stat': stat})] for stat in eng_stats]
epl_sched = pd.DataFrame(eng_stats_list).T

# building schedule df
epl_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
epl_sched['Date'] = pd.to_datetime(epl_sched['Date'])
epl_sched[['League','Season']] = ['Premier League','2022-23']

# dropping xG and Score from schedule df
epl_sched = epl_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]

# dropping xg and score from schedule df
epl_sched = epl_sched.drop(['HxG','Score','AxG'], axis = 1)

# defining results df
epl_results = epl_sched[epl_sched['Date'] < curr_date]


#uncomment after first match days

# building results df
# epl_results[['Hscore','Ascore']] = epl_results['Score'].str.split('-', 1, expand=True)
epl_results = epl_results.replace('',np.nan,regex=True)
epl_results = epl_results.dropna()
epl_results['Hscore'] = epl_results['Score'].str[:1].astype(int)
epl_results['Ascore'] = epl_results['Score'].str[-1:].astype(int)
epl_results = epl_results.drop('Score',axis = 1)
epl_results['Total'] = epl_results['Hscore'] + epl_results['Ascore']
epl_results['Act_Diff'] = epl_results['Hscore'] - epl_results['Ascore']
epl_results['HxG'] = epl_results['HxG'].replace('',0,regex=True)
epl_results['AxG'] = epl_results['AxG'].replace('',0,regex=True)
epl_results['HxG'] = epl_results['HxG'].astype(float)
epl_results['AxG'] = epl_results['AxG'].astype(float)
epl_results['xG_Diff'] = epl_results['HxG'] - epl_results['AxG']
epl_results['Result'] = np.select(condlist=[epl_results['Act_Diff'] > 0, epl_results['Act_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
epl_results['xResult'] = np.select(condlist=[epl_results['xG_Diff'] > 0, epl_results['xG_Diff'] < 0], choicelist = ['Home','Away'], default = 'Draw')
epl_results['Act_vs_Exp_Result'] = np.select(condlist=[epl_results['Result'] == epl_results['xResult']], choicelist = ['Same'], default = 'Diff')
epl_results['xTotal'] = epl_results['HxG'] + epl_results['AxG']

col_order = ['Home','Away','League','Season','Date','Hscore','Ascore','Result','Total','HxG','AxG', 'xResult', 'xTotal','Act_Diff','xG_Diff','Act_vs_Exp_Result']

epl_results = epl_results[col_order]

epl_results.to_csv('/Users/matthewfalcona/FalconaForecast/data/epl_results_2022_08_25.csv')


epl_results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/epl_results_2022_08_25.csv')


# compiling forecast/schedule df
forecast_sched = seriea_sched
forecast_sched = forecast_sched.append(ligue1_sched)
forecast_sched = forecast_sched.append(epl_sched)
forecast_sched = forecast_sched.append(bund_sched)
forecast_sched = forecast_sched.append(laliga_sched)
forecast_sched = forecast_sched.reset_index()

# normalizing team names
forecast_sched = forecast_sched.replace("Eint Frankfurt", "Frankfurt", regex = True)
forecast_sched = forecast_sched.replace("West Ham United", "WestHam", regex = True)
forecast_sched = forecast_sched.replace("Hellas Verona FC", "Verona", regex = True)
forecast_sched = forecast_sched.replace("Hertha BSC", "Hertha", regex = True)
forecast_sched = forecast_sched.replace("M'Gladbach", "Gladbach", regex = True)
forecast_sched = forecast_sched.replace("Bayern Munich", "Bayern", regex = True)
forecast_sched = forecast_sched.replace("FSV Mainz", "Mainz", regex = True)
forecast_sched = forecast_sched.replace("Mainz 05", "Mainz", regex = True)
forecast_sched = forecast_sched.replace("Greuther Fürth", "GreutherFurth", regex = True)
forecast_sched = forecast_sched.replace("Union Berlin", "UnionBerlin", regex = True)
forecast_sched = forecast_sched.replace("RB Leipzig", "RBLeipzig", regex = True)
forecast_sched = forecast_sched.replace("Werder Bremen", "WerderBremen", regex = True)
forecast_sched = forecast_sched.replace("Schalke 04", "Schalke", regex = True)
forecast_sched = forecast_sched.replace("Düsseldorf", "Dusseldorf", regex = True)
forecast_sched = forecast_sched.replace("Paderborn 07", "Paderborn", regex = True)
forecast_sched = forecast_sched.replace("Hannover 96", "Hannover", regex = True)
forecast_sched = forecast_sched.replace("Köln", "Koln", regex = True)
forecast_sched = forecast_sched.replace("Hamburger SV", "Hamburg", regex = True)
forecast_sched = forecast_sched.replace("Manchester City", "ManCity", regex = True)
forecast_sched = forecast_sched.replace("Manchester Utd", "ManUtd", regex = True)
forecast_sched = forecast_sched.replace("Leicester City", "Leicester", regex = True)
forecast_sched = forecast_sched.replace("Newcastle Utd", "Newcastle", regex = True)
forecast_sched = forecast_sched.replace("Crystal Palace", "CrystalPalace", regex = True)
forecast_sched = forecast_sched.replace("Swansea City", "Swansea", regex = True)
forecast_sched = forecast_sched.replace("Stoke City", "StokeCity", regex = True)
forecast_sched = forecast_sched.replace("West Brom", "WestBrom", regex = True)
forecast_sched = forecast_sched.replace("West Ham", "WestHam", regex = True)
forecast_sched = forecast_sched.replace("Cardiff City", "Cardiff", regex = True)
forecast_sched = forecast_sched.replace("Sheffield Utd", "SheffieldUtd", regex = True)
forecast_sched = forecast_sched.replace("Norwich City", "NorwichCity", regex = True)
forecast_sched = forecast_sched.replace("Leeds United", "LeedsUtd", regex = True)
forecast_sched = forecast_sched.replace("Aston Villa", "AstonVilla", regex = True)
forecast_sched = forecast_sched.replace('Hellas Verona','HellasVerona', regex = True)
forecast_sched = forecast_sched.replace("Paris S-G", "PSG", regex = True)
forecast_sched = forecast_sched.replace("Clermont Foot", "Clermont", regex = True)
forecast_sched = forecast_sched.replace("Saint-Étienne", "Saint-Etienne", regex = True)
forecast_sched = forecast_sched.replace("Nîmes", "Nimes", regex = True)
forecast_sched = forecast_sched.replace("Real Madrid", "RealMadrid", regex = True)
forecast_sched = forecast_sched.replace("Atlético Madrid", "Atletico", regex = True)
forecast_sched = forecast_sched.replace("Athletic Club", "AthleticBilbao", regex = True)
forecast_sched = forecast_sched.replace("Real Sociedad", "RealSociedad", regex = True)
forecast_sched = forecast_sched.replace("Rayo Vallecano", "RayoVallecano", regex = True)
forecast_sched = forecast_sched.replace("Celta Vigo", "CeltaVigo", regex = True)
forecast_sched = forecast_sched.replace("Alavés", "Alaves", regex = True)
forecast_sched = forecast_sched.replace("Cádiz", "Cadiz", regex = True)
forecast_sched = forecast_sched.replace("Leganés", "Leganes", regex = True)
forecast_sched = forecast_sched.replace("La Coruña", "LaCoruna", regex = True)
forecast_sched = forecast_sched.replace("Las Palmas", "LasPalmas", regex = True)
forecast_sched = forecast_sched.replace("Málaga", "Malaga", regex = True)
forecast_sched = forecast_sched.replace('AC Milan','Milan', regex=True)
forecast_sched = forecast_sched.replace('Celta Vigo','CeltaVigo', regex=True)
forecast_sched = forecast_sched.replace('Rayo Vallecano','RayoVallecano', regex=True)
forecast_sched = forecast_sched.replace('Alavés','Alaves', regex=True)
forecast_sched = forecast_sched.replace('Granada CF','Granada', regex=True)
forecast_sched = forecast_sched.replace('Real Sociedad','RealSociedad', regex=True)
forecast_sched = forecast_sched.replace('Real Madrid','RealMadrid', regex=True)
forecast_sched = forecast_sched.replace('SC Freiburg','Freiburg', regex=True)
forecast_sched = forecast_sched.replace('Eintracht Frankfurt','Frankfurt', regex=True)
forecast_sched = forecast_sched.replace('Borussia Monchengladbach','Gladbach', regex=True)
forecast_sched = forecast_sched.replace('Union Berlin','UnionBerlin', regex=True)
forecast_sched = forecast_sched.replace('Greuther Fürth','GreutherFurth', regex=True)
forecast_sched = forecast_sched.replace('Borussia Dortmund','Dortmund', regex=True)
forecast_sched = forecast_sched.replace('Bayer Leverkusen','Leverkusen', regex=True)
forecast_sched = forecast_sched.replace('TSG Hoffenheim','Hoffenheim', regex=True)
forecast_sched = forecast_sched.replace('Leicester City','Leicester', regex=True)
forecast_sched = forecast_sched.replace('Norwich City','NorwichCity', regex=True)
forecast_sched = forecast_sched.replace('Manchester City','ManCity', regex=True)
forecast_sched = forecast_sched.replace('Aston Villa','AstonVilla', regex=True)
forecast_sched = forecast_sched.replace('Newcastle United','Newcastle', regex=True)
forecast_sched = forecast_sched.replace('Paris Saint Germain','PSG', regex=True)
forecast_sched = forecast_sched.replace('Hellas Verona FC','HellasVerona', regex=True)
forecast_sched = forecast_sched.replace('AS Roma','Roma', regex=True)
forecast_sched = forecast_sched.replace('Inter Milan','Inter', regex=True)
forecast_sched = forecast_sched.replace('Atalanta BC','Atalanta', regex=True)
forecast_sched = forecast_sched.replace('Cádiz CF','Cadiz', regex=True)
forecast_sched = forecast_sched.replace('Elche CF','Elche', regex=True)
forecast_sched = forecast_sched.replace('Real Betis','Betis', regex=True)
forecast_sched = forecast_sched.replace('Atlético Madrid','Atletico', regex=True)
forecast_sched = forecast_sched.replace('CA Osasuna','Osasuna', regex=True)
forecast_sched = forecast_sched.replace('Athletic Bilbao','AthleticBilbao', regex=True)
forecast_sched = forecast_sched.replace('Arminia Bielefeld','Arminia', regex=True)
forecast_sched = forecast_sched.replace('RB Leipzig','RBLeipzig', regex=True)
forecast_sched = forecast_sched.replace('Hertha Berlin','Hertha', regex=True)
forecast_sched = forecast_sched.replace('VfB Stuttgart','Stuttgart', regex=True)
forecast_sched = forecast_sched.replace('VfL Wolfsburg','Wolfsburg', regex=True)
forecast_sched = forecast_sched.replace('VfL Bochum','Bochum', regex=True)
forecast_sched = forecast_sched.replace('FSV Mainz 05','Mainz', regex=True)
forecast_sched = forecast_sched.replace('Bayern Munich','Bayern', regex=True)
forecast_sched = forecast_sched.replace('FC Koln','Koln', regex=True)
forecast_sched = forecast_sched.replace('Manchester United','ManUtd', regex=True)
forecast_sched = forecast_sched.replace('Brighton and Hove Albion','Brighton', regex=True)
forecast_sched = forecast_sched.replace('Leeds United','LeedsUtd', regex=True)
forecast_sched = forecast_sched.replace('Wolverhampton Wanderers','Wolves', regex=True)
forecast_sched = forecast_sched.replace('Tottenham Hotspur','Tottenham', regex=True)
forecast_sched = forecast_sched.replace('Crystal Palace','CrystalPalace', regex=True)
forecast_sched = forecast_sched.replace('Saint Etienne','Saint-Etienne', regex=True)
forecast_sched = forecast_sched.replace('Stade de Reims','Reims', regex=True)
forecast_sched = forecast_sched.replace('AS Monaco','Monaco', regex=True)
forecast_sched = forecast_sched.replace('RC Lens','Lens', regex=True)
forecast_sched = forecast_sched.replace("Nott'ham Forest", "Forest", regex=True)
forecast_sched = forecast_sched.replace('Nottingham Forest','Forest', regex=True)
forecast_sched = forecast_sched.replace('Werder Bremen','WerderBremen', regex=True)
forecast_sched = forecast_sched.replace('Almería','Almeria', regex=True)
forecast_sched = forecast_sched.replace('AC Ajaccio','Ajaccio', regex=True)

forecast_sched['Match'] = forecast_sched['Home'] + '-' + forecast_sched['Away']

# uncomment after first matchdays


# compiling results df
results = seriea_results
results = results.append(epl_results)
results = results.append(ligue1_results)
results = results.append(laliga_results)
results = results.append(bund_results)
results = results.reset_index()

# normalizing team names
results = results.replace("Eint Frankfurt", "Frankfurt", regex = True)
results = results.replace("West Ham United", "WestHam", regex = True)
results = results.replace('Hellas Verona FC','HellasVerona', regex = True)
results = results.replace("Hertha BSC", "Hertha", regex = True)
results = results.replace("M'Gladbach", "Gladbach", regex = True)
results = results.replace("Bayern Munich", "Bayern", regex = True)
results = results.replace("FSV Mainz", "Mainz", regex = True)
results = results.replace("Mainz 05", "Mainz", regex = True)
results = results.replace("Greuther Fürth", "GreutherFurth", regex = True)
results = results.replace("Union Berlin", "UnionBerlin", regex = True)
results = results.replace("RB Leipzig", "RBLeipzig", regex = True)
results = results.replace("Werder Bremen", "WerderBremen", regex = True)
results = results.replace("Schalke 04", "Schalke", regex = True)
results = results.replace("Düsseldorf", "Dusseldorf", regex = True)
results = results.replace("Paderborn 07", "Paderborn", regex = True)
results = results.replace("Hannover 96", "Hannover", regex = True)
results = results.replace("Köln", "Koln", regex = True)
results = results.replace("Hamburger SV", "Hamburg", regex = True)
results = results.replace("Manchester City", "ManCity", regex = True)
results = results.replace("Manchester Utd", "ManUtd", regex = True)
results = results.replace("Leicester City", "Leicester", regex = True)
results = results.replace("Newcastle Utd", "Newcastle", regex = True)
results = results.replace("Crystal Palace", "CrystalPalace", regex = True)
results = results.replace("Swansea City", "Swansea", regex = True)
results = results.replace("Stoke City", "StokeCity", regex = True)
results = results.replace("West Brom", "WestBrom", regex = True)
results = results.replace("West Ham", "WestHam", regex = True)
results = results.replace("Cardiff City", "Cardiff", regex = True)
results = results.replace("Sheffield Utd", "SheffieldUtd", regex = True)
results = results.replace("Norwich City", "NorwichCity", regex = True)
results = results.replace("Leeds United", "LeedsUtd", regex = True)
results = results.replace("Aston Villa", "AstonVilla", regex = True)
results = results.replace('Hellas Verona','HellasVerona', regex = True)
results = results.replace("Paris S-G", "PSG", regex = True)
results = results.replace("Clermont Foot", "Clermont", regex = True)
results = results.replace("Saint-Étienne", "Saint-Etienne", regex = True)
results = results.replace("Nîmes", "Nimes", regex = True)
results = results.replace("Real Madrid", "RealMadrid", regex = True)
results = results.replace("Atlético Madrid", "Atletico", regex = True)
results = results.replace("Athletic Club", "AthleticBilbao", regex = True)
results = results.replace("Real Sociedad", "RealSociedad", regex = True)
results = results.replace("Rayo Vallecano", "RayoVallecano", regex = True)
results = results.replace("Celta Vigo", "CeltaVigo", regex = True)
results = results.replace("Alavés", "Alaves", regex = True)
results = results.replace("Cádiz", "Cadiz", regex = True)
results = results.replace("Leganés", "Leganes", regex = True)
results = results.replace("La Coruña", "LaCoruna", regex = True)
results = results.replace("Las Palmas", "LasPalmas", regex = True)
results = results.replace("Málaga", "Malaga", regex = True)
results = results.replace('AC Milan','Milan', regex=True)
results = results.replace('Celta Vigo','CeltaVigo', regex=True)
results = results.replace('Rayo Vallecano','RayoVallecano', regex=True)
results = results.replace('Alavés','Alaves', regex=True)
results = results.replace('Granada CF','Granada', regex=True)
results = results.replace('Real Sociedad','RealSociedad', regex=True)
results = results.replace('Real Madrid','RealMadrid', regex=True)
results = results.replace('SC Freiburg','Freiburg', regex=True)
results = results.replace('Eintracht Frankfurt','Frankfurt', regex=True)
results = results.replace('Borussia Monchengladbach','Gladbach', regex=True)
results = results.replace('Union Berlin','UnionBerlin', regex=True)
results = results.replace('Greuther Fürth','GreutherFurth', regex=True)
results = results.replace('Borussia Dortmund','Dortmund', regex=True)
results = results.replace('Bayer Leverkusen','Leverkusen', regex=True)
results = results.replace('TSG Hoffenheim','Hoffenheim', regex=True)
results = results.replace('Leicester City','Leicester', regex=True)
results = results.replace('Norwich City','NorwichCity', regex=True)
results = results.replace('Manchester City','ManCity', regex=True)
results = results.replace('Aston Villa','AstonVilla', regex=True)
results = results.replace('Newcastle United','Newcastle', regex=True)
results = results.replace('Paris Saint Germain','PSG', regex=True)
results = results.replace('Hellas Verona FC','HellasVerona', regex=True)
results = results.replace('AS Roma','Roma', regex=True)
results = results.replace('Inter Milan','Inter', regex=True)
results = results.replace('Atalanta BC','Atalanta', regex=True)
results = results.replace('Cádiz CF','Cadiz', regex=True)
results = results.replace('Elche CF','Elche', regex=True)
results = results.replace('Real Betis','Betis', regex=True)
results = results.replace('Atlético Madrid','Atletico', regex=True)
results = results.replace('CA Osasuna','Osasuna', regex=True)
results = results.replace('Athletic Bilbao','AthleticBilbao', regex=True)
results = results.replace('Arminia Bielefeld','Arminia', regex=True)
results = results.replace('RB Leipzig','RBLeipzig', regex=True)
results = results.replace('Hertha Berlin','Hertha', regex=True)
results = results.replace('VfB Stuttgart','Stuttgart', regex=True)
results = results.replace('VfL Wolfsburg','Wolfsburg', regex=True)
results = results.replace('VfL Bochum','Bochum', regex=True)
results = results.replace('FSV Mainz 05','Mainz', regex=True)
results = results.replace('Bayern Munich','Bayern', regex=True)
results = results.replace('FC Koln','Koln', regex=True)
results = results.replace('Manchester United','ManUtd', regex=True)
results = results.replace('Brighton and Hove Albion','Brighton', regex=True)
results = results.replace('Leeds United','LeedsUtd', regex=True)
results = results.replace('Wolverhampton Wanderers','Wolves', regex=True)
results = results.replace('Tottenham Hotspur','Tottenham', regex=True)
results = results.replace('Crystal Palace','CrystalPalace', regex=True)
results = results.replace('Saint Etienne','Saint-Etienne', regex=True)
results = results.replace('Stade de Reims','Reims', regex=True)
results = results.replace('AS Monaco','Monaco', regex=True)
results = results.replace('RC Lens','Lens', regex=True)
results = results.replace("Nott'ham Forest", "Forest", regex=True)
results = results.replace('Nottingham Forest','Forest', regex=True)
results = results.replace('Werder Bremen','WerderBremen', regex=True)
results = results.replace('Almería','Almeria', regex=True)
results = results.replace('AC Ajaccio','Ajaccio', regex=True)

results['ou'] = np.select(condlist=[results['Total'] > 2.5, results['Total'] < 2.5], choicelist=['Over','Under'], default='Push')

results.to_csv('/Users/matthewfalcona/FalconaForecast/data/results_{current_date}.csv'.format(current_date=date.today()), index = False)
"""

results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/results_{current_date}.csv'.format(current_date=date.today()))

##################################################################################
# odds importer

import json

# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = 'b8e276c11882ed0b6ae796cf05a42919'

SPORT = 'soccer_italy_serie_a' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'american' # decimal | american

DATE_FORMAT = 'unix' # iso | unix

sport_list = ['soccer_italy_serie_a','soccer_germany_bundesliga','soccer_spain_la_liga','soccer_france_ligue_one','soccer_epl']

markets_list = ['h2h','spreads','totals']

# italy hda
r_ita_hda = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_italy_serie_a/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'h2h',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_ita_hda.status_code != 200:
    print(f'Failed to get odds: status_code {r_ita_hda.status_code}, response body {r_ita_hda.text}')

else:
    odds_json_ita_hda = r_ita_hda.json()
    print('Number of events:', len(odds_json_ita_hda))
    #print(odds_json_ita_hda)

    # Check the usage quota
    print('Remaining requests', r_ita_hda.headers['x-requests-remaining'])
    print('Used requests', r_ita_hda.headers['x-requests-used'])

odds_ita_hda = pd.json_normalize(odds_json_ita_hda,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

# italy totals
r_ita_tot = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_italy_serie_a/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'totals',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_ita_tot.status_code != 200:
    print(f'Failed to get odds: status_code {r_ita_tot.status_code}, response body {r_ita_tot.text}')

else:
    odds_json_ita_tot = r_ita_tot.json()
    print('Number of events:', len(odds_json_ita_tot))
    #print(odds_json_ita_tot)

    # Check the usage quota
    print('Remaining requests', r_ita_tot.headers['x-requests-remaining'])
    print('Used requests', r_ita_tot.headers['x-requests-used'])

odds_ita_tot = pd.json_normalize(odds_json_ita_tot,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

#######################################################################################################

# germany hda
r_ger_hda = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_germany_bundesliga/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'h2h',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_ger_hda.status_code != 200:
    print(f'Failed to get odds: status_code {r_ger_hda.status_code}, response body {r_ger_hda.text}')

else:
    odds_json_ger_hda = r_ger_hda.json()
    print('Number of events:', len(odds_json_ger_hda))
    #print(odds_json_ger_hda)

    # Check the usage quota
    print('Remaining requests', r_ger_hda.headers['x-requests-remaining'])
    print('Used requests', r_ger_hda.headers['x-requests-used'])

odds_ger_hda = pd.json_normalize(odds_json_ger_hda,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

# germany totals
r_ger_tot = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_germany_bundesliga/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'totals',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_ger_tot.status_code != 200:
    print(f'Failed to get odds: status_code {r_ger_tot.status_code}, response body {r_ger_tot.text}')

else:
    odds_json_ger_tot = r_ger_tot.json()
    print('Number of events:', len(odds_json_ger_tot))
    #print(odds_json_ger_tot)

    # Check the usage quota
    print('Remaining requests', r_ger_tot.headers['x-requests-remaining'])
    print('Used requests', r_ger_tot.headers['x-requests-used'])

odds_ger_tot = pd.json_normalize(odds_json_ger_tot,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')


#######################################################################################################


# spain hda
r_spa_hda = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'h2h',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_spa_hda.status_code != 200:
    print(f'Failed to get odds: status_code {r_spa_hda.status_code}, response body {r_spa_hda.text}')

else:
    odds_json_spa_hda = r_spa_hda.json()
    print('Number of events:', len(odds_json_spa_hda))
    #print(odds_json_spa_hda)

    # Check the usage quota
    print('Remaining requests', r_spa_hda.headers['x-requests-remaining'])
    print('Used requests', r_spa_hda.headers['x-requests-used'])

odds_spa_hda = pd.json_normalize(odds_json_spa_hda,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

# spain totals
r_spa_tot = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'totals',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_spa_tot.status_code != 200:
    print(f'Failed to get odds: status_code {r_spa_tot.status_code}, response body {r_spa_tot.text}')

else:
    odds_json_spa_tot = r_spa_tot.json()
    print('Number of events:', len(odds_json_spa_tot))
    #print(odds_json_spa_tot)

    # Check the usage quota
    print('Remaining requests', r_spa_tot.headers['x-requests-remaining'])
    print('Used requests', r_spa_tot.headers['x-requests-used'])

odds_spa_tot = pd.json_normalize(odds_json_spa_tot,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

#######################################################################################################


# france hda
r_fra_hda = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_france_ligue_one/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'h2h',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_fra_hda.status_code != 200:
    print(f'Failed to get odds: status_code {r_fra_hda.status_code}, response body {r_fra_hda.text}')

else:
    odds_json_fra_hda = r_fra_hda.json()
    print('Number of events:', len(odds_json_fra_hda))
    #print(odds_json_fra_hda)

    # Check the usage quota
    print('Remaining requests', r_fra_hda.headers['x-requests-remaining'])
    print('Used requests', r_fra_hda.headers['x-requests-used'])

odds_fra_hda = pd.json_normalize(odds_json_fra_hda,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

# france totals
r_fra_tot = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_france_ligue_one/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'totals',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_fra_tot.status_code != 200:
    print(f'Failed to get odds: status_code {r_fra_tot.status_code}, response body {r_fra_tot.text}')

else:
    odds_json_fra_tot = r_fra_tot.json()
    print('Number of events:', len(odds_json_fra_tot))
    #print(odds_json_fra_tot)

    # Check the usage quota
    print('Remaining requests', r_fra_tot.headers['x-requests-remaining'])
    print('Used requests', r_fra_tot.headers['x-requests-used'])

odds_fra_tot = pd.json_normalize(odds_json_fra_tot,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

#######################################################################################################


# england hda
r_eng_hda = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_epl/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'h2h',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_eng_hda.status_code != 200:
    print(f'Failed to get odds: status_code {r_eng_hda.status_code}, response body {r_eng_hda.text}')

else:
    odds_json_eng_hda = r_eng_hda.json()
    print('Number of events:', len(odds_json_eng_hda))
    #print(odds_json_eng_hda)

    # Check the usage quota
    print('Remaining requests', r_eng_hda.headers['x-requests-remaining'])
    print('Used requests', r_eng_hda.headers['x-requests-used'])

odds_eng_hda = pd.json_normalize(odds_json_eng_hda,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

# england totals
r_eng_tot = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_epl/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'totals',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_eng_tot.status_code != 200:
    print(f'Failed to get odds: status_code {r_eng_tot.status_code}, response body {r_eng_tot.text}')

else:
    odds_json_eng_tot = r_eng_tot.json()
    print('Number of events:', len(odds_json_eng_tot))
    #print(odds_json_eng_tot)

    # Check the usage quota
    print('Remaining requests', r_eng_tot.headers['x-requests-remaining'])
    print('Used requests', r_eng_tot.headers['x-requests-used'])

odds_eng_tot = pd.json_normalize(odds_json_eng_tot,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

odds_table_hda = odds_ita_hda
odds_table_tot = odds_ita_tot
odds_table_tot = odds_table_tot.append(odds_ger_tot)
odds_table_hda = odds_table_hda.append(odds_ger_hda)
odds_table_tot = odds_table_tot.append(odds_spa_tot)
odds_table_hda = odds_table_hda.append(odds_spa_hda)
odds_table_tot = odds_table_tot.append(odds_fra_tot)
odds_table_hda = odds_table_hda.append(odds_fra_hda)
odds_table_tot = odds_table_tot.append(odds_eng_tot)
odds_table_hda = odds_table_hda.append(odds_eng_hda)

# normalizing team names

odds_table_tot = odds_table_tot.replace("Eint Frankfurt", "Frankfurt", regex = True)
odds_table_tot = odds_table_tot.replace('West Ham United','WestHam', regex=True)
odds_table_tot = odds_table_tot.replace('Hellas Verona FC','HellasVerona', regex = True)
odds_table_tot = odds_table_tot.replace("Hertha BSC", "Hertha", regex = True)
odds_table_tot = odds_table_tot.replace("M'Gladbach", "Gladbach", regex = True)
odds_table_tot = odds_table_tot.replace("Bayern Munich", "Bayern", regex = True)
odds_table_tot = odds_table_tot.replace("FSV Mainz", "Mainz", regex = True)
odds_table_tot = odds_table_tot.replace("Mainz 05", "Mainz", regex = True)
odds_table_tot = odds_table_tot.replace("Greuther Fürth", "GreutherFurth", regex = True)
odds_table_tot = odds_table_tot.replace("Union Berlin", "UnionBerlin", regex = True)
odds_table_tot = odds_table_tot.replace("RB Leipzig", "RBLeipzig", regex = True)
odds_table_tot = odds_table_tot.replace("Werder Bremen", "WerderBremen", regex = True)
odds_table_tot = odds_table_tot.replace("Schalke 04", "Schalke", regex = True)
odds_table_tot = odds_table_tot.replace("Düsseldorf", "Dusseldorf", regex = True)
odds_table_tot = odds_table_tot.replace("Paderborn 07", "Paderborn", regex = True)
odds_table_tot = odds_table_tot.replace("Hannover 96", "Hannover", regex = True)
odds_table_tot = odds_table_tot.replace("Köln", "Koln", regex = True)
odds_table_tot = odds_table_tot.replace("Hamburger SV", "Hamburg", regex = True)
odds_table_tot = odds_table_tot.replace("Manchester City", "ManCity", regex = True)
odds_table_tot = odds_table_tot.replace("Manchester Utd", "ManUtd", regex = True)
odds_table_tot = odds_table_tot.replace("Leicester City", "Leicester", regex = True)
odds_table_tot = odds_table_tot.replace("Newcastle Utd", "Newcastle", regex = True)
odds_table_tot = odds_table_tot.replace("Crystal Palace", "CrystalPalace", regex = True)
odds_table_tot = odds_table_tot.replace("Swansea City", "Swansea", regex = True)
odds_table_tot = odds_table_tot.replace("Stoke City", "StokeCity", regex = True)
odds_table_tot = odds_table_tot.replace("West Brom", "WestBrom", regex = True)
odds_table_tot = odds_table_tot.replace("West Ham", "WestHam", regex = True)
odds_table_tot = odds_table_tot.replace("Cardiff City", "Cardiff", regex = True)
odds_table_tot = odds_table_tot.replace("Sheffield Utd", "SheffieldUtd", regex = True)
odds_table_tot = odds_table_tot.replace("Norwich City", "NorwichCity", regex = True)
odds_table_tot = odds_table_tot.replace("Leeds United", "LeedsUtd", regex = True)
odds_table_tot = odds_table_tot.replace("Aston Villa", "AstonVilla", regex = True)
odds_table_tot = odds_table_tot.replace('Hellas Verona','HellasVerona', regex = True)
odds_table_tot = odds_table_tot.replace("Paris S-G", "PSG", regex = True)
odds_table_tot = odds_table_tot.replace("Clermont Foot", "Clermont", regex = True)
odds_table_tot = odds_table_tot.replace("Saint-Étienne", "Saint-Etienne", regex = True)
odds_table_tot = odds_table_tot.replace("Nîmes", "Nimes", regex = True)
odds_table_tot = odds_table_tot.replace("Real Madrid", "RealMadrid", regex = True)
odds_table_tot = odds_table_tot.replace("Atlético Madrid", "Atletico", regex = True)
odds_table_tot = odds_table_tot.replace("Athletic Club", "AthleticBilbao", regex = True)
odds_table_tot = odds_table_tot.replace("Real Sociedad", "RealSociedad", regex = True)
odds_table_tot = odds_table_tot.replace("Rayo Vallecano", "RayoVallecano", regex = True)
odds_table_tot = odds_table_tot.replace("Celta Vigo", "CeltaVigo", regex = True)
odds_table_tot = odds_table_tot.replace("Alavés", "Alaves", regex = True)
odds_table_tot = odds_table_tot.replace("Cádiz", "Cadiz", regex = True)
odds_table_tot = odds_table_tot.replace("Leganés", "Leganes", regex = True)
odds_table_tot = odds_table_tot.replace("La Coruña", "LaCoruna", regex = True)
odds_table_tot = odds_table_tot.replace("Las Palmas", "LasPalmas", regex = True)
odds_table_tot = odds_table_tot.replace("Málaga", "Malaga", regex = True)
odds_table_tot = odds_table_tot.replace('AC Milan','Milan', regex=True)
odds_table_tot = odds_table_tot.replace('Celta Vigo','CeltaVigo', regex=True)
odds_table_tot = odds_table_tot.replace('Rayo Vallecano','RayoVallecano', regex=True)
odds_table_tot = odds_table_tot.replace('Alavés','Alaves', regex=True)
odds_table_tot = odds_table_tot.replace('Granada CF','Granada', regex=True)
odds_table_tot = odds_table_tot.replace('Real Sociedad','RealSociedad', regex=True)
odds_table_tot = odds_table_tot.replace('Real Madrid','RealMadrid', regex=True)
odds_table_tot = odds_table_tot.replace('SC Freiburg','Freiburg', regex=True)
odds_table_tot = odds_table_tot.replace('Eintracht Frankfurt','Frankfurt', regex=True)
odds_table_tot = odds_table_tot.replace('Borussia Monchengladbach','Gladbach', regex=True)
odds_table_tot = odds_table_tot.replace('Union Berlin','UnionBerlin', regex=True)
odds_table_tot = odds_table_tot.replace('Greuther Fürth','GreutherFurth', regex=True)
odds_table_tot = odds_table_tot.replace('Borussia Dortmund','Dortmund', regex=True)
odds_table_tot = odds_table_tot.replace('Bayer Leverkusen','Leverkusen', regex=True)
odds_table_tot = odds_table_tot.replace('TSG Hoffenheim','Hoffenheim', regex=True)
odds_table_tot = odds_table_tot.replace('Leicester City','Leicester', regex=True)
odds_table_tot = odds_table_tot.replace('Norwich City','NorwichCity', regex=True)
odds_table_tot = odds_table_tot.replace('Manchester City','ManCity', regex=True)
odds_table_tot = odds_table_tot.replace('Aston Villa','AstonVilla', regex=True)
odds_table_tot = odds_table_tot.replace('Newcastle United','Newcastle', regex=True)
odds_table_tot = odds_table_tot.replace('Paris Saint Germain','PSG', regex=True)
odds_table_tot = odds_table_tot.replace('Hellas Verona FC','HellasVerona', regex=True)
odds_table_tot = odds_table_tot.replace('AS Roma','Roma', regex=True)
odds_table_tot = odds_table_tot.replace('Inter Milan','Inter', regex=True)
odds_table_tot = odds_table_tot.replace('Atalanta BC','Atalanta', regex=True)
odds_table_tot = odds_table_tot.replace('Cádiz CF','Cadiz', regex=True)
odds_table_tot = odds_table_tot.replace('Elche CF','Elche', regex=True)
odds_table_tot = odds_table_tot.replace('Real Betis','Betis', regex=True)
odds_table_tot = odds_table_tot.replace('Atlético Madrid','Atletico', regex=True)
odds_table_tot = odds_table_tot.replace('CA Osasuna','Osasuna', regex=True)
odds_table_tot = odds_table_tot.replace('Athletic Bilbao','AthleticBilbao', regex=True)
odds_table_tot = odds_table_tot.replace('Arminia Bielefeld','Arminia', regex=True)
odds_table_tot = odds_table_tot.replace('RB Leipzig','RBLeipzig', regex=True)
odds_table_tot = odds_table_tot.replace('Hertha Berlin','Hertha', regex=True)
odds_table_tot = odds_table_tot.replace('VfB Stuttgart','Stuttgart', regex=True)
odds_table_tot = odds_table_tot.replace('VfL Wolfsburg','Wolfsburg', regex=True)
odds_table_tot = odds_table_tot.replace('VfL Bochum','Bochum', regex=True)
odds_table_tot = odds_table_tot.replace('FSV Mainz 05','Mainz', regex=True)
odds_table_tot = odds_table_tot.replace('Bayern Munich','Bayern', regex=True)
odds_table_tot = odds_table_tot.replace('FC Koln','Koln', regex=True)
odds_table_tot = odds_table_tot.replace('Manchester United','ManUtd', regex=True)
odds_table_tot = odds_table_tot.replace('Brighton and Hove Albion','Brighton', regex=True)
odds_table_tot = odds_table_tot.replace('Leeds United','LeedsUtd', regex=True)
odds_table_tot = odds_table_tot.replace('Wolverhampton Wanderers','Wolves', regex=True)
odds_table_tot = odds_table_tot.replace('Tottenham Hotspur','Tottenham', regex=True)
odds_table_tot = odds_table_tot.replace('Crystal Palace','CrystalPalace', regex=True)
odds_table_tot = odds_table_tot.replace('Saint Etienne','Saint-Etienne', regex=True)
odds_table_tot = odds_table_tot.replace('Stade de Reims','Reims', regex=True)
odds_table_tot = odds_table_tot.replace('AS Monaco','Monaco', regex=True)
odds_table_tot = odds_table_tot.replace('RC Lens','Lens', regex=True)
odds_table_tot = odds_table_tot.replace("Nott'ham Forest", "Forest", regex=True)
odds_table_tot = odds_table_tot.replace('Nottingham Forest','Forest', regex=True)
odds_table_tot = odds_table_tot.replace('Werder Bremen','WerderBremen', regex=True)
odds_table_tot = odds_table_tot.replace('Almería','Almeria', regex=True)
odds_table_tot = odds_table_tot.replace('AC Ajaccio','Ajaccio', regex=True)

# creating unique matchup field
odds_table_tot['Match'] = odds_table_tot['home_team'] + '-' + odds_table_tot['away_team']

# filtering to only O/U 2.5

odds_table_tot = odds_table_tot[odds_table_tot['point'] == 2.5]


# pivoting

odds_tot = pd.pivot_table(data=odds_table_tot, index=['Match','name'], aggfunc={'price':np.mean})
odds_tot = odds_tot.reset_index()
odds_tot['price'] = np.where((odds_tot['price'] < 100) & (odds_tot['price'] >= -100), 100, odds_tot['price'])
odds_tot['price'] = odds_tot['price'].astype(int)


odds_table_hda = odds_table_hda.replace("Eint Frankfurt", "Frankfurt", regex = True)
odds_table_hda = odds_table_hda.replace('Hellas Verona FC','HellasVerona', regex=True)
odds_table_hda = odds_table_hda.replace('Hellas Verona','HellasVerona', regex = True)
odds_table_hda = odds_table_hda.replace("Hertha BSC", "Hertha", regex = True)
odds_table_hda = odds_table_hda.replace("M'Gladbach", "Gladbach", regex = True)
odds_table_hda = odds_table_hda.replace("Bayern Munich", "Bayern", regex = True)
odds_table_hda = odds_table_hda.replace("FSV Mainz", "Mainz", regex = True)
odds_table_hda = odds_table_hda.replace("Mainz 05", "Mainz", regex = True)
odds_table_hda = odds_table_hda.replace("Greuther Fürth", "GreutherFurth", regex = True)
odds_table_hda = odds_table_hda.replace("Union Berlin", "UnionBerlin", regex = True)
odds_table_hda = odds_table_hda.replace("RB Leipzig", "RBLeipzig", regex = True)
odds_table_hda = odds_table_hda.replace("Werder Bremen", "WerderBremen", regex = True)
odds_table_hda = odds_table_hda.replace("Schalke 04", "Schalke", regex = True)
odds_table_hda = odds_table_hda.replace("Düsseldorf", "Dusseldorf", regex = True)
odds_table_hda = odds_table_hda.replace("Paderborn 07", "Paderborn", regex = True)
odds_table_hda = odds_table_hda.replace("Hannover 96", "Hannover", regex = True)
odds_table_hda = odds_table_hda.replace("Köln", "Koln", regex = True)
odds_table_hda = odds_table_hda.replace("Hamburger SV", "Hamburg", regex = True)
odds_table_hda = odds_table_hda.replace("Manchester City", "ManCity", regex = True)
odds_table_hda = odds_table_hda.replace("Man City", "ManCity", regex = True)
odds_table_hda = odds_table_hda.replace("Manchester Utd", "ManUtd", regex = True)
odds_table_hda = odds_table_hda.replace("Manchester United", "ManUtd", regex = True)
odds_table_hda = odds_table_hda.replace("Man United", "ManUtd", regex = True)
odds_table_hda = odds_table_hda.replace("Leicester City", "Leicester", regex = True)
odds_table_hda = odds_table_hda.replace("Newcastle Utd", "Newcastle", regex = True)
odds_table_hda = odds_table_hda.replace("Crystal Palace", "CrystalPalace", regex = True)
odds_table_hda = odds_table_hda.replace("Swansea City", "Swansea", regex = True)
odds_table_hda = odds_table_hda.replace("Stoke City", "StokeCity", regex = True)
odds_table_hda = odds_table_hda.replace("West Brom", "WestBrom", regex = True)
odds_table_hda = odds_table_hda.replace("West Ham United", "WestHam", regex = True)
odds_table_hda = odds_table_hda.replace("West Ham", "WestHam", regex = True)
odds_table_hda = odds_table_hda.replace("Cardiff City", "Cardiff", regex = True)
odds_table_hda = odds_table_hda.replace("Sheffield Utd", "SheffieldUtd", regex = True)
odds_table_hda = odds_table_hda.replace("Norwich City", "NorwichCity", regex = True)
odds_table_hda = odds_table_hda.replace("Leeds United", "LeedsUtd", regex = True)
odds_table_hda = odds_table_hda.replace("Aston Villa", "AstonVilla", regex = True)
odds_table_hda = odds_table_hda.replace("Paris S-G", "PSG", regex = True)
odds_table_hda = odds_table_hda.replace("Clermont Foot", "Clermont", regex = True)
odds_table_hda = odds_table_hda.replace("Saint-Étienne", "Saint-Etienne", regex = True)
odds_table_hda = odds_table_hda.replace("Nîmes", "Nimes", regex = True)
odds_table_hda = odds_table_hda.replace("Real Madrid", "RealMadrid", regex = True)
odds_table_hda = odds_table_hda.replace("Atlético Madrid", "Atletico", regex = True)
odds_table_hda = odds_table_hda.replace("Athletic Club", "AthleticBilbao", regex = True)
odds_table_hda = odds_table_hda.replace("Real Sociedad", "RealSociedad", regex = True)
odds_table_hda = odds_table_hda.replace("Rayo Vallecano", "RayoVallecano", regex = True)
odds_table_hda = odds_table_hda.replace("Celta Vigo", "CeltaVigo", regex = True)
odds_table_hda = odds_table_hda.replace("Alavés", "Alaves", regex = True)
odds_table_hda = odds_table_hda.replace("Cádiz", "Cadiz", regex = True)
odds_table_hda = odds_table_hda.replace("Leganés", "Leganes", regex = True)
odds_table_hda = odds_table_hda.replace("La Coruña", "LaCoruna", regex = True)
odds_table_hda = odds_table_hda.replace("Las Palmas", "LasPalmas", regex = True)
odds_table_hda = odds_table_hda.replace("Málaga", "Malaga", regex = True)
odds_table_hda = odds_table_hda.replace('AC Milan','Milan', regex=True)
odds_table_hda = odds_table_hda.replace('Celta Vigo','CeltaVigo', regex=True)
odds_table_hda = odds_table_hda.replace('Rayo Vallecano','RayoVallecano', regex=True)
odds_table_hda = odds_table_hda.replace('Alavés','Alaves', regex=True)
odds_table_hda = odds_table_hda.replace('Granada CF','Granada', regex=True)
odds_table_hda = odds_table_hda.replace('Real Sociedad','RealSociedad', regex=True)
odds_table_hda = odds_table_hda.replace('Real Madrid','RealMadrid', regex=True)
odds_table_hda = odds_table_hda.replace('SC Freiburg','Freiburg', regex=True)
odds_table_hda = odds_table_hda.replace('Eintracht Frankfurt','Frankfurt', regex=True)
odds_table_hda = odds_table_hda.replace('Borussia Monchengladbach','Gladbach', regex=True)
odds_table_hda = odds_table_hda.replace('Union Berlin','UnionBerlin', regex=True)
odds_table_hda = odds_table_hda.replace('Greuther Fürth','GreutherFurth', regex=True)
odds_table_hda = odds_table_hda.replace('Borussia Dortmund','Dortmund', regex=True)
odds_table_hda = odds_table_hda.replace('Bayer Leverkusen','Leverkusen', regex=True)
odds_table_hda = odds_table_hda.replace('TSG Hoffenheim','Hoffenheim', regex=True)
odds_table_hda = odds_table_hda.replace('Leicester City','Leicester', regex=True)
odds_table_hda = odds_table_hda.replace('Norwich City','NorwichCity', regex=True)
odds_table_hda = odds_table_hda.replace('Manchester City','ManCity', regex=True)
odds_table_hda = odds_table_hda.replace('Aston Villa','AstonVilla', regex=True)
odds_table_hda = odds_table_hda.replace('Newcastle United','Newcastle', regex=True)
odds_table_hda = odds_table_hda.replace('Paris Saint Germain','PSG', regex=True)
odds_table_hda = odds_table_hda.replace('AS Roma','Roma', regex=True)
odds_table_hda = odds_table_hda.replace('Inter Milan','Inter', regex=True)
odds_table_hda = odds_table_hda.replace('Atalanta BC','Atalanta', regex=True)
odds_table_hda = odds_table_hda.replace('Cádiz CF','Cadiz', regex=True)
odds_table_hda = odds_table_hda.replace('Elche CF','Elche', regex=True)
odds_table_hda = odds_table_hda.replace('Real Betis','Betis', regex=True)
odds_table_hda = odds_table_hda.replace('Atlético Madrid','Atletico', regex=True)
odds_table_hda = odds_table_hda.replace('CA Osasuna','Osasuna', regex=True)
odds_table_hda = odds_table_hda.replace('Athletic Bilbao','AthleticBilbao', regex=True)
odds_table_hda = odds_table_hda.replace('Arminia Bielefeld','Arminia', regex=True)
odds_table_hda = odds_table_hda.replace('RB Leipzig','RBLeipzig', regex=True)
odds_table_hda = odds_table_hda.replace('Hertha Berlin','Hertha', regex=True)
odds_table_hda = odds_table_hda.replace('VfB Stuttgart','Stuttgart', regex=True)
odds_table_hda = odds_table_hda.replace('VfL Wolfsburg','Wolfsburg', regex=True)
odds_table_hda = odds_table_hda.replace('VfL Bochum','Bochum', regex=True)
odds_table_hda = odds_table_hda.replace('FSV Mainz 05','Mainz', regex=True)
odds_table_hda = odds_table_hda.replace('Bayern Munich','Bayern', regex=True)
odds_table_hda = odds_table_hda.replace('FC Koln','Koln', regex=True)
odds_table_hda = odds_table_hda.replace('Manchester United','ManUtd', regex=True)
odds_table_hda = odds_table_hda.replace('Brighton and Hove Albion','Brighton', regex=True)
odds_table_hda = odds_table_hda.replace('Leeds United','LeedsUtd', regex=True)
odds_table_hda = odds_table_hda.replace('Wolverhampton Wanderers','Wolves', regex=True)
odds_table_hda = odds_table_hda.replace('Tottenham Hotspur','Tottenham', regex=True)
odds_table_hda = odds_table_hda.replace('Crystal Palace','CrystalPalace', regex=True)
odds_table_hda = odds_table_hda.replace('Saint Etienne','Saint-Etienne', regex=True)
odds_table_hda = odds_table_hda.replace('Stade de Reims','Reims', regex=True)
odds_table_hda = odds_table_hda.replace('AS Monaco','Monaco', regex=True)
odds_table_hda = odds_table_hda.replace('RC Lens','Lens', regex=True)
odds_table_hda = odds_table_hda.replace("Nott'ham Forest", "Forest", regex=True)
odds_table_hda = odds_table_hda.replace('Nottingham Forest','Forest', regex=True)
odds_table_hda = odds_table_hda.replace('Werder Bremen','WerderBremen', regex=True)
odds_table_hda = odds_table_hda.replace('Almería','Almeria', regex=True)
odds_table_hda = odds_table_hda.replace('AC Ajaccio','Ajaccio', regex=True)

# creating unique matchup field
odds_table_hda['Match'] = odds_table_hda['home_team'] + '-' + odds_table_hda['away_team']

# pivoting

odds_table_hda = pd.pivot_table(data=odds_table_hda, index=['Match','name'], aggfunc={'price':np.mean})
odds_table_hda = odds_table_hda.reset_index()
odds_table_hda['price'] = np.where((odds_table_hda['price'] < 100) & (odds_table_hda['price'] >= -100), 100, odds_table_hda['price'])
odds_table_hda['price'] = odds_table_hda['price'].astype(int)

odds_table_hda.to_csv('/Users/matthewfalcona/FalconaForecast/data/odds_hda_{current_date}.csv'.format(current_date=date.today()), index = False)
odds_tot.to_csv('/Users/matthewfalcona/FalconaForecast/data/odds_tot_{current_date}.csv'.format(current_date=date.today()), index = False)

odds_table_hda = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/odds_hda_{current_date}.csv'.format(current_date=date.today()))
odds_tot = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/odds_tot_{current_date}.csv'.format(current_date=date.today()))


odds_hda = odds_table_hda

########################################################################################
# collecting current stats

# uncomment after first games are played

"""

import io
import os
import re
from datetime import datetime
from datetime import date

from selenium import webdriver

from time import sleep
import pandas as pd
from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# webdrivermanager
# VE in falconaforecast dir

gf = []
xg = []
gp = []
npxg = []
npxG_Sh = []
np_G_xG = []
prog = []
sca90 = []
gca90 = []
poss = []
ga = []
psxg = []


def wait_until_element_is_present_by_id(driver, element):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element)))

    except:
        print('could not locate element %s' % (element))


def get_by_type(locator_type):
    
        #def which generate locator type
        #:param locator_type: str set by def which implement on SeleniumDriver class
        #:return: tag type or False
        
    locator_type = locator_type.lower()
    if locator_type == 'id':
        return By.ID
    elif locator_type == 'name':
        return By.NAME
    elif locator_type == 'xpath':
        return By.XPATH
    elif locator_type == 'css':
        return By.CSS_SELECTOR
    elif locator_type == 'class':
        return By.CLASS_NAME
    elif locator_type == 'link':
        return By.LINK_TEXT
    elif locator_type == 'tag':
        return By.TAG_NAME
    else:
        print("Locator type" + locator_type + " not correct/supported")
    return False


def set_firefox_options():
    try:
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        return opts, profile

    except:
        raise Exception("Could not set firefox options for the browser. ")


def get_web_data():
    try:

        opts, profile = set_firefox_options()
        driver = webdriver.Firefox()

        driver.get("https://fbref.com/en/comps/11/Serie-A-Stats")

        data_frames = create_data_frame_object(driver)

        write_table_data_to_csv(data_frames)

    except:
        raise Exception("Could not get Web Data")


def get_table_data(driver, table_id, body_tag, row_tag):
    try:

        team_data = []

        wait_until_element_is_present_by_id(driver, table_id)

        table = driver.find_element(get_by_type('id'), table_id)

        sleep(randint(3, 5))

        body = table.find_element(get_by_type('tag'), body_tag)

        sleep(randint(2, 4))

        rows = body.find_elements(get_by_type('tag'), row_tag)

        for row in rows:
            row_class = row.get_attribute("class")

            if "Hellas Verona" in row.text:
                print(row.text)
                res_str = re.sub("Hellas Verona", "HellasVerona", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "vs" in row.text:
                print(row.text)
                res_str = re.sub("vs ", "vs", row.text)
                print(res_str)
                team_data.append(res_str)

            elif row.text != "" and body_tag == 'tbody':
                print(row.text)
                team_data.append(row.text)

            elif body_tag == 'thead' and row_class != "over_header":
                res_str = re.sub("# Pl", "#Pl", row.text)
                print(res_str)
                team_data.append(res_str)

        length = len(team_data)
        if length > 1 and body_tag == 'thead':
            team_data.pop(0)
            return team_data

        return team_data

    except:
        raise Exception("Could not get table data from table %s " %(table_id))


def create_data_frame(table1, table2):
    try:
        all_data = pd.np.concatenate((table1, table2))
        ita_curr_stats = pd.read_csv(io.StringIO('\n'.join(all_data)), delim_whitespace=True, error_bad_lines=False, engine="python")
        print(ita_curr_stats)

        return ita_curr_stats
    except:
        raise Exception("Could not create dataframe with table %s. " %(table1))


def create_data_frame_object(driver):
    try:
        tables = ["all_stats_squads_keeper_adv", "all_stats_squads_shooting", "all_stats_squads_passing", "all_stats_squads_gca", "all_stats_squads_possession"]
        
        data_frames = []
        
        for i in range(len(tables)):
            sleep(randint(2,4))
            is_true = False
 
            headers = get_table_data(driver, "{}".format(tables[i]), "thead", "tr")

            data = get_table_data(driver, "{}".format(tables[i]), "tbody", "tr")

            ita_curr_stats = create_data_frame(headers, data)

            data_frames.append(ita_curr_stats)

        return data_frames

    except:
        raise Exception("Could not create dataframe Object. ")


def write_table_data_to_csv(data_frames):
    try:
        current_directory = get_project_root()
        BASE_DIR = os.path.dirname(current_directory)
        print(BASE_DIR)

        col_df = {
            'ga': data_frames[0]['GA'],
            'psxg': data_frames[0]['PSxG'],
            'squad': data_frames[1]['Squad'],
            'gp': data_frames[1]['90s'],
            'gf': data_frames[1]['Gls'],
            'xg': data_frames[1]['xG'],
            'npxg': data_frames[1]['npxG'],
            'npxG/Sh': data_frames[1]['npxG/Sh'],
            'np:G-xG': data_frames[1]['np:G-xG'],
            'prog': data_frames[2]['Prog'],
            'sca90': data_frames[3]['SCA90'],
            'gca90': data_frames[3]['GCA90'],
            'poss': data_frames[4]['Poss']
        }

        ita_curr_stats = pd.DataFrame(col_df)
        #df = pd.to_flat_index(col_df).union()
        ita_curr_stats.to_csv('{base_dir}/data/seriea_{current_date}.csv'.format(base_dir=BASE_DIR, current_date=date.today()), index = False)
    except:
        raise Exception("Could not write column df to CSV. ")


def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))

get_web_data()

###########
# spain data coll

gf = []
xg = []
gp = []
npxg = []
npxG_Sh = []
np_G_xG = []
prog = []
sca90 = []
gca90 = []
poss = []
ga = []
psxg = []


def wait_until_element_is_present_by_id(driver, element):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element)))

    except:
        print('could not locate element %s' % (element))


def get_by_type(locator_type):
    
        #def which generate locator type
        #:param locator_type: str set by def which implement on SeleniumDriver class
        #:return: tag type or False
        
    locator_type = locator_type.lower()
    if locator_type == 'id':
        return By.ID
    elif locator_type == 'name':
        return By.NAME
    elif locator_type == 'xpath':
        return By.XPATH
    elif locator_type == 'css':
        return By.CSS_SELECTOR
    elif locator_type == 'class':
        return By.CLASS_NAME
    elif locator_type == 'link':
        return By.LINK_TEXT
    elif locator_type == 'tag':
        return By.TAG_NAME
    else:
        print("Locator type" + locator_type + " not correct/supported")
    return False


def set_firefox_options():
    try:
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        return opts, profile

    except:
        raise Exception("Could not set firefox options for the browser. ")


def get_web_data():
    try:

        opts, profile = set_firefox_options()
        driver = webdriver.Firefox()

        driver.get("https://fbref.com/en/comps/12/La-Liga-Stats")

        data_frames = create_data_frame_object(driver)

        write_table_data_to_csv(data_frames)

    except:
        raise Exception("Could not get Web Data")


def get_table_data(driver, table_id, body_tag, row_tag):
    try:

        team_data = []

        wait_until_element_is_present_by_id(driver, table_id)

        table = driver.find_element(get_by_type('id'), table_id)

        sleep(randint(3, 5))

        body = table.find_element(get_by_type('tag'), body_tag)

        sleep(randint(2, 4))

        rows = body.find_elements(get_by_type('tag'), row_tag)

        for row in rows:
            row_class = row.get_attribute("class")

            if "Real Madrid" in row.text:
                print(row.text)
                res_str = re.sub("Real Madrid", "RealMadrid", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Atlético Madrid" in row.text:
                print(row.text)
                res_str = re.sub("Atlético Madrid", "Atletico", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Athletic Club" in row.text:
                print(row.text)
                res_str = re.sub("Athletic Club", "AthleticBilbao", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Real Sociedad" in row.text:
                print(row.text)
                res_str = re.sub("Real Sociedad", "RealSociedad", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Rayo Vallecano" in row.text:
                print(row.text)
                res_str = re.sub("Rayo Vallecano", "RayoVallecano", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Celta Vigo" in row.text:
                print(row.text)
                res_str = re.sub("Celta Vigo", "CeltaVigo", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Alavés" in row.text:
                print(row.text)
                res_str = re.sub("Alavés", "Alaves", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Cádiz" in row.text:
                print(row.text)
                res_str = re.sub("Cádiz", "Cadiz", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Leganés" in row.text:
                print(row.text)
                res_str = re.sub("Leganés", "Leganes", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "La Coruña" in row.text:
                print(row.text)
                res_str = re.sub("La Coruña", "LaCoruna", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Las Palmas" in row.text:
                print(row.text)
                res_str = re.sub("Las Palmas", "LasPalmas", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Málaga" in row.text:
                print(row.text)
                res_str = re.sub("Málaga", "Malaga", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "vs" in row.text:
                print(row.text)
                res_str = re.sub("vs ", "vs", row.text)
                print(res_str)
                team_data.append(res_str)

            elif row.text != "" and body_tag == 'tbody':
                print(row.text)
                team_data.append(row.text)

            elif body_tag == 'thead' and row_class != "over_header":
                res_str = re.sub("# Pl", "#Pl", row.text)
                print(res_str)
                team_data.append(res_str)

        length = len(team_data)
        if length > 1 and body_tag == 'thead':
            team_data.pop(0)
            return team_data

        return team_data

    except:
        raise Exception("Could not get table data from table %s " %(table_id))


def create_data_frame(table1, table2):
    try:
        all_data = pd.np.concatenate((table1, table2))
        spa_curr_stats = pd.read_csv(io.StringIO('\n'.join(all_data)), delim_whitespace=True, error_bad_lines=False, engine="python")
        print(spa_curr_stats)

        return spa_curr_stats
    except:
        raise Exception("Could not create dataframe with table %s. " %(table1))


def create_data_frame_object(driver):
    try:
        tables = ["all_stats_squads_keeper_adv", "all_stats_squads_shooting", "all_stats_squads_passing", "all_stats_squads_gca", "all_stats_squads_possession"]        

        data_frames = []
        
        for i in range(len(tables)):
            sleep(randint(2,4))
            is_true = False
         
            headers = get_table_data(driver, "{}".format(tables[i]), "thead", "tr")

            data = get_table_data(driver, "{}".format(tables[i]), "tbody", "tr")

            spa_curr_stats = create_data_frame(headers, data)

            data_frames.append(spa_curr_stats)

        return data_frames

    except:
        raise Exception("Could not create dataframe Object. ")


def write_table_data_to_csv(data_frames):
    try:
        current_directory = get_project_root()
        BASE_DIR = os.path.dirname(current_directory)
        print(BASE_DIR)

        col_df = {
            'ga': data_frames[0]['GA'],
            'psxg': data_frames[0]['PSxG'],
            'squad': data_frames[1]['Squad'],
            'gp': data_frames[1]['90s'],
            'gf': data_frames[1]['Gls'],
            'xg': data_frames[1]['xG'],
            'npxg': data_frames[1]['npxG'],
            'npxG/Sh': data_frames[1]['npxG/Sh'],
            'np:G-xG': data_frames[1]['np:G-xG'],
            'prog': data_frames[2]['Prog'],
            'sca90': data_frames[3]['SCA90'],
            'gca90': data_frames[3]['GCA90'],
            'poss': data_frames[4]['Poss']
        }

        spa_curr_stats = pd.DataFrame(col_df)
        #df = pd.to_flat_index(col_df).union()
        spa_curr_stats.to_csv('{base_dir}/data/laliga_{current_date}.csv'.format(base_dir=BASE_DIR, current_date=date.today()), index = False)
    except:
        raise Exception("Could not write column df to CSV. ")


def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))

get_web_data()

##########################################################
# germany data coll

gf = []
xg = []
gp = []
npxg = []
npxG_Sh = []
np_G_xG = []
prog = []
sca90 = []
gca90 = []
poss = []
ga = []
psxg = []


def wait_until_element_is_present_by_id(driver, element):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element)))

    except:
        print('could not locate element %s' % (element))


def get_by_type(locator_type):
    
    #    def which generate locator type
     #   :param locator_type: str set by def which implement on SeleniumDriver class
      #  :return: tag type or False
        
    locator_type = locator_type.lower()
    if locator_type == 'id':
        return By.ID
    elif locator_type == 'name':
        return By.NAME
    elif locator_type == 'xpath':
        return By.XPATH
    elif locator_type == 'css':
        return By.CSS_SELECTOR
    elif locator_type == 'class':
        return By.CLASS_NAME
    elif locator_type == 'link':
        return By.LINK_TEXT
    elif locator_type == 'tag':
        return By.TAG_NAME
    else:
        print("Locator type" + locator_type + " not correct/supported")
    return False


def set_firefox_options():
    try:
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        return opts, profile

    except:
        raise Exception("Could not set firefox options for the browser. ")


def get_web_data():
    try:

        opts, profile = set_firefox_options()
        driver = webdriver.Firefox()

        driver.get("https://fbref.com/en/comps/20/Bundesliga-Stats")

        data_frames = create_data_frame_object(driver)

        write_table_data_to_csv(data_frames)

    except:
        raise Exception("Could not get Web Data")


def get_table_data(driver, table_id, body_tag, row_tag):
    try:

        team_data = []

        wait_until_element_is_present_by_id(driver, table_id)

        table = driver.find_element(get_by_type('id'), table_id)

        sleep(randint(3, 5))

        body = table.find_element(get_by_type('tag'), body_tag)

        sleep(randint(2, 4))

        rows = body.find_elements(get_by_type('tag'), row_tag)

        for row in rows:
            row_class = row.get_attribute("class")

            # bundesliga
            
            if "Eint Frankfurt" in row.text:
                print(row.text)
                res_str = re.sub("Eint Frankfurt", "Frankfurt", row.text)
                print(res_str)
                team_data.append(res_str)
            
            elif "Hertha BSC" in row.text:
                print(row.text)
                res_str = re.sub("Hertha BSC", "Hertha", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "M'Gladbach" in row.text:
                print(row.text)
                res_str = re.sub("M'Gladbach", "Gladbach", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Bayern Munich" in row.text:
                print(row.text)
                res_str = re.sub("Bayern Munich", "Bayern", row.text)
                print(res_str)
                team_data.append(res_str)
            
            elif "Mainz 05" in row.text:
                print(row.text)
                res_str = re.sub("Mainz 05", "Mainz", row.text)
                print(res_str)
                team_data.append(res_str)
            
            elif "Greuther Fürth" in row.text:
                print(row.text)
                res_str = re.sub("Greuther Fürth", "GreutherFurth", row.text)
                print(res_str)
                team_data.append(res_str)
            
            elif "Union Berlin" in row.text:
                print(row.text)
                res_str = re.sub("Union Berlin", "UnionBerlin", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "RB Leipzig" in row.text:
                print(row.text)
                res_str = re.sub("RB Leipzig", "RBLeipzig", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Werder Bremen" in row.text:
                print(row.text)
                res_str = re.sub("Werder Bremen", "WerderBremen", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Schalke 04" in row.text:
                print(row.text)
                res_str = re.sub("Schalke 04", "Schalke", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Düsseldorf" in row.text:
                print(row.text)
                res_str = re.sub("Düsseldorf", "Dusseldorf", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Paderborn 07" in row.text:
                print(row.text)
                res_str = re.sub("Paderborn 07", "Paderborn", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Hannover 96" in row.text:
                print(row.text)
                res_str = re.sub("Hannover 96", "Hannover", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Köln" in row.text:
                print(row.text)
                res_str = re.sub("Köln", "Koln", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Hamburger SV" in row.text:
                print(row.text)
                res_str = re.sub("Hamburger SV", "Hamburg", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "vs" in row.text:
                print(row.text)
                res_str = re.sub("vs ", "vs", row.text)
                print(res_str)
                team_data.append(res_str)

            elif row.text != "" and body_tag == 'tbody':
                print(row.text)
                team_data.append(row.text)

            elif body_tag == 'thead' and row_class != "over_header":
                res_str = re.sub("# Pl", "#Pl", row.text)
                print(res_str)
                team_data.append(res_str)

        length = len(team_data)
        if length > 1 and body_tag == 'thead':
            team_data.pop(0)
            return team_data

        return team_data

    except:
        raise Exception("Could not get table data from table %s " %(table_id))


def create_data_frame(table1, table2):
    try:
        all_data = pd.np.concatenate((table1, table2))
        ger_curr_stats = pd.read_csv(io.StringIO('\n'.join(all_data)), delim_whitespace=True, error_bad_lines=False, engine="python")
        print(ger_curr_stats)

        return ger_curr_stats
    except:
        raise Exception("Could not create dataframe with table %s. " %(table1))


def create_data_frame_object(driver):
    try:
        tables = ["all_stats_squads_keeper_adv", "all_stats_squads_shooting", "all_stats_squads_passing", "all_stats_squads_gca", "all_stats_squads_possession"]

        #button_ids = ["stats_shooting_squads_for_per_match_toggle", "stats_passing_squads_for_per_match_toggle", "stats_gca_squads_for_per_match_toggle", "stats_possession_squads_for_per_match_toggle","stats_shooting_squads_against_per_match_toggle", "stats_passing_squads_against_per_match_toggle", "stats_gca_squads_against_per_match_toggle", "stats_possession_squads_against_per_match_toggle"]
        
     #   switcher_ids = ['switcher_stats_squads_shooting', 'switcher_stats_squads_passing', 'switcher_stats_squads_gca', 'switcher_stats_squad_possession']

        data_frames = []
        
        for i in range(len(tables)):
            sleep(randint(2,4))
            is_true = False
        
            headers = get_table_data(driver, "{}".format(tables[i]), "thead", "tr")

            data = get_table_data(driver, "{}".format(tables[i]), "tbody", "tr")

            ger_curr_stats = create_data_frame(headers, data)

            data_frames.append(ger_curr_stats)

        return data_frames

    except:
        raise Exception("Could not create dataframe Object. ")


def write_table_data_to_csv(data_frames):
    try:
        current_directory = get_project_root()
        BASE_DIR = os.path.dirname(current_directory)
        print(BASE_DIR)

        col_df = {
            'ga': data_frames[0]['GA'],
            'psxg': data_frames[0]['PSxG'],
            'squad': data_frames[1]['Squad'],
            'gp': data_frames[1]['90s'],
            'gf': data_frames[1]['Gls'],
            'xg': data_frames[1]['xG'],
            'npxg': data_frames[1]['npxG'],
            'npxG/Sh': data_frames[1]['npxG/Sh'],
            'np:G-xG': data_frames[1]['np:G-xG'],
            'prog': data_frames[2]['Prog'],
            'sca90': data_frames[3]['SCA90'],
            'gca90': data_frames[3]['GCA90'],
            'poss': data_frames[4]['Poss']
        }

        ger_curr_stats = pd.DataFrame(col_df)
        ger_curr_stats.to_csv('{base_dir}/data/bun_{current_date}.csv'.format(base_dir=BASE_DIR, current_date=date.today()), index = False)
    except:
        raise Exception("Could not write column df to CSV. ")

def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))

get_web_data()

####################################################
# france data coll

gf = []
xg = []
gp = []
npxg = []
npxG_Sh = []
np_G_xG = []
prog = []
sca90 = []
gca90 = []
poss = []
ga = []
psxg = []


def wait_until_element_is_present_by_id(driver, element):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element)))

    except:
        print('could not locate element %s' % (element))


def get_by_type(locator_type):
    
    #    def which generate locator type
     #   :param locator_type: str set by def which implement on SeleniumDriver class
      #  :return: tag type or False
        
    locator_type = locator_type.lower()
    if locator_type == 'id':
        return By.ID
    elif locator_type == 'name':
        return By.NAME
    elif locator_type == 'xpath':
        return By.XPATH
    elif locator_type == 'css':
        return By.CSS_SELECTOR
    elif locator_type == 'class':
        return By.CLASS_NAME
    elif locator_type == 'link':
        return By.LINK_TEXT
    elif locator_type == 'tag':
        return By.TAG_NAME
    else:
        print("Locator type" + locator_type + " not correct/supported")
    return False


def set_firefox_options():
    try:
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        return opts, profile

    except:
        raise Exception("Could not set firefox options for the browser. ")


def get_web_data():
    try:

        opts, profile = set_firefox_options()
        driver = webdriver.Firefox()

        driver.get("https://fbref.com/en/comps/13/Ligue-1-Stats")

        data_frames = create_data_frame_object(driver)

        write_table_data_to_csv(data_frames)

    except:
        raise Exception("Could not get Web Data")


def get_table_data(driver, table_id, body_tag, row_tag):
    try:

        team_data = []

        wait_until_element_is_present_by_id(driver, table_id)

        table = driver.find_element(get_by_type('id'), table_id)

        sleep(randint(3, 5))

        body = table.find_element(get_by_type('tag'), body_tag)

        sleep(randint(2, 4))

        rows = body.find_elements(get_by_type('tag'), row_tag)

        for row in rows:
            row_class = row.get_attribute("class")

            if "Paris S-G" in row.text:
                print(row.text)
                res_str = re.sub("Paris S-G", "PSG", row.text)
                print(res_str)
                team_data.append(res_str)
        
            elif "Clermont Foot" in row.text:
                print(row.text)
                res_str = re.sub("Clermont Foot", "Clermont", row.text)
                print(res_str)
                team_data.append(res_str)
            
            elif "Saint-Étienne" in row.text:
                print(row.text)
                res_str = re.sub("Saint-Étienne", "Saint-Etienne", row.text)
                print(res_str)
                team_data.append(res_str)
            
            elif "Nîmes" in row.text:
                print(row.text)
                res_str = re.sub("Nîmes", "Nimes", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "vs" in row.text:
                print(row.text)
                res_str = re.sub("vs ", "vs", row.text)
                print(res_str)
                team_data.append(res_str)

            elif row.text != "" and body_tag == 'tbody':
                print(row.text)
                team_data.append(row.text)

            elif body_tag == 'thead' and row_class != "over_header":
                res_str = re.sub("# Pl", "#Pl", row.text)
                print(res_str)
                team_data.append(res_str)

        length = len(team_data)
        if length > 1 and body_tag == 'thead':
            team_data.pop(0)
            return team_data

        return team_data

    except:
        raise Exception("Could not get table data from table %s " %(table_id))


def create_data_frame(table1, table2):
    try:
        all_data = pd.np.concatenate((table1, table2))
        fra_curr_stats = pd.read_csv(io.StringIO('\n'.join(all_data)), delim_whitespace=True, error_bad_lines=False, engine="python")
        print(fra_curr_stats)

        return fra_curr_stats
    except:
        raise Exception("Could not create dataframe with table %s. " %(table1))


def create_data_frame_object(driver):
    try:
        tables = ["all_stats_squads_keeper_adv", "all_stats_squads_shooting", "all_stats_squads_passing", "all_stats_squads_gca", "all_stats_squads_possession"]        

        data_frames = []
        
        for i in range(len(tables)):
            sleep(randint(2,4))
            is_true = False
      
            headers = get_table_data(driver, "{}".format(tables[i]), "thead", "tr")

            data = get_table_data(driver, "{}".format(tables[i]), "tbody", "tr")

            fra_curr_stats = create_data_frame(headers, data)

            data_frames.append(fra_curr_stats)

        return data_frames

    except:
        raise Exception("Could not create dataframe Object. ")


def write_table_data_to_csv(data_frames):
    try:
        current_directory = get_project_root()
        BASE_DIR = os.path.dirname(current_directory)
        print(BASE_DIR)

        col_df = {
            'ga': data_frames[0]['GA'],
            'psxg': data_frames[0]['PSxG'],
            'squad': data_frames[1]['Squad'],
            'gp': data_frames[1]['90s'],
            'gf': data_frames[1]['Gls'],
            'xg': data_frames[1]['xG'],
            'npxg': data_frames[1]['npxG'],
            'npxG/Sh': data_frames[1]['npxG/Sh'],
            'np:G-xG': data_frames[1]['np:G-xG'],
            'prog': data_frames[2]['Prog'],
            'sca90': data_frames[3]['SCA90'],
            'gca90': data_frames[3]['GCA90'],
            'poss': data_frames[4]['Poss']
        }

        fra_curr_stats = pd.DataFrame(col_df)
        #df = pd.to_flat_index(col_df).union()
        fra_curr_stats.to_csv('{base_dir}/data/ligue1_{current_date}.csv'.format(base_dir=BASE_DIR, current_date=date.today()), index = False)
    except:
        raise Exception("Could not write column df to CSV. ")

def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))

get_web_data()

#########################################
# epl data coll

gf = []
xg = []
gp = []
npxg = []
npxG_Sh = []
np_G_xG = []
prog = []
sca90 = []
gca90 = []
poss = []
ga = []
psxg = []


def wait_until_element_is_present_by_id(driver, element):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element)))

    except:
        print('could not locate element %s' % (element))


def get_by_type(locator_type):
    
       # def which generate locator type
        #:param locator_type: str set by def which implement on SeleniumDriver class
        #:return: tag type or False
        
    locator_type = locator_type.lower()
    if locator_type == 'id':
        return By.ID
    elif locator_type == 'name':
        return By.NAME
    elif locator_type == 'xpath':
        return By.XPATH
    elif locator_type == 'css':
        return By.CSS_SELECTOR
    elif locator_type == 'class':
        return By.CLASS_NAME
    elif locator_type == 'link':
        return By.LINK_TEXT
    elif locator_type == 'tag':
        return By.TAG_NAME
    else:
        print("Locator type" + locator_type + " not correct/supported")
    return False


def set_firefox_options():
    try:
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        return opts, profile

    except:
        raise Exception("Could not set firefox options for the browser. ")


def get_web_data():
    try:

        opts, profile = set_firefox_options()
        driver = webdriver.Firefox()

        driver.get("https://fbref.com/en/comps/9/Premier-League-Stats")

        data_frames = create_data_frame_object(driver)

        write_table_data_to_csv(data_frames)

    except:
        raise Exception("Could not get Web Data")


def get_table_data(driver, table_id, body_tag, row_tag):
    try:

        team_data = []

        wait_until_element_is_present_by_id(driver, table_id)

        table = driver.find_element(get_by_type('id'), table_id)

        sleep(randint(3, 5))

        body = table.find_element(get_by_type('tag'), body_tag)

        sleep(randint(2, 4))

        rows = body.find_elements(get_by_type('tag'), row_tag)

        for row in rows:
            row_class = row.get_attribute("class")

            if "Manchester City" in row.text:
                print(row.text)
                res_str = re.sub("Manchester City", "ManCity", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Manchester Utd" in row.text:
                print(row.text)
                res_str = re.sub("Manchester Utd", "ManUtd", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Leicester City" in row.text:
                print(row.text)
                res_str = re.sub("Leicester City", "Leicester", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Newcastle Utd" in row.text:
                print(row.text)
                res_str = re.sub("Newcastle Utd", "Newcastle", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Crystal Palace" in row.text:
                print(row.text)
                res_str = re.sub("Crystal Palace", "CrystalPalace", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Swansea City" in row.text:
                print(row.text)
                res_str = re.sub("Swansea City", "Swansea", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Stoke City" in row.text:
                print(row.text)
                res_str = re.sub("Stoke City", "StokeCity", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "West Brom" in row.text:
                print(row.text)
                res_str = re.sub("West Brom", "WestBrom", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "West Ham" in row.text:
                print(row.text)
                res_str = re.sub("West Ham", "WestHam", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Cardiff City" in row.text:
                print(row.text)
                res_str = re.sub("Cardiff City", "Cardiff", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Sheffield Utd" in row.text:
                print(row.text)
                res_str = re.sub("Sheffield Utd", "SheffieldUtd", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Norwich City" in row.text:
                print(row.text)
                res_str = re.sub("Norwich City", "NorwichCity", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Leeds United" in row.text:
                print(row.text)
                res_str = re.sub("Leeds United", "LeedsUtd", row.text)
                print(res_str)
                team_data.append(res_str)

            elif "Aston Villa" in row.text:
                print(row.text)
                res_str = re.sub("Aston Villa", "AstonVilla", row.text)
                print(res_str)
                team_data.append(res_str)

            elif row.text != "" and body_tag == 'tbody':
                print(row.text)
                team_data.append(row.text)

            elif body_tag == 'thead' and row_class != "over_header":
                res_str = re.sub("# Pl", "#Pl", row.text)
                print(res_str)
                team_data.append(res_str)

        length = len(team_data)
        if length > 1 and body_tag == 'thead':
            team_data.pop(0)
            return team_data

        return team_data

    except:
        raise Exception("Could not get table data from table %s " %(table_id))


def create_data_frame(table1, table2):
    try:
        all_data = pd.np.concatenate((table1, table2))
        eng_curr_stats = pd.read_csv(io.StringIO('\n'.join(all_data)), delim_whitespace=True, error_bad_lines=False, engine="python")
        print(eng_curr_stats)

        return eng_curr_stats
    except:
        raise Exception("Could not create dataframe with table %s. " %(table1))


def create_data_frame_object(driver):
    try:
        tables = ["all_stats_squads_keeper_adv", "all_stats_squads_shooting", "all_stats_squads_passing", "all_stats_squads_gca", "all_stats_squads_possession"]

        data_frames = []
        
        for i in range(len(tables)):
            sleep(randint(2,4))
            is_true = False

            headers = get_table_data(driver, "{}".format(tables[i]), "thead", "tr")

            data = get_table_data(driver, "{}".format(tables[i]), "tbody", "tr")

            eng_curr_stats = create_data_frame(headers, data)

            data_frames.append(eng_curr_stats)

        return data_frames

    except:
        raise Exception("Could not create dataframe Object. ")


def write_table_data_to_csv(data_frames):
    try:
        current_directory = get_project_root()
        BASE_DIR = os.path.dirname(current_directory)
        print(BASE_DIR)

        col_df = {
            'ga': data_frames[0]['GA'],
            'psxg': data_frames[0]['PSxG'],
            'squad': data_frames[1]['Squad'],
            'gp': data_frames[1]['90s'],
            'gf': data_frames[1]['Gls'],
            'xg': data_frames[1]['xG'],
            'npxg': data_frames[1]['npxG'],
            'npxG/Sh': data_frames[1]['npxG/Sh'],
            'np:G-xG': data_frames[1]['np:G-xG'],
            'prog': data_frames[2]['Prog'],
            'sca90': data_frames[3]['SCA90'],
            'gca90': data_frames[3]['GCA90'],
            'poss': data_frames[4]['Poss']
        }

        eng_curr_stats = pd.DataFrame(col_df)
        #df = pd.to_flat_index(col_df).union()
        eng_curr_stats.to_csv('/Users/matthewfalcona/FalconaForecast/data/epl_{current_date}.csv'.format(base_dir=BASE_DIR, current_date=date.today()), index = False)
    except:
        raise Exception("Could not write column df to CSV. ")

def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))

get_web_data()


seriea_raw = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/seriea_{current_date}.csv'.format(current_date=date.today()))
ligue1_raw = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/ligue1_{current_date}.csv'.format(current_date=date.today()))
laliga_raw = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/laliga_{current_date}.csv'.format(current_date=date.today()))
bun_raw = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/bun_{current_date}.csv'.format(current_date=date.today()))
epl_raw = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/epl_{current_date}.csv'.format(current_date=date.today()))


##########################################################################################
# merging top 5 combined stats


top5_raw = seriea_raw.append(ligue1_raw)
top5_raw = top5_raw.append(laliga_raw)
top5_raw = top5_raw.append(bun_raw)
top5_raw = top5_raw.append(epl_raw)
top5_raw = top5_raw.reset_index()

top5_raw['gf'] = top5_raw['gf'] / top5_raw['gp']
top5_raw['xg'] = top5_raw['xg'] / top5_raw['gp']
top5_raw['npxg'] = top5_raw['npxg'] / top5_raw['gp']
top5_raw['np:G-xG'] = top5_raw['np:G-xG'] / top5_raw['gp']
top5_raw['prog'] = top5_raw['prog'] / top5_raw['gp']
top5_raw['psxg'] = top5_raw['psxg'] / top5_raw['gp']
top5_raw['ga'] = top5_raw['ga'] / top5_raw['gp']
top5_raw['gd'] = top5_raw['gf'] - top5_raw['ga']
top5_stats = top5_raw

top5_stats.to_csv('/Users/matthewfalcona/FalconaForecast/data/top5_stats_{current_date}.csv'.format(current_date=date.today()), index = False)
"""


top5_stats = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/top5_stats_{current_date}.csv'.format(current_date=date.today()))

top5_stats_home = top5_stats
top5_stats_home = top5_stats_home.rename(columns = {'squad':'Home'})
top5_stats_home = top5_stats_home[['Home', 'npxg','npxG/Sh','np:G-xG','prog','sca90','gca90','poss','psxg','ga','gf','xg','gd']]
top5_stats_home

top5_stats_away = top5_stats
top5_stats_away = top5_stats_away.rename(columns = {'squad':'Away'})
top5_stats_away = top5_stats_away[['Away', 'npxg','npxG/Sh','np:G-xG','prog','sca90','gca90','poss','psxg','ga','gf','xg','gd']]
top5_stats_away

forecast_sched = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_sched_raw_{current_date}.csv'.format(current_date=date.today()))

forecast_sched = pd.merge(forecast_sched, top5_stats_home, on = 'Home', how = "left")
forecast_sched = pd.merge(forecast_sched, top5_stats_away, on = 'Away', how = "left")

curr_date = date.today()
curr_date = pd.to_datetime(curr_date)
forecast_sched['Date'] = pd.to_datetime(forecast_sched['Date'])
forecast_sched = forecast_sched[forecast_sched['Date'] >= curr_date]
end_date = curr_date+pd.Timedelta(10, unit='D')
forecast_sched = forecast_sched[forecast_sched['Date'] < end_date]
forecast_sched.reset_index(drop=True,inplace=True)

print('forecast_sched:')
print(forecast_sched.head(25))

forecast_sched = forecast_sched[['Home','Away','League','Season','Date','Match', 
                                    'gf_x','ga_x','gd_x','xg_x','npxg_x','npxG/Sh_x','np:G-xG_x',
                                    'prog_x', 'sca90_x', 'gca90_x', 'poss_x','psxg_x',
                                    'gf_y','ga_y','gd_y','xg_y','npxg_y','npxG/Sh_y','np:G-xG_y',
                                    'prog_y', 'sca90_y', 'gca90_y', 'poss_y', 'psxg_y']]


forecast_sched.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_sched_{current_date}.csv'.format(current_date=date.today()), index = False)

# creating train and test sets for results model

# replicating hist table for results
# uncomment after first matchdays

results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/results_{current_date}.csv'.format(current_date=date.today()))

results_stats = pd.merge(results, top5_stats_home, on = 'Home', how = 'left')
results_stats = pd.merge(results_stats, top5_stats_away, on = 'Away', how = 'left')

results_stats.columns

# making results stats line up with top5_hist df

results_train = results_stats.drop(['Home','Away','League','Season','Date','Hscore','Ascore',
                                    'Total', 'ou','HxG','AxG', 'xResult', 'xTotal','Act_Diff',
                                    'xG_Diff','Act_vs_Exp_Result'], axis=1)

#results_train.columns
results_train = results_train[['Result', 'gf_x','ga_x','gd_x',
                                'xg_x','npxg_x','npxG/Sh_x', 'np:G-xG_x',
                                'prog_x','sca90_x','gca90_x','poss_x','psxg_x',   
                                'gf_y','ga_y','gd_y',
                                'xg_y','npxg_y','npxG/Sh_y','np:G-xG_y',
                                'prog_y','sca90_y','gca90_y', 'poss_y', 'psxg_y']]

print(results_train.columns)

top5_hist = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/top5_hist.csv')

top5_result_tt = top5_hist.drop(['Total','ou','Wk', 'Day', 'Date', 'Time',
                                'Home', 'xG', 'Score', 'xG.1', 'Away', 'Attendance',
                                'Venue', 'Referee', 'Match Report', 'Notes',
                                'Unnamed: 0_x', 'Unnamed: 0_y'], axis = 1)

#top5_result_tt.columns
top5_result_tt = top5_result_tt[['Result', 'gf_x','ga_x','gd_x',
                                'xg_x','npxg_x','npxG/Sh_x', 'np:G-xG_x',
                                'prog_x','sca90_x','gca90_x','poss_x','psxg_x',   
                                'gf_y','ga_y','gd_y',
                                'xg_y','npxg_y','npxG/Sh_y','np:G-xG_y',
                                'prog_y','sca90_y','gca90_y', 'poss_y', 'psxg_y']]

top5_result_tt = top5_result_tt.append(results_train)

top5_result_tt = top5_result_tt.dropna()
top5_result_tt.reset_index(drop=True, inplace=True)

print('top5_result_tt:')
print(top5_result_tt.shape)
print(top5_result_tt.head(25))

# feeding into hda model

from datetime import datetime
from datetime import date

from numpy.random import seed
seed(1)
import tensorflow as tf
tf.random.set_seed(2)


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras import backend as K
K.image_data_format()

from keras.utils import np_utils

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from keras.wrappers.scikit_learn import KerasClassifier, KerasRegressor
import eli5
from eli5.sklearn import PermutationImportance

import time
import io
import os
import re
import pandas as pd
import numpy as np


y = top5_result_tt.Result
x = top5_result_tt.drop(['Result','gd_x','gd_y',
                        'gf_y', 'xg_y','gf_x','xg_x', 'np:G-xG_y', 'np:G-xG_x',
                        'npxG/Sh_x','npxG/Sh_y','psxg_y','psxg_x'], axis = 1)

#x.columns = 12

x = x[['npxg_x','ga_x','sca90_x','gca90_x','prog_x','poss_x',
        'ga_y','npxg_y', 'prog_y', 'sca90_y', 'gca90_y', 'poss_y']]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

x_train.shape
x_test.shape
y_train.shape
y_test.shape


# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y_train)
y_train = encoder.transform(y_train)
# convert integers to dummy variables (i.e. one hot encoded)
y_train = np_utils.to_categorical(y_train)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y_test)
y_test = encoder.transform(y_test)
# convert integers to dummy variables (i.e. one hot encoded)
y_test = np_utils.to_categorical(y_test)

y_train.shape

# defining model function

# hyperopt

def base_model():
    model = Sequential() # for training and inference features
    model.add(Dense(50, input_dim = 12, kernel_initializer='normal', activation='tanh'))
    model.add(Dropout(.12))
    model.add(Dense(3, kernel_initializer='normal', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
    return(model)


# model fitting

start = time.time()  # TRACK TIME

model = base_model()

model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs = 50, batch_size = 100, verbose = 1)

scores = model.evaluate(x_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

# # MODEL - RESULTS


end = time.time()
final_time = end-start
print(final_time)

# predictions

forecast_result_pred = forecast_sched.drop(columns = ['Home','Away','League','Season','Date','Match',
                                                    'np:G-xG_y', 'np:G-xG_x','npxG/Sh_x','npxG/Sh_y','psxg_y','psxg_x'])

forecast_result_pred.columns

forecast_result_pred = forecast_result_pred[['npxg_x','ga_x','sca90_x','gca90_x','prog_x','poss_x',
                                            'ga_y','npxg_y', 'prog_y', 'sca90_y', 'gca90_y', 'poss_y']]

forecast_results = model.predict(forecast_result_pred)

forecast_results = pd.DataFrame(forecast_results)

forecast_results.columns = ['Away_pred','Draw_pred','Home_pred']
forecast_results = forecast_results[['Home_pred','Draw_pred','Away_pred']]

print('forecast_results:')
print(forecast_results.shape)
print(forecast_results.head(50))

forecast_results.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_hda_{current_date}.csv'.format(current_date=date.today()), index = False)

forecast = forecast_sched.merge(forecast_results, left_index=True, right_index=True)
#forecast = forecast_sched.join(forecast_results)
print('HDA Forecast')
print(forecast.shape)
print(forecast.head(50))

########################################################################################

# creating train and test sets for totals model

results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/results_{current_date}.csv'.format(current_date=date.today()))
results_stats = pd.merge(results, top5_stats_home, on = 'Home', how = 'left')
results_stats = pd.merge(results_stats, top5_stats_away, on = 'Away', how = 'left')


# making results stats line up with top5_hist df

results_stats_4 = results_stats.drop(['Home','Away','League','Season','Date','Hscore','Ascore','Result','ou','HxG','AxG', 'xResult', 'xTotal','Act_Diff','xG_Diff','Act_vs_Exp_Result'], axis=1)

results_stats_4.columns

results_stats_4 = results_stats_4[['Total', 'gf_x','ga_x','gd_x',
                                'xg_x','npxg_x','npxG/Sh_x', 'np:G-xG_x',
                                'prog_x','sca90_x','gca90_x','poss_x','psxg_x',   
                                'gf_y','ga_y','gd_y',
                                'xg_y','npxg_y','npxG/Sh_y','np:G-xG_y',
                                'prog_y','sca90_y','gca90_y', 'poss_y', 'psxg_y']]

results_stats_4.columns

results_stats_4 = results_stats_4[['Total', 'npxg_x', 'npxG/Sh_x', 'np:G-xG_x', 'prog_x',
                                    'sca90_x', 'gca90_x', 'poss_x', 'psxg_x', 'ga_x', 'gf_x', 'xg_x',
                                    'gd_x', 'npxg_y', 'npxG/Sh_y', 'np:G-xG_y', 'prog_y', 'sca90_y',
                                    'gca90_y', 'poss_y', 'psxg_y', 'ga_y', 'gf_y', 'xg_y', 'gd_y']]

top5_hist = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/top5_hist.csv')

top5_total_tt = top5_hist.drop(['Result','ou','Wk', 'Day', 'Date', 'Time',
                                'Home', 'xG', 'Score', 'xG.1', 'Away', 'Attendance',
                                'Venue', 'Referee', 'Match Report', 'Notes',
                                'Unnamed: 0_x', 'Unnamed: 0_y'], axis = 1)

top5_total_tt.columns

top5_total_tt = top5_total_tt[['Total', 'gf_x','ga_x','gd_x',
                                'xg_x','npxg_x','npxG/Sh_x', 'np:G-xG_x',
                                'prog_x','sca90_x','gca90_x','poss_x','psxg_x',   
                                'gf_y','ga_y','gd_y',
                                'xg_y','npxg_y','npxG/Sh_y','np:G-xG_y',
                                'prog_y','sca90_y','gca90_y', 'poss_y', 'psxg_y']]

top5_total_tt = top5_total_tt.append(results_stats_4)

top5_total_tt.head(150)

top5_total_tt = top5_total_tt.dropna()
top5_total_tt.reset_index(drop=True,inplace=True)

z = top5_total_tt.Total
w = top5_total_tt.drop(['Total','gd_x','gd_y','npxg_y','npxg_x',
                        'xg_y','xg_x','np:G-xG_y', 'np:G-xG_x',
                        'npxG/Sh_x','npxG/Sh_y','psxg_x','psxg_y',
                        'poss_y','poss_x','prog_y','prog_x'], axis = 1)

w.columns

w = w[['gf_x','ga_x','sca90_x','gca90_x',
        'gf_y','ga_y','sca90_y','gca90_y']]

w_train,w_test,z_train,z_test=train_test_split(w,z,test_size=0.2)

print(w_train.shape)
print(w_test.shape)
print(z_train.shape)
print(z_test.shape)


# defining totals model function

def base_model_tot():
    model = Sequential() # for training and inference features
    model.add(Dense(50, input_dim = 8, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(.1))
    model.add(Dense(1, kernel_initializer='normal', activation='relu'))
    model.compile(loss='mean_squared_logarithmic_error', optimizer='adam', metrics = ['accuracy'])
    return(model)


# model fitting

start = time.time()  # TRACK TIME

model = base_model_tot()

model.fit(w_train, z_train, validation_data = (w_test, z_test), epochs = 50, batch_size = 100, verbose = 1)

scores_tot = model.evaluate(w_test, z_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores_tot[1]*100))

# # MODEL - totals


end = time.time()
final_time = end-start
print(final_time)


# predictions

forecast_total_pred = forecast_sched.drop(columns = ['Home','Away','League','Season','Date','Match',
                                                        'gd_x','gd_y',
                                                        'prog_y','xg_y','prog_x','xg_x', 'np:G-xG_y', 'np:G-xG_x',
                                                        'npxG/Sh_x','npxG/Sh_y','psxg_y','psxg_x','poss_x','poss_y','npxg_x','npxg_y'])

#should match w columns
forecast_total_pred = forecast_total_pred[['gf_x','ga_x','sca90_x','gca90_x',
                                            'gf_y','ga_y','sca90_y','gca90_y']]


print('forecast_total_pred: ')
print(forecast_total_pred.head(50))


forecast_total = model.predict(forecast_total_pred)

forecast_total = pd.DataFrame(forecast_total)

forecast_total.columns = ['Total_pred']

print('forecast_total shape:')
print(forecast_total.shape)

forecast_total.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_total_{current_date}.csv'.format(current_date=date.today()), index = False)

forecast = forecast.merge(forecast_total, left_index=True, right_index=True)
#forecast = forecast.join(forecast_total)

print('Totals Forecast')
print(forecast.shape)
print(forecast.head(50))

########################################################################################

# creating train and test sets for o/u odds model
results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/results_{current_date}.csv'.format(current_date=date.today()))

results_stats = pd.merge(results, top5_stats_home, on = 'Home', how = 'left')
results_stats = pd.merge(results_stats, top5_stats_away, on = 'Away', how = 'left')

results_stats_2 = results_stats.drop(['Home','Away','League','Season','Date',
                                        'Hscore','Ascore','Result','Total',
                                        'HxG','AxG', 'xResult', 'xTotal','Act_Diff',
                                        'xG_Diff','Act_vs_Exp_Result'], axis=1)

results_stats_2.columns
results_stats_2 = results_stats_2[['ou','gf_x','ga_x','gd_x',
                                    'xg_x','npxg_x','npxG/Sh_x', 'np:G-xG_x',
                                    'prog_x','sca90_x','gca90_x','poss_x','psxg_x',   
                                    'gf_y','ga_y','gd_y',
                                    'xg_y','npxg_y','npxG/Sh_y','np:G-xG_y',
                                    'prog_y','sca90_y','gca90_y', 'poss_y', 'psxg_y']]

top5_hist = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/top5_hist.csv')

top5_ou_tt = top5_hist.drop(['Result','Total','Wk', 'Day', 'Date', 'Time',
                                'Home', 'xG', 'Score', 'xG.1', 'Away', 'Attendance',
                                'Venue', 'Referee', 'Match Report', 'Notes',
                                'Unnamed: 0_x', 'Unnamed: 0_y'], axis = 1)

top5_ou_tt.columns

top5_ou_tt = top5_ou_tt[['ou','gf_x','ga_x','gd_x',
                            'xg_x','npxg_x','npxG/Sh_x', 'np:G-xG_x',
                            'prog_x','sca90_x','gca90_x','poss_x','psxg_x',   
                            'gf_y','ga_y','gd_y',
                            'xg_y','npxg_y','npxG/Sh_y','np:G-xG_y',
                            'prog_y','sca90_y','gca90_y', 'poss_y', 'psxg_y']]

top5_ou_tt = top5_ou_tt.append(results_stats_2)

top5_ou_tt = top5_ou_tt.dropna()
top5_ou_tt.reset_index(drop=True,inplace=True)


b = top5_ou_tt.ou
a = top5_ou_tt.drop(['ou','gd_x','gd_y','npxg_y','npxg_x',
                        'xg_y','xg_x','np:G-xG_y', 'np:G-xG_x',
                        'npxG/Sh_x','npxG/Sh_y','psxg_x','psxg_y',
                        'poss_y','poss_x','prog_y','prog_x'], axis = 1)

a.columns

a = a[['gf_x','ga_x','sca90_x','gca90_x',
        'gf_y','ga_y','sca90_y','gca90_y']]


a_train,a_test,b_train,b_test=train_test_split(a,b,test_size=0.2)

print(a_train.shape)
print(a_test.shape)
print(b_train.shape)
print(b_test.shape)


# encode class values as integers
encoder = LabelEncoder()
encoder.fit(b_train)
b_train = encoder.transform(b_train)
# convert integers to dummy variables (i.e. one hot encoded)
b_train = np_utils.to_categorical(b_train)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(b_test)
b_test = encoder.transform(b_test)
# convert integers to dummy variables (i.e. one hot encoded)
b_test = np_utils.to_categorical(b_test)

print(b_train.shape)

# defining model function

def base_model():
    model = Sequential() # for training and inference features
    model.add(Dense(50, input_dim = 8, kernel_initializer='normal', activation='tanh'))
    model.add(Dropout(.1))
    model.add(Dense(2, kernel_initializer='normal', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
    return(model)


# model fitting

start = time.time()  # TRACK TIME

model = base_model()

model.fit(a_train, b_train, validation_data = (a_test, b_test), epochs = 50, batch_size = 100, verbose = 1)

scores = model.evaluate(a_test, b_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

# # MODEL - RESULTS


end = time.time()
final_time = end-start
print(final_time)

# predictions

forecast_ou_pred = forecast_sched.drop(columns = ['Home','Away','League','Season','Date','Match',
                                                        'gd_x','gd_y',
                                                        'prog_y', 'xg_y','prog_x','xg_x', 'np:G-xG_y', 'np:G-xG_x',
                                                        'npxG/Sh_x','npxG/Sh_y','psxg_y','psxg_x','poss_x','poss_y','npxg_x','npxg_y'])

#matches a
forecast_ou_pred = forecast_ou_pred[['gf_x','ga_x','sca90_x','gca90_x',
                                        'gf_y','ga_y','sca90_y','gca90_y']]
print('forecast_ou_pred: ')
print(forecast_ou_pred.head(50))

forecast_ou = model.predict(forecast_ou_pred)

forecast_ou = pd.DataFrame(forecast_ou)

forecast_ou.columns = ['Over_pred','Under_pred']

print('forecast_ou shape:')
print(forecast_ou.shape)

forecast_ou.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_ou_{current_date}.csv'.format(current_date=date.today()), index = False)


forecast = forecast.merge(forecast_ou, left_index=True, right_index=True)
#forecast = forecast.join(forecast_ou)
print('OU Forecast')
print(forecast.shape)
print(forecast.head(50))


###############################################################################################
# formatting forecast df

#forecast = forecast.drop(['npxg_x','npxG/Sh_x','np:G-xG_x','Prog_x','SCA90_x','GCA90_x','Poss_x','psxg_x','npxg_y','npxG/Sh_y','np:G-xG_y','Prog_y','SCA90_y','GCA90_y','Poss_y','psxg_y'],axis=1)

#forecast.columns = ['Home','Away','League','Season','Date','Match','Away_pred','Draw_pred','Home_pred','Total_pred','Over_pred','Under_pred']

forecast1 = forecast[['Home','Away','League','Season','Date','Match','Home_pred','Draw_pred','Away_pred','Total_pred','Over_pred','Under_pred']]

forecast1.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_{current_date}.csv'.format(current_date=date.today()), index = False)

###############################################################################################
# putting it all together with live odds

forecast1['home_link'] = forecast1['Match'] + '-' + forecast1['Home']
forecast1['draw_link'] = forecast1['Match'] + '-Draw'
forecast1['away_link'] = forecast1['Match'] + '-' + forecast1['Away']
forecast1['over_link'] = forecast1['Match'] + '-Over'
forecast1['under_link'] = forecast1['Match'] + '-Under'

print('forecast1_w_link:')
print(forecast1.head(50))

odds_hda['home_link'] = odds_hda['Match'] + '-' + odds_hda['name']
odds_hda['draw_link'] = odds_hda['Match'] + '-' + odds_hda['name']
odds_hda['away_link'] = odds_hda['Match'] + '-' + odds_hda['name']
odds_hda = odds_hda[['Match','name','home_link','draw_link','away_link','price']]

print('odds hda table w link:')
print(odds_hda.head(50))

odds_tot['over_link'] = odds_tot['Match'] + '-' + odds_tot['name']
odds_tot['under_link'] = odds_tot['Match'] + '-' + odds_tot['name']

print('odds tot table w link:')
print(odds_tot.head(50))

forecast_w_odds = pd.merge(forecast1, odds_hda[['home_link','price']], on = 'home_link', how = 'left')
forecast_w_odds = pd.merge(forecast_w_odds, odds_hda[['draw_link','price']], on = 'draw_link', how = 'left')
forecast_w_odds = pd.merge(forecast_w_odds, odds_hda[['away_link','price']], on = 'away_link', how = 'left')
forecast_w_odds = pd.merge(forecast_w_odds, odds_tot[['over_link','price']], on = 'over_link', how = 'left')
forecast_w_odds = pd.merge(forecast_w_odds, odds_tot[['under_link','price']], on = 'under_link', how = 'left')

forecast_w_odds = forecast_w_odds.drop(['Match','home_link','draw_link','away_link','over_link','under_link'], axis=1)

forecast_w_odds.columns = ['Home','Away','League','Season','Date','Home_pred','Draw_pred','Away_pred','Total_pred','Over_pred','Under_pred','Home_odds','Draw_odds','Away_odds','Over_odds','Under_odds']

print('Forecast w odds')
print(forecast_w_odds.shape)
print(forecast_w_odds.head(50))

forecast_w_odds.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_w_odds_{current_date}.csv'.format(current_date=date.today()), index = False)

forecast_dropna = forecast_w_odds.dropna()

print('Forecast dropped na')
print(forecast_dropna.shape)
print(forecast_dropna.head(50))


###################################################
# power ratings

pwr_stats = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/top5_stats_{current_date}.csv'.format(current_date=date.today()))
pwr_results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_sched_{current_date}.csv'.format(current_date=date.today()))
leagues = pwr_results[['Away','League']]
leagues.columns = ['squad','League']
leagues = leagues.drop_duplicates()
pwr_stats = pd.merge(pwr_stats, leagues, on='squad', how='left')
pwr_stats = pwr_stats[['squad','League','ga','poss','gca90','sca90','prog','npxg']]


# old feature importance

"""
GCA90 = .3136
psxg = .2332
SCA90 = .1415
Prog = .1232
npGxG = .1212
Poss = .0428
npxg = .0244
npxGSh = 0.00
"""
# new feature importance


gca90 = .0878
ga = .0558
poss = .009
sca90 = .0085
prog = .0051
npxg = .0015


stats_power = pwr_stats
stats_power['npxg_pwr'] = stats_power['npxg'] * npxg
stats_power['ga_pwr'] = stats_power['ga'] * ga * -1
stats_power['gca90_pwr'] = stats_power['gca90'] * gca90
stats_power['sca90_pwr'] = stats_power['sca90'] * sca90
stats_power['prog_pwr'] = stats_power['prog'] * prog
stats_power['raw_rating'] = (stats_power['npxg_pwr']+stats_power['ga_pwr']+stats_power['gca90_pwr']+stats_power['sca90_pwr']+stats_power['prog_pwr'])


# uefa league coefficient

epl_pwr = 1.286318398*.9
laliga_pwr = 1.135606518*.9
seriea_pwr = 0.885118409*.9
bun_pwr = 0.971105755*.9
ligue1_pwr = 0.72185092*.9

conditions = [
    (stats_power['League'] == 'Premier League'),
    (stats_power['League'] == 'La Liga'),
    (stats_power['League'] == 'Serie A'),
    (stats_power['League'] == 'Bundesliga'),
    (stats_power['League'] == 'Ligue 1')
    ]

values = [stats_power['raw_rating'] * epl_pwr, stats_power['raw_rating'] * laliga_pwr, stats_power['raw_rating'] * seriea_pwr, stats_power['raw_rating'] * bun_pwr, stats_power['raw_rating'] * ligue1_pwr]

stats_power['power_rating'] = np.select(conditions, values)

stats_power = stats_power.sort_values(by=['power_rating'], ascending=False)
stats_power.reset_index(drop=True,inplace=True)

print('power ratings:')
print(stats_power.head(50))
stats_power.to_csv('/Users/matthewfalcona/FalconaForecast/data/power_rating_stats_{current_date}.csv'.format(current_date=date.today()), index = False)

power_rating = stats_power[['squad','League','power_rating']]

power_rating.to_csv('/Users/matthewfalcona/FalconaForecast/data/power_rating_{current_date}.csv'.format(current_date=date.today()), index = False)