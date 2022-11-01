import requests
import json
import pandas as pd
import numpy as np


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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

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

odds_ita_hda['match'] = odds_ita_hda['home_team'] + '-' + odds_ita_hda['away_team']

pivot_ita_hda = pd.pivot_table(data=odds_ita_hda, index=['match','name'], aggfunc={'price':np.mean})
pivot_ita_hda = pivot_ita_hda.reset_index()
pivot_ita_hda['price'] = np.where((pivot_ita_hda['price'] < 100) & (pivot_ita_hda['price'] >= -100), 100, pivot_ita_hda['price'])
pivot_ita_hda['price'] = pivot_ita_hda['price'].astype(int)

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

odds_ita_tot['match'] = odds_ita_tot['home_team'] + '-' + odds_ita_tot['away_team']

pivot_ita_tot = pd.pivot_table(data=odds_ita_tot, index=['match','name'], aggfunc={'price':np.mean})
pivot_ita_tot = pivot_ita_tot.reset_index()
pivot_ita_tot['price'] = np.where((pivot_ita_tot['price'] < 100) & (pivot_ita_tot['price'] >= -100), 100, pivot_ita_tot['price'])
pivot_ita_tot['price'] = pivot_ita_tot['price'].astype(int)

"""
# italy spread
r_ita_spr = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_italy_serie_a/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'spreads',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_ita_spr.status_code != 200:
    print(f'Failed to get odds: status_code {r_ita_spr.status_code}, response body {r_ita_spr.text}')

else:
    odds_json_ita_spr = r_ita_spr.json()
    print('Number of events:', len(odds_json_ita_spr))
    #print(odds_json_ita_spr)

    # Check the usage quota
    print('Remaining requests', r_ita_spr.headers['x-requests-remaining'])
    print('Used requests', r_ita_spr.headers['x-requests-used'])

odds_ita_spr = pd.json_normalize(odds_json_ita_spr,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

odds_ita_spr['match'] = odds_ita_spr['home_team'] + '-' + odds_ita_spr['away_team']

pivot_ita_spr = pd.pivot_table(data=odds_ita_spr, index=['match','name'], aggfunc={'price':np.mean})
pivot_ita_spr = pivot_ita_spr.reset_index()
pivot_ita_spr['price'] = np.where((pivot_ita_spr['price'] < 100) & (pivot_ita_spr['price'] >= -100), 100, pivot_ita_spr['price'])
pivot_ita_spr['price'] = pivot_ita_spr['price'].astype(int)
"""

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

odds_ger_hda['match'] = odds_ger_hda['home_team'] + '-' + odds_ger_hda['away_team']

pivot_ger_hda = pd.pivot_table(data=odds_ger_hda, index=['match','name'], aggfunc={'price':np.mean})
pivot_ger_hda = pivot_ger_hda.reset_index()
pivot_ger_hda['price'] = np.where((pivot_ger_hda['price'] < 100) & (pivot_ger_hda['price'] >= -100), 100, pivot_ger_hda['price'])
pivot_ger_hda['price'] = pivot_ger_hda['price'].astype(int)

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

odds_ger_tot['match'] = odds_ger_tot['home_team'] + '-' + odds_ger_tot['away_team']
odds_ger_tot = odds_ger_tot[odds_ger_tot['point'] == 2.5]

pivot_ger_tot = pd.pivot_table(data=odds_ger_tot, index=['match','name'], aggfunc={'price':np.mean})
pivot_ger_tot = pivot_ger_tot.reset_index()
pivot_ger_tot['price'] = np.where((pivot_ger_tot['price'] < 100) & (pivot_ger_tot['price'] >= -100), 100, pivot_ger_tot['price'])
pivot_ger_tot['price'] = pivot_ger_tot['price'].astype(int)

"""
# germany spread
r_ger_spr = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_germany_bundesliga/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'spreads',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_ger_spr.status_code != 200:
    print(f'Failed to get odds: status_code {r_ger_spr.status_code}, response body {r_ger_spr.text}')

else:
    odds_json_ger_spr = r_ger_spr.json()
    print('Number of events:', len(odds_json_ger_spr))
    #print(odds_json_ger_spr)

    # Check the usage quota
    print('Remaining requests', r_ger_spr.headers['x-requests-remaining'])
    print('Used requests', r_ger_spr.headers['x-requests-used'])

odds_ger_spr = pd.json_normalize(odds_json_ger_spr,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

odds_ger_spr['match'] = odds_ger_spr['home_team'] + '-' + odds_ger_spr['away_team']

pivot_ger_spr = pd.pivot_table(data=odds_ger_spr, index=['match','name'], aggfunc={'price':np.mean})
pivot_ger_spr = pivot_ger_spr.reset_index()
pivot_ger_spr['price'] = np.where((pivot_ger_spr['price'] < 100) & (pivot_ger_spr['price'] >= -100), 100, pivot_ger_spr['price'])
pivot_ger_spr['price'] = pivot_ger_spr['price'].astype(int)
"""

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

