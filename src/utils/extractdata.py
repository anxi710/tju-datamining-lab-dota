import pandas as pd

from .readjsonl import read_matches

# 1. 提取一级标签 —— main table
def extract_main(matches_file):
    """
    从JSON对象中提取所有不含嵌套属性的一级属性。
    并对包含嵌套属性的一级属性统计其内部的数据数量。
    """
    key_name = ['game_time', 'match_id_hash', 'teamfights_number',
                'chat_number', 'game_mode', 'lobby_type']

    data = []
    for match in read_matches(matches_file):
        data.append([
            match['game_time'],
            match['match_id_hash'],
            len(match['teamfights']),
            len(match['chat']),
            match['game_mode'],
            match['lobby_type']
        ])

    return pd.DataFrame(data, columns=key_name)

# 2. 提取 objectives table
def extract_objectives(matches_file):
    """
    从 json 对象中提取 objectives 数据，将每个 objective 展开成单独的列。
    如果没有那么多 objectives，则保留空值。
    """
    # 找出 objectives 列表的最大长度
    max_len = 0
    for match in read_matches(matches_file):
        max_len = max(max_len, len(match['objectives']))

    # 生成列名
    key_name = []
    for i in range(max_len):
        key_name.append(f'objective-{i + 1}-type')
        key_name.append(f'objective-{i + 1}-player_slot')
        key_name.append(f'objective-{i + 1}-key')
        key_name.append(f'objective-{i + 1}-slot')

    # 提取数据
    data = []
    needed_keys = ['type', 'player_slot', 'key', 'slot']
    for match in read_matches(matches_file):
        row = []
        for i in range(max_len):
            if i < len(match['objectives']):
                objective = match['objectives'][i]
                for key in needed_keys:
                    row.append(objective[key] if key in objective else None)
            else:
                row.extend([None, None, None, None])
        data.append(row)

    # 将数据转换为 DataFrame
    return pd.DataFrame(data, columns=key_name)

# 3. 提取 targets table
def extract_targets(matches_file):
    """
    从 json 对象中提取 radiant_win 属性。
    """
    key_name = ['radiant_win']

    data = []
    for match in read_matches(matches_file):
        data.append([match['targets']['radiant_win']])

    return pd.DataFrame(data, columns=key_name)

# 4. 提取 teamfights table
def extract_teamfights(matches_file):
    """
    从JSON对象中提取teamfights数据，将每个teamfight和其下的player属性展开成单独的列。
    删除players中的ability_uses, deaths, deaths_pos, item_uses, 和killed字段。
    """
    # 找出 teamfights 列表的最大长度
    max_len = 0
    for match in read_matches(matches_file):
        max_len = max(max_len, len(match['teamfights']))

    # 生成列名
    key_name = []
    for i in range(max_len):
        # teamfight 的顶层字段
        key_name.append(f'teamfights-{i + 1}-end')
        key_name.append(f'teamfights-{i + 1}-start')
        key_name.append(f'teamfights-{i + 1}-deaths')
        key_name.append(f'teamfights-{i + 1}-last_death')

        # player 相关字段
        for j in range(10):
            key_name.append(f'teamfights-{i + 1}-player-{j + 1}-xp_delta')
            key_name.append(f'teamfights-{i + 1}-player-{j + 1}-damage')
            key_name.append(f'teamfights-{i + 1}-player-{j + 1}-gold_delta')
            key_name.append(f'teamfights-{i + 1}-player-{j + 1}-healing')
            key_name.append(f'teamfights-{i + 1}-player-{j + 1}-buybacks')

    # 提取数据
    data = []
    for match in read_matches(matches_file):
        row = []
        for i in range(max_len):
            if i < len(match['teamfights']):
                teamfight = match['teamfights'][i]
                row.extend([
                    teamfight.get('end'),
                    teamfight.get('start'),
                    teamfight.get('deaths'),
                    teamfight.get('last_death')
                ])

                for j in range(10):
                    if j < len(teamfight['players']):
                        player = teamfight['players'][j]
                        row.extend([
                            player.get('xp_delta'),
                            player.get('damage'),
                            player.get('gold_delta'),
                            player.get('healing'),
                            player.get('buybacks')
                        ])
                    else:
                        row.extend([None, None, None, None, None])
            else:
                row.extend([None, None, None, None])
                row.extend([None, None, None, None, None] * 10)

        data.append(row)

    # 将数据转换为 DataFrame
    return pd.DataFrame(data, columns=key_name)


# 5. 提取 players table
def extract_players(matches_file):
    """
    从 json 对象中提取 players 数据，将每个 player 和其下的多级属性展开成单独的列。
    删除指定字段，保留需要展开的字段，并处理多级嵌套。
    """
    # 生成列名
    key_name = []
    needed_key = [
        "assists", "camps_stacked", "creeps_stacked", "deaths", "denies", "gold", "health",
        "hero_id", "kills", "level", "lh", "max_health", "max_hero_hit", "max_mana",
        "nearby_creep_death_count", "obs_left_log", "obs_log", "observers_placed",
        "randomed", "rune_pickups", "sen_left_log", "sen_log", "sen_placed",
        "stuns", "teamfight_participation", "towers_killed", "xp_reasons"
    ]
    for i in range(1, 11):
        for key in needed_key:
            if key == 'xp_reasons':
                for j in range(0, 4):
                    key_name.append(f'players-{i}-{key}-{j}')
            else:
                key_name.append(f'players-{i}-{key}')

    # 提取数据
    data = []
    for match in read_matches(matches_file):
        row = []
        for player in match['players']:
            for key in needed_key:
                if key in player:
                    if key == 'xp_reasons':
                        # "xp_reasons": { "0": x, "1": x, "2": x, "3": x }
                        for sub_key in ['0', '1', '2', '3']:
                            row.append(player[key][sub_key] if sub_key in player[key] else None)
                    elif key == 'max_hero_hit':
                        row.append(player[key]['value'])
                    else:
                        row.append(player[key])
                else:
                    row.append(None)
        data.append(row)

    # 将数据转换为 DataFrame
    return pd.DataFrame(data, columns=key_name)
