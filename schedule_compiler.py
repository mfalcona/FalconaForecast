# schedule compiler

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
#ita_url = "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures"
ita_url = "https://fbref.com/en/comps/11/11611/schedule/2022-2023-Serie-A-Scores-and-Fixtures"
ita_page = requests.get(ita_url)
ita_soup = BeautifulSoup(ita_page.content, 'html.parser')
ita_stats = ['date','squad_a','xg_a','score','xg_b','squad_b']
ita_stats_list = [[td.getText() for td in ita_soup.find_all('td', {'data-stat': stat})] for stat in ita_stats]
seriea_sched = pd.DataFrame(ita_stats_list).T

# building schedule df
seriea_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
seriea_sched['Date'] = pd.to_datetime(seriea_sched['Date'])
seriea_sched[['League','Season']] = ['Serie A','2022-23']

# dropping xG and Score from schedule df
seriea_sched = seriea_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]


# dropping xg and score from schedule df
seriea_sched = seriea_sched.drop(['HxG','Score','AxG'], axis = 1)


#seriea_results.to_csv('seriea_results.csv', index=False)


###################################################################################################
# spain

#spa_url = "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures"
spa_url = "https://fbref.com/en/comps/12/11573/schedule/2022-2023-La-Liga-Scores-and-Fixtures"
spa_page = requests.get(spa_url)
spa_soup = BeautifulSoup(spa_page.content, 'html.parser')
spa_stats = ['date','squad_a','xg_a','score','xg_b','squad_b']
spa_stats_list = [[td.getText() for td in spa_soup.find_all('td', {'data-stat': stat})] for stat in spa_stats]
laliga_sched = pd.DataFrame(spa_stats_list).T

# building schedule df
laliga_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
laliga_sched['Date'] = pd.to_datetime(laliga_sched['Date'])
laliga_sched[['League','Season']] = ['La Liga','2022-23']

# dropping xG and Score from schedule df
laliga_sched = laliga_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]


# dropping xg and score from schedule df
laliga_sched = laliga_sched.drop(['HxG','Score','AxG'], axis = 1)


#########################################################################################
# france

#fra_url = "https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures"
fra_url = "https://fbref.com/en/comps/13/11585/schedule/2022-2023-Ligue-1-Scores-and-Fixtures"
fra_page = requests.get(fra_url)
fra_soup = BeautifulSoup(fra_page.content, 'html.parser')
fra_stats = ['date','squad_a','xg_a','score','xg_b','squad_b']
fra_stats_list = [[td.getText() for td in fra_soup.find_all('td', {'data-stat': stat})] for stat in fra_stats]
ligue1_sched = pd.DataFrame(fra_stats_list).T

# building schedule df
ligue1_sched.columns = ['Date','Home','HxG','Score','AxG','Away']
ligue1_sched['Date'] = pd.to_datetime(ligue1_sched['Date'])
ligue1_sched[['League','Season']] = ['Ligue 1','2022-23']

# dropping xG and Score from schedule df
ligue1_sched = ligue1_sched[['Home','Away','League','Season','Date','HxG','Score','AxG']]

# dropping xg and score from schedule df
ligue1_sched = ligue1_sched.drop(['HxG','Score','AxG'], axis = 1)



#########################################################################################
# germany

#ger_url = "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures"
ger_url = "https://fbref.com/en/comps/20/11593/schedule/2022-2023-Bundesliga-Scores-and-Fixtures"
ger_page = requests.get(ger_url)
ger_soup = BeautifulSoup(ger_page.content, 'html.parser')
ger_stats = ['date','squad_a','xg_a','score','xg_b','squad_b']
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



######################################################################################
# england

#eng_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
eng_url = "https://fbref.com/en/comps/9/11566/schedule/2022-2023-Premier-League-Scores-and-Fixtures"
eng_page = requests.get(eng_url)
eng_soup = BeautifulSoup(eng_page.content, 'html.parser')
eng_stats = ['date','squad_a','xg_a','score','xg_b','squad_b']
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


forecast_sched = seriea_sched
forecast_sched = forecast_sched.append(ligue1_sched)
forecast_sched = forecast_sched.append(epl_sched)
forecast_sched = forecast_sched.append(bund_sched)
forecast_sched = forecast_sched.append(laliga_sched)
forecast_sched = forecast_sched.dropna()
forecast_sched.reset_index(drop=True,inplace=True)
forecast_sched.to_csv('/Users/matthewfalcona/FalconaForecast/data/forecast_sched.csv'.format(current_date=date.today()), index = False)