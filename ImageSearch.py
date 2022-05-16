import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import math
import sys

class searcher:
    def __init__(self, samplePath, queryPath):
        self.samplePath = samplePath
        self.queryPath = queryPath

        #创建SIFT特征提取器
        self.sift = cv2.SIFT_create()

        #创建FLANN匹配对象
        FLANN_INDEX_KDTREE=0
        indexParams=dict(algorithm=FLANN_INDEX_KDTREE,trees=5)
        searchParams=dict(checks=50)
        self.flann=cv2.FlannBasedMatcher(indexParams,searchParams)
        self.imageCollection = self.__loadAllImages()


    def __loadAllImages(self):
        imageCollection=[]
        for parent,dirnames,filenames in os.walk(self.queryPath):
            for imgName in filenames:
                filePath=self.queryPath+imgName
                image=cv2.imread(filePath,0)
                imageCollection.append((image, imgName))
        return imageCollection


    def start(self):
        sampleImage=cv2.imread(self.samplePath,0)
        kp1, des1 = self.sift.detectAndCompute(sampleImage, None) #提取样本图⽚的特征

        comparisonImageList = []
        # for parent,dirnames,filenames in os.walk(self.queryPath):
        #     for p in filenames:
        #         p=queryPath+p
        #         queryImage=cv2.imread(p,0)

        for (queryImage, imageName) in self.imageCollection:
                kp2, des2 = self.sift.detectAndCompute(queryImage, None) #提取⽐对图⽚的特征
                matches=self.flann.knnMatch(des1,des2,k=2) #匹配特征点，为了删选匹配点，指定k为2，这样对样本图的每个特征点，返回两个匹配
                (matchNum,matchesMask)=self.__getMatchNum(matches,0.9) #通过⽐率条件，计算出匹配程度
                matchRatio=matchNum*100/len(matches)
                drawParams=dict(matchColor=(0,255,0),
                        singlePointColor=(255,0,0),
                        matchesMask=matchesMask,
                        flags=0)
                
                comparisonImage=cv2.drawMatchesKnn(sampleImage,kp1,queryImage,kp2,matches,None,**drawParams)
                comparisonImageList.append((comparisonImage,matchRatio, imageName)) #记录下结果

        comparisonImageList.sort(key=lambda x:x[1],reverse=True) #按照匹配度排序
        return comparisonImageList

    
    def __getMatchNum(self, matches,ratio):
        '''返回特征点匹配数量和匹配掩码'''
        matchesMask=[[0,0] for i in range(len(matches))]
        matchNum=0
        for i,(m,n) in enumerate(matches):
            if m.distance<ratio*n.distance: #将距离⽐率⼩于ratio的匹配点删选出来
                matchesMask[i]=[1,0]
                matchNum+=1
        return (matchNum,matchesMask)


# if __name__ == "__main__":
#     # path='C:/Users/whaiyan/Desktop/PictureSearchPicture/'
#     # queryPath=path+'Pictures/' #图库路径
#     # samplePath=path+'Sample/sample.PNG' #样本图⽚

#     # samplePath=sys.argv[1]
#     # queryPath=sys.argv[2]

#     samplePath="./Sample/image.PNG"
#     queryPath="./Pictures/"
    
#     obj = searcher(samplePath, queryPath)
#     comparisonImageList=obj.start()
#     topMatchImageName=comparisonImageList[0][2]
#     print(topMatchImageName)

    #  # 绘图显⽰
    # count=len(comparisonImageList)
    # column=2
    # row=math.ceil(count/column)
    # figure,ax=plt.subplots(row,column)
    # for index,(image,ratio, imageName) in enumerate(comparisonImageList):
    #     print(imageName)
    #     ax[int(index/column)][index%column].set_title('Similiarity %.2f%%' % ratio)
    #     ax[int(index/column)][index%column].imshow(image)
    # plt.show()












