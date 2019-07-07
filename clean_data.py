def dropStartCPTimes(df):
    """Removes any rows containing the starting point of a competition
    
    Parameters
    ----------
    df : pandas dataframe
        contains the imported dataset from the CSV file
    
    Returns
    -------
    pandas dataframe
        imported dataset from the CSV file but without rows of the
        starting point of a competition
    """

    df = df.drop(df[df.checkpoint_order == 0].index)

    return df

def createParticipation(filteredAthleteIDs, df): # THIS DOES NOT WORK

    participationsArray = []