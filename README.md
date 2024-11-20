# TJU 数据挖掘课程实践大作业

本项目是同济大学2024年秋季数据挖掘课程的实践大作业，完成 Kaggle 上的 Dota 2 Winner Prediction 比赛。

目录简介：

```powershell
.
├── README.md
├── data
│   ├── extracted_data            # 从原始数据中初步提取的数据文件
│   ├── input_test.jsonl          # 小样本测试数据（100 个）
│   ├── sample_submission.csv     # 示例提交文件
│   ├── small_train_matches.json  # 小样本测试数据（30 个）
│   ├── test_features.csv         # 主办方提供的测试特征集
│   ├── test_matches.jsonl        # 主办方提供的原始测试数据集
│   ├── train_features.csv        # 主办方提供的训练特征集
│   ├── train_matches.jsonl       # 主办方提供的原始训练数据集
│   └── train_targets.csv         # 主办方提供的训练标签集
├── docs
├── linux_proc_cmd.txt
├── note
│   ├── RF_DT  # 随机森林和决策树笔记
│   ├── lightgbm-allFeature-importance.ipynb
│   ├── lightgbm-starter-code.ipynb
│   ├── lightgbm.ipynb
│   └── start.ipynb  # 主办方提供的入门笔记
├── requirements.txt
└── src
    ├── data               # 存放处理后的数据及结果数据
    ├── datapreproc.ipynb  # 数据预处理
    ├── test.ipynb         # 在该文件中测试数据预处理和训练过程中遇到的问题
    ├── train.ipynb        # 训练模型
    └── utils              # 存放预处理及训练过程中可能用到的功能函数
```

---

使用 `conda create --name dota2 --file requirements.txt python=3.10(jupyter)` 创建适用于本项目的 conda 环境。

---

## Workflow

- [x] 10/11 - 10/19：理解原始数据中的特征含义，初步进行特征选择

- [x] 选择需要的特征后从原始数据中提取所需数据

- [ ] 清理提取到的数据，进行类别编码

- [ ] 进行可能的数据标准化 / 归一化

- [ ] 对初步处理的数据进行特征工程

- [ ] 降维（可选）

- [ ] 训练模型

- [ ] 结果分析与调优

- [ ] 模型评价

- [ ] 撰写报告
