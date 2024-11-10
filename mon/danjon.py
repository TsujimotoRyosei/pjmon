import random

def playerpm():
    player_name = "プレイヤー"
    player_level = 1
    player_hp = random.randint(50, 101)
    player_mp = random.randint(70, 101)
    count = 0
    player_data = [player_name, player_level, player_hp, player_hp, player_mp, player_mp, count]
    return player_data

def monsterbox(player_data):
    monsters = ['スライム', 'ゴブリン', 'オーク', 'ドラゴン']
    count = player_data[6]  # 現在のモンスターのインデックス
    if count < len(monsters):
        monster_hp_ranges = [(30, 41), (51, 61), (80, 91), (150, 201)]
        monster_hp = random.randint(*monster_hp_ranges[count])
        monster_data = [monsters[count], monster_hp]
        return monster_data, player_data
    return None, player_data  # ドラゴンを倒した場合


def convert_newlines_to_br(text):
    return text.replace("\n", "<br>")

def battle(monster_data, player_data, player_ch):
    monster_name, monster_hp = monster_data
    player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count= player_data
    player_at = random.randint(10, 16)
    player_mt = random.randint(20, 31)
    player_rc = random.randint(25, 41)
    monster_ch = random.choice(['0', '1'])
    player_qh = random.choice(['0', '1'])
    
    if count > 0: #レベルアップによる攻撃力アップ
        player_at += player_level * 5
        player_mt += player_level * 5
    
    if player_ch == 'attack':
        if player_qh == '1':
            player_at = int(player_at * 1.5)
            action_result = f"{player_name}はクリティカルヒットを出した！\n"
            monster_hp -= player_at
            action_result += f"{player_name}は剣で攻撃をした。\n{monster_name}に{player_at}ダメージを与えた。\n\n"
        else:
            monster_hp -= player_at
            action_result = f"{player_name}は剣で攻撃をした。\n{monster_name}に{player_at}ダメージを与えた。\n\n"
    elif player_ch == 'magic' and player_mp >= 20:
        if player_qh == '1':
            player_mt = int(player_mt * 2)
            action_result = f"{player_name}はクリティカルヒットを出した！\n"
            monster_hp -= player_mt
            player_mp -= 20
            action_result += f"{player_name}は魔法で攻撃をした。\n{monster_name}に{player_mt}ダメージを与えた。\n\n"
        else:
            monster_hp -= player_mt
            player_mp -= 20
            action_result = f"{player_name}は魔法で攻撃をした。\n{monster_name}に{player_mt}ダメージを与えた。\n\n"
    elif player_ch == 'heal':
        if player_qh == '1':
            # HPとMPを全回復する
            player_hp = player_hp2
            player_mp = player_mp2
            action_result = f"{player_name}はHPとMPを全回復した。\n\n"
        else:    
            hp_healed = min(player_rc, player_hp2 - player_hp)
            mp_healed = min(player_rc, player_mp2 - player_mp)
            player_hp += hp_healed
            player_mp += mp_healed
            action_result = f"{player_name}はHPを{hp_healed}、MPを{mp_healed}回復した。\n\n"
    elif player_ch == 'run' and monster_ch == '0':
        return convert_newlines_to_br(f"{player_name}は逃げ出し、成功した。"), [None, None]
    else:
        action_result = f"{player_name}の行動は不明です。"
    
    if monster_hp > 0:
        # モンスターが攻撃
        if monster_name == 'スライム':
            monster_attack = random.randint(10, 16)
        elif monster_name == 'ゴブリン':
            monster_attack = random.randint(20, 26)
        elif monster_name == 'オーク':
            monster_attack = random.randint(25, 30)
        elif monster_name == 'ドラゴン':
            monster_attack = random.randint(30, 41)
        player_hp -= monster_attack
        action_result += f"{monster_name}が攻撃してきた！\n{player_name}は{monster_attack}のダメージを受けた。\n\n"    

    if monster_hp <= 0:
        action_result += f"{monster_name}を倒した！ \n{player_name}のレベルが1上がった。"
        count += 1
        player_level += 1
        player_hp = player_hp2 + 10
        player_mp = player_mp2 + 10
        player_hp2, player_mp2 = player_hp, player_mp
        player_data = [player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count]
        monster_hp = 0
        return convert_newlines_to_br(action_result), [None, player_data]
    elif player_hp <= 0:
        return f"{player_name}は倒れた。ゲームオーバー。", [None, None]

    monster_data = [monster_name, monster_hp]
    player_data = [player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count]
    return convert_newlines_to_br(action_result), [monster_data, player_data]

def main():
    player_data = playerpm()
    monster_data, player_data = monsterbox(player_data)
    result, _ = battle(monster_data, player_data, "attack")  # 仮のテストとして"attack"を渡す
    print(result)

if __name__ == "__main__":
    main()
