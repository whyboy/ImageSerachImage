# 该文件主要是对爬下来的图片进行重名名

from cmath import nan
from email.header import Header
import os
import sys
import cv2
import pandas as pd
import numpy as np

# def findMissingImageIds(folder):



def imageNameConverterHelper(folder):
    
    # with open(infoFilePath, encoding="utf8") as f:
    #     line = f.readline()
    #     while line:
    #         # print(line)
    #         lineSplit = line.split(',')
    #         print(len(lineSplit))
    #         line = f.readline()

    infoCsvFilePath = os.path.join(folder, "Image_0-10000.csv")
    df = pd.read_csv(infoCsvFilePath, encoding="utf8")

    srcImageFolder = os.path.join(folder, "Image_0-10000")
    storeImageFolder = os.path.join(folder, "Image_0-10000-new")
    storeInfoCsv =  os.path.join(folder, "Image_0-10000-new.csv")
    colums = df.columns.values
    print(colums)
    
    # do the mapping work
    # Note colums[1] is the image path, colums[2] is the ID
    df[colums[1]] = df[colums[1]].apply(lambda x: str(x))
    df[colums[2]] = df[colums[2]].apply(lambda x: str(x))

    # delete the "nan" rows
    df = df[df[colums[1]] != "nan"]
    df = df[df[colums[2]] != "nan"]
    
    df["文本"] = df["文本"].apply(lambda x: int(x[1::]))

    df = df.sort_values(by=colums[2])
    df = df.reset_index()

    # for index, row in df.iterrows():

    #     imagePath = row[colums[1]]
    #     if str(imagePath) == "nan":
    #         print("index:" + str(index) + " imagePath is Nan")
    #         continue
    #     imageName = imagePath.split("\\")[-1]
        
    #     imageId = row[colums[2]]
    #     if str(imageId) == "nan":
    #         print("index: " + str(index) + " imageId is nan")
    #         continue

    #     imageId = row[colums[2]][1::]
        
    #     srcImagePath = os.path.join(srcImageFolder, imageName)
    #     storeImagePath = os.path.join(storeImageFolder, imageId + ".PNG")
        
    #     # print(storeImagePath)
    #     srcImage = cv2.imread(srcImagePath)
    #     cv2.imwrite(storeImagePath, srcImage)

    
    print(df.head(5))
    df_ = df[colums[2::]]
    df_.to_csv(storeInfoCsv)


if __name__ == '__main__':
    folder = "C:/Users/whaiyan/Desktop/final_crawel/"
    imageNameConverterHelper(folder)




