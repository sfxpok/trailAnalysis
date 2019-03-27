import pandas as pd
import sys

import tkdk, filter

def main():

    csvfile = pd.read_json("config.json")

    df = pd.read_csv(csvfile.loc[0, 'csvfile']) # read CSV file

    filterCompetition = input("Qual é a competição? MIUT/ULTRA/Marathon/Mini")
    filterYearComp = input("Qual é o ano da competição?")
    
    df = tkdk.competitionFilter(df, filterCompetition, filterYearComp)

    athleteIDs = df['inscription_athlete_athlete_id'].unique()

    if len(sys.argv) == 1:
        quantityArg = input('Quantos atletas?: ')
        tkdk.createPlots(tkdk.getFilter('-r', int(quantityArg), athleteIDs, df), df)
    else:
        filterArg = sys.argv[1]
        quantityArg = int(sys.argv[2])
        tkdk.createPlots(tkdk.getFilter(filterArg, quantityArg, athleteIDs, df), df)

if __name__ == '__main__':
    main()
