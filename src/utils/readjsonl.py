import os
import ujson as json
from tqdm import tqdm

def read_matches(matches_file):
    """ 生成器函数，用于读取比赛数据 """

    MATCHES_COUNT = {
        'test_matches.jsonl': 10000,
        'train_matches.jsonl': 39675
    }

    _, filename = os.path.split(matches_file)
    total_matches = MATCHES_COUNT.get(filename)

    with open(matches_file) as fin:
        for line in tqdm(fin, total=total_matches):
            yield json.loads(line)
