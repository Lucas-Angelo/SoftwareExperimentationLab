import json
import requests

from src.utils.clear import clearTerminal
from src.graphql.RepositoriesGraphQL import getRepositoriesGraphQL

def repHasOneHundredPR(node):
    minPullRequests = 100
    hasOneHundredPR = False
    mergedPR = node['mergedPullRequests']['totalCount']
    closedPR = node['closedPullRequests']['totalCount']
    if (mergedPR + closedPR) >= minPullRequests:
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
        try:
            request = requests.post(url=url, headers=headers, json=query)
            if request.status_code == 200:
                return request.text
            else:
                print("Trying again because query failed to run returning code of {}. {}".format(request.status_code, query))
        except Exception:
            request = None
            print("Trying again because occured a exception on request.")

def fetchRepositories(ACCESS_TOKEN):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    totalRepositories = 100
    dataPerPage = "10"
    endCursor= "null"
    hasNextPage = True

    repositoriesJsonList = []
    i = 0
    while hasNextPage and len(repositoriesJsonList) < totalRepositories:
        query = getRepositoriesGraphQL(dataPerPage, endCursor)

        resultFromRequest = sendRequest(query, url, headers)
        
        edges = json.loads(resultFromRequest)['data']['search']['edges']
        for edge in edges:
            node = edge['node']
            if repHasOneHundredPR(node) and len(repositoriesJsonList) < totalRepositories:
                repositoriesJsonList.append(node)


        hasNextPage = getHasNextPage(resultFromRequest)
        endCursor = getEndCursor(resultFromRequest)

        clearTerminal()
        print("Number of repositories fetched: " + str(len(repositoriesJsonList)) + "/" + str(totalRepositories))
        i=i+1

    return repositoriesJsonList