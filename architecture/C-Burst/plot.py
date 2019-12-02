import sys
import math
import matplotlib.pyplot as plt

INTERVAL = 2e8
def main():
    fr = open("log1/LRU/miss.log",'r')
    line = fr.readline()
    if line == '' or line == None :
            return
    print(line.split(',')[0].split(' ')[-1])
    oldtimestamp = int(line.split(',')[0].split(' ')[-1]) + int(line.split(',')[-1])
    intervalDict = dict()
    while True:
        line = fr.readline()
        if line == '' or line == None :
            break
        timestamp = int(line.split(',')[0].split(' ')[-1])
        dealtime = int(line.split(',')[-1])
        if (timestamp - oldtimestamp) > INTERVAL:
            intervalDict.setdefault(timestamp - oldtimestamp-INTERVAL,0)
            intervalDict[timestamp-oldtimestamp-INTERVAL] += 1
            oldtimestamp = timestamp
        elif (timestamp - oldtimestamp) < 0:
            oldtimestamp += dealtime
        else:
            oldtimestamp = timestamp
    fr.close()
    orderList = sorted(intervalDict.items(),key = lambda x: x[0])
    sum = 0
    cdfList = []
    for key,value in orderList:
        sum += value
        cdfList.append((key,sum))
    # print(orderList)
    plt.figure()
    plt.xlim([0, cdfList[-1][0]*20/INTERVAL])
    plt.ylim([0, 1])
    plt.plot([cdfList[i][0] * 20/INTERVAL for i in range(len(cdfList))],[cdfList[i][1]/sum for i in range(len(cdfList))],c = 'r',label = 'cdf')
    # plt.plot([orderList[i][0] * 20/INTERVAL for i in range(len(orderList))],[orderList[i][1]/sum for i in range(len(orderList))],c = 'b',label = 'pdf')
    plt.legend()
    plt.show()
if __name__ == '__main__':
    main()
