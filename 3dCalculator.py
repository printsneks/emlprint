'''
 Name of file: 3dCalculator
 Purpose: Calculates time it takes to print based on previous data

 Author(s): Brian Shotliff

 Date Created:

'''

# all import statements
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import re
import math
import csv
# all functions, each function has a docstring
class Gcode:
    # This one checks the gcode

    def __init__(self, file):
        self._time = ''
        self._xyChange = 0
        self._zChange = 0
        self._xyDistance = 0
        self._zDistance = 0
        self._file = file
        self._csv = '\settings\data.csv'

        self._linIntercept = 0
        self._changeXYCoef  = 0
        self._changeZCoef = 0
        self._distanceXYCoef = 0
        self._distanceZCoef = 0
    def getCsv(self):
        return self._csv

    def getFile(self):
        return self._file
    def setXYChange(self, newXY):
        self._xyChange = newXY
    def getXYChange(self):
        return self._xyChange
    def setZChange(self, newZ):
        self._ZChange = newZ
    def getZChange(self):
        return self._ZChange
    def setXYDistance(self, distance):
        self._xyDistance = distance
    def getXYDistance(self):
        return self._xyDistance
    def setZDistance(self, distance):
        self._zDistance = distance
    def getZDistance(self):
        return self._zDistance
    def setTime(self, time):
        self._time = time
    def getTime(self):
        return self._time

    def setLinIntercept(self, linCoef):
        self._linIntercept = linCoef
    def getLinIntercept(self):
        return self._linIntercept
    def setChangeXYCoef(self, coef):
        self._changeXYCoef = coef
    def getChangeXYCoef(self):
        return self._changeXYCoef
    def setChangeZCoef(self, coef):
        self._changeZCoef = coef
    def getChangeZCoef(self):
        return self._changeZCoef
    def setDistanceXYCoef(self, coef):
        self._distanceXYCoef = coef
    def getDistanceXYCoef(self):
        return self._distanceXYCoef
    def setDistanceZCoef(self, coef):
        self._distanceZCoef = coef
    def getDistanceZCoef(self):
        return self._distanceZCoef

    def evalFile(self, file, TR):
        """
        eval File processes the gcode file looking for travel distances and how many times the file changes directions
        in the XY/Z
        :param file: gcode file
        :return: Nothing
        """

        # textFile = os.path.join(sys.path[0], file)
        # textFile = open(textFile, "r")
        print(file)
        textFile = open(file, "r")
        fullFile = []
        # line = ''
        xyChange = 0
        zChange = 0
        xValues = []
        yValues = []
        zValues = []

        xyDistance = []
        # formats the file f or our purpose and adds it to fullFile so we can close it
        for line in textFile:
            line = line.replace("\n", "")
            line = line.replace(" ", "")
            fullFile.append(line)
        textFile.close()
        # Grabs all the coordinates
        for item in fullFile:
            if "G1X" in item:
                xyChange = xyChange + 1
                matchX = re.search('(?<=G1X)[0-9.]+', item)
                matchY = re.search('(?<=Y)[0-9.]+', item)
                # print('X : {:} | Y : {:}'.format(matchX.group(0), matchY.group(0)))
                xValues.append(matchX.group(0))
                yValues.append(matchY.group(0))
            elif "G1Z" in item:
                zChange = zChange + 1
                matchZ = re.search('(?<=G1Z)[0-9.]+', item)
                zValues.append(matchZ.group(0))
        self.setXYChange(xyChange)
        self.setZChange(zChange)

        # Distances
        for i in range(1, len(xValues)):
            distance = (float(xValues[i]) - float(xValues[i - 1])) ** 2 + (
                        float(yValues[i]) - float(yValues[i - 1])) ** 2
            distance = math.sqrt(distance)
            xyDistance.append(distance)

        xyFinalDistance = 0
        for item in xyDistance:
            xyFinalDistance = xyFinalDistance + item

        zDistance = float(zValues[-1]) - float(zValues[0])
        self.setXYDistance(xyFinalDistance)
        self.setZDistance(zDistance)
        # print('{:},{:},{:},{:}'.format(self.getXYDistance(),self.getXYChange(),self.getZDistance(),self.getZChange()))
        # print('X,Y Plane Distance : {:} | Z Plane Distance : {:} | X,Y Directional Changes : {:} | Z Directional Changes : {:}'.format(self.getXYDistance(), self.getZDistance(), self.getXYChange(),self.getZChange()))
        # print()
        if TR:
            self.guessTime()
        updateCsv = input("Update csv [y/n] : ").upper()
        if updateCsv == "Y":
            # need to clean this up
            file = self.getCsv()
            cwd = os.getcwd() # gets  current directory
            file = cwd + file
            csvRow = [self.getXYDistance(), self.getZDistance(), self.getXYChange(),self.getZChange()]
            with open(file, 'a') as csvFile:
                writer = csv.writer(csvFile, lineterminator='\n')
                writer.writerow(csvRow)



    def guessTime(self):
        file = self.getCsv()
        cwd = os.getcwd()  # gets  current directory
        file = cwd + file
        data = pd.read_csv(file)

        # visualize the data
        sns.pairplot(data, x_vars=['distanceXY', 'distanceZ', 'changeXY', 'changeZ'],
                     y_vars='time')
        sns.pairplot(data, x_vars=['distanceXY', 'distanceZ', 'changeXY', 'changeZ'],
                     y_vars='time', kind='reg')
        # plt.show()


        featureCol = ['distanceXY', 'distanceZ', 'changeXY', 'changeZ'] #Whatever the feature columns are going to be
        x = data[featureCol]

        y = data['time']# New header needs to be time

        X_train, X_test, Y_train, Y_test = train_test_split(x, y, random_state=1)

        linreg = LinearRegression()
        linreg.fit(X_train, Y_train)
        # print(linreg.fit(X_train, Y_train))
        self.setLinIntercept(linreg.intercept_)
        self.setDistanceXYCoef(linreg.coef_[0])
        self.setDistanceZCoef(linreg.coef_[1])
        self.setChangeXYCoef(linreg.coef_[2])
        self.setChangeZCoef(linreg.coef_[3])
        myZip = zip(featureCol, linreg.coef_)
        # print(list(myZip))
        # print("Intercept ", self.getLinIntercept())
        # print("Distance XY Coef ", self.getDistanceXYCoef())
        # print("Distance Z Coef ", self.getDistanceZCoef())
        # print("Change XY coef ", self.getChangeXYCoef())
        # print("Change Z Coef ", self.getChangeZCoef())
        # print("#########")
        time = self.getLinIntercept() + self.getDistanceXYCoef() * self.getXYDistance() + \
               self.getDistanceZCoef() * self.getZDistance() +\
               self.getChangeXYCoef() * self.getXYChange() + \
               self.getChangeZCoef() * self.getZChange()
        hours = int(time // 3600)
        minutes = int((time - (hours * 3600)) // 60)
        seconds = int(round((time - ((hours * 3600) + (minutes * 60)))))
        print("Hours:Minutes:Seconds => {:}:{:}:{:}".format(hours, minutes, seconds))
        # print(time)
    def updateRealTime(self, time):
        file = self.getCsv()
        cwd = os.getcwd()  # gets  current directory
        file = cwd + file
        csvFile = open(file)
        contents = csvFile.read()
        csvFile.close()
        contents = contents[:-1]
        csvFile = open(file, 'w')
        csvFile.write(contents)
        csvFile.close()
        time = ',' + str(time) + '\n'
        with open(file, 'a') as csvFile:
            csvFile.write(time)
    def userInputTime(self, time):
        time = time.split(':')
        tempHours = int(time[0]) * 3600
        tempMinutes = int(time[1]) * 60
        tempSeconds = int(time[2])

        time = tempHours + tempMinutes + tempSeconds
        print('{:} | {:} | {:}'.format(tempHours, tempMinutes, tempSeconds))
        # print(time)
        self.updateRealTime(time)


# main function, main needs a docstring, too
def main():
    dasLoop = True
    while dasLoop:
        print("Enter the corresponding Letter to perform an action\n")
        print("A ) Evaluate the file, provide an estimation and add it to the CSV")
        print("B ) Add a real time to the CSV")
        print("C ) First time Data (Empty Csv)")
        print("Q ) Exit the program")
        choice = input("Enter your choice : ")
        choice = choice.upper()
        if choice == "A" or choice == "B" or choice == "C" or choice == "Q":

            if choice == "A":
                file = input("Enter Gcode file location : ")
                file = file.replace("\\", "\\\\")
                gCode = Gcode(file)
                gCode.evalFile(gCode.getFile(), True)
            elif choice == "B":
                file = input("Enter Gcode file location : ")
                file = file.replace("\\", "\\\\")
                gCode = Gcode(file, False)
                gCode.userInputTime(input("Time Hours:Minutes:Seconds => "))
            elif choice == "C":
                file = input("Enter Gcode file location : ")
                file = file.replace("\\", "\\\\")
                gCode = Gcode(file, False)
                gCode.evalFile(gCode.getFile())
            elif choice == "Q":
                dasLoop = False
        else:
            print("Choice not recognized : ", choice)

# main function call
if __name__ == '__main__':
    main()
