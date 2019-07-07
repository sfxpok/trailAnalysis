import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

import filter_data

# time must be in seconds
# distance must be in meters

def createPlots(filteredAthleteIDs, df):
    """Generates a set of plots with linear regression after filtering
    a dataset with athletes
    
    Parameters
    ----------
    filteredAthleteIDs : list
        Athletes to generate plots with
    df : pandas dataframe
        Contains the already filtered data previously
    """

    # every athlete's plot is generated inside this for
    for athlete in filteredAthleteIDs:
    
        plt.clf() # clean plot

        print("### Processing athlete number: " + str(athlete) + " ###")

        # NOTA: Podem haver atletas que não foram registados em alguns CPs

        # usually the cleanDataToPlot()'s objective is to setup
        # a correct datatype for the checkpoint time
        tempAthleteData = cleanDataToPlot(1, athlete, df)

        # preparing data to calculate linear regression
        Xdist = tempAthleteData['distancia_acumulada']
        Ytime = tempAthleteData['CPTimeSeconds']
        #m, b = best_fit_slope_and_intercept(Xdist, Ytime)

        regression_line = filter_data.regressionLineCalculate(Xdist, Ytime)

        # scatter plot; X: distance traveled; Y: time passed
        ax = plt.subplot()
        ax.scatter(Xdist, Ytime)
        ax.plot(Xdist, regression_line, color="red")
        ax.set_xlabel('distância percorrida (metros)')
        ax.set_ylabel('tempo passado (segundos)')

        # the axis limits are determined accordingly to the dataset we are using,
        # hence the functions setXAxisLimits(), setYAxisLimits() and
        # getLongestCPTime()
        plt.xlim(setXAxisLimits(Xdist, 1), setXAxisLimits(Xdist, 0))
        plt.ylim(setYAxisLimits(Ytime, 1), getLongestCPTime(df))
        #plt.xlim(0, 120000)
        #plt.ylim(0, 120000)
        #plt.ylim(0, 80000)
        #plt.autoscale(enable=True)
        plt.savefig(str(athlete) + '_xDistance_yTime')

        #plt.show()

def getLongestCPTime(df):
    """Fetches the longest CPTime to define Y axis limits
    
    Parameters
    ----------
    df : pandas dataframe
        Contains an unfiltered dataset
    
    Returns
    -------
    integer
        Longest registered CPTime
    """


    dfLastAthlete = df.tail(1)
    dfLastAthlete = df[df['inscription_athlete_athlete_id'] == int(dfLastAthlete['inscription_athlete_athlete_id'])]

    #print(dfLastAthlete)

    longestCPTimeInt64 = pd.DatetimeIndex(dfLastAthlete['CPTime']) # datatype conversion
    
    #print(longestCPTimeInt64)
    
    longestCPTimeSeconds = filter_data.convertTimeToSeconds(longestCPTimeInt64)
    longestCPTimeSeconds = max(longestCPTimeSeconds)
    
    longestCPTimeSeconds += 5000 # give an additional space in the Y axis

    return longestCPTimeSeconds

# athleteOrCompetition set to 0 means the ID must be related to competition ID
# athleteOrCompetition set to 1 means the ID must be related to athlete ID
def cleanDataToPlot(athleteOrCompetition, ID, df):
    """Renames any checkpoint that is not ordered correctly and it
    converts CPTime's timestamp to seconds
    
    Parameters
    ----------
    athleteOrCompetition : integer
        Describes whether the data to be cleaned is related to an
        athlete or to a competition (the latter can be ignored)
    ID : integer
        ID corresponding to an athlete or a competition
    df : pandas dataframe
        Contains a filtered dataframe to be modified and cleaned
        according to the athlete/competition ID
    
    Returns
    -------
    pandas dataframe
        Modified dataframe that can be used to plot graphs
    """

    # at the state of this code, this if condition is never false
    if (athleteOrCompetition):
        athleteData = df[df['inscription_athlete_athlete_id'] == int(ID)]
    else:
        athleteData = df[df['Competition'] == int(ID)]
    
    athleteData.iloc[-1, athleteData.columns.get_loc('checkpoint_order')] = 14 # last checkpoint has got ID 99

    # convert to DatetimeIndex, important to convert to seconds later on
    CPTimeInt64 = pd.DatetimeIndex(athleteData['CPTime']) # datatype conversion

    # timestamp conversion to seconds
    CPTimeSeconds = filter_data.convertTimeToSeconds(CPTimeInt64)
    athleteData['CPTimeSeconds'] = CPTimeSeconds

    return athleteData

