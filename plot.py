import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

import filter_data

# time must be in seconds
# distance must be in meters

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

        regression_line = filter_data.regressionLineCalculate(Xdist, Ytime)


        # scatter plot; X: distance traveled; Y: time passed
        ax = plt.subplot()
        ax.scatter(Xdist, Ytime)
        ax.plot(Xdist, regression_line, color="red")
        ax.set_xlabel('distância percorrida (metros)')
        ax.set_ylabel('tempo passado (segundos)')
        plt.xlim(setXAxisLimits(Xdist, 1), setXAxisLimits(Xdist, 0))
        plt.ylim(setYAxisLimits(Ytime, 1), getLongestCPTime(df))
        #plt.xlim(0, 120000)
        #plt.ylim(0, 120000)
        #plt.ylim(0, 80000)
        #plt.autoscale(enable=True)
        plt.savefig(str(athlete) + '_xDistance_yTime')

        #plt.show()

def getLongestCPTime(df):
    dfLastAthlete = df.tail(1)
    dfLastAthlete = df[df['inscription_athlete_athlete_id'] == int(dfLastAthlete['inscription_athlete_athlete_id'])]

    print(dfLastAthlete)

    longestCPTimeInt64 = pd.DatetimeIndex(dfLastAthlete['CPTime']) # datatype conversion
    
    print(longestCPTimeInt64)
    
    longestCPTimeSeconds = filter_data.convertTimeToSeconds(longestCPTimeInt64)
    longestCPTimeSeconds = max(longestCPTimeSeconds)
    
    longestCPTimeSeconds += 5000 # give an additional space in the Y axis

    return longestCPTimeSeconds

def cleanDataToPlot(athleteID, df):
    athleteData = df[df['inscription_athlete_athlete_id'] == int(athleteID)]
    athleteData.iloc[-1, athleteData.columns.get_loc('checkpoint_order')] = 14 # last checkpoint has got ID 99

    CPTimeInt64 = pd.DatetimeIndex(athleteData['CPTime']) # datatype conversion

    CPTimeSeconds = filter_data.convertTimeToSeconds(CPTimeInt64)
    athleteData['CPTimeSeconds'] = CPTimeSeconds

    return athleteData

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

        regression_line = filter_data.regressionLineCalculate(Xdist, Ytime)
        competitionLabel = getCompetitionLabel(competitionID)

        ax = plt.subplot()
        ax.scatter(Xdist, Ytime, label = competitionLabel)
        ax.plot(Xdist, regression_line)
        ax.set_xlabel('distância percorrida (metros)')
        ax.set_ylabel('tempo passado (segundos)')        
        plt.xlim(0, 120000)
        plt.ylim(0, 80000)

    plt.legend()
    plt.savefig("testingMultPlot")
    plt.show()

def setXAxisLimits(distance, getMinLimit):
    # x axis limit: max distance (in meters) from the dataset

    if (getMinLimit):
        distance = distance.min()
    else:
        distance = distance.max()

    distanceDigits = len(str(abs(distance)))
    roundingDistancePrecision = distanceDigits - 1
    xDistanceAxisLimit = round(distance, roundingDistancePrecision) # i.e. round(116200, 4) = 120000

    if (getMinLimit == False):
        xDistanceAxisLimit += 5000

    return xDistanceAxisLimit

def setYAxisLimits(CPTimeSeconds, getMinLimit):
    # y axis limit: max time (in seconds) from the dataset

    if (getMinLimit):
        CPTimeSeconds = CPTimeSeconds.min()
    else:
        CPTimeSeconds = CPTimeSeconds.max()

    CPTimeDigits = len(str(abs(CPTimeSeconds)))
    roundingCPTimePrecision = CPTimeDigits - 1
    yCPTimeAxisLimit = round(CPTimeSeconds, roundingCPTimePrecision)

    if (getMinLimit == False):
        yCPTimeAxisLimit += 5000

    return yCPTimeAxisLimit


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