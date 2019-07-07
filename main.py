import pandas as pd
import sys
import argparse

import filter_data, plot, io_op

def main():
    """Main function of the program, it checks which argument was
    picked and it collects the dataset chosen in the config file
    """

    args = getArgs()

    df = getDataSet()

    if args.multRuns: # THIS IS NOT WORKING

        athleteIDsVariousComps = []
        insertingData = 1

        while (insertingData):
            athleteID = int(input("Insira o ID do atleta com várias participações (insire 0 para terminar a inserção)\n"))

            if athleteID != 0:
                athleteIDsVariousComps.append(athleteID)
            else:
                insertingData = 0

        plot.multiplePlotting(athleteIDsVariousComps, df)
        sys.exit(0) # shut down

    filterCompetition = input("Qual é a competição? MIUT/ULTRA/Marathon/Mini\n")
    filterYearComp = input("Qual é o ano da competição?\n")
    
    df = filter_data.competitionFilter(df, filterCompetition, filterYearComp)

    dfOrdered = df.drop(df[df.distancia_mapa != df['distancia_mapa'].max()].index)
    athleteIDs = dfOrdered['inscription_athlete_athlete_id'].unique()

    if args.quart:
        
        # initial dataset goes through a set of filters, but the second
        # and fifth argument in the function getFilter() do not matter
        # for this method of analysis
        dfFiltered = filter_data.getFilter('-q', None, athleteIDs, df)

        # outputs a csv file with the results of the quartiles
        io_op.writeToCSVFile(dfFiltered, filterCompetition, filterYearComp)

    if args.reglin:
        if not (args.first or args.last or args.random):
            print("Está em falta um argumento referente à ordem dos atletas. A sair do programa...")
            sys.exit(1)

        # fetches number of athletes through a user input
        numOfAthletes = getNumberOfAthletes()

        # fetches type of ranking order
        typeOfOrder = getTypeOfOrder()

        # generates plots with linear regression
        dfFiltered = filter_data.getFilter(typeOfOrder, numOfAthletes, athleteIDs, df)
        plot.createPlots(dfFiltered, df)

    sys.exit(0) # shut down, everything is done

def getTypeOfOrder():
    """Verifies chosen argument to order the dataset of athletes
    
    Returns
    -------
    typeOfOrder
        flag with the set of ordered ranked athletes
    """

    # fetches input arguments before runtime to get the order of
    # ranked athletes
    args = getArgs()

    if args.first:
        typeOfOrder = '-f'
    elif args.last:
        typeOfOrder = '-l'
    elif args.random:
        typeOfOrder = '-r'

    return typeOfOrder

def getConfigSettings():
    """Fetches and loads configuration parameters from a file (config.json)
    
    Returns
    -------
    configFile
        loaded configuration data from config.json
    """

    configFile = pd.read_json("config.json")

    return configFile

def getDataSet():
    """Imports and loads a CSV file as a dataset to be analyzed
    
    Returns
    -------
    df
        a pandas dataframe with the whole file's data
    """

    configFile = getConfigSettings()

    # reads a configured CSV file in the config.json file settings
    df = pd.read_csv(configFile.loc['csvfile', 'csv-settings'])

    return df

def getNumberOfAthletes():
    """Sends a prompt to the terminal and waits for an integer input
    corresponding to the amount of athletes to analyze
    
    Returns
    -------
    numOfAthletes
        number of athletes to analyze
    """

    numOfAthletes = input('Quantos atletas?: ')

    return int(numOfAthletes) # it must return the number of athletes as an integer

def getArgs():
    """Parses any given argument and stores them to be used later on
    
    Returns
    -------
    parse_args()
        keeps any given arguments stored during runtime
    """

    parser = argparse.ArgumentParser(description='Projeto Análise de Dados de Trails 2019')
    parser.add_argument('-reglin', action='store_true', help='regressão linear (best-fit)')
    parser.add_argument('-quart', action='store_true', help='quartis')

    parser.add_argument('-first', action='store_true', help='primeiros X atletas classificados')
    parser.add_argument('-last', action='store_true', help='últimos X atletas classificados')
    parser.add_argument('-random', action='store_true', help='X atletas aleatórios')

    parser.add_argument('-multRuns', action='store_true', help='atleta com várias participações (método: reg. linear)')
    
    try:
        return parser.parse_args()
    except IOError:
        print('Algo correu mal na leitura dos argumentos. A sair do programa...')
        sys.exit(1)

if __name__ == '__main__':
    main()
