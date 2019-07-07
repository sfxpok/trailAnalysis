#import MySQLdb # changed library to avoid python2
#import regular expression module
import re
import csv
import databaseCredentials
import mysql.connector # to download this: sudo pip3 install mysql-connector
import numpy as np

db_address = databaseCredentials.login['db_address']
username = databaseCredentials.login['username']
password = databaseCredentials.login['password']
db_name = databaseCredentials.login['db_name']

mydb = mysql.connector.connect(user=username, password=password,
                              host=db_address,
                              database=db_name)

cursor = mydb.cursor(buffered=True)

#mydb = MySQLdb.connect(db_address, username, password, db_name)
#cursor = mydb.cursor()

# Type         Table/View            Database    Column
# Table    athlete                    miut2014    athlete_id
# Table    athlete_gps                miut2014    athlete_id    no records
# Table    athlete_gps_competition    miut2014    athlete_id    no records
# Table    inscription                miut2014    inscription_id
# Table    inscription                miut2014    athlete_athlete_id
# Table    medical_data            miut2014    inscription_inscription_id
# Table    notification            miut2014    inscription_inscription_id    no records
# Table    notification            miut2014    athlete_id    no records
# Table    time_checkpoint            miut2014    inscription_athlete_athlete_id

# Find duplicate athletes (just one for now)
# Id of one athlete

def findAllDuplicateAthletes():
    """Returns any rows containing duplicate athletes in the database
    """

    arrayDuplicateAthletes = np.array([])
    arrayAthletesWithSmallestIDs = np.array([])

    # getDuplicateAthletes = ("SELECT a.* \
    #                               FROM athlete a \
    #                               JOIN \
    #                               (SELECT name, birthday, COUNT(*) \
    #                                   FROM athlete \
    #                                   GROUP BY name, birthday \
    #                                   HAVING COUNT(*) > 1) b \
    #                               ON a.name=b.name \
    #                               AND a.email=b.email \
    #                               AND a.birthday=b.birthday \
    #                               AND a.raking_name=b.raking_name \
    #                               AND a.raking_name_last=b.raking_name_last \
    #                               ORDER BY a.name \
    #                               ")

    # cursor.execute(getDuplicateAthletes)
    # arrayDuplicateAthletes = cursor.fetchall()

    getAthletesWithSmallestIDs = ("SELECT \
                              MIN(athlete_id), \
                              name, \
                              email, \
                              birthday, \
                              raking_name, \
                              raking_name_last \
                              FROM \
                              miuttest.athlete \
                              GROUP BY name, email, birthday, raking_name, raking_name_last \
                              HAVING COUNT(*) > 1 \
                              ")

    cursor.execute(getAthletesWithSmallestIDs)
    arrayAthletesWithSmallestIDs = cursor.fetchall()

    # conversion was necessary to do operations on the array
    arrayAthletesWithSmallestIDs = convertToNumPyArray(arrayAthletesWithSmallestIDs)

    #print (arrayAthletesWithSmallestIDs)

    for dupRow in arrayAthletesWithSmallestIDs:
        athleteToKeep = dupRow[1]
        #print("Nome de atleta: " + str(athleteToKeep) + "\n")

        # this if condition is only meant for parsing purposes with athletes
        # that contain a ' in their names
        if "'" in str(athleteToKeep):
            positionToAddApostrophe = str(athleteToKeep.find("'"))
            athleteToKeep = str(athleteToKeep)[:int(positionToAddApostrophe)] + "'" + str(athleteToKeep)[int(positionToAddApostrophe):]

        getSmallestAthleteID = ("SELECT MIN(athlete_id) AS SmallestAthleteID FROM athlete WHERE name = '%s'" % athleteToKeep)

        smallestAthleteID = runSQLQuery(getSmallestAthleteID)
        print("ID mínimo do atleta " + str(athleteToKeep) + " é: " + str(smallestAthleteID[0][0]) + "\n")
        #smallestAthleteID = np.array([4917])

        getAthleteIDsToDelete = ("SELECT athlete_id FROM athlete WHERE name = '%s' AND athlete_id NOT IN (%d)" % (athleteToKeep, smallestAthleteID[0][0]))
        athleteIDsToDelete = runSQLQuery(getAthleteIDsToDelete)

        if not athleteIDsToDelete:
            continue

        #athleteIDsToDelete = parseArrayToString(athleteIDsToDelete)
        
        updateDuplicateID(smallestAthleteID[0][0], athleteIDsToDelete)

        deleteDuplicateRows = ("DELETE FROM athlete WHERE name = '%s' AND athlete_id NOT IN (%d)" % (athleteToKeep, smallestAthleteID[0][0]))
        seeDeletedDuplicateRows = ("SELECT * FROM athlete WHERE name = '%s' AND athlete_id NOT IN (%d)" % (athleteToKeep, smallestAthleteID[0][0]))
        deleteTransaction(deleteDuplicateRows, seeDeletedDuplicateRows)

