# -*- coding: utf-8 -*-
"""
app_lidarStrobeParser
"""
import glob
import time
import tkinter as tk
from tkinter import filedialog

DATA_START_LINE = 10
TS_LINE_NUMBER = 13
END_OF_FILE = "@"
LINE_ENDING = "\n"
TIME_DELIMETER = "."

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        # Define frame size and position in the screen :
        ScreenSizeX = master.winfo_screenwidth()  # Get screen width [pixels]
        ScreenSizeY = master.winfo_screenheight() # Get screen height [pixels]
        ScreenRatio = 0.8                              # Set the screen ratio for width and height
        FrameSizeX  = int(ScreenSizeX * ScreenRatio)
        FrameSizeY  = int(ScreenSizeY * ScreenRatio)
        FramePosX   = (ScreenSizeX - FrameSizeX)/2 # Find left and up border of window
        FramePosY   = (ScreenSizeY - FrameSizeY)/2
        #self.master.geometry("%sx%s+%s+%s"%(FrameSizeX,FrameSizeY,FramePosX,FramePosY))
        #self.master.geometry("500x500")
        self.PADDING = 4
        self.createWidgets()

    def createWidgets(self):
        # First row
        self.sourcePathLabel = tk.Label(self.master)
        self.sourcePathLabel["text"] = "Source folder:"
        self.sourcePathLabel.grid(row=0, column=0, padx=4, pady=4)
        
        self.sourcePathInput = tk.Entry(self.master)
        self.sourcePathInput["width"] = 50
        self.sourcePathInput.grid(row=0, column=1, padx=4, pady=4)
        
        self.sourcePathButton = tk.Button(self.master)
        self.sourcePathButton["text"] = "Browse"
        self.sourcePathButton["command"] = self.chooseSourcePath
        self.sourcePathButton.grid(row=0, column=2, padx=4, pady=4)
        
        # Second row
        self.targetPathLabel = tk.Label(self.master)
        self.targetPathLabel["text"] = "Targer folder:"
        self.targetPathLabel.grid(row=1, column=0, padx=4, pady=4)

        self.targetPathInput = tk.Entry(self.master)
        self.targetPathInput["width"] = 50
        self.targetPathInput.grid(row=1, column=1, padx=4, pady=4)
        
        self.targetPathButton = tk.Button(self.master)
        self.targetPathButton["text"] = "Browse"
        self.targetPathButton["command"] = self.chooseTargetPath
        self.targetPathButton.grid(row=1, column=2, columnspan=3, padx=4, pady=4)
        
        # Third row
        self.prefixLabel = tk.Label(self.master)
        self.prefixLabel["text"] = "Prefix for files:"
        self.prefixLabel.grid(row=2, column=0, padx=4, pady=4)
        
        self.prefixInput = tk.Entry(self.master)
        self.prefixInput["width"] = 50
        self.prefixInput.grid(row=2, column=1, padx=4, pady=4)

        # Fouth row
        self.statusLabel = tk.Label(self.master)
        self.statusLabel["text"] = "Write paths and name prefix"
        self.statusLabel.grid(row=3, column=0, columnspan=3, padx=4, pady=4)

        # Fifth row
        self.parseButton = tk.Button(self.master)
        self.parseButton["text"] = "Parse Data"
        self.parseButton["command"] = self.parseData
        self.parseButton.grid(row=4, column=0, columnspan=3, padx=4, pady=4)

    def parseData(self):
        targetPath = self.targetPathInput.get() + "\\"
        sourcePath = self.sourcePathInput.get() + "\\"
        prefix = self.prefixInput.get()
        print(targetPath)
        routineOverAllFilesInPath(sourcePath, targetPath, prefix)
        
    def chooseTargetPath(self):
        selectedPath = filedialog.askdirectory()
        if(selectedPath != ""):
            self.targetPathInput.delete(0, tk.END)
            self.targetPathInput.insert(0, selectedPath)    
            
    def chooseSourcePath(self):
        selectedPath = filedialog.askdirectory()
        if(selectedPath != ""):
            self.sourcePathInput.delete(0, tk.END)
            self.sourcePathInput.insert(0, selectedPath)

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
    # Get list of the files
    dataFiles = getFilesInFolder(path, "dat")  
    
    # Processing all files 
    for dataFile in dataFiles:
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
    
if __name__== "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()