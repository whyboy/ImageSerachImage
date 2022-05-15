# 该文件主要是对爬下来的图片进行重名名

import os
import sys
import cv2
import pandas as pd

def imageNameConverterHelper(infoCsvFilePath):
    
    # with open(infoFilePath, encoding="utf8") as f:
    #     line = f.readline()
    #     while line:
    #         # print(line)
    #         lineSplit = line.split(',')
    #         print(len(lineSplit))
    #         line = f.readline()

    df = pd.read_csv(infoCsvFilePath, encoding="utf8")

    srcImageFolder = 'C:/Users/whaiyan/Desktop/crawlResult/Image_0-30'
    storeImageFolder = 'C:/Users/whaiyan/Desktop/crawlResult/Image_0-30-new'
    colums = df.columns.values
    print(colums)
    for index, row in df.iterrows():
        # print(index)
        # print(row)
        imagePath = row[colums[1]]
        imageName = imagePath.split("\\")[-1]
        imageId = row[colums[2]]
        print(imageName)
        print(imageId)

        srcImagePath = os.path.join(srcImageFolder, imageName)
        storeImagePath = os.path.join(storeImageFolder, imageId + ".PNG")

        srcImage = cv2.imread(srcImagePath)
        cv2.imwrite(storeImagePath, srcImage)

    print(df.head(5))

    
    



if __name__ == '__main__':
    infoFilePath = "C:/Users/whaiyan/Desktop/crawlResult/BoredApe_0-30.csv"
    imageNameConverterHelper(infoFilePath)
    
    # with open(infoFilePath, encoding="utf8") as f:
    #     line = f.readline()
    #     while line:
    #         print(line)
    #         line = f.readline()




