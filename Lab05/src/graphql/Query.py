def getUserAndRepositoriesWithGraphQL(repositoriesQuantity):
    newQuery = """
    {
      user(login: "lucas-angelo") {
        login
        repositories(
          orderBy: {field: CREATED_AT, direction: DESC}, 
          first: """ + str(repositoriesQuantity) + """
        ) {
          edges {
            node {
              nameWithOwner
            }
          }
        }
      }
    }
    """
    newQuery = {'query': newQuery.replace('\n', ' ')}
    return newQuery