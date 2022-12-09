import csv
import numpy
from pathlib import Path

root_path = Path(__file__).parent / "..\\..\\..\\"

from pathlib import Path

def saveInCSV(dataArray):
    result_file = str(root_path) + '\\result.csv'
    input_in_path = Path(__file__).parent / result_file
    data_file = open(str(input_in_path), 'a', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    count = 0
    #for data in resultArray:

        #data['totalPullRequests'] = None

        #if count == 0:
        #    # Writing headers of CSV file
        #    header = data.keys()
        #    csv_writer.writerow(header)
        #    count += 1
    

        # Writing data of CSV file
    csv_writer.writerows(dataArray)
    
    data_file.close()

def saveResult(resultArray):
    result_file = str(root_path) + '\\result.csv'
    input_in_path = Path(__file__).parent / result_file
    numpy.savetxt(str(input_in_path), resultArray, delimiter=",")
    #saveInCSV(resultArray)
