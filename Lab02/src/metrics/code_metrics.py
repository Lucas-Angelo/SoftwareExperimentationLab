import os
import pandas as pd
from github import Github
from pathlib import Path
from multiprocessing.pool import ThreadPool as Pool

from src.utils.clear import clearTerminal

root_path = Path(__file__).parent / "..\\..\\"
repositories_path = Path(__file__).parent / (str(root_path) + "\\repositories")

def deleteRepository(actualRepository):
    out_path = str(root_path) + '\\out\\' + actualRepository.name
    print("\n---> Deleting {}".format(actualRepository.name))
    os.system("rm -rf {}/{}".format(str(repositories_path), actualRepository.name))
    os.system("rm -rf {}".format(out_path + "class.csv"))
    os.system("rm -rf {}".format(out_path + "method.csv"))
    print("---> Repository {} deleted from disk.".format(actualRepository.name))

def defineCodeMetricValues(repositories_fetched, index, actualRepository):
    out_path = str(root_path) + '\\out\\' + actualRepository.name + "class.csv"
    metrics_df = pd.read_csv(out_path, usecols=['loc', 'cbo', 'dit', 'lcom']) # Values generated by CK Metrics
    medians = metrics_df.median(skipna=True)
    sums = metrics_df.sum(skipna=True)
    repositories_fetched.loc[index, 'LOC'] = sums['loc']
    repositories_fetched.loc[index, 'CBO'] = medians['cbo']
    repositories_fetched.loc[index, 'DIT'] = medians['dit']
    repositories_fetched.loc[index, 'LCOM'] = medians['lcom']
    print("---> Repository {} code metrics: LOC={} ; CBO={} ; DIT={} ; LCOM={}".format(actualRepository.name, str(sums['loc']), str(medians['cbo']), str(medians['dit']), str(medians['lcom'])))

def calculeCodeMetrics(actualRepository):
    print("\n---> Calculating code metrics with CK from repository {}.".format(actualRepository.name))
    jar_file = str(root_path) + '\\jar\\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
    jar_path = Path(__file__).parent / jar_file
    out_path = str(root_path) + '\\out\\' + actualRepository.name
    erros = os.system("java -jar {} {}/{}/ 1 0 0 {}".format(str(jar_path), str(repositories_path), actualRepository.name, out_path))
    return erros

def cloneRepository(actualRepository):
    print("---> Clonning {}".format(actualRepository.name))
    os.system("git clone {} {}/{}".format(actualRepository.clone_url, str(repositories_path), actualRepository.name))
    print("---> {} cloned.".format(actualRepository.name))

def rowIsEmpty(repository_row):
    return (str(repository_row['LOC']) == "nan" or str(repository_row['CBO']) == "nan" or str(repository_row['DIT']) == "nan" or str(repository_row['LCOM']) == "nan")

def getData():
    repositories_file = str(root_path) + '\\data.csv'
    input_in_path = Path(__file__).parent / repositories_file
    return pd.read_csv(str(input_in_path), header=0, sep=',')

def runRepository(i, repository_row, repositories_fetched, github):
    if rowIsEmpty(repository_row):
        try:
            actualRepository = github.get_repo(repository_row['nameWithOwner'])

            #clearTerminal()
            cloneRepository(actualRepository)
            errorsOnJar = calculeCodeMetrics(actualRepository)

            defineCodeMetricValues(repositories_fetched, i, actualRepository)
            repositories_fetched.to_csv(str(root_path) + '\\data_with_code_metrics.csv', index=False, header=True)
            
            deleteRepository(actualRepository)

            if errorsOnJar != 0:
                raise Exception("\nError at CK metrics jar...")

        except Exception as error:
            print('\nError on repository index {}'.format(i))
            print(error)

pool_size = 20  # your "parallelness"

# define worker function before a Pool is instantiated
def worker(i, repository_row, repositories_fetched, github):
    try:
        runRepository(i, repository_row, repositories_fetched, github)
    except:
        print('error with repository')

def generateCodeMetrics(ACCESS_TOKEN):
    github = Github("admited", ACCESS_TOKEN)
    repositories_fetched = getData()

    pool = Pool(pool_size)

    for i, repository_row in repositories_fetched.iterrows():
        pool.apply_async(worker, (i, repository_row, repositories_fetched, github,))

    pool.close()
    pool.join()
    print("\nCode metrics was calculated")