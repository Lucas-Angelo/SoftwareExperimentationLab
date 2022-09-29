from dotenv import dotenv_values

from src.api.github import fetchRepositories
from src.utils.data import saveData

config = dotenv_values(".env")
ACCESS_TOKEN = config["ACCESS_TOKEN"]

def main():
    val = input("Do you want fetch the 100 repositories from Github? (y/n): ")
    if(val=="y"):
        resultArray = fetchRepositories(ACCESS_TOKEN)
        saveData(resultArray)
        print("All repositories were fetched and saved in csv file")
    #val = input("Do you want calculate PR metrics? (y/n): ")
    #if(val=="y"):
        #generatePRMetrics(ACCESS_TOKEN)

main()