from dotenv import dotenv_values

from src.api.github import fetchRepositories
from src.utils.data import saveData
from src.metrics.repository_metrics import generateRepositoryMetrics
from src.metrics.code_metrics import generateCodeMetrics

config = dotenv_values(".env")
ACCESS_TOKEN = config["ACCESS_TOKEN"]

def main():
    val = input("Do you want fetch repositories from Github? (y/n): ")
    if(val=="y"):
        resultArray = fetchRepositories(ACCESS_TOKEN)
        saveData(resultArray)
        generateRepositoryMetrics(resultArray)
        print("All repositories were fetched and saved in csv file")
    val = input("Do you want calculate code metrics? (y/n): ")
    if(val=="y"):
        generateCodeMetrics(ACCESS_TOKEN)

main()