def getCompetitionLabel(competitionID):
    """Fetches a competition label, which is constituted by a name
    and a year
    
    Parameters
    ----------
    competitionID : integer
        Competition unique ID
    
    Returns
    -------
    string
        Contains a string with a competition name and year appear on plots legend
    """

    dfCompetition = pd.read_json("competitions.json", orient='columns')
    dfCompetition = dfCompetition.loc[dfCompetition['competition_id'] == int(competitionID)]
    competitionLabel = dfCompetition["name"] + " " + dfCompetition["year"].map(str)
    competitionLabel = competitionLabel.iloc[0]

    return competitionLabel

def getAdequateCompetitions(tempAthleteData): # THIS DOES NOT WORK
    tempCompetitionData = tempAthleteData.sort_values('distancia_mapa', ascending=False).drop_duplicates(['Competition'])
    tempCompetitionData = tempCompetitionData.drop(tempCompetitionData[tempCompetitionData.distancia_mapa < tempCompetitionData.distancia_mapa.max() - 1000].index)
    
    cond = tempAthleteData['Competition'].isin(tempCompetitionData['Competition']) == False
    tempAthleteData.drop(tempAthleteData[cond].index, inplace = True)

def multiplePlotting(filteredAthleteIDs, df): # ONLY WORKS FOR UNIQUE ATHLETE IDs

    Xdist = []
    Ytime = []

    for athlete in filteredAthleteIDs:

        print("### Processing competition number: " + str(athlete) + " ###")

        tempAthleteData = cleanDataToPlot(1, athlete, df)

        #getAdequateCompetitions(tempAthleteData)

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

def plotQuartiles(globalPerformanceQuartiles): # THIS DOES NOT WORK

    for val in globalPerformanceQuartiles.iteritems():
        print(val)

    test = globalPerformanceQuartiles.to_numpy()
    print(test)

    globalPerformanceQuartiles.plot(kind='box')


def setXAxisLimits(distance, getMinLimit):
    """Get distance (in meters) from the dataset. This distance is
    meant to set the X axis limit in the plots and it can either
    be the minimum or maximum distance
    
    Parameters
    ----------
    distance : pandas dataframe
        Set of distances throughout the checkpoints
    getMinLimit : bool
        0: Get maximum distance possible
        1: Get minimum distance possible
    
    Returns
    -------
    integer
        Maximum or minimum distance to be used as a limit in the X axis
        of a plot
    """

    if (getMinLimit):
        distance = distance.min()
    else:
        distance = distance.max()

    distanceDigits = len(str(abs(distance)))
    roundingDistancePrecision = distanceDigits - 1
    xDistanceAxisLimit = round(distance, roundingDistancePrecision) # i.e. round(116200, 4) = 120000

    # add a tiny bit of space for the plot if we need the maximum distance
    if (getMinLimit == False):
        xDistanceAxisLimit += 5000

    return xDistanceAxisLimit

def setYAxisLimits(CPTimeSeconds, getMinLimit):
    """Get CPTime (in seconds) from the dataset. This CPTime is
    meant to set the Y axis limit in the plots and it can either
    be the minimum or maximum CPTime
    
    Parameters
    ----------
    CPTimeSeconds : pandas dataframe
        Contains an athlete's checkpoint recorded times
    getMinLimit : bool
        0: Get maximum CPTime possible
        1: Get minimum CPTime possible
    
    Returns
    -------
    integer
        Maximum or minimum CPTime to be used as a limit in the Y axis
        of a plot
    """

    if (getMinLimit):
        CPTimeSeconds = CPTimeSeconds.min()
    else:
        CPTimeSeconds = CPTimeSeconds.max()

    CPTimeDigits = len(str(abs(CPTimeSeconds)))
    roundingCPTimePrecision = CPTimeDigits - 1
    yCPTimeAxisLimit = round(CPTimeSeconds, roundingCPTimePrecision)

    # add a tiny bit of space for the plot if we need the maximum CPTime
    if (getMinLimit == False):
        yCPTimeAxisLimit += 5000

    return yCPTimeAxisLimit

def getAthletesManually(): # WORKS BUT IT MUST BE USED MANUALLY
    filteredAthleteIDs = input('Insire IDs dos atletas: ') # example: 115321, 123812, 251180
    filteredAthleteIDs = filteredAthleteIDs.split(",")
    filteredAthleteIDs = [x.strip(' ') for x in filteredAthleteIDs] # making sure there are no spaces
