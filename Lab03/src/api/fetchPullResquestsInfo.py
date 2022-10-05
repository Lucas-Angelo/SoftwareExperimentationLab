import json
import requests
import pandas as pd
from pathlib import Path
from dateutil import parser

from src.utils.clear import clearTerminal
from src.graphql.PullRequestsGraphQL import getPullRequestsGraphQL
from src.utils.csv.savePullRequestsCSV import savePullRequestsInCSV

root_path = Path(__file__).parent / "..\\..\\"

def mergedPullRequestOverOneHour(node):
    minMinutes =60
    hasOneHourOrMore = False
    createdAt = parser.parse(node['createdAt'])
    mergedAt = parser.parse(node['mergedAt'])
    minutes_diff = (mergedAt - createdAt).total_seconds() / 60.0
    if(minutes_diff>=minMinutes):
        hasOneHourOrMore = True
    return hasOneHourOrMore

def closedPullRequestOverOneHour(node):
    minMinutes =60
    hasOneHourOrMore = False
    createdAt = parser.parse(node['createdAt'])
    closedAt = parser.parse(node['closedAt'])
    minutes_diff = (closedAt - createdAt).total_seconds() / 60.0
    if(minutes_diff>=minMinutes):
        hasOneHourOrMore = True
    return hasOneHourOrMore

def pullRequestHasOneORMoreThan1Review(node):
    minReviews = 1
    hasOneORMoreThan1Review = False
    reviewCounts = node['reviews']['totalCount']
    if (reviewCounts) >= minReviews:
        hasOneORMoreThan1Review = True
    return hasOneORMoreThan1Review

def getMergedPullRequestsEndCursor(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    endCursor = jsonResult['data']['repository']['mergedPullRequests']['pageInfo']['endCursor']
    return endCursor

def getMergedPullRequestsHasNextPage(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    hasNextPage = jsonResult['data']['repository']['mergedPullRequests']['pageInfo']['hasNextPage']
    return hasNextPage

def getClosedPullRequestsEndCursor(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    endCursor = jsonResult['data']['repository']['closedPullRequests']['pageInfo']['endCursor']
    return endCursor

def getClosedPullRequestsHasNextPage(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    hasNextPage = jsonResult['data']['repository']['closedPullRequests']['pageInfo']['hasNextPage']
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

def getRepositoriesCSV():
    repositories_file = str(root_path) + '\\repositories.csv'
    input_in_path = Path(__file__).parent / repositories_file
    return pd.read_csv(str(input_in_path), header=0, sep=',', engine='python', encoding="ISO-8859-1")

def fetchPullRequestsInfo(ACCESS_TOKEN):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    dataPerPage = "20"

    repositoriesCSVList = getRepositoriesCSV()
    pullRequestJsonList = []

    pullRequestsTotalFetched = 0
    for i, repository_row in repositoriesCSVList.iterrows():
        currentPullRequestJsonList = []
        
        closedPullRequestsNodePagesRead = []
        mergedPullRequestsNodePagesRead = []

        closedPullRequestsEndCursor = "null"
        mergedPullRequestsEndCursor = "null"
        closedPullRequestsHasNextPage = True
        mergedPullRequestsHasNextPage = True

        repositoryOwner = repository_row["owner"]
        repositoryName = repository_row["name"]
    
        pullRequestsTotalFetchedOnThisRepository = 0
        while closedPullRequestsHasNextPage or mergedPullRequestsHasNextPage:
            pullRequestsQuery = getPullRequestsGraphQL(repositoryOwner, repositoryName, dataPerPage, closedPullRequestsEndCursor, mergedPullRequestsEndCursor)
            pullResquestsResponse = sendRequest(pullRequestsQuery, url, headers)

            try:
                json.loads(pullResquestsResponse) == None 
                json.loads(pullResquestsResponse)['data'] == None 
                json.loads(pullResquestsResponse)['data']['repository'] == None 
                json.loads(pullResquestsResponse)['data']['repository']['closedPullRequests'] == None 
                json.loads(pullResquestsResponse)['data']['repository']['closedPullRequests']["nodes"] == None 
                json.loads(pullResquestsResponse)['data']['repository']['mergedPullRequests'] == None 
                json.loads(pullResquestsResponse)['data']['repository']['mergedPullRequests']["nodes"] == None
            except:
                break

            closedPullRequestsNodes = json.loads(pullResquestsResponse)['data']['repository']['closedPullRequests']["nodes"]
            closedPullRequestsNodeStart = json.loads(pullResquestsResponse)['data']['repository']['closedPullRequests']["pageInfo"]["startCursor"]
            if(len(closedPullRequestsNodes) > 0 and closedPullRequestsNodeStart not in closedPullRequestsNodePagesRead):
                for node in closedPullRequestsNodes:
                    if pullRequestHasOneORMoreThan1Review(node) and closedPullRequestOverOneHour(node):
                        pullRequestJsonList.append(node)
                        currentPullRequestJsonList.append(node)
                closedPullRequestsNodePagesRead.append(closedPullRequestsNodeStart)
            closedPullRequestsHasNextPage = getClosedPullRequestsHasNextPage(pullResquestsResponse)
            if(closedPullRequestsHasNextPage):
                closedPullRequestsEndCursor = getClosedPullRequestsEndCursor(pullResquestsResponse)

            mergedPullRequestsNodes = json.loads(pullResquestsResponse)['data']['repository']['mergedPullRequests']["nodes"]
            mergedPullRequestsNodeStart = json.loads(pullResquestsResponse)['data']['repository']['mergedPullRequests']["pageInfo"]["startCursor"]
            if(len(mergedPullRequestsNodes) > 0 and mergedPullRequestsNodeStart not in mergedPullRequestsNodePagesRead):
                for node in mergedPullRequestsNodes:
                    if pullRequestHasOneORMoreThan1Review(node) and mergedPullRequestOverOneHour(node):
                        pullRequestJsonList.append(node)
                        currentPullRequestJsonList.append(node)
                mergedPullRequestsNodePagesRead.append(mergedPullRequestsNodeStart)
            mergedPullRequestsHasNextPage = getMergedPullRequestsHasNextPage(pullResquestsResponse)
            if(mergedPullRequestsHasNextPage):
                mergedPullRequestsEndCursor = getMergedPullRequestsEndCursor(pullResquestsResponse)
            
            clearTerminal()
            pullRequestsTotalFetchedOnThisRepository += len(closedPullRequestsNodes) + len(mergedPullRequestsNodes)
            messageTotal = "Total pull requests with reviews >= 1 and not closed/merged by bots fetched: " + str(len(pullRequestJsonList))
            print(messageTotal)
            messageActualRep = "Total pull requests fetched at the current repository (" + str(i) + ") : https://github.com/" + repositoryOwner + "/" + repositoryName +  " is: " + str(pullRequestsTotalFetchedOnThisRepository) 
            print(messageActualRep)
            pullRequestsTotalFetched += pullRequestsTotalFetchedOnThisRepository
        savePullRequestsInCSV(currentPullRequestJsonList)

    clearTerminal()
    print("Total pull requests with reviews >= 1 fetched: " + str(len(pullRequestJsonList)) + "/" + str(pullRequestsTotalFetched) + " total pull requests fetched at all repositories")
    return pullRequestJsonList