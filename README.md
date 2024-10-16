# TJU 数据挖掘课程实践大作业

本项目是同济大学2024年秋季数据挖掘课程的实践大作业，完成 Kaggle 上的 Dota 2 Winner Prediction 比赛。

目录简介：

```powershell
.
|
+-- .gitignore                   # 跟踪时需要忽略的文件
|
+-- requirements.txt             # 需要安装的 python 软件包
|
+-- README.md                    # 当前文件
|
+-- data                       # 数据集
|   |
|   +-- sample_submission.csv    # 测试结果提交模版
|   |
|   +-- test_features.csv        # 测试用特征集
|   |
|   +-- train_features.csv       # 训练用特征集
|   |
|   +-- train_targets.csv        # 训练用标签集
|   |
|   +-- linux_proc_cmd.txt       # 处理数据用到的 Linux 命令
|   |
|   +-- small_train_matches.json # 前二十个原始训练数据样本（方便打开查看）
|   |
|   +-- matches_features_all.txt # 原始数据中的所有 feature
|
+-- docs                       # 课程提交所需文档
|
+-- note                       # 项目完成过程中的参考资料及笔记
|   |
|   +-- start.ipynb              # 入门教程（Jupyter Notebook 版）
|   |
|   +-- images                 # 存放笔记中用到的图片
|   |
|   +-- decisiontree.py          # 手写决策树代码
|   |
|   +-- decisiontree.ipynb       # 决策树笔记
|   |
|   +-- randomforest.py          # 手写随机森林代码
|   |
|   +-- randomforest.ipynb       # 随机森林笔记
|   |
|   +-- lightgbm.ipynb           # lightgbm 模型相关代码
|
+-- src                        # 源代码
    |
    +-- data                     # 模型训练用数据
    |
    +-- train.py                 # 模型训练
    |
    +-- datapreproc.py           # 数据预处理
```

---

使用 `conda create --name dota2 --file requirements.txt python=3.10(jupyter)` 创建适用于本项目的 conda 环境。

---

## Workflow

- [ ] 10/11 - 10/20：理解原始数据中的特征含义，初步进行特征选择

- [ ] 选择需要的特征后从原始数据中提取所需数据

- [ ] 清理提取到的数据，进行类别编码

- [ ] 进行可能的数据标准化 / 归一化

- [ ] 对初步处理的数据进行特征工程

- [ ] 降维（可选）

- [ ] 训练模型

- [ ] 结果分析与调优

- [ ] 模型评价

- [ ] 撰写报告
