import json
import csv

from pathlib import Path

def saveInCSV(resultArray):
    input_file = '..\\..\\data.csv'
    input_in_path = Path(__file__).parent / input_file
    data_file = open(str(input_in_path), 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    count = 0
    for rep in resultArray:

        if count == 0:
            # Writing headers of CSV file
            header = rep.keys()
            csv_writer.writerow(header)
            count += 1
        
        rep['mergedPullRequests'] = rep['mergedPullRequests']['totalCount']
        rep['closedPullRequests'] = rep['closedPullRequests']['totalCount']

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
