# -*- coding: utf-8 -*-
"""
app_lidarStrobeParser
"""
import logging
import glob
import time

DATA_START_LINE = 10
TS_LINE_NUMBER = 13
END_OF_FILE = "@"
LINE_ENDING = "\n"
TIME_DELIMETER = "."

def getFilesInFolder(pathToFolder, fileFormat):
    query = pathToFolder + "*." + fileFormat
    result = glob.glob(query)
    
    return result


def getStrobeValuesFromLine(line):
    line = line.strip()
    delimeterIndex = line.find("\t")
    first = int(line[0 : delimeterIndex])
    second= int(line[(delimeterIndex + 1) :])
  
    return (first, second)

def getDiffForStrobe(data, strobeNumber):
    curStrobe_first, curStrobe_second = getStrobeValuesFromLine(data[strobeNumber - 1])
    prevStrobe_first, prevStrobe_second = getStrobeValuesFromLine(data[strobeNumber - 2])
    diff_first = curStrobe_first - prevStrobe_first
    diff_second = curStrobe_second - prevStrobe_second
    
    return(diff_first, diff_second)

def convertTimeToDecimal(timeInStr):
    result = time.strptime(timeInStr, "%H:%M:%S")
    result = str(result[3]) + TIME_DELIMETER + str(int((result[4] * 60 / 3600)*100))
    return result

def dataFileHandle(inputFilepath):
    startTime = ""
    strobeDiffs_first = [0, 0, 0, 0]
    strobeDiffs_second = [0, 0, 0, 0]
    
    # Open file for reading
    f = open(inputFilepath, mode="r")#, newline="\r\n")
    
    # Read first dummy lines
    for i in range(0, 9, 1):
        f.readline()
    
    # Read time of start
    line = f.readline()
    startTime = line[(line.find("\t")):].strip()
        
    # Convert time to decimal format
    startTime = convertTimeToDecimal(startTime)
    
    # Read two dummy lines
    f.readline()
    f.readline()
    
    # Read all meanings lines 
    data = f.readlines()
    
    strobeDiffs_first[0], strobeDiffs_second[0] = getDiffForStrobe(data, 500)
    strobeDiffs_first[1], strobeDiffs_second[1] = getDiffForStrobe(data, 1000)
    strobeDiffs_first[2], strobeDiffs_second[2] = getDiffForStrobe(data, 1500)
    strobeDiffs_first[3], strobeDiffs_second[3] = getDiffForStrobe(data, 2000)
    
    # Close file
    f.close()
    
    return (startTime, strobeDiffs_first, strobeDiffs_second)

def getFilename(prefix, strobe, channel):
    return prefix + "_" + str(strobe) + "_" + str(channel) + ".txt"

def appendResultsToFile(path, name, time, diff):
    f = open(path + name, mode='a')
    f.write(str(time))
    f.write("\t")
    f.write(str(diff))
    f.write(LINE_ENDING)

def routineOverAllFilesInPath(path, outputPath, prefix):
    logging.log(logging.DEBUG, "Routine over all files is started")
    
    # Get list of the files
    dataFiles = getFilesInFolder(path, "dat")  
    
    # Processing all files 
    for dataFile in dataFiles:
        logging.log(logging.DEBUG, " + Processing file > " + dataFile)
        # Get time and diffs
        time, diff_first, diff_second = dataFileHandle(dataFile)
        # Form output files
        # First channel
        appendResultsToFile(outputPath, getFilename(prefix, 500, 1), time, diff_first[0]);
        appendResultsToFile(outputPath, getFilename(prefix, 1000, 1), time, diff_first[1]);
        appendResultsToFile(outputPath, getFilename(prefix, 1500, 1), time, diff_first[2]);
        appendResultsToFile(outputPath, getFilename(prefix, 2000, 1), time, diff_first[3]);
        # Second channel
        appendResultsToFile(outputPath, getFilename(prefix, 500, 2), time, diff_second[0]);
        appendResultsToFile(outputPath, getFilename(prefix, 1000, 2), time, diff_second[1]);
        appendResultsToFile(outputPath, getFilename(prefix, 1500, 2), time, diff_second[2]);
        appendResultsToFile(outputPath, getFilename(prefix, 2000, 2), time, diff_second[3]);
    
    logging.log(logging.DEBUG, "Routine over all files is ended")    
    
if __name__== "__main__":
    logging.basicConfig()
    routineOverAllFilesInPath(".\\samples\\", ".\\output\\", "test")