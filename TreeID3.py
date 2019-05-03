import math
from TreeNode import TreeNode
class TreeID3(object):
    def __init__(self, data, className):
        self.clsData = data[className]
        data.pop(className)
        self.data = data
        self.clsIndex = {}
        self.indexCls = {}
        index = 0
        for i in self.clsData:
            if i not in self.clsIndex:
                self.clsIndex[i] = index
                self.indexCls[index] = i
                index += 1
        self.clsLength = index

    def run(self):
        self.root = TreeNode("root", "root", self.data, self.clsData)
        self.build(self.root)

    def travel(self):
        self.T(self.root)

    def T(self, root):
        print("LabelName: {0}, Value: {1}, IsLeaf: {2}, Result: {3}".format(root.labelName, root.value, root.leaf, root.result))
        if not root.nodeList:
            return
        for i in root.nodeList:
            self.T(i)

    def build(self, root):
        """
        首先计算父节点的 Gain 然后计算所有可分裂属性的 Gain_item 找到信息增益最大的那个, 如果信息增益都小于 0 那么就不继续分裂 分裂之后对子节点继续分裂
        PS: 后面会强制要求没有数据的时候不进行子节点的分裂
        终止条件:
        1. 如果data只有一个类别
        2. 如果cls都是一个类别
        3. 信息增益没有任何一个是增加的情况下
        """
        data = root.data.copy()
        clsData = root.clsData.copy()
        # 记录每个类别出现次数
        clsCal = [0] * self.clsLength
        for i in clsData:
            clsCal[self.clsIndex[i]] += 1
        # 如果都是一个类别了，那么就当做叶子节点就可以了
        if max(clsCal) == len(clsData):
            root.leaf = True
            root.result = clsData[0]
            return

        # 如果只有一个标签了那么找最大的分配就好了
        if not data:
            root.leaf = True
            root.result = self.indexCls[clsCal.index(max(clsCal))]
            return

        # 计算类别的信息增益Gain
        gain = self.clsGainCalculate(clsData)

        # 计算每一次分裂的信息增益量
        gainList = {}
        for item in data.keys():
            gainList[item] = self.entropyCalculate(data[item], clsData)
        # print(gainList)
        # 找到最小的信息增益量
        minValue = 10
        minItem = ""
        for item in gainList.keys():
            if gainList[item] < minValue:
                minValue = gainList[item]
                minItem = item

        # 如果信息增益都小于0 那么就不分裂了 直接给定类别
        if minValue > gain:
            root.leaf = True
            root.result = self.indexCls[clsCal.index(max(clsCal))]
            return

        # 否则的话开始进行信息的分裂
        itemIndex = {}
        for i in range(len(data[minItem])):
            if data[minItem][i] not in itemIndex:
                itemIndex[data[minItem][i]] = [i]
            else:
                itemIndex[data[minItem][i]].append(i)

        for key in itemIndex.keys():
            # print(key)
            # 直接默认不会对没有数据的进行分裂
            # 将该类别的数据取出来然后进行正式的节点分裂
            subData = {}
            subClass = []
            for k in data.keys():
                subData[k] = []
                for item in itemIndex[key]:
                    subData[k].append(data[k][item])
            for item in itemIndex[key]:
                subClass.append(clsData[item])

            subData.pop(minItem)

            # 分裂
            node = TreeNode(minItem, key, subData, subClass)
            root.nodeList.append(node)
            self.build(node)


    def clsGainCalculate(self, cls):
        length = len(cls)
        clsNum = [0] * self.clsLength
        value = 0
        for i in cls:
            clsNum[self.clsIndex[i]] += 1
        for i in clsNum:
            if i == 0:
                continue
            value -= i/length * math.log2(i/length)
        return value

    def entropyCalculate(self, data, cls):
        """
        itemsDict{
            data[i]:[cls1, cls2, cls3 ......]
        }
        """
        itemsDict = {}
        length = len(data)
        V = 0
        for i in range(length):
            if data[i] not in itemsDict:
                itemsDict[data[i]]=[0] * self.clsLength
            itemsDict[data[i]][self.clsIndex[cls[i]]] += 1
        for key, value in itemsDict.items():
            l = sum(value)
            v = 0
            for i in value:
                if i == 0:
                    continue
                v -= i/l * math.log2(i/l)
            # print(l,length,v)
            V += l/length * v
        return V
    def test(self, valueDict):
        node = self.root
        while not node.leaf:
            print("LabelName: {0}, Value: {1}, IsLeaf: {2}, Result: {3}".format(node.labelName, node.value, node.leaf,node.result))
            for i in node.nodeList:
                if valueDict[i.labelName] == i.value:
                    node = i
        print("The classification is: ",node.result)