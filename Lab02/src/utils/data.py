import json
import csv

from dateutil import parser
from datetime import datetime
from pathlib import Path

def calculate_age(created, typeOfAge):
    dt = parser.parse(created)
    delta = datetime.now() - datetime(dt.year, dt.month, dt.day)
    if(typeOfAge == "days"):
        return delta.days
    elif(typeOfAge == "years"):
        return round(delta.days / 365.25, 2)
    else:
        return delta.seconds

def saveInCSV(resultArray):
    input_file = '..\\..\\data.csv'
    input_in_path = Path(__file__).parent / input_file
    data_file = open(str(input_in_path), 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    null = None
    count = 0
    for rep in resultArray:
        
        rep['ageinyears'] = null
        rep['LOC'] = null
        rep['CBO'] = null
        rep['DIT'] = null
        rep['LCOM'] = null

        if count == 0:
            # Writing headers of CSV file
            header = rep.keys()
            csv_writer.writerow(header)
            count += 1

        rep['ageinyears'] = calculate_age(rep['createdAt'], "years")

        if(rep['releases'] is not None and rep['releases']['totalCount'] is not None):
            rep['releases'] = rep['releases']['totalCount']
        else:
            rep['releases'] = null

        # Writing data of CSV file
        csv_writer.writerow(rep.values())
    
    data_file.close()

def saveJsonResult(resultArray):
    input_file = '..\\..\\data.json'
    input_in_path = Path(__file__).parent / input_file
    with open(str(input_in_path), 'w', encoding='utf-8') as f:
        json.dump(resultArray, f, ensure_ascii=False, indent=4)


def saveData(resultArray):
    saveJsonResult(resultArray)
    saveInCSV(resultArray)