def writeToLog(message, exceptionFlag):
    """Writes a message error to a log
    
    Parameters
    ----------
    message : string
        Contains a SQL message
    exceptionFlag : integer
        If the flag is 1, it means there's an error
    """

    if (exceptionFlag):
        logFile = open("sqlexceptions.log", "a+")
        print("»»»»»»»»»»»» Ocorreu uma excepção: " + message + "\n")
    else:
        logFile = open("sqltransactions.log", "a+")
    
    logFile.write(message + "\n")
    logFile.close()

def executeTransaction(mydb, queryID):
    """Executes a given transaction. It can be either an UPDATE or
    DELETE query
    
    Parameters
    ----------
    mydb : database settings
        Contains settings regarding to the database being used
    queryID : integer
        If the ID is 0, it's an UPDATE query. If the ID is 1,
        it's a DELETE query
    """

    mydb.commit()

    if (queryID == 0):
        print ("########## Transacção feita. (UPDATE) ##########")
    elif (queryID == 1):
        print ("########## Transacção feita. (DELETE) ##########")

def updateTransaction(updateQuery, selectQuery):
    """Executes an UPDATE query and it's transaction
    
    Parameters
    ----------
    updateQuery : string
        UPDATE query
    selectQuery : string
        SELECT query
    """

    #print ("*** UPDATING THE FOLLOWING ROWS ***")

    #print (selectQuery + "\n")
    
    #try:
    cursor.execute(selectQuery)
    #except Exception as e:
        #writeToLog("MySQL error: %s" % str(e), 1)
    
    #updatedRows = cursor.fetchall()

    #displayRowsOnTerminal(updatedRows)

    #print (updateQuery + "\n")

    try:
        cursor.execute(updateQuery)
        writeToLog(updateQuery, 0)
    except Exception as e:
        writeToLog("MySQL error: %s" % str(e), 1)
        writeToLog(updateQuery, 0)

    executeTransaction(mydb, 0)
        
    #print ("*** UPDATE DONE ***")

def deleteTransaction(deleteQuery, selectQuery):
    """Executes a DELETE query and it's transaction
    
    Parameters
    ----------
    deleteQuery : string
        DELETE query
    selectQuery : string
        SELECT query
    """

    #print("*** DELETING THE FOLLOWING ROWS ***")

    try:
        cursor.execute(selectQuery)
    except Exception as e:
        writeToLog("MySQL error: %s" % str(e), 1)

    #deletedRows = cursor.fetchall()

    #displayRowsOnTerminal(deletedRows)

    try:
        cursor.execute(deleteQuery)
        writeToLog(deleteQuery, 0)
    except Exception as e:
        writeToLog("MySQL error: %s" % str(e), 1)
        writeToLog(deleteQuery, 0)

    executeTransaction(mydb, 1)

    #print ("*** DELETION DONE ***")

