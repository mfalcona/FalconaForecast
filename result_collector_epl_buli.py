import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
from datetime import date

curr_date = date.today()
curr_date = pd.to_datetime(curr_date)


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


# defining results df
bund_results = bund_sched[bund_sched['Date'] < curr_date]

# dropping xg and score from schedule df
bund_sched = bund_sched.drop(['HxG','Score','AxG'], axis = 1)




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

bund_sched.to_csv('/Users/matthewfalcona/FalconaForecast/data/buli_sched_{current_date}.csv'.format(current_date=date.today()), index = False)

bund_results.to_csv('/Users/matthewfalcona/FalconaForecast/data/buli_results_{current_date}.csv'.format(current_date=date.today()), index = False)


#bund_results = pd.read_csv('/Users/matthewfalcona/FalconaForecast/data/buli_results_2022_08_25.csv')

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

# defining results df
epl_results = epl_sched[epl_sched['Date'] < curr_date]

# dropping xg and score from schedule df
epl_sched = epl_sched.drop(['HxG','Score','AxG'], axis = 1)


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

epl_sched.to_csv('/Users/matthewfalcona/FalconaForecast/data/epl_sched_{current_date}.csv'.format(current_date=date.today()), index = False)

epl_results.to_csv('/Users/matthewfalcona/FalconaForecast/data/epl_results_{current_date}.csv'.format(current_date=date.today()), index = False)

