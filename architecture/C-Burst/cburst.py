# ▪ Memory Cache size: 128 MB
# ▪ Block size: 4 KB
# ▪ Cache replacement algorithm: LRU(性能区域)+C-Bursty(能耗区域)
# ▪ Initial partition: 性能区域(50%)+C-Burst(50%)
# ▪ 可以容忍的 performance loss:(相对全部用 LRU 管理,缺失率提高 10%)
# ▪ 每次划分调整的粒度是 2MB
# ▪ Epoch: 10s

import numpy as np
import os
import queue
import datetime, time

SOURCE_PATH = os.environ['HOME'] + "/data/trace/CBursty/"

DESTINATION_PATH = "log"

ADDRESS = 64

BLOCK_NUM = 1 << 15


class CBurst:
    def __init__(self, source, destination):
        self.source_path = source
        self.destination_path = destination
        des_folder = source
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)

    def saveLog(self, fp, addr, state):
        """
        :param fp:保存文件的指针
        :param addr: miss的地址
        :param state: miss或者hit 字符串类型
        :return:
        """
        fp.write(addr + " " + state + "\n")
        return

    def fileLists(self):
        """
        打开给定目录的文件
        :return:返回打开文件列表
        """
        file_list = os.listdir(self.source_path)
        fps = []
        for file in file_list:
            fp = open(self.source_path + file, 'r')
            fps.append(fp)

        return fps

    def closeFile(self, fp):
        """
        关闭文件
        :param fp:文件列表
        :return:
        """
        for i in range(len(fp)):
            fp[i].close()

    def getBlockTag(self, dec, block_num):
        """
        :param dec:10进制字符串
        :param block_num:块个数
        :return: 块tag
        """
        result = []
        temp = int(dec, 10)
        temp = temp >> 12
        temp = temp << 12
        result.append(temp)
        for i in range(1, block_num):
            temp = temp + (1 << 12)
            result.append(temp)
        return result


class LRUOnly(CBurst):
    def __init__(self, source, destination):
        super().__init__(source, destination)
        self.path = source
        self.path = destination
        self.cache = []
        self.hit = 0.0
        self.miss = 0.0
        self.total = 0.0

    def isHit(self, index):  # 判断是否命中
        hit_flag = False
        line = 0
        for i in range(len(self.cache) - 1, -1, -1):
            if self.cache[i] == 0:
                break
            elif index == self.cache[i]:
                line = i
                hit_flag = True
                break
        if hit_flag:
            return line
        else:
            return -1

    def run(self):
        file_list = super().fileLists()
        current_lines = ["0" for _ in range(len(file_list))]
        # finish_flags = [False for _ in range(len(file_list))]

        while True:
            self.total += 1
            for i in range(len(current_lines)):  # current_lines 保存的是每个文件顶部的行
                if current_lines[i] == "0":
                    current_lines[i] = file_list[i].readline()
                elif current_lines[i] == "":
                    current_lines.pop(i)
            if len(set(current_lines)) == 0:
                break
            current_line = 0
            min_time = float('inf')
            for i in range(len(current_lines)):  # 找出current_lines中timestamp最小的，作为本次循环使用的数据
                line = current_lines[i].strip().split(',')
                if (float(line[0]) - min_time) < 0:
                    min_time = float(line[0])
                    current_line = i
            line = current_lines[current_line].strip().split(',')
            addr = line[4]  # 获取本次处理的地址
            block_num = int(line[5]) // (1 << 12) + 1  # 本次处理的块数
            block_indexs = super().getBlockTag(addr, block_num)
            hit_flag = [False for _ in range(block_num)]
            for i in range(block_num):  # 命中检测
                if block_indexs[i] in self.cache:
                    self.hit += 1
                    self.cache.remove(block_indexs[i])
                    self.cache.append(block_indexs[i])
                    hit_flag[i] = True

            for i in range(block_num):  # 缺失处理
                if not hit_flag[i]:
                    self.miss += 1
                    if len(self.cache) < BLOCK_NUM:
                        self.cache.append(block_indexs[i])
                    else:
                        self.cache.pop(0)
                        self.cache.append(block_indexs[i])
            if self.total % 5000 == 0:
                print(current_lines[current_line], self.hit, self.miss, len(self.cache), self.total, "\naccuracy：",
                      self.hit / (self.hit + self.miss), time.time())
            current_lines[current_line] = "0"

        super().closeFile(file_list)
        print(self.hit / (self.miss + self.hit))
        # block_group = []
        # block_group_info = []
        # blocks = []
        # for line in file_list[0]:
        #     words = line.strip().split(',')
        #     blocks.append(words)
        #     print((float(blocks[len(blocks)-1][0]) - float(blocks[0][0]))/10**6)
        #     if float(blocks[len(blocks)-1][0]) - float(blocks[0][0]) > 10**7:
        #         block_group.append(blocks[:len(blocks)-1].copy())
        #
        #         exit(0)

        # print(lines)


if __name__ == '__main__':
    test = LRUOnly(SOURCE_PATH, DESTINATION_PATH)
    test.run()
