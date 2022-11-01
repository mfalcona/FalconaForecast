
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

            elif "Almería" in row.text:
                print(row.text)
                res_str = re.sub("Almería", "Almeria", row.text)
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

            elif "Nott'ham Forest" in row.text:
                print(row.text)
                res_str = re.sub("Nott'ham Forest","Forest", row.text)
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