odds_spa_hda['match'] = odds_spa_hda['home_team'] + '-' + odds_spa_hda['away_team']

pivot_spa_hda = pd.pivot_table(data=odds_spa_hda, index=['match','name'], aggfunc={'price':np.mean})
pivot_spa_hda = pivot_spa_hda.reset_index()
pivot_spa_hda['price'] = np.where((pivot_spa_hda['price'] < 100) & (pivot_spa_hda['price'] >= -100), 100, pivot_spa_hda['price'])
pivot_spa_hda['price'] = pivot_spa_hda['price'].astype(int)

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

odds_spa_tot['match'] = odds_spa_tot['home_team'] + '-' + odds_spa_tot['away_team']

pivot_spa_tot = pd.pivot_table(data=odds_spa_tot, index=['match','name'], aggfunc={'price':np.mean})
pivot_spa_tot = pivot_spa_tot.reset_index()
pivot_spa_tot['price'] = np.where((pivot_spa_tot['price'] < 100) & (pivot_spa_tot['price'] >= -100), 100, pivot_spa_tot['price'])
pivot_spa_tot['price'] = pivot_spa_tot['price'].astype(int)

"""
# spain spread
r_spa_spr = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'spreads',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_spa_spr.status_code != 200:
    print(f'Failed to get odds: status_code {r_spa_spr.status_code}, response body {r_spa_spr.text}')

else:
    odds_json_spa_spr = r_spa_spr.json()
    print('Number of events:', len(odds_json_spa_spr))
    #print(odds_json_spa_spr)

    # Check the usage quota
    print('Remaining requests', r_spa_spr.headers['x-requests-remaining'])
    print('Used requests', r_spa_spr.headers['x-requests-used'])

odds_spa_spr = pd.json_normalize(odds_json_spa_spr,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

odds_spa_spr['match'] = odds_spa_spr['home_team'] + '-' + odds_spa_spr['away_team']

pivot_spa_spr = pd.pivot_table(data=odds_spa_spr, index=['match','name'], aggfunc={'price':np.mean})
pivot_spa_spr = pivot_spa_spr.reset_index()
pivot_spa_spr['price'] = np.where((pivot_spa_spr['price'] < 100) & (pivot_spa_spr['price'] >= -100), 100, pivot_spa_spr['price'])
pivot_spa_spr['price'] = pivot_spa_spr['price'].astype(int)
"""

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

odds_fra_hda['match'] = odds_fra_hda['home_team'] + '-' + odds_fra_hda['away_team']

pivot_fra_hda = pd.pivot_table(data=odds_fra_hda, index=['match','name'], aggfunc={'price':np.mean})
pivot_fra_hda = pivot_fra_hda.reset_index()
pivot_fra_hda['price'] = np.where((pivot_fra_hda['price'] < 100) & (pivot_fra_hda['price'] >= -100), 100, pivot_fra_hda['price'])
pivot_fra_hda['price'] = pivot_fra_hda['price'].astype(int)

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

odds_fra_tot['match'] = odds_fra_tot['home_team'] + '-' + odds_fra_tot['away_team']

pivot_fra_tot = pd.pivot_table(data=odds_fra_tot, index=['match','name'], aggfunc={'price':np.mean})
pivot_fra_tot = pivot_fra_tot.reset_index()
pivot_fra_tot['price'] = np.where((pivot_fra_tot['price'] < 100) & (pivot_fra_tot['price'] >= -100), 100, pivot_fra_tot['price'])
pivot_fra_tot['price'] = pivot_fra_tot['price'].astype(int)

