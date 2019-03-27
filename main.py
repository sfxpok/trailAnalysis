import pandas as pd
import sys

import filter, plot

def main():

    configfile = pd.read_json("config.json")

    df = pd.read_csv(configfile.loc[0, 'csvfile']) # read CSV file

    filterCompetition = input("Qual é a competição? MIUT/ULTRA/Marathon/Mini")
    filterYearComp = input("Qual é o ano da competição?")
    
    df = filter.competitionFilter(df, filterCompetition, filterYearComp)

    athleteIDs = df['inscription_athlete_athlete_id'].unique()

    if len(sys.argv) == 1:
        quantityArg = input('Quantos atletas?: ')
        plot.createPlots(filter.getFilter('-r', int(quantityArg), athleteIDs, df), df)
    else:
        filterArg = sys.argv[1]
        quantityArg = int(sys.argv[2])
        plot.createPlots(filter.getFilter(filterArg, quantityArg, athleteIDs, df), df)

if __name__ == '__main__':
    main()
