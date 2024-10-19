import pandas as pd
import ujson as json       # 用于读入 .json 文件

# 获取原始数据中的所有特征及其父子关系
def extract_keys(data, parent_key=None, res=None):
    """ 递归提取 JSON 对象中的键及其父子关系 """
    if res is None:
        res = set()

    if isinstance(data, dict):
        for key, val in data.items():
            current_key = f"{parent_key}.{key}" if parent_key else key
            res.add((parent_key, key))
            extract_keys(val, current_key, res)
    elif isinstance(data, list):
        for item in data:
            extract_keys(item, parent_key, res)

    return res

def build_tree(tuples):
    """ 根据父子关系列表构建树结构 """
    tree = {}

    for path, node in tuples:
        if path is None:
            # 如果没有路径，直接在根级别创建该节点
            if node not in tree:
                tree[node] = {}  # 执行顺序不定！
            continue

        parts = path.split('.')  # 将路径按照 '.' 分割
        current_level = tree     # 从树的根节点开始

        # 遍历路径中的每一段，逐层创建节点
        for part in parts:
            if part not in current_level:
                current_level[part] = {}  # 如果不存在该节点，创建一个字典表示该节点
            current_level = current_level[part]  # 继续向下层递归

        if node not in current_level:
            current_level[node] = {}  # 将当前节点添加到树中

    return tree

# 将树格式化打印到 .txt 文件中
def print_tree(tree, depth=0, file=None):
    """ dfs 遍历树并打印 """
    for key, val in tree.items():
        print(f"{'    ' * depth}{key}", file=file)
        print_tree(val, depth + 1, file)

if __name__ == '__main__':

    features_rel_set = set()

    with open('data/features_description.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    extract_keys(data, res=features_rel_set)

    # print(len(features_rel_set))

    # for rel in features_rel_set:
    #     print(rel)

    features_rel_df = pd.DataFrame(features_rel_set, columns=["parent", "child"])

    features_rel_df = features_rel_df[features_rel_df['child'] != 'description']
    features_rel_df = features_rel_df[features_rel_df['child'] != 'priority']
    features_rel_df = features_rel_df[features_rel_df['child'] != 'extra-info']

    features_rel = features_rel_df.apply(lambda x: tuple(x), axis=1).values

    # print(len(features_rel))
    # for rel in features_rel:
    #     if rel[0] == 'chat':
    #         print(rel)
    # for rel in features_rel_df.values:
    #     print(rel)

    features_tree = build_tree(features_rel)

    # for key, val in features_tree.items():
    #     print(key)
    # print(features_tree)

    with open('data/features_tree.txt', 'w', encoding='utf-8') as f:
        print_tree(features_tree, file=f)
