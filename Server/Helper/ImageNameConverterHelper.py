# 该文件主要是对爬下来的图片进行重名名

from cmath import nan
from email.header import Header
import os
import sys
import cv2
import pandas as pd
import numpy as np


# Step-1
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

    for index, row in df.iterrows():

        imagePath = row[colums[1]]
        if str(imagePath) == "nan":
            print("index:" + str(index) + " imagePath is Nan")
            continue
        imageName = imagePath.split("\\")[-1]
        
        imageId = row[colums[2]]
        if str(imageId) == "nan":
            print("index: " + str(index) + " imageId is nan")
            continue

        imageId = row[colums[2]][1::]
        
        srcImagePath = os.path.join(srcImageFolder, imageName)
        storeImagePath = os.path.join(storeImageFolder, imageId + ".PNG")
        
        # print(storeImagePath)
        srcImage = cv2.imread(srcImagePath)
        cv2.imwrite(storeImagePath, srcImage)

    
    print(df.head(5))
    df_ = df[colums[2::]]
    df_.to_csv(storeInfoCsv)



# Step-2
def findMissingImageIds(folder):
    infoCsvFilePath = os.path.join(folder, "Image_0-10000-new.csv")
    df = pd.read_csv(infoCsvFilePath, encoding="utf8", index_col=0)
    print(df.head(2))
    
    colums = df.columns.values

    df[colums[0]] = df[colums[0]].apply(lambda x: int(x))

    tmpDict = dict()
    for val in df[colums[0]]:
        if val not in tmpDict:
            tmpDict[val] = 1
        else:
            print("dupicate image ID: %d" % val)

    
    idDict = {val:True for val in df[colums[0]]}
    missingIdCollection = []
    for i in range(10000):
        if i not in idDict:
            missingIdCollection.append(i)
    
    # print(missingIdCollection)
    print("missing image count: %d" % (len(missingIdCollection)))

    baseUrl = "https://opensea.io/assets/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/"
    
    urlCollection = []
    storeUrlFilePath = os.path.join(folder, "url.txt")
    with open(storeUrlFilePath, "w") as f:
        for missingId in missingIdCollection:
            url = baseUrl + str(missingId)
            f.writelines(url + "\n")

    return missingIdCollection

# Step-3
def mergeTheMissingImage(folder):
    infoCsvFilePath = os.path.join(folder, "Image_missing.csv")
    df = pd.read_csv(infoCsvFilePath, encoding="utf8")
    missingIdCollection = findMissingImageIds(folder)

    df['文本'] = missingIdCollection
    print(df.head(2))

    colums = df.columns.values

    # do the mapping work
    # Note colums[1] is the image path, colums[2] is the ID
    df[colums[1]] = df[colums[1]].apply(lambda x: str(x))
    df[colums[2]] = df[colums[2]].apply(lambda x: str(x))

    # delete the "nan" rows
    df = df[df[colums[1]] != "nan"]
    df = df[df[colums[2]] != "nan"]
    

    srcImageFolder = os.path.join(folder, "Image_missing")
    storeImageFolder = os.path.join(folder, "Image_missing-new")
    
    # # storeInfoCsv =  os.path.join(folder, "Image_missing-new.csv")
    # for index, row in df.iterrows():
    #     imagePath = row[colums[1]]
    #     imageName = imagePath.split("\\")[-1]

    #     imageId = row[colums[2]]
    #     # imageId = row[colums[2]][1::]
        
    #     srcImagePath = os.path.join(srcImageFolder, imageName)

    #     print(srcImagePath)

    #     storeImagePath = os.path.join(storeImageFolder, imageId + ".PNG")
        
    #     # print(storeImagePath)
    #     srcImage = cv2.imread(srcImagePath)
    #     cv2.imwrite(storeImagePath, srcImage)

    # print(np.shape(df))

    # Do the merge work
    df_1 = df[colums[2::]]

    dataPath = os.path.join(folder, "Image_0-10000-new.csv")
    df_2 = pd.read_csv(dataPath, encoding="utf8", index_col=0)
    
    print("shape:")
    print(np.shape(df_1))
    print(np.shape(df_2))
    
    print(df_1.columns.values)
    print(df_2.columns.values)
    data = pd.concat([df_1, df_2], axis=0, ignore_index=True)
    
    print(np.shape(data))
    data = data.rename(columns={"文本":"ID"})
    print(data.head(2))

    data["ID"] = data["ID"].apply(lambda x: int(x))
    print(data.columns.values)

    data = data.sort_values(by="ID")
    # data = data.reset_index()
    print("hehe")
    print(data.columns.values)
    print(data.head(2))

    dataPath = os.path.join(folder, "data.csv")
    data.to_csv(dataPath, index=False)


if __name__ == '__main__':
    folder = "C:/Users/whaiyan/Desktop/final_crawel/"

    # imageNameConverterHelper(folder)
    # findMissingImageIds(folder)
    mergeTheMissingImage(folder)



