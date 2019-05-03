import pandas as pd
filePath = "./data.csv"

data = pd.read_csv(filePath)
dataDict = {}
for i in data.keys():
    dataDict[i] = list(data[i])

# print(dataDict)