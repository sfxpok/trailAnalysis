from statistics import mean

# function for linear regression

def best_fit_slope_and_intercept(xs, ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

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
