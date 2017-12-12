# -*- coding: utf-8 -*-
"""
app_lidarStrobeParser
"""
import logging
import glob

DATA_START_LINE = 10
TS_LINE_NUMBER = 13
END_OF_FILE = "@"

def getFilesInFolder(pathToFolder, fileFormat):
    result = []
    quiery = ""
    
    query = pathToFolder + "*." + fileFormat
    result = glob.glob(pathToFolder + "*." + fileFormat)
    
    return result

def getStrobeDiffsFromFile(pathToFile, strobeNumbers):
    result = []
    
    return result

def timeFromFile():
    result = ""
    
    return result

def dataFileHandle(inputFilepath):
    startTime = ""
    strobeDiffs_first = []
    strobeDiffs_second = []
    
    # Open file for reading
    f = open(inputFilepath, mode="r")#, newline="\r\n")
    
    # Read first dummy lines
    for i in range(0, 9, 1):
        f.readline()
    
    # Read time of start
    line = f.readline()
    startTime = line[(line.find("\t")):].lstrip().rstrip()
        
    # Convert time to decimal format
    
    # Read two dummy lines
    f.readline()
    f.readline()
    
    # Read data for strobes diffs
    print(f.readline())
    
    # Close file
    f.close()
    
    return (startTime, strobeDiffs_first, strobeDiffs_second)


def routineOverAllFilesInPath(path, outputPath, prefix):
    logging.log(logging.DEBUG, "Routine over all files is started")
    
    # Get list of the files
    dataFiles = getFilesInFolder(path, "dat")
    print(dataFiles)
    
    
    # Processing all files
    for dataFile in dataFiles:
        logging.log(logging.DEBUG, " + Processing file > " + dataFile)
        dataFileHandle(dataFile)

    logging.log(logging.DEBUG, "Routine over all files is ended")    

if __name__== "__main__":
    logging.basicConfig()
    routineOverAllFilesInPath(".\\samples\\", ".\\output\\", "test")