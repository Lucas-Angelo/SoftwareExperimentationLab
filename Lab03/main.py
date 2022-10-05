from dotenv import dotenv_values

from src.api.fetchPullResquestsInfo import fetchPullRequestsInfo
from src.api.fetchRepositoriesInfo import fetchRepositories
from src.utils.csv.saveRepositoriesCSV import saveRepositoriesInCSV

config = dotenv_values(".env")
ACCESS_TOKEN = config["ACCESS_TOKEN"]

def main():
    val = input("Do you want fetch the 100 repositories from Github? (y/n): ")
    if(val=="y"):
        repositoriesJson = fetchRepositories(ACCESS_TOKEN)
        saveRepositoriesInCSV(repositoriesJson)
        print("All repositories were fetched and saved in csv file")
    val = input("Do you want calculate PR metrics? (y/n): ")
    if(val=="y"):
        repositoriesJson = fetchPullRequestsInfo(ACCESS_TOKEN)
        print("All pull requests were fetched and saved in csv file")

main()