def updateDuplicateID(keepAthID, dupAthIDArray):
    """Executes various UPDATE transactions regarding the time checkpoints and
    ID inscriptions

    
    Parameters
    ----------
    keepAthID : integer
        Athlete ID to keep, usually means it is the smallest ID
    dupAthIDArray : integer
        Athlete IDs considered to be duplicates of the ID above (keepAthID)
    """

    stringWithIDsToUpdate = parseArrayToString(dupAthIDArray)

    #print ("STRINGWITHIDSTOUPDATE: " + stringWithIDsToUpdate)

    updateDupIDsinsc = "UPDATE inscription SET athlete_athlete_id = %d WHERE athlete_athlete_id IN (%s)" % (keepAthID, stringWithIDsToUpdate)
    updateDupIDstimecp = "UPDATE time_checkpoint SET inscription_athlete_athlete_id = %d WHERE inscription_athlete_athlete_id IN (%s)" % (keepAthID, stringWithIDsToUpdate)

    seeUpdatedDuplicateRows = "SELECT * FROM inscription WHERE athlete_athlete_id IN (%s)" % (stringWithIDsToUpdate)
    updateTransaction(updateDupIDsinsc, seeUpdatedDuplicateRows)

    seeUpdatedDuplicateRows = "SELECT * FROM time_checkpoint WHERE inscription_athlete_athlete_id IN (%s)" % (stringWithIDsToUpdate)
    updateTransaction(updateDupIDstimecp, seeUpdatedDuplicateRows)

def parseArrayToString(npArray):
    """Parses an array with athlete IDs to a string
    
    Parameters
    ----------
    npArray : NumPy array
        Contains a set of athlete IDs
    
    Returns
    -------
    string
        Contains a set of athlete IDs
    """

    stringWithID = ""

    for athleteID in npArray:
        stringWithID += str(athleteID[0]) + ", "

    stringWithID = stringWithID.rstrip(', ')

    #print ("STRINGWITHID: " + stringWithID)

    return stringWithID

def displayRowsOnTerminal(rowsToDisplay):
    """Only for output purposes of data related to an athlete
    
    Parameters
    ----------
    rowsToDisplay : array
        Athlete ID
    """

    for dbrow in rowsToDisplay:
        #print ("AthID=%d\tName=%s\temail=%s\tbirthdate=%s" % (dbrow[0], dbrow[1], dbrow[2], dbrow[3]))
        print ("AthID=%d\t" % (dbrow[0]))

def runSQLQuery(query):
    """Executes a SQL query
    
    Parameters
    ----------
    query : string
        SQL query
    
    Returns
    -------
    array
        Output of the result from the SQL query
    """


    cursor.execute(query)
    resultArray = cursor.fetchall()
    convertToNumPyArray(resultArray)

    return resultArray

def convertToNumPyArray(oldArray):
    """Converts an array to a NumPy array, meant to do other operations
    in an array
    
    Parameters
    ----------
    oldArray : array
        Array with athlete data
    
    Returns
    -------
    NumPy array
        NumPy array with athlete data
    """

    newArray = np.array(oldArray)

    return newArray

def findDupAthletes(athID):
    # With one ID, find athletes wit same name, NIF, CC...
    vQuery = ("SELECT * FROM athlete WHERE athlete_id = '%d'" % athID)
    cursor.execute(vQuery)
    results = cursor.fetchall()
    for dbrow in results:
        print ("AthID=%d\tName=%s\temail=%s\tbirthdate=%s" % (dbrow[0], dbrow[1], dbrow[2], dbrow[3]))
        print
        vQuery = ("SELECT * \
                FROM athlete \
                WHERE name like '%s' \
                ORDER BY athlete_id" % dbrow[1])
        cursor.execute(vQuery)
        athletes = cursor.fetchall()
        print ("Athletes found by name: %s" % cursor.rowcount)
        for dbathl in athletes:
            print ("AthID=%d\tName=%s\temail=%s\tbirthdate=%s" % (dbathl[0], dbathl[1], dbathl[2], dbathl[3]))

        vQuery = ("SELECT * FROM athlete WHERE birthday like '%s' ORDER BY athlete_id" % dbrow[3])
        cursor.execute(vQuery)
        athletes = cursor.fetchall()
        print ("Athletes found by birthdate: %s" % cursor.rowcount)
        for dbathl in athletes:
            print ("AthID=%d\tName=%s\temail=%s\tbirthdate=%s" % (dbathl[0], dbathl[1], dbathl[2], dbathl[3]))

    pass

def unifyDupAthletes (keepAthID, dupAthID):
    vQuery = ("START TRANSACTION ")
    # Update inscriptions
    #  change athlete_athlete_id

    # Update time_checkpoint
    #  change inscription_athlete_athlete_id


    pass

findAllDuplicateAthletes()
# findDupAthletes(5136)
# Event variables
cursor.close()
print ("Done")
