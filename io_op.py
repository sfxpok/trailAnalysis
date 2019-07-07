import pandas as pd

def writeToCSVFile(data, compName, yearNumber):
    """Generates a CSV file with the quantiles output
    
    Parameters
    ----------
    data : pandas dataframe
        quantile output data
    compName : string
        competition name
    yearNumber : integer
        competition year
    """

    csvFileName = compName + "_" + str(yearNumber) + "_" + "quartiles.csv"

    data.to_csv(path_or_buf=csvFileName, header=False)