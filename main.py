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

    dfOrdered = df.drop(df[df.distancia_mapa != df['distancia_mapa'].max()].index)
    athleteIDs = dfOrdered['inscription_athlete_athlete_id'].unique()

    if args.quart:
        io_op.writeToCSVFile(filter_data.getFilter('-q', 0, athleteIDs, df, 0), filterCompetition, filterYearComp)

    if args.reglin:

        if not (args.first or args.last or args.random):
            print("Está em falta um argumento referente à ordem dos atletas. A sair do programa...")
            sys.exit(1)

        numOfAthletes = getNumberOfAthletes()
        typeOfOrder = getTypeOfOrder()
        plot.createPlots(filter_data.getFilter(typeOfOrder, numOfAthletes, athleteIDs, df, 0), df)

    sys.exit(0) # shut down

def getTypeOfOrder():
    args = getArgs()

    if args.first:
        typeOfOrder = '-f'
    elif args.last:
        typeOfOrder = '-l'
    elif args.random:
        typeOfOrder = '-r'

    return typeOfOrder

def getConfigSettings():
    configFile = pd.read_json("config.json")

    return configFile

def getDataSet():
    configFile = getConfigSettings()

    df = pd.read_csv(configFile.loc['csvfile', 'csv-settings']) # read CSV file

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
        print('Algo correu mal na leitura dos argumentos. A sair do programa...')
        sys.exit(1)

if __name__ == '__main__':
    main()
