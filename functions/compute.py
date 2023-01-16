import csv
import pandas as pd
from functions.read_write_azure import read_data_from_azure

DaysOfWeek = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

class CourseAPied:
    def __init__(self, name):
        self.name = name

    def getSpeed_kmh(self, temps, distance):
        return distance/temps * 60//10/100

    def show(self):
        return self

    def data_from_csv(self, csv_file):
        #lg.info("Opening data file {}".format(csv_file))
        self.dataframe = read_data_from_azure(csv_file)
        self.currentFile = csv_file
        self.dataframe['Vitesse [km/h]'] = self.getSpeed_kmh(self.dataframe['Durée [mn]'], self.dataframe['Distance [m]'])
        #lg.info("File imported")
        self.dataframe.index=self.getDayOfWeek()
        return self.dataframe

    def writeLine(self, date, lieu, temps, distance):
        with open(self.currentFile,'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, lieu, temps, distance])

    def getDayOfWeek(self):
        b = []
        for i,j in self.dataframe.iterrows():
            b.append(DaysOfWeek[pd.to_datetime(self.formatDate(self.dataframe["Date"][i])).dayofweek])
        return b

    def formatDate(self, date):
        return date.split("/")[1] + "/" + date.split("/")[0] + "/" + date.split("/")[2]
