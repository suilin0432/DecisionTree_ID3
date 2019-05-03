from Data import dataDict
from TreeID3 import TreeID3
# 划分子节点之后继续对其余的子节点进行划分
# print(dataDict)
tree = TreeID3(dataDict.copy(), "Class")

tree.run()
print("Begin traveling the Tree.")
tree.travel()

# 下面是测试
print("\n\n")

# 父属性的信息熵测试
print(tree.clsGainCalculate(dataDict["Class"]))

# 子属性的信息熵测试
print(tree.entropyCalculate(dataDict["Job"], dataDict["Class"]))

# 测试决策判断
valueDict = {
    "Education":"undergraduate",
    "Sex":"man",
    "Language":"cet4",
    "Character":"a1",
    "Job":"b1"
}
print("Decision test.")
tree.test(valueDict)

