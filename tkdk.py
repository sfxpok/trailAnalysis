import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import random
from sklearn import datasets, linear_model
from statistics import mean

filterArg = sys.argv[1]
quantityArg = sys.argv[2]

# time must be in seconds
# distance must be in meters

# function for linear regression

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

# convert hh:mm:ss to seconds

def convertTimeToSeconds(checkPointTime):
    startTime = CPTimeInt64.hour[0]
    startTimeToMidnightInSeconds = 60*60*(24-startTime)

    startDay = CPTimeInt64.day[0]

    CPTimeSeconds = []

    for i in range(len(CPTimeInt64.day)):
        if (i > 0 and i < len(CPTimeInt64.day)) and (CPTimeInt64.day[i] != startDay):
            CPTimeSeconds.append(CPTimeInt64.hour[i] * 3600 + CPTimeInt64.minute[i] * 60 + CPTimeInt64.second[i] + startTimeToMidnightInSeconds) # hhmmss to seconds
        else:
            CPTimeSeconds.append(CPTimeInt64.hour[i] * 3600 + CPTimeInt64.minute[i] * 60 + CPTimeInt64.second[i])

    return CPTimeSeconds

def getFilter(dataSet = filterArg, numberOfAthletes = quantityArg):
    # import every athlete from a competition to a dataframe

    df = pd.read_csv('MIUT2014-2018_temposEdistancias.csv') # read CSV file
    athleteIDs = df['inscription_athlete_athlete_id'].unique()

    if (dataSet == "f"): # first X
        filteredAthleteIDs = athleteIDs[:quantityArg]
    elif (dataSet == "l"): # last X
        filteredAthleteIDs = athleteIDs[-quantityArg:]
    elif (dataSet == "r"): # random X
        filteredAthleteIDs = random.sample(athleteIDs, quantityArg)
    else:
        print("Filtro desconhecido. Ler documentação.")
        return # do not execute script


fetchAthleteIDs = input('Insire IDs dos atletas: ') # example: 115321, 123812, 251180
fetchAthleteIDs = fetchAthleteIDs.split(",")
fetchAthleteIDs = [x.strip(' ') for x in fetchAthleteIDs] # making sure there are no spaces

# MIUT2018 athlete IDs
# first 9 athletes
#fetchAthleteIDs = "116854,114564,115470,116624,115314,116859,116850,114977,115030"
# last 9 athletes
#fetchAthleteIDs = "114356,115780,114905,115542,115017,116825,115026,116419,115335"
# random 9 athletes
#fetchAthleteIDs = "115366,116078,116300,115656,114751,115403,114628,115201,116232"

df = pd.read_csv('MIUT2014-2018_temposEdistancias.csv') # read CSV file

for athlete in fetchAthleteIDs: # athletes over 24h on the competitive will have bad results @ see CPTimeSeconds
    
    print("### Processing athlete number: " + athlete + " ###")

    # NOTA: Podem haver atletas que não foram registados em alguns CPs

    tempAthleteData = df[df['inscription_athlete_athlete_id'] == int(athlete)]
    tempAthleteData.iloc[-1, tempAthleteData.columns.get_loc('checkpoint_order')] = 14

    CPTimeInt64 = pd.DatetimeIndex(tempAthleteData['CPTime']) # datatype conversion

    tempAthleteData['CPTimeSeconds'] = convertTimeToSeconds(CPTimeInt64)

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
    m, b = best_fit_slope_and_intercept(Xdist, Ytime)

    regression_line = [] # clean array, this is important
    regression_line = [(m*x)+b for x in Xdist]

    # scatter plot; X: distance traveled; Y: time passed
    fig, ax = plt.subplots()
    ax.scatter(Xdist, Ytime)
    ax.plot(Xdist, regression_line, color="red")
    ax.set_xlabel('distância percorrida')
    ax.set_ylabel('tempo passado')
    plt.savefig(athlete + '_xDistance_yTime')

    #plt.show()