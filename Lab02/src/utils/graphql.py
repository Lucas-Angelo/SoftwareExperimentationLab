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