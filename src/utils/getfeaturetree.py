import pandas as pd
from .readjsonl import read_matches

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

def get_keys_relation(path_to_data):
    keys_rel_set = set()

    for match in read_matches(path_to_data):
        keys_rel_set.update(extract_keys(match))

    keys_rel_df = pd.DataFrame(keys_rel_set, columns=["parent", "child"])

    keys_rel_df.fillna("NULL", inplace=True)

    # 去除 child 为数字的行
    keys_rel_df = keys_rel_df[~keys_rel_df["child"].str.isnumeric()]

    # 去除 parent 最后一个单元为数字的行
    keys_rel_df = keys_rel_df[~keys_rel_df["parent"].str.split(".").apply(lambda x: x[-1]).str.isnumeric()]

    # 去除不重要的键
    keys_rel_df = keys_rel_df[keys_rel_df["parent"].str.split(".").apply(lambda x: x[-1]) != "ability_uses"]
    keys_rel_df = keys_rel_df[keys_rel_df["parent"].str.split(".").apply(lambda x: x[-1]) != "item_uses"]
    keys_rel_df = keys_rel_df[keys_rel_df["parent"].str.split(".").apply(lambda x: x[-1]) != "damage_inflictor"]
    keys_rel_df = keys_rel_df[keys_rel_df["parent"].str.split(".").apply(lambda x: x[-1]) != "hero_hits"]
    keys_rel_df = keys_rel_df[keys_rel_df["parent"].str.split(".").apply(lambda x: x[-1]) != "damage_inflictor_received"]
    keys_rel_df = keys_rel_df[keys_rel_df["parent"].str.split(".").apply(lambda x: x[-1]) != "purchase"]

    # 去除所有含有 "npc_dota" 的行
    keys_rel_df = keys_rel_df[~keys_rel_df["parent"].str.contains("npc_dota")]
    keys_rel_df = keys_rel_df[~keys_rel_df["child"].str.contains("npc_dota")]

    return keys_rel_df.apply(lambda x: tuple(x), axis=1).values

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

def print_tree(tree, depth=0, file=None):
    """ 将树格式化打印到 .txt 文件中 """

    for key, val in tree.items():
        print(f"{'    ' * depth}{key}", file=file)
        print_tree(val, depth + 1, file)
