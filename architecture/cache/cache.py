"""
cache size : 128KB
block size : 8 Bytes
for a 64-bit memory address
cache replacement algorithm : LRU
"""

import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

ADDRESS = 64
BLOCK = 1 << 14
SOURCE = "trace"
DESTINATION = "log"


def save(f, addr, state):
    """

    :param f:保存文件的指针
    :param addr: miss的地址
    :param state: miss或者hit 字符串类型
    :return:
    """
    f.write(addr + " " + state + "\n")
    return


def hexToBin(hex):
    """

    :param hex:16进制字符串
    :return: 转换成二进制字符串
    """
    result = int(hex, 16)
    result = bin(result)
    result = result[2:]
    result = result.rjust(ADDRESS, '0')
    return result


class DirectMapping:
    def __init__(self):
        self.cache = np.zeros([BLOCK, 3], dtype=np.int64)  # 0：tag 1：offset 2：LRU
        self.hit_num = 0
        self.miss_num = 0
        self.total = 0

    def run(self):
        source_files = os.listdir(SOURCE)
        des_folder = DESTINATION + "/DirectMapping/"
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)
        with open(des_folder + "result.log", encoding="utf-8", mode='w+') as result_log:  # 循环遍历trace中的文件
            for file in source_files:
                self.cache.fill(0)
                self.hit_num = 0
                self.miss_num = 0
                self.total = 0
                name = file.split(".")[0]

                with open(SOURCE + "/" + file, encoding="utf-8") as source, \
                        open(DESTINATION + "/DirectMapping/" + name + ".log", encoding="utf-8", mode='w+') as log:
                    for line in source:
                        self.total += 1
                        addr = hexToBin(line.split()[1])
                        tag = int(addr[0:47], 2)
                        index = int(addr[47:47 + 14], 2)
                        offset = int(addr[47 + 14:], 2)
                        if self.cache[index][0] != tag:
                            self.miss_num += 1
                            save(log, line.split()[1], "miss")
                            self.miss(tag, index, offset)
                        elif self.cache[index][0] == tag:
                            self.hit_num += 1
                            self.hit(index)
                    result_log.write("DirectMapping " + name + " hit rate is " + str(self.getHitRate()) + "\n")
                    print(name, self.getHitRate())
        print()

    def LRU(self, index):
        return

    def hit(self, index):
        self.LRU(index)
        return

    def miss(self, tag, index, offset):
        self.cache[index][0] = tag
        self.cache[index][1] = offset
        self.LRU(index)
        return

    def getHitRate(self):
        hit_rate = self.hit_num / self.total
        return hit_rate


