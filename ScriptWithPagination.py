import requests
import json
import csv

with open('.env', 'r') as file:
    access_token = file.read().replace('\n', '')
ACCESS_TOKEN = access_token

def saveInCSV():
    with open('result.json') as json_file:
        data = json.load(json_file)
    data_file = open('data_file.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    count = 0
    for rep in data:
        if count == 0:
    
            # Writing headers of CSV file
            header = rep.keys()
            csv_writer.writerow(header)
            count += 1
    
        # Writing data of CSV file
        csv_writer.writerow(rep.values())
    
    data_file.close()

def saveJsonResult(resultArray):
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(json.dumps(resultArray))[0], f, ensure_ascii=False, indent=4)

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
    numberOfPages = 3
    
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
    return resultArray

def main():
    resultArray = paginationLoop()
    saveJsonResult(resultArray)
    saveInCSV()

main()