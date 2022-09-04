
import os
import json
import csv
import requests
import pandas as pd
import dataframe_image as dfi
import matplotlib.pyplot as plt
from dateutil import parser
from datetime import datetime
from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(".env")
ACCESS_TOKEN = config["ACCESS_TOKEN"]

def boxPlotToPNG(df):
    myFig = plt.figure()
    plt.title('Boxplot')
    input_file = 'informations\\boxplot.png'
    input_in_path = Path(__file__).parent / input_file
    stud_bplt = df.boxplot(showfliers=False)
    stud_bplt.plot()
    myFig.savefig(str(input_in_path), format="png")

    columnsList = ['stargazerCount', 'releases', 'ageinyears']
    columnsTitlesList = ['Stars Count', 'Releases Count', 'Age In Years']
    i = 0;
    for column in columnsList:
        myFig = plt.figure()
        plt.title(columnsTitlesList[i])
        input_file = 'informations\\boxplot' + (columnsTitlesList[i].replace(' ', '')) + '.png'
        input_in_path = Path(__file__).parent / input_file
        df.boxplot(
            column=[column]
        )
        myFig.savefig(str(input_in_path), format="png")
        i+=1

def descriveToPNG(df):
    input_file = 'informations\describe.png'
    input_in_path = Path(__file__).parent / input_file
    describe = df.describe()
    df_styled = describe.style.background_gradient()
    dfi.export(df_styled,str(input_in_path))

def saveInfo():
    input_file = 'data.csv'
    input_in_path = Path(__file__).parent / input_file
    df = pd.read_csv(str(input_in_path), header=0, sep=',')
    descriveToPNG(df)
    cls()
    boxPlotToPNG(df)

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
    input_file = 'data.csv'
    input_in_path = Path(__file__).parent / input_file
    data_file = open(str(input_in_path), 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    null = None
    count = 0
    for rep in resultArray:
        
        rep['ageinyears'] = null

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
    input_file = 'data.json'
    input_in_path = Path(__file__).parent / input_file
    with open(str(input_in_path), 'w', encoding='utf-8') as f:
        json.dump(resultArray, f, ensure_ascii=False, indent=4)

def setNextPage(hasNextPage, actualEndCursor, i, numberOfPages):
    if(hasNextPage == False or i==numberOfPages-1):
        hasNextPage = False
    else:
        actualEndCursor = actualEndCursor

def getEndCursor(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    endCursor = jsonResult['data']['search']['pageInfo']['endCursor']
    return endCursor

def getHasNextPage(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    hasNextPage = jsonResult['data']['search']['pageInfo']['hasNextPage']
    return hasNextPage

def sendRequest(query, url, headers):
    request = requests.post(url=url, headers=headers, json=query)
    if request.status_code == 200:
        return request.text
    else:
        raise Exception("Query failed to run returning code of {}. {}".format(request.status_code, query))

def generateQuery(isFirstRequest, hasNextPage, actualEndCursor, dataPerPage, afterValue):
    if isFirstRequest == False and hasNextPage == True:
        afterValue = 'after: "' + actualEndCursor + '"'
    newQuery = """
    {
        search(
            """ + afterValue + """
            query: "stars:>500, sort:stars-desc, language:Java"
            type: REPOSITORY
            first: """ + dataPerPage + """
        ) {
            pageInfo {
                startCursor
                hasNextPage
                endCursor
            }
            nodes {
                ... on Repository {
                    id
                    stargazerCount
                    nameWithOwner
                    url
                    createdAt
                    releases(first: 1) {
                        totalCount
                    }
                }
            }
        }
    }
    """
    newQuery = {'query': newQuery.replace('\n', ' ')}
    return newQuery

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def getRepositoriesWithPaginationLoop():
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    isFirstRequest = True
    dataPerPage = "20"
    numberOfPages = 50
    totalRepositories = int(dataPerPage) * numberOfPages;
    
    hasNextPage = True
    actualEndCursor = ""

    afterValue= ""

    resultArray = []
    i = 0
    while hasNextPage and i < numberOfPages:
        query = generateQuery(isFirstRequest, hasNextPage, actualEndCursor, dataPerPage, afterValue)

        resultFromRequest = sendRequest(query, url, headers)
        isFirstRequest = False

        resultArray.append(json.loads(resultFromRequest)['data']['search']['nodes'])

        hasNextPage = getHasNextPage(resultFromRequest)
        actualEndCursor = getEndCursor(resultFromRequest)
        setNextPage(hasNextPage, actualEndCursor, i, numberOfPages)

        cls()
        actualCount = (i+1)*int(dataPerPage)
        print("Number of repositories fetched: " + str(actualCount) + "/" + str(totalRepositories))
        i=i+1

    newArray = []
    for internArr in resultArray:
        for x in internArr:
            newArray.append(x)
    resultArray = newArray

    return resultArray

def main():
    resultArray = getRepositoriesWithPaginationLoop()
    saveJsonResult(resultArray)
    saveInCSV(resultArray)
    saveInfo()
    print("All repositories were fetched and saved in csv file")

main()