class GroupConnection:
    def __init__(self):
        self.cache = np.zeros([BLOCK, 3], dtype=np.int64)  # 0：tag 1：offset 2：LRU 3：候选位的编码
        self.ways = [2, 4, 8, 16]
        self.group_size = 2
        self.hit_num = 0
        self.first_hit = 0
        self.miss_num = 0
        self.no_first_hit = 0
        self.total = 0
        self.index_offset = 0
        self.des_folder = DESTINATION + "/GroupConnection/"

    def run(self):
        source_files = os.listdir(SOURCE)
        if not os.path.exists(self.des_folder):
            os.makedirs(self.des_folder)
        with open(self.des_folder + "result.log", encoding="utf-8", mode='w+') as result_log:  # 循环遍历trace中的文件
            for way in self.ways:
                self.group_size = way
                des_folder = self.des_folder + str(self.group_size) + "ways/"
                if not os.path.exists(des_folder):
                    os.makedirs(des_folder)
                for file in source_files:  # 遍历所有的trace
                    # file = "astar.trace"
                    self.cache.fill(0)  # 重新初始化
                    self.hit_num = 0
                    self.miss_num = 0
                    self.total = 0
                    self.index_offset = int(np.log2(way))
                    name = file.split(".")[0]

                    with open(SOURCE + "/" + file, encoding="utf-8") as source, \
                            open(des_folder + name + ".log", encoding="utf-8", mode='w+') as log:
                        for line in source:
                            self.total += 1
                            addr = hexToBin(line.split()[1])  # 补全64位地址
                            tag = int(addr[0:47 + self.index_offset], 2)
                            group = int(addr[47 + self.index_offset:61], 2)
                            offset = int(addr[61:], 2)
                            hit_flag = False
                            for i in range(self.group_size):
                                if self.cache[group * self.group_size + i][0] == tag:
                                    # save(log, line.split()[1], "hit" + str(index))
                                    hit_flag = True
                                    self.hit(i, group)
                                    break
                            if not hit_flag:
                                save(log, line.split()[1], "miss")
                                self.miss(tag, 0, offset, group)
                        hit_rate = self.getHitRate()
                        result_log.write("GroupConnection " + name + " for " + str(self.group_size) +
                                         " ways prediction group connection the hit rate is " + str(hit_rate) + "\n")
                        print(name, "for", way, "ways prediction group connection the hit rate is ", hit_rate)
                result_log.write("\n")
                print()
        print()

    def LRU(self, index, group, state):
        flag = False
        lru_result = -1
        if not state:  # hit的情况
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] != 0:
                    self.cache[group * self.group_size + i][2] += 1
            self.cache[group * self.group_size + index][2] = 1
            return -100
        else:  # miss的情况
            max_num = -1
            max_index = -1
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] == 0:  # 如果有空位直接加入
                    if not flag:
                        lru_result = i
                        flag = True
                else:  # 没有空位的话整体 + 1
                    if self.cache[group * self.group_size + i][2] > max_num:  # 找出当下最大的index
                        max_num = self.cache[group * self.group_size + i][2]
                        max_index = i
                    if self.cache[group * self.group_size + i][2] != 0:
                        self.cache[group * self.group_size + i][2] += 1  # 把所有的index +1 更新
            if not flag:
                lru_result = max_index
        return lru_result

    def hit(self, index, group):
        self.hit_num += 1
        self.LRU(index, group, False)
        return

    def miss(self, tag, index, offset, group):
        self.miss_num += 1
        index_in = self.LRU(index, group, state=True)
        if index_in < self.group_size:
            self.cache[group * self.group_size + index_in][0] = tag  # 根据LRU算法跟新tag
            self.cache[group * self.group_size + index_in][1] = offset
            self.cache[group * self.group_size + index_in][2] = 1
        return index_in

    def getHitRate(self):
        hit_rate = self.hit_num / self.total
        return hit_rate


class GroupConnectionChangeSize:
    def __init__(self):
        self.size = [3, 4, 5, 6, 7]
        self.index_offset = 17
        self.index_size = 14
        self.cache = np.zeros([14, 3], dtype=np.int64)
        self.group_size = 4
        self.hit_num = 0
        self.miss_num = 0
        self.total = 0
        self.des_folder = DESTINATION + "/GroupConnectionChangeSize/"

    def run(self):
        source_files = os.listdir(SOURCE)
        if not os.path.exists(self.des_folder):
            os.makedirs(self.des_folder)
        with open(self.des_folder + "result.log", encoding="utf-8", mode='w+') as result_log:  # 保存个文件中的准确率等信息
            for size in self.size:
                des_folder = self.des_folder + str(1 << size) + "Byte/"
                if not os.path.exists(des_folder):
                    os.makedirs(des_folder)
                for file in source_files:  # 循环遍历trace中的文件
                    self.cache = np.zeros([1 << self.index_size, 3], dtype=np.int64)
                    self.hit_num = 0
                    self.miss_num = 0
                    self.total = 0
                    name = file.split(".")[0]

                    with open(SOURCE + "/" + file, encoding="utf-8") as source, \
                            open(des_folder + name + ".log", encoding="utf-8", mode='w+') as log:
                        for line in source:
                            self.total += 1
                            addr = hexToBin(line.split()[1])
                            tag = int(addr[0:49], 2)
                            group = int(addr[49:64 - size], 2)
                            offset = int(addr[61:], 2)
                            hit_flag = False
                            for i in range(self.group_size):
                                if self.cache[group * self.group_size + i][0] == tag:
                                    # save(log, line.split()[1], "hit" + str(index))
                                    hit_flag = True
                                    self.hit(i, group)
                                    break
                            if not hit_flag:
                                save(log, line.split()[1], "miss")
                                self.miss(tag, 0, offset, group)
                        result_log.write("GroupConnectionChangeSize " + name + " for " + str(
                            1 << size) + " block size, the hit rate is " + str(
                            self.getHitRate()) + "\n")
                        print(name, "for", 1 << size, " block size, the hit rate is", self.getHitRate())
                result_log.write("\n")
                print()
        print()

    def LRU(self, index, group, state):
        flag = False
        lru_result = -1
        if not state:  # hit的情况
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] != 0:
                    self.cache[group * self.group_size + i][2] += 1
            self.cache[group * self.group_size + index][2] = 1
            return -100
        else:  # miss的情况
            max_num = -1
            max_index = -1
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] == 0:  # 如果有空位直接加入
                    if not flag:
                        lru_result = i
                        flag = True
                else:  # 没有空位的话整体 + 1
                    if self.cache[group * self.group_size + i][2] > max_num:  # 找出当下最大的index
                        max_num = self.cache[group * self.group_size + i][2]
                        max_index = i
                    if self.cache[group * self.group_size + i][2] != 0:
                        self.cache[group * self.group_size + i][2] += 1  # 把所有的index +1 更新
            if not flag:
                lru_result = max_index
        return lru_result

    def hit(self, index, group):
        self.hit_num += 1
        self.LRU(index, group, False)
        return

    def miss(self, tag, index, offset, group):
        self.miss_num += 1
        index_in = self.LRU(index, group, state=True)
        if index_in < self.group_size:
            self.cache[group * self.group_size + index_in][0] = tag  # 根据LRU算法跟新tag
            self.cache[group * self.group_size + index_in][1] = offset
            self.cache[group * self.group_size + index_in][2] = 1
        return index_in

    def getHitRate(self):
        hit_rate = self.hit_num / self.total
        return hit_rate


