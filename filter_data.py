import random
import sys
import pandas as pd
from statistics import mean

import clean_data, main, plot

def best_fit_slope_and_intercept(xs, ys):
    """Calculates linear regression (best-fit)
    
    Parameters
    ----------
    xs : pandas dataframe
        contains data regarding the X axis
    ys : pandas dataframe
        contains data regarding the Y axis
    
    Returns
    -------
    float
        both m and b variables are related to the slope as a result
    """

    try:
        m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
            ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
        b = mean(ys) - m*mean(xs)
    
        return m, b
        
    except ZeroDivisionError:
        print("Divisão por zero no cálculo da regressão linear.")
        sys.exit(1)

def regressionLineCalculate(X, Y):
    """Calculates the linear regression slope
    
    Parameters
    ----------
    X : pandas dataframe
        contains data regarding the X axis
    Y : pandas dataframe
        contains data regarding the Y axis
    
    Returns
    -------
    float
        the regression line slope
    """

    m, b = best_fit_slope_and_intercept(X, Y)

    regression_line = [] # clean array, this is important
    regression_line = [(m*x)+b for x in X]

    return regression_line

def convertTimeToSeconds(checkPointTime):
    """Converts time in DatatimeIndex object format (see pandas docs)
    to seconds
    
    Parameters
    ----------
    checkPointTime : DatetimeIndex
        Contains a timestamp with a year, month, day, hour,
        minute and second
    
    Returns
    -------
    Integer
        Converted timestamp in seconds
    """

    startTime = checkPointTime.hour[0]
    
    # seconds in 1 minute * minutes in 1 hour * hours in 1 day
    oneDayInSeconds = 60*60*24

    startDay = checkPointTime.day[0]
    
    CPTimeSeconds = [] # array must be clean

    # every timestamp will be converted
    for i in range(len(checkPointTime.day)):

        # check if the day the competition started has gone to the next day
        if (checkPointTime.day[i] != startDay):
            CPTimeSeconds.append(checkPointTime.hour[i] * 3600 + checkPointTime.minute[i] * 60 + checkPointTime.second[i] + oneDayInSeconds)
        else:
            CPTimeSeconds.append(checkPointTime.hour[i] * 3600 + checkPointTime.minute[i] * 60 + checkPointTime.second[i])

    return CPTimeSeconds

def competitionFilter(df, competitionName, competitionYear):
    """Filters a given dataset within the competition filters
    (name and year)
    
    Parameters
    ----------
    df : pandas dataframe
        Contains the imported dataset from the CSV file initially
    competitionName : string
        Competition's name
    competitionYear : string
        Competition's year
    
    Returns
    -------
    pandas dataframe
        Filtered dataset within the competition filters
    """

    # imports an established competitions "database"
    dfCompetition = pd.read_json("competitions.json", orient='columns')
    
    dfCompetition['year'] = dfCompetition['year'].astype(int) # convert year to integer datatype
    competitionYear = int(competitionYear) # convert year to integer datatype

    # string parsing and criteria at the same time to pick only one competition
    dfCompetition = dfCompetition.loc[(dfCompetition['name'] == str.upper(competitionName)) | (dfCompetition['name'] == str.capitalize(competitionName))]
    dfCompetition = dfCompetition.loc[dfCompetition['year'] == competitionYear]

    # now that we only have one competition in the dataframe, fetch the competition's ID we asked for
    fetchCompetition = int(dfCompetition['competition_id'])
    
    # finally, fetch any row corresponding to the competition we picked
    # according to the competition's ID
    df = df[df.Competition == fetchCompetition]

    return df

def createOrderedBoard(df): # THIS DOES NOT WORK

    dfFiltered = df[['checkpoint_order', 'inscription_athlete_athlete_id', 'CPTime']]
    lastCP = dfFiltered.loc[dfFiltered['checkpoint_order'].idxmax()][0]
    dfFiltered = dfFiltered.loc[dfFiltered['checkpoint_order'] == lastCP]

    #dfFiltered = dfFiltered.drop_duplicates(['inscription_athlete_athlete_id'], keep='last')
    CPTimeInt64 = pd.DatetimeIndex(dfFiltered['CPTime'])
    dfFiltered['CPTime'] = convertTimeToSeconds(CPTimeInt64)

    dfFiltered = dfFiltered.sort_values(by = ['CPTime'])

    # if you want athletes in the last places, just reverse the data
    # dfFiltered = dfFiltered.iloc[::-1]

    return dfFiltered   

