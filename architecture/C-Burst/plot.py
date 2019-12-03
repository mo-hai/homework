import sys
import math
import matplotlib.pyplot as plt

INTERVAL = 2e8


def readlog(filename):
    fr = open(filename, 'r')
    line = fr.readline()
    if line == '' or line == None:
        return
    print(line.split(',')[0].split(' ')[-1])
    oldtimestamp = int(line.split(',')[0].split(' ')[-1]) + int(line.split(',')[-1])
    intervalDict = dict()
    while True:
        line = fr.readline()
        if line == '' or line == None:
            break
        timestamp = int(line.split(',')[0].split(' ')[-1])
        dealtime = int(line.split(',')[-1])
        if (timestamp - oldtimestamp) > INTERVAL:
            intervalDict.setdefault(timestamp - oldtimestamp - INTERVAL, 0)
            intervalDict[timestamp - oldtimestamp - INTERVAL] += 1
            oldtimestamp = timestamp
        elif (timestamp - oldtimestamp) < 0:
            oldtimestamp += dealtime
        else:
            oldtimestamp = timestamp
    fr.close()
    orderList = sorted(intervalDict.items(), key=lambda x: x[0])
    sum = 0
    cdfList = []
    for key, value in orderList:
        sum += value
        cdfList.append((key, sum))
    return cdfList


def main():
    # cdfList_lru = readlog("one_file_log/LRU/miss.log")
    # cdfList_cburst = readlog("one_file_log/CBurst/miss.log")
    # cdfList_cburstlru = readlog("one_file_log/CBurstLRU/miss.log")
    cdfList_lru = readlog("one_file_log_size = 512/LRU/miss.log")
    cdfList_cburst = readlog("one_file_log_size = 512/CBurst/miss.log")
    cdfList_cburstlru = readlog("one_file_log_size = 512/CBurstLRU/miss.log")
    plt.figure()
    plt.xlim([0, 30])
    plt.ylim([0, 1])
    sum_lru = cdfList_lru[-1][1]
    sum_cburst = cdfList_cburst[-1][1]
    sum_cburst_lru = cdfList_cburstlru[-1][1]
    plt.plot([cdfList_lru[i][0] * 20 / INTERVAL for i in range(len(cdfList_lru))],
             [cdfList_lru[i][1] / sum_lru for i in range(len(cdfList_lru))], c='r', label='cdf-lru')
    plt.plot([cdfList_cburst[i][0] * 20 / INTERVAL for i in range(len(cdfList_cburst))],
             [cdfList_cburst[i][1] / sum_cburst for i in range(len(cdfList_cburst))], c='b', label='cdf-cburst')
    plt.plot([cdfList_cburstlru[i][0] * 20 / INTERVAL for i in range(len(cdfList_cburstlru))],
             [cdfList_cburstlru[i][1] / sum_cburst_lru for i in range(len(cdfList_cburstlru))], c='aqua', label='cdf-cburstLRU')

    # plt.plot([orderList[i][0] * 20/INTERVAL for i in range(len(orderList))],[orderList[i][1]/sum for i in range(len(orderList))],c = 'b',label = 'pdf')
    plt.legend()
    plt.show()


def main1():
    fr = open("allline10s.txt", 'r')
    blockset = set()
    for line in fr.readlines():
        arglist = line.split(',')
        addr = int(arglist[-3])
        size = int(arglist[-2])
        tag = addr >> 12
        blocks = math.ceil((addr + size) / (1 << 12)) - tag
        for i in range(blocks):
            blockset.add(tag + i)
    print(len(blockset))


if __name__ == '__main__':
    main()
