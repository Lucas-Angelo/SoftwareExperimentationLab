def getPullRequestsGraphQL(repositoryOwner, repositoryName, dataPerPage, closedPullRequestsEndCursor, mergedPullRequestsEndCursor):
    if(closedPullRequestsEndCursor != "null"):
        closedPullRequestsAfter = 'after: "' + closedPullRequestsEndCursor + '"'
    else:
        closedPullRequestsAfter = 'after: ' + closedPullRequestsEndCursor
    if(mergedPullRequestsEndCursor != "null"):
        mergedPullRequestsAfter = 'after: "' + mergedPullRequestsEndCursor + '"'
    else:
        mergedPullRequestsAfter = 'after: ' + mergedPullRequestsEndCursor
    newQuery = """
    query {
      repository(owner: """ + '"' + repositoryOwner + '"' + """, name: """ + '"' + repositoryName + '"' + """) {
        closedPullRequests: pullRequests(
          states: CLOSED
          first: """ + dataPerPage + """
          """ + closedPullRequestsAfter + """
        ) {
          pageInfo {
            startCursor
            hasNextPage
            endCursor
          }
          nodes {
            id
            url
            reviews(first: 1) {
              totalCount
            }
            files(first: 1) {
              totalCount
            }
            additions
            deletions
            createdAt
            mergedAt
            closedAt
            bodyHTML
            participants(first: 1) {
              totalCount
            }
            comments(first: 1) {
              totalCount
            }
            state
          }
        }
        mergedPullRequests: pullRequests(
          states: MERGED
          first: """ + dataPerPage + """
          """ + mergedPullRequestsAfter + """
        ) {
          pageInfo {
            startCursor
            hasNextPage
            endCursor
          }
          nodes {
            id
            url
            reviews(first: 1) {
              totalCount
            }
            files(first: 1) {
              totalCount
            }
            additions
            deletions
            createdAt
            mergedAt
            closedAt
            bodyHTML
            participants(first: 1) {
              totalCount
            }
            comments(first: 1) {
              totalCount
            }
            state
          }
        }
      }
    }
    """
    newQuery = {'query': newQuery.replace('\n', ' ')}
    return newQuery