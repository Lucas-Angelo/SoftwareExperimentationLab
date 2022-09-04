import json
import requests

from src.utils.clear import clearTerminal
from src.utils.graphql import generateQuery

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

def fetchRepositories(ACCESS_TOKEN):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    isFirstRequest = True
    dataPerPage = "1"
    numberOfPages = 2
    totalRepositories = int(dataPerPage) * numberOfPages
    
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

        clearTerminal()
        actualCount = (i+1)*int(dataPerPage)
        print("Number of repositories fetched: " + str(actualCount) + "/" + str(totalRepositories))
        i=i+1

    newArray = []
    for internArr in resultArray:
        for x in internArr:
            newArray.append(x)
    resultArray = newArray

    return resultArray