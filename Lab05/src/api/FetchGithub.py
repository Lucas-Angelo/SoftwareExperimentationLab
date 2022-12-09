import json
import requests
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path

from src.utils.OS import clearTerminal
from src.graphql.Query import getUserAndRepositoriesWithGraphQL

def getEndCursor(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    endCursor = jsonResult['data']['user']['repositories']['pageInfo']['endCursor']
    return endCursor

def getHasNextPage(resultFromRequest):
    jsonResult = json.loads(resultFromRequest)
    hasNextPage = jsonResult['data']['user']['repositories']['pageInfo']['hasNextPage']
    return hasNextPage

def sendGraphQLRequest(query, url, headers):
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

def fetchGraphQL(ACCESS_TOKEN, repositoriesQuantity):
    graphQLURL = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    totalRequests = 100

    graphQLDurations = []
    graphQLSize = []
    graphQLDurations = []
    graphQLSize = []
    i = 0
    while i < totalRequests:
        query = getUserAndRepositoriesWithGraphQL(repositoriesQuantity)

        start_time = datetime.now()
        resultFromRequest = sendGraphQLRequest(query, graphQLURL, headers)
        end_time = datetime.now()

        duration = (end_time - start_time).total_seconds() * 1000
        graphQLDurations.append(duration)

        dataSize = sys.getsizeof(resultFromRequest)
        graphQLSize.append(dataSize)

        print(i)
        print('GraphQL Duration: {}'.format(duration))
        print('GraphQL Size: {}'.format(dataSize))
        # clearTerminal()
        i=i+1

    root_path = Path(__file__).parent / "..\\..\\"
    result_file = str(root_path) + '\\resultOneRep.csv'
    if(repositoriesQuantity==50):
        result_file = str(root_path) + '\\resultFifityRep.csv'
    input_in_path = Path(__file__).parent / result_file
    df= pd.DataFrame(data={'GraphQLDurations': graphQLDurations,  
                       'GraphQLSizes':graphQLSize})
    df.to_csv(str(input_in_path), index=False)
    return [graphQLDurations, graphQLSize]

def sendRESTRequest(url, headers):
    request = None
    while(request == None or request.status_code != 200):
        try:
            request = requests.get(url=url, headers=headers)
            if request.status_code == 200:
                return request.text
            else:
                print("Trying again because query failed to run returning code of {}. {}".format(request.status_code))
        except Exception:
            request = None
            print("Trying again because occured a exception on request.")

def fetchREST(ACCESS_TOKEN, repositoriesQuantity):
    restURL = 'https://api.github.com/'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    totalRequests = 100

    restDurations = []
    restSize = []
    i = 0
    while i < totalRequests:
        restPath = 'users/lucas-angelo/repos?sort=created&direction=desc&per_page={}'.format(repositoriesQuantity)

        start_time = datetime.now()
        resultFromRequest = sendRESTRequest((restURL+restPath), headers)
        end_time = datetime.now()

        duration = (end_time - start_time).total_seconds() * 1000
        restDurations.append(duration)

        dataSize = sys.getsizeof(resultFromRequest)
        restSize.append(dataSize)
        
        print(i)
        print('REST Duration: {}'.format(duration))
        print('REST Size: {}'.format(dataSize))
        # clearTerminal()
        i=i+1

    root_path = Path(__file__).parent / "..\\..\\"
    result_file = str(root_path) + '\\resultOneRep.csv'
    if(repositoriesQuantity==50):
        result_file = str(root_path) + '\\resultFifityRep.csv'
    input_in_path = Path(__file__).parent / result_file
    df_csv = pd.read_csv(str(input_in_path))
    df= pd.DataFrame(restDurations)
    df_csv['RESTDurations'] = df
    df= pd.DataFrame(restSize)
    df_csv['RESTSizes'] = df
    df_csv.to_csv(str(input_in_path), index=False)
    return [restDurations, restSize]