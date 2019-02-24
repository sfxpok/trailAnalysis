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

df = pd.read_csv('andris_disttime.csv') # read CSV file

#cptimeSeconds = df.CPTime.str[11:]

CPTimeInt64 = pd.DatetimeIndex(df['CPTime']) # datatype conversion
CPTimeSeconds = CPTimeInt64.hour * 3600 + CPTimeInt64.minute * 60 + CPTimeInt64.second # hhmmss to seconds

dfModified = df # keeping original data intact
dfModified['CPTimeSeconds'] = CPTimeSeconds
dfModified['checkpoint_order'][14] = 14 # last checkpoint ID is 99 on the database

# line plot; X: CP number; Y: time passed
fig, ax = plt.subplots()
ax.plot(dfModified['checkpoint_order'], dfModified['CPTimeSeconds'])
plt.plot()

# preparing data to calculate linear regression
Xdist = dfModified['distancia_acumulada']
Ytime = dfModified['CPTimeSeconds']
m, b = best_fit_slope_and_intercept(Xdist, Ytime)

regression_line = [] # clean array, this is important
regression_line = [(m*x)+b for x in Xdist]

# scatter plot; X: distance traveled; Y: time passed
fig, ax = plt.subplots()
ax.scatter(Xdist, Ytime)
ax.plot(Xdist, regression_line, color="red")
plt.show()