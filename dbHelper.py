

from cmath import isnan
import pandas as pd
import os
import sys
from tinydb import TinyDB

def insertImageProperty():
    imagePropertyInfoFile = "/home/azureuser/Code/101web3/ImageSerachImage/Image_0-30-new.csv"
    df = pd.read_csv(imagePropertyInfoFile, index_col=0)
    print(df.head(2))
    db = TinyDB('db.json')
    for index, row in df.iterrows():
        tmpDict = {"id" : str(row[0])}
        
        for i in range(1, len(row)-2, 3):
            print(i)
            key = str(row[i])
            if key != "nan":
                val = str(row[i+1]) + ", " + str(row[i+2])
                tmpDict[key] = val

        print(tmpDict)
        db.insert(tmpDict)

if __name__ == "__main__":
    print(os.getcwd())
    print(sys.argv[0])
    print(os.path.abspath('.'))
    insertImageProperty()
