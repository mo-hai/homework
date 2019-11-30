# ▪ Memory Cache size: 128 MB
# ▪ Block size: 4 KB
# ▪ Cache replacement algorithm: LRU(性能区域)+C-Bursty(能耗区域)
# ▪ Initial partition: 性能区域(50%)+C-Burst(50%)
# ▪ 可以容忍的 performance loss:(相对全部用 LRU 管理,缺失率提高 10%)
# ▪ 每次划分调整的粒度是 2MB
# ▪ Epoch: 10s

import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor
import queue
import sys
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

    def saveLog(self, fp, content):
        fp.write(content)
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

    def getBlockTag(self, dec, block_size):
        """
        :param dec:10进制字符串
        :param block_num:块个数
        :return: 块tag
        """
        begin_addr = int(dec)
        begin_tag = begin_addr >> 12
        block_num = int(np.ceil((begin_addr + block_size) / 4096)) - begin_tag
        return begin_tag, block_num


class LRUOnly(CBurst):
    def __init__(self, source, destination):
        super().__init__(source, destination)
        self.path = source
        self.des_path = destination + "/LRU/"
        self.cache_tag = {}
        self.cache_index = {}
        self.hit = 0.0
        self.miss = 0.0
        self.total = 0.0

    def run(self):
        if not os.path.exists(self.des_path):
            os.makedirs(self.des_path)
        w = open(self.des_path + "missdes.log", "w+")
        file_list = list(reversed(super().fileLists()))
        current_lines = ["0" for _ in range(len(file_list))]
        t1 = time.process_time()
        full_flag = False
        while True:
            for i in range(len(current_lines)):  # current_lines 保存的是每个文件顶部的行
                if current_lines[i] == "0":
                    current_lines[i] = file_list[i].readline()
                elif current_lines[i] == "":
                    current_lines.pop(i)
            if current_lines[0] == "":
                current_lines.pop(0)
            if len(set(current_lines)) == 0:
                break
            current_line = 0
            min_time = sys.maxsize
            for i in range(len(current_lines)):  # 找出current_lines中timestamp最小的，作为本次循环使用的数据
                if current_lines[i] == "":
                    continue
                line = current_lines[i].strip().split(',')
                if (int(line[0]) - min_time) < 0:
                    min_time = int(line[0])
                    current_line = i
            if min_time == sys.maxsize:
                print("error")
                break
            line = current_lines[current_line].strip().split(',')
            tag, block_num = super().getBlockTag(line[4], int(line[5]))
            # hit_flag = [False for _ in range(block_num)]
            hit_flag = True
            for i in range(block_num):  # 命中检测
                if self.cache_tag.__contains__(tag + i):
                    t = time.process_time()
                    index = self.cache_tag[tag + i]
                    self.cache_tag.pop(tag + i)
                    self.cache_index.pop(index)
                    self.cache_index[t] = tag + i
                    self.cache_tag[tag + i] = t
                else:
                    hit_flag = False
                    if not full_flag and len(self.cache_tag) < BLOCK_NUM:
                        t = time.process_time()
                        self.cache_index[t] = tag + i
                        self.cache_tag[tag + i] = t
                    else:
                        if not full_flag:
                            full_flag = True
                        t = time.process_time()
                        tag_temp = list(self.cache_tag.keys())[0]
                        index = self.cache_tag[tag_temp]
                        self.cache_tag.pop(tag_temp)
                        self.cache_index.pop(index)
                        self.cache_tag[tag + i] = t
                        self.cache_index[t] = tag + i

            if hit_flag:
                self.hit += 1
                # super().saveLog(w, "hit " + current_lines[current_line])
            else:
                super().saveLog(w, "miss " + current_lines[current_line])
                self.miss += 1


            self.total += 1
            if self.total % 50000 == 0:
                print(current_lines[current_line], self.hit, self.miss, len(self.cache_tag), self.total, "\naccuracy：",
                      self.hit / self.total, time.process_time() - t1)
                t1 = time.process_time()
            current_lines[current_line] = "0"

        super().closeFile(file_list)
        w.close()
        print(self.hit / (self.miss + self.hit))
        print(self.hit, self.total)
        with open(self.des_path + "result.log", "w+") as result_log:
            result_log.write("accuracy: " + str(self.hit / self.total) + "hit_num: " + str(self.hit) + "\n")


class CBustOnly(CBurst):
    def __init__(self, source, destination):
        super().__init__(source, destination)
        self.path = source
        self.des_path = destination + "/CBust/"
        self.cache = []
        self.cache_tag = {}
        self.cache_index = {}
        self.hit = 0.0
        self.miss = 0.0
        self.total = 0.0

    def run(self):
        if os.path.exists(self.des_path):
            os.makedirs(self.des_path)
        w = open(self.des_path + "miss.log")
        file_list = super().fileLists()
        block_group = []
        block_group_info = []
        blocks = []
        while True:
            break

        # for line in file_list[0]:
        #     words = line.strip().split(',')
        #     blocks.append(words)
        #     print((float(blocks[len(blocks)-1][0]) - float(blocks[0][0]))/10**6)
        #     if float(blocks[len(blocks)-1][0]) - float(blocks[0][0]) > 10**7:
        #         block_group.append(blocks[:len(blocks)-1].copy())
        #
        #         exit(0)

        # print(lines)
        super().closeFile(file_list)
        w.close()


if __name__ == '__main__':
    if not os.path.exists(DESTINATION_PATH):
        os.makedirs(DESTINATION_PATH)
    test = LRUOnly(SOURCE_PATH, DESTINATION_PATH)
    test.run()
