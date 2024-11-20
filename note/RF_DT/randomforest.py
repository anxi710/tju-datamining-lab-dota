# Random Forest Regressor
import numpy as np
from decisiontree import DecisionTreeRegressor

class RandomForestRegressor:
    """ 随机森林回归器 """
    def __init__(self, n_estimators=10, max_depth=10):
        """ 初始化随机森林回归器

        parameter:
            1. n_estimators : 估计器个数
            2. max_depth    : 决策树最大深度
            3. max_features : 每次划分时使用的特征个数（未给出的话则为总特征数开方取整）
        """
        self.n_estimators = n_estimators
        self.max_depth    = max_depth
        self.trees        = None  # 森林中的决策树

    def fit(self, x:list, y:list):
        """ 使用训练数据拟合随机森林模型

        parameter:
            1. x: 训练集数据
            2. y: 训练集标签
        """
        x = np.array(x)
        y = np.array(y)
        dts = []  # 决策树数组
        for _ in range(self.n_estimators):
            x_train, y_train = self.bootstrap(x, y)
            dt = DecisionTreeRegressor(max_depth=self.max_depth)
            dt.fit(x_train, y_train)
            dts.append(dt)
        self.trees = dts

    def bootstrap(self, x:list, y:list):
        """ 自助抽样

        parameter:
            1. x: 数据集
            2. y: 标签集

        Tips:
            在随机森林中，对于一个大小为 N 的数据集，需要有放回的随机抽样 N 次，以生成用于训练的数据集
        """
        n_samples   = x.shape[0]
        sample_idx  = np.random.choice(n_samples, n_samples, replace=True)
        return x[sample_idx], y[sample_idx]

    def predict(self, x) -> list:
        """ 使用训练好的模型进行预测

        parameter:
            1. x: 测试集

        returned value:
            预测结果
        """
        # 预测结果
        y_predict = np.zeros(x.shape[0])

        for i in range(self.n_estimators):
            dt = self.trees[i]
            y_predict += dt.predict(x)

        y_predict /= self.n_estimators
        return y_predict

if __name__ == "__main__":
    from sklearn.datasets import fetch_california_housing
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor as BenchmarkModel
    from sklearn.metrics import mean_squared_error

    housing = fetch_california_housing()
    x, y = housing.data, housing.target

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # print("x_train=")
    # print(x_train)
    import time
    start = time.time()

    benchmark_model = BenchmarkModel()
    benchmark_model.fit(x_train, y_train)
    y_pred_benchmark = benchmark_model.predict(x_test)
    mse_benchmark    = mean_squared_error(y_test, y_pred_benchmark)
    print('Benchmark MSE:', mse_benchmark)
    print(f"代码执行时间: {time.time() - start}秒")

    start = time.time()
    model = RandomForestRegressor()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print(y_pred)
    mse    = mean_squared_error(y_test, y_pred)
    print('MSE:', mse)
    print(f"代码执行时间: {time.time() - start}秒")

