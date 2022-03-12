import urllib.request
from datetime import datetime

import json

import os.path
from os import listdir

def get_owid_file():
    """ Downloads today's owid Portugal Data, if it hasn't already been downloaded """
    date_today = datetime.today().strftime('%Y-%m-%d')
    file_name = 'owid-' + date_today + '.json'

    cur_dir = os.path.dirname(__file__)
    parent_dir = os.path.split(cur_dir)[0]
    files_directory = parent_dir + "\\Code\\_Data"
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-4:]) == "json"]

    if file_name in list_files: # Checks if there was already downloaded a file today
        print("Today's file already exists")
    else:
        print('Beginning file download with urllib module')
        url = 'https://covid.ourworldindata.org/data/owid-covid-data.json'

        urllib.request.urlretrieve(url, 'Code\\_Data\\' + file_name)
        print("File Downloaded")

    return date_today


def format_owid_data():
    """ Obtains and formats data from OWID, returning dates and COVID-19 cases """

    date_today = get_owid_file()

    file_name_today = 'owid-' + date_today + '.json'
    data_json = "Code\\_Data\\" + file_name_today


    with open(data_json, 'r') as f:
       data = json.load(f) # A dictionary

    pt_data = data["PRT"] # Portugal ISO code
    daily_data = pt_data["data"] # Obtaining the daily information (array)

    dates = []
    new_cases = []

    # Later check with 'new_cases_smoothed' and/or 'new_cases_smoothed_per_million'
    for i in range(len(daily_data)):
        dates.append(daily_data[i]["date"])

        try:
            if daily_data[i]["new_cases"] > 0:
                new_cases.append(daily_data[i]["new_cases"])

            else:
                new_cases.append(0) # If there are negative values it's not a data error but a counting error.
                # For instance in 02/05/2020 there's a negative value to balance a miscount (some values were counted twice) in one of the previous days

        except: # If that date (dictionary) doesn't have a 'new_cases' value
            new_cases.append(0)
    
    return dates, new_cases



if __name__ == "__main__":

    format_owid_data()