"""
# france spread
r_fra_spr = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_france_ligue_one/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'spreads',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_fra_spr.status_code != 200:
    print(f'Failed to get odds: status_code {r_fra_spr.status_code}, response body {r_fra_spr.text}')

else:
    odds_json_fra_spr = r_fra_spr.json()
    print('Number of events:', len(odds_json_fra_spr))
    #print(odds_json_fra_spr)

    # Check the usage quota
    print('Remaining requests', r_fra_spr.headers['x-requests-remaining'])
    print('Used requests', r_fra_spr.headers['x-requests-used'])

odds_fra_spr = pd.json_normalize(odds_json_fra_spr,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

odds_fra_spr['match'] = odds_fra_spr['home_team'] + '-' + odds_fra_spr['away_team']

pivot_fra_spr = pd.pivot_table(data=odds_fra_spr, index=['match','name'], aggfunc={'price':np.mean})
pivot_fra_spr = pivot_fra_spr.reset_index()
pivot_fra_spr['price'] = np.where((pivot_fra_spr['price'] < 100) & (pivot_fra_spr['price'] >= -100), 100, pivot_fra_spr['price'])
pivot_fra_spr['price'] = pivot_fra_spr['price'].astype(int)
"""

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

odds_eng_hda['match'] = odds_eng_hda['home_team'] + '-' + odds_eng_hda['away_team']

pivot_eng_hda = pd.pivot_table(data=odds_eng_hda, index=['match','name'], aggfunc={'price':np.mean})
pivot_eng_hda = pivot_eng_hda.reset_index()
pivot_eng_hda['price'] = np.where((pivot_eng_hda['price'] < 100) & (pivot_eng_hda['price'] >= -100), 100, pivot_eng_hda['price'])
pivot_eng_hda['price'] = pivot_eng_hda['price'].astype(int)

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

odds_eng_tot['match'] = odds_eng_tot['home_team'] + '-' + odds_eng_tot['away_team']

pivot_eng_tot = pd.pivot_table(data=odds_eng_tot, index=['match','name'], aggfunc={'price':np.mean})
pivot_eng_tot = pivot_eng_tot.reset_index()
pivot_eng_tot['price'] = np.where((pivot_eng_tot['price'] < 100) & (pivot_eng_tot['price'] >= -100), 100, pivot_eng_tot['price'])
pivot_eng_tot['price'] = pivot_eng_tot['price'].astype(int)

"""
# england spread
r_eng_spr = requests.get(
    'https://api.the-odds-api.com/v4/sports/soccer_epl/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': 'spreads',
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if r_eng_spr.status_code != 200:
    print(f'Failed to get odds: status_code {r_eng_spr.status_code}, response body {r_eng_spr.text}')

else:
    odds_json_eng_spr = r_eng_spr.json()
    print('Number of events:', len(odds_json_eng_spr))
    #print(odds_json_eng_spr)

    # Check the usage quota
    print('Remaining requests', r_eng_spr.headers['x-requests-remaining'])
    print('Used requests', r_eng_spr.headers['x-requests-used'])

odds_eng_spr = pd.json_normalize(odds_json_eng_spr,
record_path=['bookmakers','markets','outcomes'],
meta=['id','sport_key','home_team','away_team'],
errors='ignore')

odds_eng_spr['match'] = odds_eng_spr['home_team'] + '-' + odds_eng_spr['away_team']

pivot_eng_spr = pd.pivot_table(data=odds_eng_spr, index=['match','name'], aggfunc={'price':np.mean})
pivot_eng_spr = pivot_eng_spr.reset_index()
pivot_eng_spr['price'] = np.where((pivot_eng_spr['price'] < 100) & (pivot_eng_spr['price'] >= -100), 100, pivot_eng_spr['price'])
pivot_eng_spr['price'] = pivot_eng_spr['price'].astype(int)
"""
"""
tables = [pivot_eng_hda, pivot_eng_tot, pivot_fra_hda, pivot_fra_tot, pivot_ger_hda, pivot_ger_tot, pivot_ita_hda, pivot_ita_tot, pivot_spa_hda, pivot_spa_tot]

odds_table = []
for t in tables:
    odds_table.append(t)
    return odds_table

"""
odds_table = pivot_eng_hda
odds_table = odds_table.append(pivot_eng_tot)
odds_table = odds_table.append(pivot_fra_hda)
odds_table = odds_table.append(pivot_fra_tot)
odds_table = odds_table.append(pivot_ger_hda)
odds_table = odds_table.append(pivot_ger_tot)
odds_table = odds_table.append(pivot_ita_hda)
odds_table = odds_table.append(pivot_ita_tot)
odds_table = odds_table.append(pivot_spa_hda)
odds_table = odds_table.append(pivot_spa_tot)
odds_table = odds_table.reset_index()
print(odds_table)
