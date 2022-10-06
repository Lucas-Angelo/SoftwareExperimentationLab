import json
import csv
from dateutil import parser
from datetime import datetime
from pathlib import Path

root_path = Path(__file__).parent / "..\\..\\..\\"

flag=0

def calculate_age(createdAt, closedAt, typeOfAge):
    createdDate = parser.parse(createdAt)
    closedDate = parser.parse(closedAt)
    delta = datetime(closedDate.year, closedDate.month, closedDate.day) - datetime(createdDate.year, createdDate.month, createdDate.day)
    if(typeOfAge == "days"):
        return delta.days
    elif(typeOfAge == "years"):
        return round(delta.days / 365.25, 2)
    else:
        return delta.seconds

def saveInCSV(pullRequestJsonList):
    pullrequests_file = str(root_path) + '\\pullrequests.csv'
    input_in_path = Path(__file__).parent / pullrequests_file
    data_file = open(str(input_in_path), 'a', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)

    for pullrequest in pullRequestJsonList:
        global flag
        pullrequest['analisesTimeInDays'] = None
        pullrequest['bodyHTMLLength'] = None

        pullrequest['reviews'] = pullrequest['reviews']['totalCount']
        pullrequest['files'] = pullrequest['files']['totalCount']

        bodyHTMLreplaced = pullrequest['bodyHTML']
        bodyHTMLreplaced = bodyHTMLreplaced.replace('\n', ' ').replace('\r', '')
        pullrequest['bodyHTML'] = bodyHTMLreplaced

        pullrequest['participants'] = pullrequest['participants']['totalCount']
        pullrequest['comments'] = pullrequest['comments']['totalCount']
        
        pullrequest['analisesTimeInDays'] = calculate_age(pullrequest['createdAt'], pullrequest['closedAt'], "days")

        pullrequest['bodyHTMLLength'] = str(len(bodyHTMLreplaced))

        del pullrequest['id']
        del pullrequest['url']
        del pullrequest['bodyHTML']

        if flag==0:
            # Writing headers of CSV file
            header = pullrequest.keys()
            csv_writer.writerow(header)
        flag+=1

        # Writing data of CSV file
        csv_writer.writerow(pullrequest.values())
    
    data_file.close()

def saveJsonResult(pullRequestJsonList):
    pullrequests_file = str(root_path) + '\\pullrequests.json'
    input_in_path = Path(__file__).parent / pullrequests_file
    with open(str(input_in_path), 'a', encoding='utf-8') as f:
        json.dump(pullRequestJsonList, f, ensure_ascii=False, indent=4)


def savePullRequestsInCSV(pullRequestJsonList):
    saveJsonResult(pullRequestJsonList)
    print("Pull requests JSON Updated")
    saveInCSV(pullRequestJsonList)
    print("Pull requests CSV Updated")
