class TreeNode(object):
    def __init__(self, labelName, value, data, clsData):
        """
        :param labelName: 分类类别名称
        :param value: 分类类别值
        :param data: 当前包含数据
        :param clsData: 当前包含的分类数据
        :param leaf: 是否为最后的叶子结果节点
        :param result: 是叶子节点的时候记录输出的分类结果
        :param nodeList: 子节点集合
        """
        self.labelName = labelName
        self.value = value
        self.data = data
        self.clsData = clsData
        self.leaf = False
        self.result = None
        self.nodeList = []