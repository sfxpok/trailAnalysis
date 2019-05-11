import random
import sys
import pandas as pd
from statistics import mean

import clean_data, main

# function for linear regression

def best_fit_slope_and_intercept(xs, ys):

    try:
        m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
            ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
        b = mean(ys) - m*mean(xs)
    
        return m, b
        
    except ZeroDivisionError:
        print("Divisão por zero no cálculo da regressão linear.")
        sys.exit(1)

def regressionLineCalculate(X, Y):

    m, b = best_fit_slope_and_intercept(X, Y)

    regression_line = [] # clean array, this is important
    regression_line = [(m*x)+b for x in X]

    return regression_line

# convert hh:mm:ss to seconds

def convertTimeToSeconds(checkPointTime):
    startTime = checkPointTime.hour[0]
    startTimeToMidnightInSeconds = 60*60*(24-startTime)

    startDay = checkPointTime.day[0]

    CPTimeSeconds = []

    for i in range(len(checkPointTime.day)):
        if (i > 0 and i < len(checkPointTime.day)) and (checkPointTime.day[i] != startDay):
            CPTimeSeconds.append(checkPointTime.hour[i] * 3600 + checkPointTime.minute[i] * 60 + checkPointTime.second[i] + startTimeToMidnightInSeconds) # hhmmss to seconds
        else:
            CPTimeSeconds.append(checkPointTime.hour[i] * 3600 + checkPointTime.minute[i] * 60 + checkPointTime.second[i])

    return CPTimeSeconds

def competitionFilter(df, competitionName, competitionYear):

    dfCompetition = pd.read_json("competitions.json", orient='columns')
    
    dfCompetition['year'] = dfCompetition['year'].astype(int)
    competitionYear = int(competitionYear)

    dfCompetition = dfCompetition.loc[(dfCompetition['name'] == str.upper(competitionName)) | (dfCompetition['name'] == str.capitalize(competitionName))]
    dfCompetition = dfCompetition.loc[dfCompetition['year'] == competitionYear]

    fetchCompetition = int(dfCompetition['competition_id'])
    
    #df = df.query('competition_id == fetchCompetition')
    df = df[df.Competition == fetchCompetition]

    return df

def createOrderedBoard(df): # change this name

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

#def cleanAthleteID():
#    oldID = 
#    newID = 
#
#    df.loc[df.inscription_athlete_athlete_id == 1304, 'inscription_athlete_athlete_id'] = 116659
#    df.loc[df['inscription_athlete_athlete_id'] == 1304]

def getFilter(filterArg, numberOfAthletes, athleteIDs, dfFiltered, df):
    # import every athlete from a competition to a dataframe
    if (filterArg == "-f"): # first X
        #createOrderedBoard(df) to be tested
        filteredAthleteIDs = athleteIDs[:numberOfAthletes]
    elif (filterArg == "-l"): # last X
        filteredAthleteIDs = athleteIDs[-numberOfAthletes:]
    elif (filterArg == "-r"): # random X
        filteredAthleteIDs = random.sample(list(athleteIDs), numberOfAthletes)
    elif (filterArg == "-s"): # M or F?
        filterSex = input("Qual é o sexo? M/F? NÃO TESTADO")
        
        dfFiltered = dfFiltered.loc[dfFiltered['sex'] == filterSex]
        athleteIDs = dfFiltered['inscription_athlete_athlete_id'].unique()

        # athleteIDs = filterArg['sex'] = filterSex
        filteredAthleteIDs = random.sample(list(athleteIDs), numberOfAthletes)

    elif (filterArg == "-e"): # which echelon?
        filterEchelon = input("Qual é o escalão? NÃO TESTADO") # hard filter to create because it is mixed with sex

        dfFiltered = dfFiltered.loc[dfFiltered['echelon'] == filterEchelon]
        athleteIDs = dfFiltered['inscription_athlete_athlete_id'].unique()        

        #athleteIDs = filterArg['echelon'] = filterEchelon
        filteredAthleteIDs = random.sample(list(athleteIDs), numberOfAthletes)
    elif (filterArg == '-q'): # quartiles

        configFile = main.getConfigSettings()

        firstQuartile = configFile.loc['firstQuartile', 'quartile-settings']
        secondQuartile = configFile.loc['secondQuartile', 'quartile-settings']
        thirdQuartile = configFile.loc['thirdQuartile', 'quartile-settings']

        dfFiltered = clean_data.dropStartCPTimes(dfFiltered)
        CPTimeDateTime = pd.to_datetime(dfFiltered['CPTime'])

        globalPerformanceQuartiles = CPTimeDateTime.quantile([float(firstQuartile), float(secondQuartile), float(thirdQuartile)])
        print(globalPerformanceQuartiles)

        return globalPerformanceQuartiles

    else: # do not execute script
        print("Filtro desconhecido. Ler documentação.")
        sys.exit(1)
    
    return filteredAthleteIDs
