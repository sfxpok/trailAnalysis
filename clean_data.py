def dropStartCPTimes(df):
    df = df.drop(df[df.checkpoint_order == 0].index)

    return df

def createParticipation(filteredAthleteIDs, df): # only meant for multiplePlotting()

    participationsArray = []