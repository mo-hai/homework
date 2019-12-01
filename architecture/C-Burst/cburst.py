# ▪ Memory Cache size: 128 MB
# ▪ Block size: 4 KB
# ▪ Cache replacement algorithm: LRU(性能区域)+C-Bursty(能耗区域)
# ▪ Initial partition: 性能区域(50%)+C-Burst(50%)
# ▪ 可以容忍的 performance loss:(相对全部用 LRU 管理,缺失率提高 10%)
# ▪ 每次划分调整的粒度是 2MB
# ▪ Epoch: 10s

import numpy as np
import os
import sys
import time

SOURCE_PATH = os.environ['HOME'] + "/data/trace/CBursty/"

DESTINATION_PATH = "log"

EPOCH = 10 ** 8
LEVEL = 16
BLOCK_NUM = 1 << 15


class CBurst:
    def __init__(self, source, destination):
        self.source_path = source
        self.destination_path = destination

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
        block_size = int(block_size)
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
        w = open(self.des_path + "miss.log", "w+")
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
            hit_flag = True
            for i in range(block_num):  # 命中检测
                if self.cache_tag.__contains__(tag + i):
                    self.hit += 1
                    t = time.process_time()
                    index = self.cache_tag[tag + i]
                    self.cache_tag.pop(tag + i)
                    self.cache_index.pop(index)
                    self.cache_index[t] = tag + i
                    self.cache_tag[tag + i] = t
                else:
                    hit_flag = False
                    self.miss += 1
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
            if not hit_flag:
                super().saveLog(w, "miss " + current_lines[current_line])


            self.total += 1
            if self.total % 10000 == 0:
                print(current_lines[current_line], self.hit, self.miss, len(self.cache_tag), self.total, "\nmiss rate：",
                      self.miss / (self.miss + self.total), time.process_time() - t1)
                t1 = time.process_time()
            current_lines[current_line] = "0"

        super().closeFile(file_list)
        w.close()
        print(self.hit / (self.miss + self.hit))
        print(self.hit, self.total)
        with open(self.des_path + "result.log", "w+") as result_log:
            result_log.write("accuracy: " + str(self.hit / (self.miss + self.total)) + "\nhit_num: " + str(self.hit) +
                            "\nmiss_num: " + str(self.miss) + "\n lines: " + str(self.total) + "\n")


