import json
import requests

from src.utils.clear import clearTerminal
from src.utils.getRepositoriesGraphQL import getRepositoriesGraphQL

def repHasOneHundredPR(node):
    hasOneHundredPR = False
    mergedPR = node['mergedPullRequests']['totalCount']
    closedPR = node['closedPullRequests']['totalCount']
    if (mergedPR + closedPR) >= 100:
        hasOneHundredPR = True
    return hasOneHundredPR

def getEndCursor(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    endCursor = jsonResult['data']['search']['pageInfo']['endCursor']
    return endCursor

def getHasNextPage(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    hasNextPage = jsonResult['data']['search']['pageInfo']['hasNextPage']
    return hasNextPage

def sendRequest(query, url, headers):
    request = None
    while(request == None or request.status_code != 200):
        request = requests.post(url=url, headers=headers, json=query)
        if request.status_code == 200:
            return request.text
        else:
            print("Trying again because query failed to run returning code of {}. {}".format(request.status_code, query))

def fetchRepositories(ACCESS_TOKEN):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    totalRepositories = 100
    dataPerPage = "10"
    endCursor= "null"
    hasNextPage = True

    resultArray = []
    i = 0
    while hasNextPage and len(resultArray) < 100:
        query = getRepositoriesGraphQL(dataPerPage, endCursor)

        resultFromRequest = sendRequest(query, url, headers)

        edges = json.loads(resultFromRequest)['data']['search']['edges']
        for edge in edges:
            node = edge['node']
            if repHasOneHundredPR(node) and len(resultArray) < 100:
                resultArray.append(node)


        hasNextPage = getHasNextPage(resultFromRequest)
        endCursor = getEndCursor(resultFromRequest)

        clearTerminal()
        print("Number of repositories fetched: " + str(len(resultArray)) + "/" + str(totalRepositories))
        i=i+1

    return resultArray