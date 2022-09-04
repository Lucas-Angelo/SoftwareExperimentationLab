import os
import pandas as pd
import dataframe_image as dfi
import matplotlib.pyplot as plt
from pathlib import Path

from src.utils.clear import clearTerminal

def boxPlotToPNG(df):
    myFig = plt.figure()
    plt.title('Boxplot')
    input_file = '..\\..\\informations\\boxplot.png'
    input_in_path = Path(__file__).parent / input_file
    stud_bplt = df.boxplot(showfliers=False)
    stud_bplt.plot()
    myFig.savefig(str(input_in_path), format="png")

    columnsList = ['stargazerCount', 'releases', 'ageinyears']
    columnsTitlesList = ['Stars Count', 'Releases Count', 'Age In Years']
    i = 0
    for column in columnsList:
        myFig = plt.figure()
        plt.title(columnsTitlesList[i])
        input_file = '..\\..\\informations\\boxplot' + (columnsTitlesList[i].replace(' ', '')) + '.png'
        input_in_path = Path(__file__).parent / input_file
        df.boxplot(
            column=[column]
        )
        myFig.savefig(str(input_in_path), format="png")
        i+=1

def descriveToPNG(df):
    input_file = '..\\..\\informations\describe.png'
    input_in_path = Path(__file__).parent / input_file
    describe = df.describe()
    df_styled = describe.style.background_gradient()
    dfi.export(df_styled,str(input_in_path))

def generateRepositoryMetrics(resultArray):
    df = pd.json_normalize(resultArray)
    descriveToPNG(df)
    clearTerminal()
    boxPlotToPNG(df)