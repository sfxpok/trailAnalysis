import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets, linear_model
from statistics import mean

# time must be in seconds
# distance must be in meters

# function for linear regression

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

#athleteData = np.genfromtxt('andris_disttime.csv', names=True, dtype=None, delimiter=',')
#athleteData[0][4][11:] <--- DATETIME COLUMN WITH TIME ONLY

fetchAthleteIDs = input('Insire IDs dos atletas: ') # example: 115321, 123812, 251180
fetchAthleteIDs = fetchAthleteIDs.split(",")
fetchAthleteIDs = [x.strip(' ') for x in fetchAthleteIDs] # making sure there are no spaces

df = pd.read_csv('MIUT2014-2018_temposEdistancias.csv') # read CSV file

#cptimeSeconds = df.CPTime.str[11:]

CPTimeInt64 = pd.DatetimeIndex(df['CPTime']) # datatype conversion
CPTimeSeconds = CPTimeInt64.hour * 3600 + CPTimeInt64.minute * 60 + CPTimeInt64.second # hhmmss to seconds

dfModified = df # keeping original data intact
dfModified['CPTimeSeconds'] = CPTimeSeconds
# dfModified['checkpoint_order'][14] = 14 # last checkpoint ID is 99 on the database

for athlete in fetchAthleteIDs:
    
    tempAthleteData = dfModified[dfModified['inscription_athlete_athlete_id'] == int(athlete)]
    tempAthleteData.iloc[14, tempAthleteData.columns.get_loc('checkpoint_order')] = 14

    # line plot; X: CP number; Y: time passed
    fig, ax = plt.subplots()
    ax.plot(tempAthleteData['checkpoint_order'], tempAthleteData['CPTimeSeconds'])
    ax.set_xlabel('número do CP')
    ax.set_ylabel('tempo passado')
    plt.savefig(athlete + '_xCPnum_yTime')
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