class CBustOnly(CBurst):
    def __init__(self, source, destination):
        super().__init__(source, destination)
        self.path = source
        self.des_path = destination + "/CBurst/"
        self.block_group = [[] for _ in range(LEVEL)]
        self.blocks = []
        self.groups_size = 0
        self.blocks_size = 0
        self.hit = 0.0
        self.miss = 0.0
        self.total = 0.0

    def checkHit(self, line):
        tag, block_num = super().getBlockTag(line[4], line[5])
        hit_flag = [False for _ in range(block_num)]

        for i in range(block_num):  # in_buffer 中寻找
            if tag + i in self.blocks:
                hit_flag[i] = True
                self.hit += 1
            else:
                self.miss += 1
                hit_flag[i] = False
                self.blocks.append(tag + i)
                if self.groups_size + len(self.blocks) > BLOCK_NUM:
                    pop_size = 0
                    flag = False
                    for row in range(LEVEL - 1, -1, -1):
                        while len(self.block_group[row]):
                            if self.groups_size + len(self.blocks) - pop_size < BLOCK_NUM:
                                flag = True
                                break
                            pop_size += len(self.block_group[row].pop(0))
                        if flag:
                            break
                    self.groups_size -= pop_size

        for i in range(block_num):  # 冷块中寻找
            if not hit_flag[i]:
                for row in range(LEVEL):
                    if hit_flag[i]:
                        break
                    level_len = len(self.block_group[row])
                    level_down = []
                    for col in range(level_len):
                        if tag + i in self.block_group[row][col]:
                            self.block_group[row][col].remove(tag + i)
                            if len(self.block_group[row][col]) > 0 and int(np.log2(len(self.block_group[row][col]))) < row:
                                level_down.append(col)
                            self.blocks.append(tag + i)
                            self.groups_size -= 1
                            hit_flag[i] = True
                            self.hit += 1
                            break
                    for i in range(len(level_down)):
                        temp = self.block_group[row].pop(level_down[i])
                        self.block_group[row - 1].append(temp)

        return all(hit_flag)


    def run(self):
        if not os.path.exists(self.des_path):
            os.makedirs(self.des_path)
        miss_file = open(self.des_path + "miss.log", "w+")
        file_list = super().fileLists()
        current_lines = ["0" for _ in range(len(file_list))]

        end_time = 0
        start_flag = True

        while True:
            for i in range(len(current_lines)):
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
                exit(0)
            line = current_lines[current_line].strip().split(",")

            if start_flag:
                end_time = int(line[0]) + EPOCH
                start_flag = False

            if int(line[0]) > end_time:
                if len(self.blocks) > 0:
                    if self.groups_size + len(self.blocks) > BLOCK_NUM:
                        print("boom")
                        exit(0)
                    group_index = int(np.log2(len(self.blocks)))
                    self.groups_size += len(self.blocks)
                    self.block_group[group_index].append(self.blocks.copy())  # 将当前block_group 加入队列
                    self.blocks.clear()

                end_time = int(line[0]) + EPOCH  # 处理下一个block_group
            hit_flag = self.checkHit(line)
            if not hit_flag:
                super().saveLog(miss_file, "miss " + current_lines[current_line])

            self.total += 1
            if self.total % 50000 == 0:
                print(current_lines[current_line], self.miss, self.hit, self.total,
                      "\naccuracy:", self.hit / (self.hit + self.miss), self.groups_size + len(self.blocks))
            current_lines[current_line] = "0"

        super().closeFile(file_list)
        miss_file.close()
        with open(self.des_path + "result.log", "w+") as result_log:
            result_log.write("accuracy: " + str(self.hit / (self.miss + self.total)) + "\nhit_num: " + str(self.hit) +
                            "\nmiss_num: " + str(self.miss) + "\n lines: " + str(self.total) + "\n")


