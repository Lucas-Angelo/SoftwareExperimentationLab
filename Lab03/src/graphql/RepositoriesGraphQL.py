def getRepositoriesGraphQL(dataPerPage, endCursor):
    if(endCursor != "null"):
        after = 'after: "' + endCursor + '"'
    else:
        after = 'after: ' + endCursor
    newQuery = """
    {
      search(
        query: "stars:>1000, sort:stars-desc"
        type: REPOSITORY
        first: """ + dataPerPage + """
        """ + after + """
      ) {
        pageInfo {
          startCursor
          hasNextPage
          endCursor
        }
        edges {
          node {
            ... on Repository {
              id
              name
              owner {
                login
              }
              mergedPullRequests: pullRequests(states: MERGED, first: 1) {
                totalCount
              }
              closedPullRequests: pullRequests(states: CLOSED, first: 1) {
                totalCount
              }
            }
          }
        }
      }
    }
    """
    newQuery = {'query': newQuery.replace('\n', ' ')}
    return newQuery