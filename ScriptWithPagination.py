import requests
import json
import csv
from dateutil import parser
from datetime import datetime

with open('.env', 'r') as file:
    access_token = file.read().replace('\n', '')
ACCESS_TOKEN = access_token

def calculate_age(created):
    dt = parser.parse(created)
    delta = datetime.now() - datetime(dt.year, dt.month, dt.day)
    return delta.days

def saveInCSV(resultArray):
    data_file = open('data_file.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    null = None
    count = 0
    for rep in resultArray:
        
        rep['lastrelease'] = null
        rep['ageindays'] = null
        rep['dayssincelastupdate'] = null
        rep['dayssincelastrelease'] = null

        if count == 0:
            # Writing headers of CSV file
            header = rep.keys()
            csv_writer.writerow(header)
            count += 1

        rep['ageindays'] = calculate_age(rep['createdAt'])
        rep['dayssincelastupdate'] = calculate_age(rep['updatedAt'])

        if(
            rep['releases'] is not None and 
            len(rep['releases']['nodes']) > 0 and
            rep['releases']['nodes'][0] is not None and 
            rep['releases']['nodes'][0]['createdAt'] is not None
            ):
            rep['lastrelease'] = rep['releases']['nodes'][0]['createdAt']
            rep['dayssincelastrelease'] = calculate_age(rep['lastrelease'])

        if(rep['releases'] is not None and rep['releases']['totalCount'] is not None):
            rep['releases'] = rep['releases']['totalCount']
        else:
            rep['releases'] = null

        if(rep['primaryLanguage'] is not None and rep['primaryLanguage']['name'] is not None):
            rep['primaryLanguage'] = rep['primaryLanguage']['name']
        else:
            rep['primaryLanguage'] = null
        
        if(rep['pullrequestsmerged'] is not None and rep['pullrequestsmerged']['totalCount'] is not None):
            rep['pullrequestsmerged'] = rep['pullrequestsmerged']['totalCount']
        else:
            rep['pullrequestsmerged'] = null
        
        if(rep['issues'] is not None and rep['issues']['totalCount'] is not None):
            rep['issues'] = rep['issues']['totalCount']
        else:
            rep['issues'] = null

        if(rep['issuesclosed'] is not None and rep['issuesclosed']['totalCount'] is not None):
            rep['issuesclosed'] = rep['issuesclosed']['totalCount']
        else:
            rep['issuesclosed'] = null
        # Writing data of CSV file
        csv_writer.writerow(rep.values())
    
    data_file.close()

def saveJsonResult(resultArray):
    with open('result.json', 'w', encoding='utf-8') as f:
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

def generateQuery(isFirstRequest, hasNextPage, actualEndCursor, dataPerPage, afterStringToPagination):
    if isFirstRequest == False and hasNextPage == True:
        afterStringToPagination = 'after: "' + actualEndCursor + '"'
    newQuery = """
    {
        search(
            """ + afterStringToPagination + """
            query: "stars:>500, sort:stars-desc"
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
                    updatedAt
                    releases(first: 1, orderBy: {field: CREATED_AT, direction: DESC}) {
                        totalCount
                    nodes {
                        createdAt
                    }
                    }
                    primaryLanguage {
                        name
                    }
                    pullrequestsmerged: pullRequests(states: MERGED) {
                        totalCount
                    }
                    issues: issues {
                        totalCount
                    }
                    issuesclosed: issues(states: CLOSED) {
                        totalCount
                    }
                }
            }
        }
    }
    """
    newQuery = {'query': newQuery.replace('\n', ' ')}
    return newQuery

def paginationLoop():
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}

    isFirstRequest = True
    dataPerPage = "20"
    numberOfPages = 50
    
    hasNextPage = True
    actualEndCursor = ""

    afterStringToPagination= ""

    resultArray = []
    i = 0
    while hasNextPage and i < numberOfPages:
        query = generateQuery(isFirstRequest, hasNextPage, actualEndCursor, dataPerPage, afterStringToPagination)

        resultFromRequest = sendRequest(query, url, headers)
        isFirstRequest = False

        resultArray.append(json.loads(resultFromRequest)['data']['search']['nodes'])

        hasNextPage = getHasNextPage(resultFromRequest)
        actualEndCursor = getEndCursor(resultFromRequest)
        setNextPage(hasNextPage, actualEndCursor, i, numberOfPages)

        print(i)
        i=i+1

    newArray = []
    for internArr in resultArray:
        for x in internArr:
            newArray.append(x)
    resultArray = newArray;

    return resultArray

def main():
    resultArray = paginationLoop()
    saveJsonResult(resultArray)
    saveInCSV(resultArray)

main()