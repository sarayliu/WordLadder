# Sara Liu, 9/13/18

import sys
import time

wordFile = open('wordList.txt')
wordContent = wordFile.readlines()
print('Words: ', len(wordContent))
wordFile.close()


def isNeighbor(word1, word2):
    if len(word1) == len(word2):
        count = 0
        for index in range(len(word1)):
            if not word1[index] == word2[index]:
                count += 1
                if count > 1:
                    return False
        if count == 1:
            return True
    return False


def neighborList():
    global pairs
    for index1 in range(len(wordContent)):
        for index2 in range(index1 + 1, len(wordContent)):
            if isNeighbor(wordContent[index1].strip(), wordContent[index2].strip()):
                pairs += 1
                neighDict[wordContent[index1].strip()].append(wordContent[index2].strip())
                neighDict[wordContent[index2].strip()].append(wordContent[index1].strip())


t1 = time.time()
neighDict = {}
for i in range(len(wordContent)):
    neighDict[wordContent[i].strip()] = []
pairs = 0
neighborList()
t2 = time.time()
print('Neighbor pairs: ', pairs)
print('Time to find number of neighbor pairs: ', round(t2-t1, 2), 's')

if len(sys.argv) == 2:
    word = sys.argv[1]
    if word not in neighDict:
        print(word, 'is not in the dictionary')
    else:
        neighList = neighDict[word]
        print('Number of neighbors for ', word, ': ', len(neighList), '; List of neighbors: ', neighList)

mostNeigh = 0
wordMostNeigh = ''
noNeighCount = 0
distinctPairCount = 0
degrees = []
degreeCount = 0
for aWord in neighDict:
    if len(neighDict[aWord]) > mostNeigh:
        mostNeigh = len(neighDict[aWord])
        wordMostNeigh = aWord
    if len(neighDict[aWord]) == 0:
        noNeighCount += 1
    if len(neighDict[aWord]) == 1:
        if len(neighDict[neighDict[aWord][0]]) == 1:
            distinctPairCount += 1
    if len(neighDict[aWord]) not in degrees:
        degrees.append(len(neighDict[aWord]))
        degreeCount += 1
print(wordMostNeigh, ' has the most number of neighbors: ', mostNeigh, 'neighbors')
print('Number of words with no neighbors: ', noNeighCount)
distinctPairCount /= 2
print('Number of distinct pairs: ', int(distinctPairCount))
degrees.sort()
print('Number of degrees: ', degreeCount, '; List of degrees: ', degrees)


def connect(word1):
    parseMe = [word1]
    cc = {word1}
    while parseMe:
        someWord = parseMe[0]
        del parseMe[0]
        for neighbor in neighDict[someWord]:
            if neighbor not in cc:
                parseMe.append(neighbor)
                cc.add(neighbor)
    return cc


ccSizes = []
k3Count = 0
for aWord in neighDict:
    connectedComponent = connect(aWord)
    if len(connectedComponent) not in ccSizes:
        ccSizes.append(len(connectedComponent))
    if len(connectedComponent) == 3:
        ccList = list(connectedComponent)
        if len(neighDict[ccList[0]]) == len(neighDict[ccList[1]]) == len(neighDict[ccList[2]]) == 2:
            # if ccList[1] in neighDict[ccList[0]] and ccList[2] in neighDict[ccList[0]]:
            k3Count += 1
ccSizes.sort()
print('Number of connected component sizes: ', len(ccSizes))
# print('Connected component sizes: ', ccSizes)
k3Count /= 3
print('Number of K3s: ', int(k3Count))
