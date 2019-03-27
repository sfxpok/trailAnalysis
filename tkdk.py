import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import random
from sklearn import datasets, linear_model

import filter

# time must be in seconds
# distance must be in meters

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

def getFilter(filterArg, numberOfAthletes, athleteIDs, dfFiltered):
    # import every athlete from a competition to a dataframe
    if (filterArg == "-f"): # first X
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
    else: # do not execute script
        print("Filtro desconhecido. Ler documentação.")
        sys.exit(1)
    
    return filteredAthleteIDs

def createPlots(filteredAthleteIDs, df):

    for athlete in filteredAthleteIDs:
    
        plt.clf() # clean plot

        print("### Processing athlete number: " + str(athlete) + " ###")

        # NOTA: Podem haver atletas que não foram registados em alguns CPs

        tempAthleteData = cleanDataToPlot(athlete, df)

        #tempAthleteData = df[df['inscription_athlete_athlete_id'] == int(athlete)]
        #tempAthleteData.iloc[-1, tempAthleteData.columns.get_loc('checkpoint_order')] = 14

        #CPTimeInt64 = pd.DatetimeIndex(tempAthleteData['CPTime']) # datatype conversion

        #tempAthleteData['CPTimeSeconds'] = convertTimeToSeconds(CPTimeInt64)

        # line plot; X: CP number; Y: time passed
        #fig, ax = plt.subplots()
        #ax.plot(tempAthleteData['checkpoint_order'], tempAthleteData['CPTimeSeconds'])
        #ax.set_xlabel('número do CP')
        #ax.set_ylabel('tempo passado')
        #plt.savefig(athlete + '_xCPnum_yTime')
        #plt.plot()

        # preparing data to calculate linear regression
        Xdist = tempAthleteData['distancia_acumulada']
        Ytime = tempAthleteData['CPTimeSeconds']
        #m, b = best_fit_slope_and_intercept(Xdist, Ytime)

        #regression_line = [] # clean array, this is important
        #regression_line = [(m*x)+b for x in Xdist]

        regression_line = regressionLineCalculate(Xdist, Ytime)


        # scatter plot; X: distance traveled; Y: time passed
        ax = plt.subplot()
        ax.scatter(Xdist, Ytime)
        ax.plot(Xdist, regression_line, color="red")
        ax.set_xlabel('distância percorrida')
        ax.set_ylabel('tempo passado')
        plt.xlim(0, 120000)
        plt.ylim(0, 80000)
        plt.savefig(str(athlete) + '_xDistance_yTime')

        #plt.show()

def cleanDataToPlot(athleteID, df):
    athleteData = df[df['inscription_athlete_athlete_id'] == int(athleteID)]
    athleteData.iloc[-1, athleteData.columns.get_loc('checkpoint_order')] = 14

    CPTimeInt64 = pd.DatetimeIndex(athleteData['CPTime']) # datatype conversion

    athleteData['CPTimeSeconds'] = convertTimeToSeconds(CPTimeInt64)

    return athleteData

def regressionLineCalculate(X, Y):

    m, b = best_fit_slope_and_intercept(X, Y)

    regression_line = [] # clean array, this is important
    regression_line = [(m*x)+b for x in X]

    return regression_line

def getCompetitionLabel(competitionID):

    dfCompetition = pd.read_json("competitions.json", orient='columns')
    dfCompetition = dfCompetition.loc[dfCompetition['competition_id'] == int(competitionID)]
    competitionLabel = dfCompetition["name"] + " " + dfCompetition["year"].map(str)
    competitionLabel = competitionLabel.iloc[0]

    return competitionLabel

def multiplePlotting(filteredAthleteIDs, df):

    Xdist = []
    Ytime = []

    for athlete in filteredAthleteIDs:

        print("### Processing athlete number: " + str(athlete) + " ###")

        tempAthleteData = cleanDataToPlot(athlete, df)

        Xdist = tempAthleteData['distancia_acumulada']
        Ytime = tempAthleteData['CPTimeSeconds']
        competitionID = tempAthleteData.iloc[0]['Competition']

        regression_line = regressionLineCalculate(Xdist, Ytime)
        competitionLabel = getCompetitionLabel(competitionID)

        ax = plt.subplot()
        ax.scatter(Xdist, Ytime, label = competitionLabel)
        ax.plot(Xdist, regression_line)
        ax.set_xlabel('distância percorrida')
        ax.set_ylabel('tempo passado')
        plt.xlim(0, 120000)
        plt.ylim(0, 80000)

    plt.legend()
    plt.savefig("testingMultPlot")
    plt.show()


def getAthletesManually():
    filteredAthleteIDs = input('Insire IDs dos atletas: ') # example: 115321, 123812, 251180
    filteredAthleteIDs = filteredAthleteIDs.split(",")
    filteredAthleteIDs = [x.strip(' ') for x in filteredAthleteIDs] # making sure there are no spaces

# MIUT2018 athlete IDs
# first 9 athletes
#filteredAthleteIDs = "116854,114564,115470,116624,115314,116859,116850,114977,115030"
# last 9 athletes
#filteredAthleteIDs = "114356,115780,114905,115542,115017,116825,115026,116419,115335"
# random 9 athletes
#filteredAthleteIDs = "115366,116078,116300,115656,114751,115403,114628,115201,116232"