class MRUGroupConnection:
    def __init__(self):
        self.cache = np.zeros([BLOCK, 3], dtype=np.int64)  # 0：tag 1：offset 2：LRU
        self.ways = [2, 4, 8, 16]
        self.group_size = 2
        self.hit_num = 0
        self.first_hit = 0
        self.miss_num = 0
        self.no_first_hit = 0
        self.total = 0
        self.index_offset = 0
        self.des_folder = DESTINATION + "/MRUGroupConnection/"

    def run(self):
        source_files = os.listdir(SOURCE)
        if not os.path.exists(self.des_folder):
            os.makedirs(self.des_folder)
        with open(self.des_folder + "result.log", encoding="utf-8", mode='w+') as result_log:  # 循环遍历trace中的文件
            for way in self.ways:
                self.group_size = way
                des_folder = self.des_folder + str(self.group_size) + "ways/"
                if not os.path.exists(des_folder):
                    os.makedirs(des_folder)
                for file in source_files:  # 遍历所有的trace
                    # file = "astar.trace"
                    mru = np.zeros(BLOCK // self.group_size, dtype=np.int64)
                    self.cache.fill(0)  # 重新初始化
                    self.hit_num = 0
                    self.miss_num = 0
                    self.first_hit = 0
                    self.no_first_hit = 0
                    self.total = 0
                    self.index_offset = int(np.log2(way))
                    name = file.split(".")[0]

                    with open(SOURCE + "/" + file, encoding="utf-8") as source, \
                            open(des_folder + name + ".log", encoding="utf-8", mode='w+') as log:
                        for line in source:
                            self.total += 1
                            addr = hexToBin(line.split()[1])  # 补全64位地址
                            tag = int(addr[0:47 + self.index_offset], 2)
                            group = int(addr[47 + self.index_offset:61], 2)
                            offset = int(addr[61:], 2)
                            hit_flag = False
                            if self.cache[group * self.group_size + mru[group]][0] == tag:
                                self.first_hit += 1
                                self.hit(mru[group], group)
                                # save(log, line.split()[1], "hit ")
                                continue
                            for i in range(self.group_size):
                                if self.cache[group * self.group_size + i][0] == tag:
                                    # save(log, line.split()[1], "hit")
                                    self.no_first_hit += 1
                                    mru[group] = i
                                    hit_flag = True
                                    self.hit(i, group)
                                    break
                            if not hit_flag:
                                save(log, line.split()[1], "miss")
                                mru[group] = self.miss(tag, 0, offset, group)
                        hit_rate = self.getHitRate()
                        result_log.write("MRU prediction GroupConnection " + name + " for " + str(self.group_size) +
                                         " ways MRU prediction group connection the hit rate is " + str(hit_rate[0]) +
                                         " first hit rate is " + str(hit_rate[1]) +
                                         " no first hit rate is " + str(hit_rate[2]) + "\n")
                        print(name, "for", way,
                              "ways MRU prediction group connection the hit rate, first hit rate and no first hit rate are",
                              hit_rate[0], hit_rate[1], hit_rate[2])
                result_log.write("\n")
                print()
        print()

    def LRU(self, index, group, state):
        flag = False
        lru_result = -1
        if not state:  # hit的情况
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] != 0:
                    self.cache[group * self.group_size + i][2] += 1
            self.cache[group * self.group_size + index][2] = 1
            return -100
        else:  # miss的情况
            max_num = -1
            max_index = -1
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] == 0:  # 如果有空位直接加入
                    if not flag:
                        lru_result = i
                        flag = True
                else:  # 没有空位的话整体 + 1
                    if self.cache[group * self.group_size + i][2] > max_num:  # 找出当下最大的index
                        max_num = self.cache[group * self.group_size + i][2]
                        max_index = i
                    if self.cache[group * self.group_size + i][2] != 0:
                        self.cache[group * self.group_size + i][2] += 1  # 把所有的index +1 更新
            if not flag:
                lru_result = max_index
        return lru_result

    def hit(self, index, group):
        self.hit_num += 1
        self.LRU(index, group, False)
        return

    def miss(self, tag, index, offset, group):
        self.miss_num += 1
        index_in = self.LRU(index, group, state=True)
        if index_in < self.group_size:
            self.cache[group * self.group_size + index_in][0] = tag  # 根据LRU算法跟新tag
            self.cache[group * self.group_size + index_in][1] = offset
            self.cache[group * self.group_size + index_in][2] = 1
        return index_in

    def getHitRate(self):
        hit_rate = self.hit_num / self.total
        first_hit_rate = self.first_hit / self.total
        no_first_hit_rate = self.no_first_hit / self.total
        return hit_rate, first_hit_rate, no_first_hit_rate


