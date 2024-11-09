import random
import sys

def playerpm():
    player_name = input('プレイヤーの名前を入力してください:')
    player_level = 1
    player_hp = int(random.randrange(50,101))
    player_mp = int(random.randrange(70,101))
    player_hp2 = player_hp
    player_mp2 = player_mp
    count = int(0)
    down = int(0)
    monsterbox(player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count, down)

def monsterbox(player_name: str, player_level: int, player_hp: int, player_hp2: int, player_mp: int, player_mp2: int, count: int, down: int):
    monster = ['スライム', 'ゴブリン', 'オーク', 'ドラゴン']
    print(str(monster[count]) + 'が出現した')
    if count == 0: #スライム
        monster_hp = int(random.randrange(30,41))
        battle(monster[0], monster_hp, player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count, down)
    if count == 1: #ゴブリン
        monster_hp = int(random.randrange(51,61))
        battle(monster[1], monster_hp, player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count, down)
    if count == 2: #オーク
        monster_hp = int(random.randrange(80,91))
        battle(monster[2], monster_hp, player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count, down)
    if count == 3: #ドラゴン
        monster_hp = int(random.randrange(150,201))
        battle(monster[3], monster_hp, player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count, down)

def battle(monster_name: str, monster_hp: int, player_name: str, player_level: int, player_hp: int, player_hp2: int, player_mp: int, player_mp2: int, count: int, down: int):
    while(monster_hp > 0):
        player_at = int(random.randrange(10,16))  #プレイヤーの攻撃
        player_mt = int(random.randrange(20,31))  #プレイヤーの魔法攻撃
        player_rc = int(random.randrange(25,41))  #プレイヤーの回復
        monster_ch = str(random.randrange(0,2))   #モンスターの選択
        player_qh = str(random.randrange(0,11))
        if count > 0 and down == 1: #レベルアップによる攻撃力アップ,HPとMPの回復&上限アップ
            player_level += 1
            player_hp = player_hp2
            player_mp = player_mp2
            player_hp += 10
            player_mp += 10
            player_hp2 = player_hp
            player_mp2 = player_mp
            down = 0
        if count > 0:
            player_at += player_level * 5
            player_mt += player_level * 5
        print(str(monster_name)+'のHP:' + str(monster_hp))
        print(str(player_name) + 'のレベル:' + str(player_level))
        print(str(player_name) + 'のHP:' + str(player_hp) + ' ' + str(player_name) + 'のMP:' + str(player_mp))
        print('1:剣で攻撃 2:魔法で攻撃(MP20) 3:回復 4:逃げる')
        player_ch = input()
        if monster_name == 'スライム': #スライム出現の場合
            monster_at = int(random.randrange(10,16))
        elif monster_name == 'ゴブリン': #ゴブリン出現の場合
            monster_at = int(random.randrange(20,26))
        elif monster_name == 'オーク': #オーク出現の場合
            monster_at = int(random.randrange(25,30))
        elif monster_name == 'ドラゴン': #ドラゴン出現の場合
            monster_at = int(random.randrange(30,41))
        if player_ch == '1':   #剣で攻撃を選んだ場合
            print(str(player_name) + 'は剣で攻撃をした')
            if player_qh == '1': #クリティカルヒットした場合
                print('モンスターにクリティカルヒットした')
                player_at = int(player_at * 1.5)
                monster_hp -= player_at
            else: #通常の場合
                monster_hp -= player_at
            print(str(monster_name) + 'に' + str(player_at) + 'ダメージ与えた')
            if monster_hp > 0:  #モンスターが倒れなかった場合
                player_hp -= monster_at
                print(str(monster_name) + 'が攻撃してきた')
                print(str(player_name) + 'は' + str(monster_at) + 'ダメージ受けた')
                if player_hp <= 0:  #プレイヤーが倒れた場合
                    print(str(player_name) + 'は倒れた')
                    sys.exit(0)
        elif player_ch == '2':  #魔法で攻撃を選んだ場合
            if player_mp > 20:
                monster_hp -= player_mt
                player_mp -= 20
                print(str(player_name) + 'は魔法で攻撃をした')
                print(str(monster_name) + 'に' + str(player_mt) + 'ダメージを与えた')
                if monster_hp > 0:  #モンスターが倒れなかった場合
                    player_hp -= monster_at
                    print(str(monster_name) + 'が攻撃してきた')
                    print(str(player_name) + 'は' + str(monster_at) + 'ダメージ受けた')
                    if player_hp <= 0: #プレイヤーが倒れた場合
                        print(str(player_name) + 'は倒れた')
                        sys.exit(0)
            else:
                print('魔法を使うことができない')
        elif player_ch == '3':  #回復を選んだ場合
            player_rc2 = 0      #HPの回復量
            player_rc3 = 0      #MPの回復量
            player_c1 = 0       #HP回復した回数
            player_c2 = 0       #MP回復した回数
            if player_hp == player_hp2 and player_mp == player_mp2:
                print(str(player_name) + 'のHPとMPはMAXである')
                print()
                continue
            if player_mp < player_mp2:
                if player_hp + player_rc <= player_hp2 and player_c1 == 0: #回復量がHPの上限以下の場合
                    player_hp += player_rc
                    player_c1 = 1
                if player_mp + player_rc <= player_mp2 and player_c2 == 0: #回復量がMPの上限より以下の場合
                    player_mp += player_rc
                    player_c2 = 1
                if player_hp + player_rc > player_hp2 and player_c1 == 0: #回復量がHPの上限を超えた場合
                    player_rc2 = player_hp2 - player_hp
                    player_hp = player_hp2
                    player_c1 = 1
                if player_mp + player_rc > player_mp2 and player_c2 == 0: #回復量がMPの上限を超えた場合
                    player_rc3 = player_mp2 - player_mp
                    player_mp = player_mp2
                    player_c2 = 1
                if player_rc2 == 0 and player_rc3 == 0: #回復量が両方超えなかった場合
                    print(str(player_name) + 'の' + 'HPとMPが' + str(player_rc) + '回復した')
                if player_rc2 != 0 and player_rc3 == 0: #回復量がHPだけ超えた場合
                    print(str(player_name) + 'のHPが' + str(player_rc2) + ',MPが' + str(player_rc) + '回復した') 
                if player_rc2 == 0 and player_rc3 != 0: #回復量がMPだけ超えた場合
                    print(str(player_name) + 'のHPが' + str(player_rc) + ',MPが' + str(player_rc3) + '回復した')
                if player_rc2 != 0 and player_rc3 != 0: #回復量が両方超えた場合
                    print(str(player_name) + 'のHPが' + str(player_rc2) + ',MPが' + str(player_rc3) + '回復した')
            if player_mp == player_mp2 and player_hp != player_hp2 and player_c1 == 0:
                if player_hp + player_rc <= player_hp2: #回復量がHPの上限以下の場合
                    player_hp += player_rc
                elif player_hp + player_rc > player_hp2: #回復量がHPの上限を超えた場合
                    player_rc2 = player_hp2 - player_hp
                    player_hp = player_hp2
                if player_rc2 == 0: #回復量がHPの上限を超えなかった場合
                    print(str(player_name) + 'のHPが' + str(player_rc) + '回復した')
                elif player_rc2 != 0: #回復量がHPの上限を超えた場合
                    print(str(player_name) + 'のHPが' + str(player_rc2) + '回復した')
            player_hp -= monster_at
            print(str(monster_name) + 'が攻撃してきた')
            print(str(player_name) + 'は' + str(monster_at) + 'ダメージ受けた')
            if player_hp <= 0: #プレイヤーが倒れた場合
                        print(str(player_name) + 'は倒れた')
                        sys.exit(0)
        elif player_ch == '4':  #逃げるを選んだ場合
            print(str(player_name) + 'は逃げた')
            if monster_ch == '0': #逃げることに成功した場合
                print(str(monster_name) + 'から逃げることに成功した')
                sys.exit(0)
            elif monster_ch == '1': #逃げることに失敗した場合
                print('しかし' + str(monster_name) + 'から逃げることができなかった')
        elif player_ch == 'q': #qを入力した場合
            print('ゲームを終了します')
            sys.exit(0)
        else: #1~4以外の文字を入力した場合
            print('1~4の数字を入力してください')
        if monster_hp > 0: #表示を見やすくするため
            print()
    print(str(monster_name) + 'を倒した')
    print(str(player_name) + 'のレベルが1上がった' )
    print()
    count += 1
    down = 1
    if count == 4: #すべてのモンスターを倒した場合
        print('すべてのモンスターを倒した')
        sys.exit(0)
    elif count < 4: #まだすべてのモンスターを倒していない場合
        monsterbox(player_name, player_level, player_hp, player_hp2, player_mp, player_mp2, count, down)

if __name__ == "__main__":
    playerpm()
