# Decision Tree Regressor
import numpy as np

class RegressorNode:
    """ 回归决策树中的结点 """

    def __init__(self, feature_idx:int=None, value:float=None, mse:float=None,
                 left_child=None, right_child=None):
        """ 初始化决策树节点

        parameter:
            1. feature_idx : 子集划分所依据的特征的下标
            2. value       : 子集划分所依据的特征的阈值（当节点为叶结点时为分类值）
            3. mse         : 样本的均方误差
            4. left_child  : 左子节点
            5. right_child : 右子节点
        """
        self.feature_idx = feature_idx
        self.value       = value
        self.mse         = mse
        self.left_child  = left_child
        self.right_child = right_child

class DecisionTreeRegressor:
    """ 回归决策树 """

    def __init__(self, max_depth:int=None, min_samples_leaf:int=None):
        """ 初始化决策树（设置超参数的值）

        parameter:
            1. max_depth        : 决策树最大深度
            2. min_samples_leaf : 叶节点最小样本数
        """
        self.max_depth        = max_depth
        self.min_samples_leaf = min_samples_leaf

    def fit(self, x:list, y:list):
        """ 使用训练集拟合回归决策树

        parameter:
            1. x: 训练集数据（二维列表，x[i] 表示第 i 个样本，x[i][j] 表示第 i 个样本的第 j 个特征）
            2. y: 训练数据像集（y[i] 表示第 i 个样本的像）
        """
        x = np.array(x)
        y = np.array(y)
        self.root = self.buildTree(x, y, 0)

    def buildTree(self, x:list, y:list, depth:int) -> RegressorNode:
        """ 根据训练数据递归构建回归决策树

        parameter:
            1. x     : 样本特征
            2. y     : 样本真值
            3. depth : 决策树深度

        Tips:
            在回归决策树中，节点的值被设置为节点所拥有的样本的真值的均值
        """
        node = RegressorNode()
        # 递归终止条件
        if len(y) == 0:  # 当没有样本时直接返回
            return node  # 最后构建出来的应该是一个满二叉树，所以可能出现无样本的叶节点
                         # 但是该叶节点不可能被访问到！
        y_unique = np.unique(y)  # 获取所有不同的真值
        if len(y_unique) == 1:   # 只存在一种真值时，令其为分类值
            node.value = y_unique[0]
            return node
        if self.max_depth is not None and depth >= self.max_depth:
            node.value = np.average(y)  # 如果节点所在深度大于等于预设的最大值，则令其为叶节点，并设置分类值为所有样本的均值
            return node
        if self.min_samples_leaf is not None and len(y) <= self.min_samples_leaf:
            node.value = np.average(y)  # 如果节点的样本数少于等于预设的最小值，则令其为叶节点，并设置分类值为所有样本的均值
            return node

        # 计算中间节点的参数
        min_mse         = np.inf     # 均方误差最小值
        min_feature_idx = None       # 使得均方误差最小的特征的索引值
        min_threshold   = None       # 使得均方误差最小的特征的划分阈值
        for i in range(x.shape[1]):  # 寻找使得均方误差最小的特征及划分阈值
            mse, threshold = self.calcMse(x[:, i], y)
            if min_mse > mse:
                min_mse         = mse
                min_feature_idx = i
                min_threshold   = threshold

        node.mse         = min_mse
        node.feature_idx = min_feature_idx
        node.value       = min_threshold

        # print(min_threshold)

        x_lt             = x[:, min_feature_idx] < min_threshold
        x_gt             = x[:, min_feature_idx] > min_threshold
        node.left_child  = self.buildTree(x[x_lt,:], y[x_lt], depth + 1)
        node.right_child = self.buildTree(x[x_gt,:], y[x_gt], depth + 1)

        return  node

    def calcMiddle(self, x:list) -> list:
        """ 计算连续型特征的俩俩均值

        parameter:
            1. x: 一维列表，在测试节点中只测试一个特征的取值，
                  因此我们只需要计算一个特征对应的所有可能取值的中值
                  并用该中值来划分数据集

        Tips: 该函数用于 calcMse 函数中确定连续型随机变量的所有可能的划分阈值
        """
        x = np.array(x)
        x = np.sort(x)  # 对 x 进行排序，方便计算相邻两个取值的均值
        if len(x) == 0:
            return np.array([])

        middle = np.array([])
        for i in range(len(x) - 1):  # 能进入该函数计算的 x 的长度一定大于 1
            if x[i] == x[i + 1]:     # 对于相同的两个 x 值不设划分阈值
                continue
            middle = np.append(middle, (x[i] + x[i + 1]) / 2)

        return middle  # 如果 len(np.unique(x)) == 1，则无法用来获取任何信息，
                       # 此时 middle 为空，符合预期

    def calcMse(self, x:list, y:list) -> tuple:
        """ 计算样本的均方误差

        parameter:
            1. x: 样本特征集，一维列表
            2. y: 样本真值集，一维列表

        returned value:
            返回一个 tuple(float, float)，其中 tuple[0] 为最小的均方误差
        """
        middle    = self.calcMiddle(x)

        min_mse   = np.inf
        threshold = np.inf
        for i in range(len(middle)):
            y_lt      = y[x < middle[i]]
            left_mse  = np.sum((y_lt - np.average(y_lt)) ** 2)
            y_gt      = y[x > middle[i]]
            right_mse = np.sum((y_gt - np.average(y_gt)) ** 2)

            # 以划分后左右字节点的 MSE 的加权平均作为该节点的 MSE
            mse = len(y_lt) / len(y) * left_mse + len(y_gt) / len(y) * right_mse
            if min_mse > mse:
                min_mse   = mse
                threshold = middle[i]

        return min_mse, threshold

    def predict(self, x:list) -> list:
        """ 用拟合好的回归决策树进行预测

        parameter:
            1. x: 测试集

        returned value:
            返回预测结果，一个行向量
        """
        y = np.zeros(x.shape[0])

        stack = [(self.root, [i for i in range(len(x))])]
        while len(stack) > 0:
            node, x_idx = stack.pop()
            if node.left_child is None and node.right_child is None:
                y[x_idx] = node.value
                continue
            # 注意决策树是一棵满二叉树！
            x_lt_idx = [idx for idx in x_idx if x[idx][node.feature_idx] < node.value]
            x_gt_idx = [idx for idx in x_idx if x[idx][node.feature_idx] > node.value]
            if len(x_lt_idx) > 0:
                stack.append((node.left_child, x_lt_idx))
            if len(x_gt_idx) > 0:
                stack.append((node.right_child, x_gt_idx))

        return y

if __name__ == "__main__":
    from sklearn.datasets import fetch_california_housing
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeRegressor as BenchmarkModel
    from sklearn.metrics import mean_squared_error

    housing = fetch_california_housing()
    x, y = housing.data, housing.target

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # print("x_train=")
    # print(x_train)
    import time
    start = time.time()

    benchmark_model = BenchmarkModel(max_depth=5)
    benchmark_model.fit(x_train, y_train)
    y_pred_benchmark = benchmark_model.predict(x_test)
    mse_benchmark    = mean_squared_error(y_test, y_pred_benchmark)
    print(y_pred_benchmark)
    print('Benchmark MSE:', mse_benchmark)
    print(f"代码执行时间: {time.time() - start}秒")

    start = time.time()
    model = DecisionTreeRegressor(max_depth=5)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print(y_pred)
    mse    = mean_squared_error(y_test, y_pred)
    print('MSE:', mse)
    print(f"代码执行时间: {time.time() - start}秒")