class MultiColumn:
    def __init__(self):
        self.cache = np.zeros([BLOCK, 4], dtype=np.int64)  # 0：tag 1：offset 2：LRU 3：候选位的编码
        self.ways = [2, 4, 8, 16]
        self.group_size = 2
        self.hit_num = 0
        self.first_hit = 0
        self.no_first_hit = 0
        self.miss_num = 0
        self.index_offset = 0
        self.total = 0
        self.des_folder = DESTINATION + "/MultiColumn/"

    def run(self):
        source_files = os.listdir(SOURCE)
        if not os.path.exists(self.des_folder):
            os.makedirs(self.des_folder)
        with open(self.des_folder + "result.log", encoding="utf-8", mode='w+') as result_log:
            count = 0
            for way in self.ways:
                count += 1
                self.group_size = way
                des_folder = self.des_folder + str(self.group_size) + "ways/"
                if not os.path.exists(des_folder):
                    os.makedirs(des_folder)
                for file in source_files:  # 遍历所有的trace
                    self.cache.fill(0)  # 重新初始化
                    self.hit_num = 0
                    self.miss_num = 0
                    self.first_hit = 0
                    self.no_first_hit = 0
                    self.total = 0
                    self.index_offset = int(np.log2(way))
                    name = file.split(".")[0]

                    with open(SOURCE + "/" + file, encoding="utf-8") as source, \
                            open(des_folder + name + ".log", encoding="utf-8", mode='w+') as log:
                        for line in source:  # 遍历文件中的所有行
                            self.total += 1
                            addr = hexToBin(line.split()[1])
                            tag = int(addr[0:47 + self.index_offset], 2)
                            group = int(addr[47 + self.index_offset:61], 2)
                            offset = int(addr[61:], 2)

                            select_location = int(bin(tag)[-self.index_offset:], 2)
                            if self.cache[group * self.group_size + select_location][0] == tag:  # 根据tag后几位直接命中，则为一次命中
                                self.first_hit += 1
                                self.hit(select_location, group)  # 在主位上命中，不需要交换，跟新LRU即可
                                continue

                            str_location = bin(self.cache[group * self.group_size + select_location][3])[2:].rjust(
                                self.group_size, '0')
                            hit_flag = False
                            for i in range(self.group_size):
                                if str_location[i] == '1':
                                    if self.cache[group * self.group_size + i][0] == tag:
                                        # save(log, line.split()[1], "hit")
                                        self.no_first_hit += 1
                                        hit_flag = True
                                        self.hit(i, group)
                                        self.swapTag(group * self.group_size + i,
                                                     group * self.group_size + select_location)
                                        break
                            if not hit_flag:
                                """
                                不命中的情况下,首先使用LRU替换算法得到一个替换块，记为location1，修改location1对应位置上的数据
                                对应的候选位置，接下来交换location1与select_location的tag，接下来修改select_location的后选位，
                                
                                """
                                replacement = self.miss(tag, self.index_offset, offset, group)
                                str_location = str_location[:replacement] + '1' + str_location[replacement + 1:]
                                self.cache[group * self.group_size + select_location][3] = int(str_location, 2)
                                self.swapTag(group * self.group_size + select_location,
                                             group * self.group_size + replacement)

                        hit_rate = self.getHitRate()
                        result_log.write("MultiColumn prediction " + name + " for " + str(self.group_size) +
                                         " ways group connection the hit rate is " + str(hit_rate[0]) +
                                         " first hit rate is " + str(hit_rate[1]) +
                                         " no first hit rate is " + str(hit_rate[2]) + "\n")
                        print(name, "for", way,
                              "ways MultiColumn prediction group connection the hit rate, first hit rate and no first hit rate are",
                              hit_rate[0], hit_rate[1], hit_rate[2])
                result_log.write("\n")
                print()
        print()

    def swapTag(self, index1, index2):
        # self.cache[index1][:3], self.cache[index2][:3] = self.cache[index2][:3], self.cache[index1][:3]
        for i in range(3):
            temp = self.cache[index1][i]
            self.cache[index1][i] = self.cache[index2][i]
            self.cache[index2][i] = temp

    def LRU(self, index, group, state):
        flag = False
        lru_result = -1
        if not state:  # hit的情况
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] != 0:
                    self.cache[group * self.group_size + i][2] += 1
            self.cache[group * self.group_size + index][2] = 1
            return -100
        else:  # miss的情况
            max_num = -1
            max_index = -1
            for i in range(self.group_size):
                if self.cache[group * self.group_size + i][2] == 0:  # 如果有空位直接加入
                    if not flag:
                        lru_result = i
                        flag = True
                else:  # 没有空位的话整体 + 1
                    if self.cache[group * self.group_size + i][2] > max_num:  # 找出当下最大的index
                        max_num = self.cache[group * self.group_size + i][2]
                        max_index = i
                    if self.cache[group * self.group_size + i][2] != 0:
                        self.cache[group * self.group_size + i][2] += 1  # 把所有的index +1 更新
            if not flag:
                lru_result = max_index
        return lru_result

    def hit(self, index, group):
        self.hit_num += 1
        self.LRU(index, group, False)
        return

    def miss(self, tag, index, offset, group):
        self.miss_num += 1
        index_in = self.LRU(index, group, state=True)

        old_tag = self.cache[group * self.group_size + index_in][0]
        old_tag = bin(old_tag)[2:]
        select_location = int(old_tag[-index:], 2)  # 取出替换数组对应的组号
        select_num = self.cache[group * self.group_size + select_location][3]
        str_location = bin(select_num)[2:].rjust(self.group_size, '0')
        str_location = str_location[:index_in] + '0' + str_location[index_in + 1:]
        self.cache[group * self.group_size + select_location][3] = int(str_location, 2)  # 跟新被替换元素的主位上的候选位

        if index_in < self.group_size:
            self.cache[group * self.group_size + index_in][0] = tag  # 根据LRU算法跟新tag
            self.cache[group * self.group_size + index_in][1] = offset
            self.cache[group * self.group_size + index_in][2] = 1
        return index_in

    def getHitRate(self):
        hit_rate = self.hit_num / self.total
        first_hit_rate = self.first_hit / self.total
        no_first_hit_rate = self.no_first_hit / self.total
        return hit_rate, first_hit_rate, no_first_hit_rate


if __name__ == '__main__':
    des_folder = DESTINATION
    if not os.path.exists(des_folder):
        os.makedirs(des_folder)
    n = input("0:全部执行\n1：执行第一题\n2：执行第二题\n3：执行第三题\n4：执行第四题\n5:执行问题六\n")
    n = int(n)
    if n == 0:
        with ProcessPoolExecutor(max_work=5) as process_pool:
            print("DirectMapping:")
            process_pool.submit(DirectMapping().run)
            print("GroupConnection:")
            process_pool.submit(GroupConnection().run)
            print("MRUGroupConnection:")
            process_pool.submit(MRUGroupConnection().run)
            print("MultiColumn:")
            process_pool.submit(MultiColumn().run)
            print("GroupConnectionChangeSize")
            process_pool.submit(GroupConnectionChangeSize().run)
    elif n == 1:
        print("DirectMapping:")
        DirectMapping().run()
    elif n == 2:
        print("GroupConnection:")
        GroupConnection().run()
    elif n == 3:
        print("MRUGroupConnection:")
        MRUGroupConnection().run()
    elif n == 4:
        print("MultiColumn:")
        MultiColumn().run()
    elif n == 5:
        print("GroupConnectionChangeSize")
        GroupConnectionChangeSize().run()
