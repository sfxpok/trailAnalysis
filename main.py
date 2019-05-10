import pandas as pd
import sys
import argparse

import filter_data, plot, io_op

def main():
    args = getArgs()

    df = getDataSet()

    filterCompetition = input("Qual é a competição? MIUT/ULTRA/Marathon/Mini\n")
    filterYearComp = input("Qual é o ano da competição?\n")
    
    df = filter_data.competitionFilter(df, filterCompetition, filterYearComp)

    athleteIDs = df['inscription_athlete_athlete_id'].unique()

    if args.quart:
        io_op.writeToCSVFile(filter_data.getFilter('-q', 0, athleteIDs, df, 0), filterCompetition, filterYearComp)

    if args.reglin:
        numOfAthletes = getNumberOfAthletes()
        typeOfOrder = getTypeOfOrder()
        plot.createPlots(filter_data.getFilter(typeOfOrder, numOfAthletes, athleteIDs, df), df)

    sys.exit(0) # shut down

def getTypeOfOrder():
    if args.first:
        typeOfOrder = 'f'
    elif args.last:
        typeOfOrder = 'l'
    elif args.random:
        typeOfOrder = 'r'

    return chr(typeOfOrder)

def getDataSet():
    configfile = pd.read_json("config.json")

    df = pd.read_csv(configfile.loc[0, 'csvfile']) # read CSV file

    return df

def getNumberOfAthletes():
    numOfAthletes = input('Quantos atletas?: ')

    return int(numOfAthletes)

def getArgs():

    parser = argparse.ArgumentParser(description='Projeto Análise de Dados de Trails 2019')
    parser.add_argument('-reglin', action='store_true', help='regressão linear (best-fit)')
    parser.add_argument('-quart', action='store_true', help='quartis')

    parser.add_argument('-first', action='store_true', help='primeiros X atletas classificados')
    parser.add_argument('-last', action='store_true', help='últimos X atletas classificados')
    parser.add_argument('-random', action='store_true', help='X atletas aleatórios')
    
    try:
        return parser.parse_args()
    except IOError:
        parser.error(str(msg))
    #args.method(**vars(args))

    #if not (args.process or args.upload):
        #parser.error('No action requested.')

if __name__ == '__main__':
    #getArgs()
    main()
