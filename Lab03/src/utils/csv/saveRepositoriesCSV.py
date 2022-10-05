import json
import csv
from pathlib import Path

root_path = Path(__file__).parent / "..\\..\\..\\"

from pathlib import Path

def saveInCSV(resultArray):
    repositories_file = str(root_path) + '\\repositories.csv'
    input_in_path = Path(__file__).parent / repositories_file
    data_file = open(str(input_in_path), 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    count = 0
    for rep in resultArray:

        rep['totalPullRequests'] = None

        if count == 0:
            # Writing headers of CSV file
            header = rep.keys()
            csv_writer.writerow(header)
            count += 1
        
        rep['owner'] = rep['owner']['login']
        rep['mergedPullRequests'] = rep['mergedPullRequests']['totalCount']
        rep['closedPullRequests'] = rep['closedPullRequests']['totalCount']
        rep['totalPullRequests'] = str(int(rep['mergedPullRequests'])+int(rep['closedPullRequests']))

        # Writing data of CSV file
        csv_writer.writerow(rep.values())
    
    data_file.close()

def saveJsonResult(resultArray):
    repositories_file = str(root_path) + '\\repositories.json'
    input_in_path = Path(__file__).parent / repositories_file
    with open(str(input_in_path), 'w', encoding='utf-8') as f:
        json.dump(resultArray, f, ensure_ascii=False, indent=4)


def saveRepositoriesInCSV(resultArray):
    saveJsonResult(resultArray)
    saveInCSV(resultArray)