class CBustLRU(CBurst):
    def __init__(self, source, destination):
        super().__init__(source, destination)
        self.path = source
        self.des_path = destination + "/CBurstLRU/"

        self.block_group = [[] for _ in range(LEVEL)]
        self.blocks = []
        self.cache_tag = {}
        self.cache_index = {}
        self.lru_blocks = BLOCK_NUM / 2
        self.cburst_blocks = BLOCK_NUM / 2
        self.mesh_size = 1 << 9
        self.groups_size = 0
        self.blocks_size = 0
        self.hit = 0.0
        self.miss = 0.0
        self.total = 0.0


        self.lru_hit = 0.0  # lru_only var
        self.lru_miss = 0.0
        self.lru_cache_tag = {}
        self.lru_cache_index = {}

    def addToLRU(self, tag):
        if len(self.cache_tag) < self.lru_blocks:  # 在冷块中命中提到lru区域
            t = time.process_time()
            self.cache_index[t] = tag
            self.cache_tag[tag] = t
        else:
            t = time.process_time()
            tag_temp = list(self.cache_tag.keys())[0]
            index = self.cache_tag[tag_temp]
            self.cache_tag.pop(tag_temp)
            self.cache_index.pop(index)
            self.cache_tag[tag] = t
            self.cache_index[t] = tag

    def checkHit(self, line):
        tag, block_num = super().getBlockTag(line[4], line[5])
        hit_flag = [False for _ in range(block_num)]
        for i in range(block_num):
            if not hit_flag[i]:
                if self.cache_tag.__contains__(tag + i):
                    t = time.process_time()
                    index = self.cache_tag[tag + i]
                    self.cache_tag.pop(tag + i)
                    self.cache_index.pop(index)
                    self.cache_index[t] = tag + i
                    self.cache_tag[tag + i] = t
                    hit_flag[i] = True

        for i in range(block_num):  # in_buffer 中寻找
            if not hit_flag[i]:
                if tag + i in self.blocks:
                    hit_flag[i] = True
                    self.addToLRU(tag + i)
                else:
                    self.blocks.append(tag + i)
                    hit_flag[i] = False
                    if self.groups_size + len(self.blocks) > self.cburst_blocks:
                        pop_size = 0
                        flag = False
                        for row in range(LEVEL - 1, -1, -1):
                            while len(self.block_group[row]):
                                if self.groups_size + len(self.blocks) - pop_size < self.cburst_blocks:
                                    flag = True
                                    break
                                pop_size += len(self.block_group[row].pop(0))
                            if flag:
                                break
                        self.groups_size -= pop_size
                        if self.groups_size + len(self.blocks) > self.cburst_blocks:  # 如果cburst区域很小了，就需要吧in buffer区域的数据加入lru区域
                            over_size  = int(self.groups_size + len(self.blocks) - self.cburst_blocks)
                            for i in range(over_size):
                                if self.cache_tag.__contains__(self.blocks[i]):
                                    t = time.process_time()
                                    index = self.cache_tag[self.blocks[i]]
                                    self.cache_tag.pop(self.blocks[i])
                                    self.cache_index.pop(index)
                                    self.cache_index[t] = self.blocks[i]
                                    self.cache_tag[self.blocks[i]] = t
                                else:
                                    self.addToLRU(self.blocks[i])
                            for i in range(over_size):
                                self.blocks.pop(0)

        for i in range(block_num):  # 冷块中寻找
            if not hit_flag[i]:
                for row in range(LEVEL):
                    if hit_flag[i]:
                        break
                    level_len = len(self.block_group[row])
                    level_down = []
                    for col in range(level_len):
                        if tag + i in self.block_group[row][col]:
                            self.block_group[row][col].remove(tag + i)
                            if len(self.block_group[row][col]) > 0 and int(np.log2(len(self.block_group[row][col]))) < row:
                                level_down.append(col)
                            self.addToLRU(tag + i)  # 添加到LRU区中
                            self.groups_size -= 1
                            hit_flag[i] = True
                            break
                    for i in range(len(level_down)):
                        temp = self.block_group[row].pop(level_down[i])
                        self.block_group[row - 1].append(temp)
        for i in range(len(hit_flag)):
            if hit_flag[i]:
                self.hit += 1
            else:
                self.miss += 1
        return all(hit_flag)

    def LRUOnly(self, line):
        tag, block_num = super().getBlockTag(line[4], line[5])
        hit_flag = True
        for i in range(block_num):  # 命中检测
            if self.lru_cache_tag.__contains__(tag + i):
                self.lru_hit += 1
                t = time.process_time()
                index = self.lru_cache_tag[tag + i]
                self.lru_cache_tag.pop(tag + i)
                self.lru_cache_index.pop(index)
                self.lru_cache_index[t] = tag + i
                self.lru_cache_tag[tag + i] = t
            else:
                hit_flag = False
                self.lru_miss += 1
                if len(self.lru_cache_tag) < BLOCK_NUM:
                    t = time.process_time()
                    self.lru_cache_index[t] = tag + i
                    self.lru_cache_tag[tag + i] = t
                else:
                    t = time.process_time()
                    tag_temp = list(self.lru_cache_tag.keys())[0]
                    index = self.lru_cache_tag[tag_temp]
                    self.lru_cache_tag.pop(tag_temp)
                    self.lru_cache_index.pop(index)
                    self.lru_cache_tag[tag + i] = t
                    self.lru_cache_index[t] = tag + i




    def run(self):
        if not os.path.exists(self.des_path):
            os.makedirs(self.des_path)
        miss_file = open(self.des_path + "miss.log", "w+")
        file_list = super().fileLists()
        current_lines = ["0" for _ in range(len(file_list))]

        end_time = 0
        start_flag = True

        while True:
            for i in range(len(current_lines)):
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
                exit(0)
            line = current_lines[current_line].strip().split(",")

            if start_flag:
                end_time = int(line[0]) + EPOCH
                start_flag = False

            if int(line[0]) > end_time:
                if len(self.blocks) > 0:
                    if self.groups_size + len(self.blocks) > self.cburst_blocks > self.mesh_size:
                        print("boom")
                        exit(0)
                    group_index = int(np.log2(len(self.blocks)))
                    self.groups_size += len(self.blocks)
                    if self.groups_size > self.cburst_blocks:
                        print("error")
                        exit(0)
                    self.block_group[group_index].append(self.blocks.copy())  # 将当前block_group 加入队列
                    self.blocks.clear()

            hit_flag = self.checkHit(line)
            self.LRUOnly(line)

            if not hit_flag:
                super().saveLog(miss_file, "miss " + current_lines[current_line])
            self.total += 1
            if self.total % 5000 == 0:
                if abs(((self.miss / (self.miss + self.hit)) - (self.lru_miss / (self.lru_miss + self.lru_hit)))) > 0.1 and self.cburst_blocks > self.mesh_size:
                    self.lru_blocks += self.mesh_size
                    self.cburst_blocks -= self.mesh_size
                    if self.cburst_blocks < self.groups_size:
                        pop_num = int(self.groups_size - self.cburst_blocks)
                        pop_size = 0
                        flag = False
                        for row in range(LEVEL - 1, -1, -1):
                            while len(self.block_group[row]):
                                if pop_size >= pop_num:
                                    flag = True
                                    break
                                pop_size += len(self.block_group[row].pop(0))
                            if flag:
                                break
                        self.groups_size -= pop_size
                elif abs(((self.miss / (self.miss + self.hit)) - (self.lru_miss / (self.lru_hit + self.lru_miss)))) < 0.1 and self.lru_blocks > self.mesh_size:
                    self.lru_blocks -= self.mesh_size
                    if self.lru_blocks < len(self.cache_tag):
                        pop_num = int(len(self.cache_tag) - self.lru_blocks)
                        temp_tag = list(self.cache_tag.keys())
                        temp_index = list(self.cache_index.keys())
                        for i in range(pop_num):
                            if i < len(temp_tag):
                                self.cache_index.pop(temp_index[i])
                                self.cache_tag.pop(temp_tag[i])
                        self.cburst_blocks += self.mesh_size
            if self.total % 10000 == 0:
                print(current_lines[current_line], self.lru_miss / (self.lru_hit + self.lru_miss), self.miss / (self.hit + self.miss), self.total, "\n",
                      self.lru_blocks, self.cburst_blocks, "\n",
                      len(self.cache_tag), self.groups_size + len(self.blocks))
            current_lines[current_line] = "0"

        super().closeFile(file_list)
        miss_file.close()
        with open(self.des_path + "result.log", "w+") as result_log:
            result_log.write("accuracy: " + str(self.hit / (self.miss + self.total)) + "\nhit_num: " + str(self.hit) +
                            "\nmiss_num: " + str(self.miss) + "\n lines: " + str(self.total) + "\n")






if __name__ == '__main__':
    if not os.path.exists(DESTINATION_PATH):
        os.makedirs(DESTINATION_PATH)

    choose = input('1：第一题\n2:第二题 \n3:第三题\n')
    if choose == '1':
        test = LRUOnly(SOURCE_PATH, DESTINATION_PATH)
        test.run()
    elif choose == '2':
        test = CBustOnly(SOURCE_PATH, DESTINATION_PATH)
        test.run()
    elif choose == '3':
        test = CBustLRU(SOURCE_PATH, DESTINATION_PATH)
        test.run()


