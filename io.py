import pandas as pd

def writeToCSVFile(data, compName, yearNumber):

    csvFileName = compName + "_" + str(yearNumber) + "_" + "quartiles.csv"

    data.to_csv(path_or_buf=csvFileName)