def getFilter(filterArg, numberOfAthletes, athleteIDs, dfFiltered):
    """Get a set of athletes according to the number of athletes
    from the user input and the selected filter through an
    argument along with the imported dataset from a
    CSV file
    
    Parameters
    ----------
    filterArg : string
        Order of ranking argument
    numberOfAthletes : integer
        Number of athletes to analyze
    athleteIDs : pandas dataframe
        Set of unique athlete IDs, unfiltered
    dfFiltered : pandas dataframe
        Contains a filtered dataframe (this is very generalized as this
        function is used in various parts of the code)
    
    Returns
    -------
    pandas dataframe
        Filtered dataset according to the athlete's ranking order and
        the number of athletes selected
    """

    if (filterArg == "-f"): # first X
        filteredAthleteIDs = athleteIDs[:numberOfAthletes]
    elif (filterArg == "-l"): # last X
        filteredAthleteIDs = athleteIDs[-numberOfAthletes:]
    elif (filterArg == "-r"): # random X
        filteredAthleteIDs = random.sample(list(athleteIDs), numberOfAthletes)
    elif (filterArg == "-s"): # THIS DOES NOT WORK
        filterSex = input("Qual é o sexo? M/F? NÃO TESTADO")
        
        dfFiltered = dfFiltered.loc[dfFiltered['sex'] == filterSex]
        athleteIDs = dfFiltered['inscription_athlete_athlete_id'].unique()

        # athleteIDs = filterArg['sex'] = filterSex
        filteredAthleteIDs = random.sample(list(athleteIDs), numberOfAthletes)

    elif (filterArg == "-e"): # THIS DOES NOT WORK
        filterEchelon = input("Qual é o escalão? NÃO TESTADO") # hard filter to create because it is mixed with sex

        dfFiltered = dfFiltered.loc[dfFiltered['echelon'] == filterEchelon]
        athleteIDs = dfFiltered['inscription_athlete_athlete_id'].unique()        

        #athleteIDs = filterArg['echelon'] = filterEchelon
        filteredAthleteIDs = random.sample(list(athleteIDs), numberOfAthletes)
    elif (filterArg == '-q'): # quartiles

        # fetch quartile settings in config.json
        configFile = main.getConfigSettings()

        firstQuartile = configFile.loc['firstQuartile', 'quartile-settings']
        secondQuartile = configFile.loc['secondQuartile', 'quartile-settings']
        thirdQuartile = configFile.loc['thirdQuartile', 'quartile-settings']

        # used to subtract the final result because we don't want the time and date of the competition
        # we want the time related to the duration of the competition
        startCompetitionTime = dfFiltered.CPTime.min()
        startCompetitionTime = pd.to_datetime(startCompetitionTime, format='%Y-%m-%d %H:%M:%S') # convert str to timestamp object

        # remove any records related to the starting point of the competition
        dfFiltered = clean_data.dropStartCPTimes(dfFiltered)

        # quartiles calculated only for the finish line
        dfFiltered = dfFiltered.loc[dfFiltered['checkpoint_order'] == dfFiltered.checkpoint_order.max()]

        # convert to datetime format, or otherwise the quantile() function will not work
        CPTimeDateTime = pd.to_datetime(dfFiltered['CPTime'])

        globalPerformanceQuartiles = CPTimeDateTime.quantile([float(firstQuartile), float(secondQuartile), float(thirdQuartile)])

        globalPerformanceQuartiles = globalPerformanceQuartiles - startCompetitionTime

        print(globalPerformanceQuartiles)

        #plot.plotQuartiles(globalPerformanceQuartiles)

        return globalPerformanceQuartiles

    else: # do not execute script
        print("Filtro desconhecido. Ler documentação.")
        sys.exit(1)
    
    return filteredAthleteIDs
