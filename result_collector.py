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

"""

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

#bund_results.to_csv('/Users/matthewfalcona/FalconaForecast/data/buli_results_2022_08_25.csv')



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

#epl_results.to_csv('/Users/matthewfalcona/FalconaForecast/data/epl_results_2022_08_25.csv')

"""

bund_sched = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/buli_sched_{current_date}.csv'.format(current_date=date.today()))
epl_sched = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/epl_sched_{current_date}.csv'.format(current_date=date.today()))


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

forecast_sched.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_sched_raw_{current_date}.csv'.format(current_date=date.today()), index = False)

# uncomment after first matchdays


bund_results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/buli_results_{current_date}.csv'.format(current_date=date.today()))

epl_results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/epl_results_{current_date}.csv'.format(current_date=date.today()))


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