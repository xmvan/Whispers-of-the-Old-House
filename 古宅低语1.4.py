import random
import time

MAX_STAT = 18
HIGH_FEAR = 6
SUITS = ["♠", "♥", "♦", "♣"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

K_SECRETS = {
    "♠": {
        "name": "谋杀与怨念",
        "description": "古宅曾是一个残忍连环杀手的巢穴。他的恶灵即是古宅本身，渴望永远重复他的暴行。",
        "modifier": 0,
        "hint": "墙上反复出现同一组抓痕，像是在计数受害者。",
    },
    "♥": {
        "name": "扭曲的爱",
        "description": "古宅的主人曾进行黑暗仪式企图复活死去的爱人，却将两者的灵魂痛苦地融合并束缚于此。",
        "modifier": 2,
        "hint": "卧室里两具交缠的影子永不分开，即使没有人站在窗前。",
    },
    "♦": {
        "name": "贪婪的契约",
        "description": "宅邸的原主人与某个不可名状的存在签订了契约，古宅变成了一座活体监狱。",
        "modifier": "hand_bonus",
        "hint": "金库账本最后一页用血写着：代价已付，门却永远关上。",
    },
    "♣": {
        "name": "异界裂隙",
        "description": "古宅建造在一个现实世界的薄弱点上，抑制着另一个充满噩梦的维度渗透进来。",
        "modifier": 3,
        "hint": "花园地下传来潮汐般的呼吸，泥土按不存在的星图排列。",
    },
}

ROLES = {
    "1": {
        "name": "调查员",
        "desc": "调查房间时检定难度-1，更容易发现线索。",
        "bonus": "investigate",
    },
    "2": {
        "name": "医生",
        "desc": "稳住心神额外恢复1点，使用绷带多恢复1点生命。",
        "bonus": "medic",
    },
    "3": {
        "name": "学者",
        "desc": "揭示秘密时投掷结果+3，梅花房间更容易读懂痕迹。",
        "bonus": "scholar",
    },
    "4": {
        "name": "猎手",
        "desc": "探索黑桃房间受到的伤害-1（至少为0）。",
        "bonus": "hunter",
    },
    "5": {
        "name": "灵媒",
        "desc": "每回合开始时若理智低于一半，自动恢复1点理智。",
        "bonus": "medium",
    },
}

ITEMS = {
    "提灯": "下次检定结果+2，使用后消失。",
    "绷带": "立即恢复3点生命。",
    "护身符": "立即恢复3点理智。",
    "钥匙": "揭示秘密时难度-3，可保留到揭示时自动消耗。",
    "旧日记": "直接加入一张手牌线索。",
    "镇静剂": "本回合忽略一次理智伤害。",
    "圣水": "恐惧等级-1（最低为1）。",
    "地图残页": "将1张已探索房间洗回牌堆，并抽1张手牌。",
}

ROOM_NAMES = {
    "♠": ["刑讯地下室", "猎枪陈列室", "锈蚀铁笼间", "血渍走廊", "停尸冷藏室",
           "绞架大厅", "诅咒祭坛", "枯井竖井", "密门暗室", "剥皮工坊",
           "猎犬棚", "武器库废墟"],
    "♥": ["褪色起居室", "双人卧室", "儿童玩具房", "婚礼礼堂", "绣花闺房",
           "家庭肖像厅", "温暖壁炉房", "玫瑰温室", "梳妆间", "旧日餐厅",
           "摇篮阁楼", "情人书信室"],
    "♦": ["金库前厅", "账房", "珠宝展柜", "书房密室", "钟表修理间",
           "收藏品陈列室", "赌桌沙龙", "酒窖", "契约签署厅", "保险柜走廊",
           "古董画廊", "银器储藏室"],
    "♣": ["常春藤回廊", "迷宫花园", "温室废墟", "喷泉庭院", "仆役通道",
           "东翼连廊", "雨廊", "石像庭院", "树篱迷宫", "地下通道口",
           "礼拜小堂", "墓园边门"],
}

ROOM_FLAVOR = {
    "♠": "空气里有铁锈与陈年血迹的味道，地板上的刮痕指向更深处。",
    "♥": "这里曾有人生活过。余温还在，却像一张笑错了的脸。",
    "♦": "抽屉、暗格和积灰的盒子似乎藏着还能用的东西。",
    "♣": "足迹、符文和被刻意擦掉的箭头叠在一起，像有人反复进出。",
}

D30_INFO = {
    1: ("群魔乱舞", "所有肖像画的眼睛开始流血并注视着玩家"),
    2: ("血肉之墙", "墙壁变得柔软、温热并开始搏动"),
    3: ("时光倒流", "场景切换回刚进入古宅时的样子"),
    4: ("窃窃私语", "恶毒声音在每个人耳边低语最深处的秘密"),
    5: ("镜像自我", "每个玩家都在倒影中看到另一个充满恶意的自己"),
    6: ("无尽回廊", "通道被封锁，出口消失"),
    7: ("孩童歌谣", "远处传来空灵、走调的孩童歌唱声"),
    8: ("提线木偶", "一名玩家的手臂不由自主地抬起"),
    9: ("腐化盛宴", "房间出现腐烂生蛆但却散发着香气的盛宴"),
    10: ("死者苏生", "已故之人重新出现并变得更强大"),
    11: ("空间折叠", "房间之间的空间关系发生扭曲变化"),
    12: ("记忆侵蚀", "玩家的记忆被古宅逐渐吞噬"),
    13: ("虫巢爆发", "无数虫类从各种缝隙中涌出"),
    14: ("哀悼之影", "半透明的哀悼者身影在房间角落出现"),
    15: ("献祭要求", "古宅要求玩家献上祭品"),
    16: ("时间跳跃", "时间突然跳跃，蜡烛烧掉一大截"),
    17: ("寄生触手", "油腻的触须状物从影子中伸出"),
    18: ("全视之眼", "天花板上睁开一只巨大的眼睛"),
    19: ("声音剥夺", "所有的声音瞬间消失"),
    20: ("过去重现", "古宅中曾发生的悲剧事件重现在眼前"),
    21: ("扭曲生长", "古宅的木质结构开始疯狂生长"),
    22: ("信任危机", "古宅的低语在玩家之间播种猜疑"),
    23: ("重力失效", "房间内的重力方向突然改变"),
    24: ("模仿者", "门外传来模仿亲友的呼救声"),
    25: ("绝望具象", "玩家的恐惧凝聚成黑色人形"),
    26: ("生命汲取", "古宅从玩家身上吸取生命力"),
    27: ("强制交换", "玩家之间的理智或生命值被强制交换"),
    28: ("门户洞开", "地板上出现通往绝对黑暗的洞口"),
    29: ("古宅之心", "玩家短暂感受到古宅那古老冰冷的意识"),
    30: ("古宅获胜", "古宅展示了它真正的力量"),
}

TRAGEDIES = [
    "一个家庭成员在餐厅被毒杀的瞬间",
    "一个孩子被锁在阁楼中慢慢饿死的最后时刻",
    "女主人发疯后纵火焚烧东翼的场景",
    "男主人在地下室进行黑暗仪式的过程",
    "管家在厨房用银叉刺死入侵者后，自己也消失在墙里",
    "双胞胎之一把另一个推进枯井，却听见井底传来自己的笑声",
    "一场午夜舞会，宾客在第三支华尔兹时全部变成肖像画",
    "牧师试图净化宅邸，圣水落地却烧出一张契约签名",
]


def card_str(card):
    return f"{card['suit']}{card['value']}"


def yn(prompt):
    return input(prompt).strip().lower() in ("y", "yes", "是")


def room_title(card):
    names = ROOM_NAMES.get(card["suit"], ["未知房间"])
    idx = VALUES.index(card["value"]) if card["value"] in VALUES else 0
    return names[idx % len(names)]


class HorrorMansionGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.fear_level = 1
        self.max_fear_level = 6
        self.mansion_deck = []
        self.core_secrets = []
        self.explored_rooms = []
        self.hand_cards = []
        self.defeated_monsters = []
        self.game_over = False
        self.victory = False
        self.ending_note = ""
        self.silence_mode = False
        self.silence_duration = 0
        self.trust_crisis = False
        self.trust_crisis_duration = 0
        self.last_action = ""
        self.d30_event_count = 0
        self.consecutive_d30 = 0
        self.next_turn_difficulty_penalty = False
        self.skip_mansion_turn = False
        self.skip_player_turn = False
        self.eye_of_mansion = False
        self.eye_duration = 0
        self.temp_fear_increase = False
        self.original_fear = 1
        self.fear_delay = 0
        self.journal = []
        self.sanctuaries = []
        self.secrets_seen = 0
        self.check_bonus = 0

    @property
    def high_fear(self):
        return self.fear_level >= HIGH_FEAR

    @property
    def alive(self):
        return [p for p in self.players if p["alive"]]

    def dmg(self, low, high=None):
        high = low if high is None else high
        return high if self.high_fear else low

    def roll(self, sides):
        return random.randint(1, sides)

    def add_journal(self, text):
        if text not in self.journal:
            self.journal.append(text)
            print(f"【日志】{text}")

    def grant_item(self, player, item=None):
        item = item or random.choice(list(ITEMS))
        player["items"].append(item)
        print(f"{player['name']} 获得道具【{item}】：{ITEMS[item]}")
        return item

    def hurt(self, player, sanity=0, health=0):
        if sanity and player.get("calm_ward"):
            print(f"{player['name']} 的镇静剂抵消了这次理智伤害")
            player["calm_ward"] = False
            sanity = 0
        if sanity:
            player["sanity"] = max(0, player["sanity"] - sanity)
        if health:
            player["health"] = max(0, player["health"] - health)

    def heal(self, player, sanity=0, health=0):
        if sanity:
            player["sanity"] = min(player.get("max_sanity", MAX_STAT), player["sanity"] + sanity)
        if health:
            player["health"] = min(player.get("max_health", MAX_STAT), player["health"] + health)

    def hurt_alive(self, sanity=0, health=0, msg=None):
        for p in self.alive:
            self.hurt(p, sanity, health)
            if msg:
                print(msg.format(name=p["name"], sanity=sanity, health=health))

    def lose_max_sanity(self, player, amount=1):
        player["max_sanity"] = max(8, player["max_sanity"] - amount)
        player["sanity"] = min(player["sanity"], player["max_sanity"])

    def raise_fear(self, amount=1):
        self.fear_level = min(self.max_fear_level, self.fear_level + amount)
        print(f"恐惧等级提升至: {self.fear_level}")

    def draw_to_hand(self):
        if not self.mansion_deck:
            return None
        card = self.mansion_deck.pop()
        self.hand_cards.append(card)
        return card

    def return_rooms(self, n):
        n = min(n, len(self.explored_rooms))
        for _ in range(n):
            self.mansion_deck.append(self.explored_rooms.pop())
        random.shuffle(self.mansion_deck)
        return n

    def maybe_d30(self, chance, msg):
        if self.fear_level >= 5 and random.random() < chance:
            print(msg)
            self.trigger_d30_event()
            return True
        return False

    def check_all(self, last_action=None, fail=None, ok=None, difficulty=None):
        for i, p in enumerate(self.players):
            if not p["alive"]:
                continue
            if last_action:
                self.last_action = last_action
            if not self.check_success(difficulty=difficulty, player_idx=i):
                if fail:
                    fail(p, i)
            elif ok:
                ok(p, i)

    def choose_role(self, name):
        print(f"\n为 {name} 选择身份：")
        for key, role in ROLES.items():
            print(f"  {key}) {role['name']} — {role['desc']}")
        choice = input("输入编号 (默认1): ").strip() or "1"
        if choice not in ROLES:
            choice = "1"
        role = ROLES[choice]
        print(f"{name} 成为了【{role['name']}】")
        return role

    def setup_game(self):
        print("===== 古宅低语 - 游戏初始化 =====")
        print("提示：检定使用D8；恐惧每两回合才上升一级；揭示失败不会立刻团灭。")
        for i in range(self.num_players):
            name = input(f"请输入玩家{i + 1}的名称: ").strip() or f"玩家{i + 1}"
            role = self.choose_role(name)
            self.players.append({
                "name": name,
                "role": role["name"],
                "bonus": role["bonus"],
                "sanity": MAX_STAT,
                "health": MAX_STAT,
                "alive": True,
                "stunned": False,
                "restricted": False,
                "max_sanity": MAX_STAT,
                "max_health": MAX_STAT,
                "items": [],
                "calm_ward": False,
            })
            print(f"欢迎 {name} 加入游戏！")

        starter = random.choice(self.players)
        self.grant_item(starter, "提灯")
        print(f"进入古宅前，{starter['name']} 在门廊找到了一盏还能亮的提灯。")

        self.create_decks()
        print("古宅牌堆和核心秘密已创建...")
        print(f"初始恐惧等级: {self.fear_level}")
        print("游戏准备就绪！古宅的大门缓缓打开...")
        time.sleep(1)

    def create_decks(self):
        full_deck = [{"suit": s, "value": v} for s in SUITS for v in VALUES]
        self.core_secrets = [c for c in full_deck if c["value"] == "K"]
        random.shuffle(self.core_secrets)
        self.mansion_deck = [c for c in full_deck if c["value"] != "K"]
        random.shuffle(self.mansion_deck)
        self.hand_cards = []
        self.explored_rooms = []

    def check_success(self, difficulty=None, player_idx=0):
        difficulty = self.fear_level if difficulty is None else difficulty
        difficulty = max(2, difficulty)
        player = self.players[player_idx] if player_idx < len(self.players) else None
        if self.last_action == "调查房间" and player and player.get("bonus") == "investigate":
            difficulty = max(2, difficulty - 1)
            print("【调查员】调查难度-1")
        if self.last_action == "探索房间" and player and player.get("bonus") == "scholar" and self.explored_rooms:
            if self.explored_rooms[-1]["suit"] == "♣":
                difficulty = max(2, difficulty - 1)
                print("【学者】解读痕迹更容易")
        if self.high_fear:
            difficulty += 1
            print(f"【恐惧笼罩】检定难度+1 (当前难度: {difficulty})")
        if self.next_turn_difficulty_penalty:
            difficulty += 1
            print(f"【环境压抑】检定难度+1 (当前难度: {difficulty})")
        roll = self.roll(8)
        bonus = self.check_bonus
        self.check_bonus = 0
        total = roll + bonus
        bonus_txt = f"+{bonus}" if bonus else ""
        print(f"投掷D8: {roll}{bonus_txt}, 合计{total}, 难度: {difficulty}")
        return total >= difficulty

    def show_hud(self, player):
        print(f"理智: {player['sanity']}/{player['max_sanity']}, 生命: {player['health']}/{player['max_health']}")
        print(f"身份: {player['role']} | 恐惧: {self.fear_level}/{self.max_fear_level} | 手牌: {len(self.hand_cards)} | 已探索: {len(self.explored_rooms)}")
        if player["items"]:
            print("道具: " + ", ".join(player["items"]))
        if self.journal:
            print(f"日志条目: {len(self.journal)} 条 (行动6可查阅)")
        if self.silence_mode:
            print("【声音剥夺中】你无法听到任何声音，也无法说话")
        if self.trust_crisis:
            print("【信任危机】玩家之间不能共享信息")

    def player_turn(self, player_idx):
        player = self.players[player_idx]
        if not player["alive"]:
            print(f"{player['name']} 已失去行动能力")
            return
        if self.skip_player_turn:
            print(f"由于时间跳跃，跳过{player['name']}的回合")
            self.skip_player_turn = False
            return
        if player["stunned"]:
            print(f"{player['name']} 处于眩晕状态，跳过回合")
            player["stunned"] = False
            return
        if player.get("bonus") == "medium" and player["sanity"] < player["max_sanity"] / 2:
            self.heal(player, sanity=1)
            print(f"【灵媒】低语安抚了你，恢复1点理智")
        if player["restricted"]:
            print(f"{player['name']} 的行动受到限制，只能探索")
            self.last_action = "探索房间"
            self.explore_room(player_idx)
            player["restricted"] = False
            return

        print(f"\n===== {player['name']}的回合 =====")
        self.show_hud(player)

        actions = {
            "1": ("探索房间", self.explore_room),
            "2": ("调查房间", self.investigate_room),
            "3": ("稳住心神", self.calm_mind),
            "4": ("使用道具", self.use_item),
            "5": ("互助", self.help_ally),
            "6": ("查阅日志", self.read_journal),
        }
        choice = input("选择行动: (1)探索 (2)调查 (3)稳住心神 (4)道具 (5)互助 (6)日志: ").strip()
        if choice in actions:
            name, fn = actions[choice]
            self.last_action = name
            fn(player_idx)
        else:
            print("无效行动，改为探索房间")
            self.last_action = "探索房间"
            self.explore_room(player_idx)

    def special_room(self, player, card):
        value = card["value"]
        if value == "A":
            print("【王牌房间】你撞见了宅邸的关键节点。")
            card = self.draw_to_hand()
            if card:
                print(f"额外获得线索: {card_str(card)}")
            self.add_journal("王牌房间里藏着通往核心秘密的拼图碎片。")
        elif value == "J":
            print("【仆役残影】一个身着制服的模糊身影为你让开一条路。")
            if yn("跟随仆人？可能获得道具，也可能受惊 (y/n): "):
                if self.roll(8) >= 3:
                    self.grant_item(player)
                else:
                    self.hurt(player, sanity=1)
                    print("仆人忽然转过头，脸是空的。你失去1点理智。")
        elif value == "Q":
            print("【女主人幻影】她坐在窗边，邀请你听一段往事。")
            if yn("倾听？(y/n): "):
                self.add_journal(random.choice(TRAGEDIES))
                self.heal(player, sanity=2)
                print("往事让你更理解这座宅邸，恢复2点理智。")
                if self.core_secrets:
                    suit = self.core_secrets[0]["suit"]
                    self.add_journal(K_SECRETS[suit]["hint"])
        elif value == "10":
            print("【危险升级】这个房间特别不安分，但你也可能趁乱拿走东西。")
            if yn("冒险搜刮？(y/n): "):
                self.grant_item(player)
                if self.roll(8) <= 2:
                    self.hurt(player, health=1)
                    print("碎玻璃划伤了你，失去1点生命。")

    def explore_room(self, player_idx):
        if not self.mansion_deck:
            print("古宅已探索完毕！也许该把线索拼起来了。")
            if len(self.hand_cards) >= 3:
                if yn("牌堆空了，是否立刻尝试揭示秘密？(y/n): "):
                    self.reveal_secret()
            return

        card = self.mansion_deck.pop()
        self.explored_rooms.append(card)
        title = room_title(card)
        print(f"探索到新房间: {card_str(card)} 「{title}」")
        print(ROOM_FLAVOR.get(card["suit"], "这里很安静，安静得不对。"))
        player = self.players[player_idx]
        encounter = max(2, self.fear_level)
        if self.high_fear:
            print("【恐惧笼罩】遭遇难度增加")
            encounter += 1

        if card["suit"] == "♠":
            print("一股寒意袭来...")
            if not self.check_success(difficulty=encounter, player_idx=player_idx):
                damage = self.dmg(1, 1)
                extra = 1 if self.high_fear else 0
                if player.get("bonus") == "hunter":
                    damage = max(0, damage - 1)
                    extra = 0
                    print("【猎手】你扛住了部分冲击")
                print(f"你未能完全抵抗恐惧，失去{damage + extra}点理智和{damage}点生命")
                self.hurt(player, damage + extra, damage)
            else:
                print("你成功抵抗了恐惧")
                if random.random() < 0.35:
                    self.grant_item(player, random.choice(["绷带", "护身符"]))
            self.defeated_monsters.append(card)

        elif card["suit"] == "♥":
            print("你看到了一些令人安心的东西...")
            self.sanctuaries.append(card)
            if yn("选择恢复3点理智？(y/n): "):
                self.heal(player, sanity=3)
                print("温暖稍纵即逝，但确实帮了你。")
                d4 = self.roll(4)
                print(f"投掷D4: {d4}")
                trap = 4 if not self.high_fear else 3
                if d4 >= trap:
                    damage = self.dmg(1, 1)
                    print(f"你发现那是假象，失去{damage}点理智")
                    self.hurt(player, sanity=damage)
                else:
                    print("这一次，安慰是真的。")
                    if random.random() < 0.3:
                        self.grant_item(player, "护身符")

        elif card["suit"] == "♦":
            print("你找到了一些可能有用的东西...")
            hand_card = self.draw_to_hand()
            if hand_card:
                print(f"获得手牌: {card_str(hand_card)}")
            if random.random() < 0.55:
                self.grant_item(player)
            d4 = self.roll(4)
            print(f"投掷D4: {d4}, 恐惧等级: {self.fear_level}")
            chance = 0.25 if self.high_fear else (0.12 if self.fear_level >= 5 else 0)
            if random.random() < chance:
                print("你的行动惊动了古宅深处的存在！")
                self.trigger_d30_event()
            elif d4 >= self.fear_level + 1:
                print("你惊动了什么！")
                self.mansion_action()

        elif card["suit"] == "♣":
            print("你发现了奇怪的痕迹...")
            diff = max(2, self.fear_level - (1 if player.get("bonus") == "scholar" else 0))
            if self.check_success(difficulty=diff, player_idx=player_idx):
                if self.core_secrets:
                    secret = self.core_secrets[0]
                    print(f"你瞥见了古宅的秘密: {card_str(secret)}")
                    self.add_journal(K_SECRETS[secret["suit"]]["hint"])
                    self.secrets_seen += 1
                else:
                    print("你没有发现更多秘密")
                if random.random() < 0.4:
                    extra = self.draw_to_hand()
                    if extra:
                        print(f"痕迹旁还压着一张纸条: {card_str(extra)}")
            else:
                damage = self.dmg(1, 1)
                print(f"你什么也没看懂，反而感到困惑，失去{damage}点理智")
                self.hurt(player, sanity=damage)

        self.special_room(player, card)
        self.check_player_status()

    def investigate_room(self, player_idx):
        if not self.explored_rooms:
            print("没有房间可以调查")
            return
        print("调查房间...")
        recent = self.explored_rooms[-3:]
        print("最近探索过: " + ", ".join(f"{card_str(c)}「{room_title(c)}」" for c in recent))
        difficulty = max(2, self.fear_level)
        if self.check_success(difficulty=difficulty, player_idx=player_idx):
            card = self.draw_to_hand()
            if not card:
                print("没有更多线索了")
                return
            print(f"你发现了一个线索: {card_str(card)}")
            print(f"当前手牌: {len(self.hand_cards)}张")
            for i, c in enumerate(self.hand_cards, 1):
                print(f"{i}. {card_str(c)}")
            if random.random() < 0.25:
                self.grant_item(self.players[player_idx], random.choice(["旧日记", "地图残页", "钥匙"]))
            required = 3 if self.high_fear else 4
            if len(self.hand_cards) >= required:
                print(f"你已收集到{len(self.hand_cards)}张手牌 (需要{required}张来揭示秘密)")
                if yn("是否尝试揭示秘密？(y/n): "):
                    self.reveal_secret()
        else:
            print("调查失败，没有发现任何东西")
            print("你至少记下了房间的格局，恢复1点理智。")
            self.heal(self.players[player_idx], sanity=1)
            self.maybe_d30(0.08, "你的失败调查引起了古宅的注意！")

    def calm_mind(self, player_idx):
        player = self.players[player_idx]
        print("尝试稳住心神...")
        in_sanctuary = bool(self.sanctuaries)
        difficulty = max(2, self.fear_level - (1 if in_sanctuary else 0))
        if in_sanctuary:
            print("你躲进了先前发现的安心角落。")
        if self.check_success(difficulty=difficulty, player_idx=player_idx):
            recover = 3 if not self.high_fear else 2
            if player.get("bonus") == "medic":
                recover += 1
            self.heal(player, sanity=recover)
            print(f"理智恢复{recover}点")
            if random.random() < 0.2:
                self.heal(player, health=1)
                print("你也包扎了一下伤口，恢复1点生命")
        else:
            print("未能完全稳住心神，但深呼吸仍有效，恢复1点理智")
            self.heal(player, sanity=1)
            self.maybe_d30(0.08, "你的精神波动吸引了古宅的恶意！")

    def use_item(self, player_idx):
        player = self.players[player_idx]
        if not player["items"]:
            print("你没有任何道具。")
            return
        print("可用道具：")
        for i, item in enumerate(player["items"], 1):
            print(f"  {i}. {item} — {ITEMS[item]}")
        raw = input("使用哪一件？输入编号 (其他取消): ").strip()
        if not raw.isdigit() or not (1 <= int(raw) <= len(player["items"])):
            print("取消使用。")
            return
        item = player["items"].pop(int(raw) - 1)
        print(f"使用了【{item}】")
        if item == "提灯":
            self.check_bonus = 2
            print("提灯照亮了前方，下次检定+2")
        elif item == "绷带":
            amount = 4 if player.get("bonus") == "medic" else 3
            self.heal(player, health=amount)
            print(f"恢复{amount}点生命")
        elif item == "护身符":
            self.heal(player, sanity=3)
            print("恢复3点理智")
        elif item == "钥匙":
            player["items"].append("钥匙")
            print("钥匙最好留到揭示秘密时自动生效。已放回。")
        elif item == "旧日记":
            card = self.draw_to_hand()
            if card:
                print(f"日记夹着一张牌: {card_str(card)}")
            else:
                print("日记只剩下空白页。")
                self.heal(player, sanity=2)
        elif item == "镇静剂":
            player["calm_ward"] = True
            print("你准备好忽略下一次理智伤害")
        elif item == "圣水":
            if self.fear_level > 1:
                self.fear_level -= 1
                print(f"圣水让宅邸退缩了一寸，恐惧等级: {self.fear_level}")
            else:
                self.heal(player, sanity=2, health=2)
                print("宅邸尚在沉睡，圣水只是让你好受些。")
        elif item == "地图残页":
            if self.explored_rooms:
                n = self.return_rooms(1)
                print(f"你绕开了{n}个危险房间")
            card = self.draw_to_hand()
            if card:
                print(f"地图背面是线索: {card_str(card)}")

    def help_ally(self, player_idx):
        player = self.players[player_idx]
        others = [p for p in self.alive if p is not player]
        if not others:
            print("没有可以互助的同伴，你只能靠自己。恢复2点理智。")
            self.heal(player, sanity=2)
            return
        if self.trust_crisis:
            print("信任危机中无法互助，你只能默默握住自己的手腕，恢复1点理智。")
            self.heal(player, sanity=1)
            return
        print("选择帮助对象：")
        for i, p in enumerate(others, 1):
            print(f"  {i}. {p['name']} 理智{p['sanity']}/{p['max_sanity']} 生命{p['health']}/{p['max_health']}")
        raw = input("输入编号: ").strip()
        if not raw.isdigit() or not (1 <= int(raw) <= len(others)):
            print("没有人被选中。")
            return
        target = others[int(raw) - 1]
        print("1) 安抚（你-1理智，对方+3理智）  2) 包扎（你-1生命，对方+3生命）")
        kind = input("选择: ").strip()
        if kind == "2":
            self.hurt(player, health=1)
            self.heal(target, health=3)
            print(f"{player['name']} 为 {target['name']} 包扎，对方恢复3点生命")
        else:
            self.hurt(player, sanity=1)
            self.heal(target, sanity=3)
            print(f"{player['name']} 稳住了 {target['name']}，对方恢复3点理智")

    def read_journal(self, player_idx):
        player = self.players[player_idx]
        print("===== 探索日志 =====")
        if not self.journal:
            print("还没有记下任何线索。你在回忆中勉强找回一丝平静，恢复1点理智。")
            self.heal(player, sanity=1)
            return
        for i, entry in enumerate(self.journal, 1):
            print(f"{i}. {entry}")
        print(f"已瞥见核心秘密痕迹 {self.secrets_seen} 次")
        self.heal(player, sanity=1)
        print("整理思绪后恢复1点理智。")

    def trigger_d30_event(self):
        self.d30_event_count += 1
        self.consecutive_d30 += 1
        print(f"\n=== D30事件 #{self.d30_event_count} ===")
        if self.consecutive_d30 > 1:
            print(f"【连续事件】这是连续第{self.consecutive_d30}个D30事件！")
        d30 = self.roll(30)
        name, _ = D30_INFO.get(d30, ("未知事件", ""))
        print(f"D30投掷: {d30} - {name}")
        getattr(self, f"event_{d30}", self.event_default)()
        if self.high_fear and random.random() < 0.12:
            print("【连锁反应】一个事件引发了另一个事件！")
            self.trigger_d30_event()

    def mansion_action(self):
        d4 = self.roll(4)
        print(f"古宅行动投掷D4: {d4}")

        if self.fear_level <= 3:
            if d4 <= 2:
                print("窸窣作响...无事发生，但令人不安")
            elif d4 == 3:
                print("幻象出现...")
                if self.alive:
                    p = random.choice(self.alive)
                    idx = self.players.index(p)
                    if not self.check_success(player_idx=idx):
                        print(f"{p['name']} 未能抵抗幻象，失去1点理智")
                        self.hurt(p, sanity=1)
                    else:
                        print(f"{p['name']} 看穿了幻象")
            elif random.random() < 0.1:
                print("古宅的不安凝聚成了实体！")
                self.trigger_d30_event()
            else:
                print("古宅的秘密逼近...")
                if self.core_secrets:
                    print(f"你瞥见了古宅的秘密: {card_str(self.core_secrets[0])}")
                    self.add_journal(K_SECRETS[self.core_secrets[0]["suit"]]["hint"])

        elif self.fear_level <= 5:
            if d4 == 1:
                if self.alive:
                    p = random.choice(self.alive)
                    print(f"{p['name']} 受到物质攻击，失去1点生命")
                    self.hurt(p, health=1)
            elif d4 == 2:
                print("精神攻击！所有玩家进行检定")
                self.check_all(
                    fail=lambda p, i: (self.hurt(p, sanity=1), print(f"{p['name']} 未能抵抗精神攻击，失去1点理智"))
                )
            elif d4 == 3:
                print("空间扭曲...房间位置发生变化")
                if self.explored_rooms:
                    random.shuffle(self.explored_rooms)
                    print("房间布局已改变")
            else:
                print("高潮事件发生！")
                self.trigger_d30_event()

        else:
            print("【极度恐惧】古宅的恶意达到了顶峰！")
            if d4 == 4:
                print("高潮事件发生！")
                self.trigger_d30_event()
            elif random.random() < 0.4:
                self.trigger_d30_event()
            elif d4 == 1:
                self.hurt_alive(health=2)
                print("所有玩家受到2点生命伤害")
            elif d4 == 2:
                print("强烈精神攻击！所有玩家进行检定")

                def fail(p, i):
                    self.hurt(p, sanity=2)
                    print(f"{p['name']} 未能抵抗精神攻击，失去2点理智")

                def ok(p, i):
                    self.hurt(p, sanity=1)
                    print(f"{p['name']} 部分抵抗了精神攻击，失去1点理智")

                self.check_all(fail=fail, ok=ok)
            else:
                print("空间完全重构！")
                keep = min(5, len(self.explored_rooms))
                if self.explored_rooms:
                    self.explored_rooms = random.sample(self.explored_rooms, keep)
                    print(f"只保留了{keep}个房间，其余房间被重新洗入牌堆")

        self.check_player_status()

    def _tick_flag(self, flag, duration, end_msg):
        if not getattr(self, flag):
            return
        setattr(self, duration, getattr(self, duration) - 1)
        if getattr(self, duration) <= 0:
            setattr(self, flag, False)
            print(end_msg)

    def mansion_turn(self):
        if self.skip_mansion_turn:
            print("古宅因献祭而平静，跳过古宅回合")
            self.skip_mansion_turn = False
            return

        print("\n===== 古宅回合 =====")
        self.fear_delay += 1
        if self.fear_delay >= 2 and self.fear_level < self.max_fear_level:
            self.fear_delay = 0
            self.fear_level += 1
            print(f"恐惧等级提升至: {self.fear_level}")
            messages = {
                3: "【恐惧加深】古宅的低语变得更加清晰...",
                5: "【高压将至】宅邸开始苏醒，请尽快拼起线索。",
                6: "【绝望降临】古宅完全苏醒，你们的时间不多了！",
            }
            if self.fear_level in messages:
                print(messages[self.fear_level])
        else:
            print("古宅还在观察你们，恐惧暂未加深。")

        self.consecutive_d30 = 0
        self.mansion_action()
        self._tick_flag("silence_mode", "silence_duration", "声音恢复了...")
        self._tick_flag("trust_crisis", "trust_crisis_duration", "信任危机解除了...")
        self._tick_flag("eye_of_mansion", "eye_duration", "全视之眼消失了...")
        if self.temp_fear_increase:
            self.fear_level = self.original_fear
            self.temp_fear_increase = False
            print("恐惧等级恢复正常")
        self.next_turn_difficulty_penalty = False
        if self.high_fear and random.random() < 0.18:
            print("古宅的恶意自发凝聚！")
            self.trigger_d30_event()

    def reveal_secret(self):
        if not self.core_secrets:
            print("没有秘密可以揭示")
            return
        required = 3 if self.high_fear else 4
        if len(self.hand_cards) < required:
            print(f"手牌不足（需要{required}张）")
            return
        print("弃掉所有手牌，尝试揭示秘密...")
        hand_count = len(self.hand_cards)
        self.hand_cards = []
        secret_card = self.core_secrets[0]
        info = K_SECRETS.get(secret_card["suit"], {"name": "未知的秘密", "description": "这是一个未知的秘密", "modifier": 0})
        print(f"古宅的核心秘密: {card_str(secret_card)} - {info['name']}")
        print(info["description"])
        print("进行最终对抗...")
        difficulty = 6 + self.fear_level * 2
        keys = sum(1 for p in self.players for item in p["items"] if item == "钥匙")
        if keys:
            difficulty = max(6, difficulty - 3 * min(keys, 2))
            print(f"钥匙降低了揭示难度，当前难度: {difficulty}")
            remaining = min(keys, 2)
            for p in self.players:
                while remaining and "钥匙" in p["items"]:
                    p["items"].remove("钥匙")
                    remaining -= 1
        scholar_bonus = 3 if any(p["alive"] and p.get("bonus") == "scholar" for p in self.players) else 0
        result = self.roll(30)
        print(f"投掷D30: {result}, 难度: {difficulty}")
        modifier = info.get("modifier", 0)
        if modifier == "hand_bonus":
            bonus = hand_count * 2
            result += bonus
            print(f"弃掉了{hand_count}张手牌，获得+{bonus}加值")
        else:
            result += modifier
            print(f"秘密修饰: {modifier}")
        result += scholar_bonus
        if scholar_bonus:
            print(f"学者加值: +{scholar_bonus}")
        result += min(4, self.secrets_seen)
        if self.secrets_seen:
            print(f"先前窥见的痕迹加值: +{min(4, self.secrets_seen)}")
        print(f"最终结果: {result}")
        if result >= difficulty:
            print("你们成功了！理解了秘密并找到了出路")
            self.core_secrets.pop(0)
            self.victory = True
            self.game_over = True
            wounds = any(p["sanity"] < p["max_sanity"] / 2 or p["health"] < p["max_health"] / 2 for p in self.alive)
            self.ending_note = "你们带着伤痕逃出黎明。" if wounds else "你们几乎完整地夺回了自己。"
        else:
            print("对抗失败，但你们没有立刻被吞噬——古宅只是更饿了。")
            self.hurt_alive(sanity=3, health=1, msg="{name} 被反噬，失去{sanity}点理智和{health}点生命")
            self.raise_fear()
            secret = self.core_secrets.pop(0)
            self.core_secrets.append(secret)
            print("这个秘密被重新藏了起来。收集更多手牌后可以再试。")
            self.check_player_status()

    def check_player_status(self):
        for p in self.players:
            if p["sanity"] <= 0 or p["health"] <= 0:
                if p["alive"]:
                    p["alive"] = False
                    print(f"{p['name']} 已失去意识或发疯")
        if not self.alive:
            print("所有玩家都失败了...游戏结束")
            self.game_over = True
            self.ending_note = "宅邸收下了所有闯入者。"

    def event_default(self):
        print("发生了难以名状的恐怖事件")
        if self.alive:
            p = random.choice(self.alive)
            damage = self.dmg(1, 2)
            self.hurt(p, sanity=damage)
            print(f"{p['name']} 失去了{damage}点理智")

    def event_1(self):
        print("所有墙上的肖像画的眼睛都开始流血并注视着玩家！诡异的低语在画框中回荡。")
        d = self.dmg(1, 2)
        self.check_all(
            fail=lambda p, i: (self.hurt(p, sanity=d), print(f"{p['name']} 未能抵抗恐惧，失去{d}点理智")),
            ok=lambda p, i: print(f"{p['name']} 成功避开了那些注视"),
        )

    def event_2(self):
        print("你们所在的房间墙壁突然变得柔软、温热，并开始有节奏地搏动，如同活物！")
        d = self.dmg(1, 2)
        self.check_all(
            last_action="躲避墙壁",
            fail=lambda p, i: (self.hurt(p, health=d), print(f"{p['name']} 被墙壁'舔舐'，受到{d}点伤害")),
            ok=lambda p, i: print(f"{p['name']} 成功躲开了蠕动的墙壁"),
        )

    def event_3(self):
        print("场景瞬间切换回你们刚进入古宅时的样子！一切都回到了最初的时刻。")
        keep = min(2, len(self.hand_cards))
        lost = len(self.hand_cards) - keep
        self.hand_cards = self.hand_cards[:keep]
        print(f"你们失去了{lost}张手牌，仍保住{keep}张")
        if self.high_fear and self.explored_rooms:
            n = self.return_rooms(min(2, len(self.explored_rooms) // 2))
            print(f"{n}个已探索房间被重新洗入牌堆")

    def event_4(self):
        print("一个清晰而恶毒的声音在每个人耳边低语一个他们最深处的秘密或恐惧！")
        d = self.dmg(1, 2)
        self.hurt_alive(sanity=d)
        print(f"所有存活玩家失去{d}点理智")

    def event_5(self):
        print("每个玩家都在房间的玻璃或水渍倒影中看到另一个充满恶意的自己！那倒影似乎在嘲笑你们。")
        self.original_fear = self.fear_level
        self.fear_level = min(self.max_fear_level, self.fear_level + 1)
        self.temp_fear_increase = True
        print(f"恐惧等级暂时提升至: {self.fear_level}")

    def event_6(self):
        print("探索区所有通道被收回并洗回古宅牌堆，出口被暂时封锁了！")
        corridors = [c for c in self.explored_rooms if c["suit"] in ("♦", "♣")]
        for c in corridors[: max(0, len(corridors) - 1)]:
            self.explored_rooms.remove(c)
            self.mansion_deck.append(c)
        random.shuffle(self.mansion_deck)
        print("部分通道牌被收回，至少留下一条路")
        if self.high_fear and self.hand_cards:
            lost = min(1, len(self.hand_cards))
            del self.hand_cards[-lost:]
            print(f"{lost}张手牌丢失了")

    def event_7(self):
        print("远处传来空灵、走调的孩童歌唱声，歌词模糊地叙述着古宅的悲剧！")
        self.add_journal(random.choice(TRAGEDIES))
        if yn("竖起耳朵听完整首歌？可能提升恐惧，但能获得线索 (y/n): "):
            extra = self.draw_to_hand()
            if extra:
                print(f"歌词变成了线索: {card_str(extra)}")
            if random.random() < 0.4:
                self.raise_fear()
        else:
            print("你们堵住耳朵，歌谣渐渐远去。")

    def event_8(self):
        print("一名随机玩家的手臂不由自主地抬起，指向一个方向！")
        if not self.alive:
            return
        player = random.choice(self.alive)
        player["restricted"] = True
        print(f"{player['name']} 的行动受到限制")
        if self.mansion_deck:
            peek = self.mansion_deck[-1]
            print(f"那只手指向的方向隐约是: {card_str(peek)}")

    def event_9(self):
        print("房间的桌上突然出现一桌腐烂生蛆、但却散发着令人无法抗拒香气的盛宴！")
        if yn("是否选择食用？(y/n): ") and self.alive:
            p = random.choice(self.alive)
            heal = 3
            self.heal(p, health=heal)
            print(f"{p['name']} 恢复{heal}点生命")
            if random.random() < 0.35:
                self.lose_max_sanity(p)
                print(f"{p['name']} 感到胃里多了一样东西，永久失去1点最大理智值")
            else:
                print("这一次，食物只是恶心，没有更深的代价。")

    def event_10(self):
        print("一个死去的人重新出现，并变得更加强大！")
        if not self.defeated_monsters:
            print("但今夜没有死者回应召唤。宅邸空欢喜一场。")
            return
        monster = self.defeated_monsters.pop()
        bonus = 1
        print(f"{card_str(monster)} 重新出现！")
        print(f"这个死者变得更强大，检定难度+{bonus}")
        d = self.dmg(1, 2)
        self.check_all(
            last_action="对抗死者",
            difficulty=self.fear_level + bonus,
            fail=lambda p, i: (
                self.hurt(p, d, d),
                print(f"{p['name']} 未能抵抗死者，失去{d}点理智和{d}点生命"),
            ),
            ok=lambda p, i: print(f"{p['name']} 成功抵抗了死者"),
        )

    def event_11(self):
        print("空间本身开始扭曲折叠，房间之间的关系变得混乱不堪！")
        if not self.explored_rooms:
            return
        random.shuffle(self.explored_rooms)
        print("所有已探索房间的位置发生了随机变化")
        if self.high_fear and len(self.explored_rooms) > 1:
            n = self.return_rooms(1)
            print(f"{n}个房间在空间折叠中丢失了")

    def event_12(self):
        print("古宅开始吞噬你们的记忆，过去的经历变得模糊不清！")
        for p in self.alive:
            if self.hand_cards and random.random() < 0.35:
                lost = self.hand_cards.pop()
                print(f"{p['name']} 忘记了关于{card_str(lost)}的记忆")
            if random.random() < 0.45:
                self.hurt(p, sanity=1)
                print(f"{p['name']} 失去1点理智")

    def event_13(self):
        print("无数黑色甲虫、蜈蚣和其他不知名的虫类从地板缝隙、墙壁裂缝中涌出！")
        d = self.dmg(1, 2)
        self.check_all(
            last_action="躲避虫群",
            fail=lambda p, i: (self.hurt(p, health=d), print(f"{p['name']} 被虫群叮咬，受到{d}点伤害")),
            ok=lambda p, i: print(f"{p['name']} 成功躲开了虫群"),
        )

    def event_14(self):
        print("一个半透明的女性身影出现在房间角落，低声啜泣着，空气中弥漫着悲伤与寒冷。")
        d = self.dmg(1, 2)
        self.check_all(
            fail=lambda p, i: (self.hurt(p, sanity=d), print(f"{p['name']} 被哀悼之影的悲伤感染，失去{d}点理智")),
            ok=lambda p, i: (self.heal(p, sanity=1), print(f"{p['name']} 轻轻应了一声，悲伤减轻，恢复1点理智")),
        )
        print("哀悼之影的存在让环境变得更加压抑，下一回合所有检定难度+1")
        self.next_turn_difficulty_penalty = True

    def event_15(self):
        print("古宅传达出一个明确的要求：需要献祭！")
        if not (self.alive and (self.hand_cards or True)):
            return
        print("选择献祭：1)一张手牌 2)一名玩家的1点最大理智值 3)一件道具")
        choice = input("请输入选择(1/2/3): ").strip()
        if choice == "1" and self.hand_cards:
            card = self.hand_cards.pop()
            print(f"你们献祭了{card_str(card)}，古宅暂时平静了")
            self.skip_mansion_turn = True
        elif choice == "2" and self.alive:
            p = random.choice(self.alive)
            self.lose_max_sanity(p)
            print(f"{p['name']} 永久失去了1点最大理智值作为祭品，古宅暂时平静了")
            self.skip_mansion_turn = True
        elif choice == "3":
            owners = [p for p in self.alive if p["items"]]
            if owners:
                p = random.choice(owners)
                item = p["items"].pop()
                print(f"{p['name']} 献上了【{item}】，古宅暂时平静了")
                self.skip_mansion_turn = True
            else:
                print("没有道具可献。古宅不悦，但没有立刻发怒。")
        else:
            print("你们拒绝献祭。古宅记下了这笔账，但没有立刻加码。")
            if random.random() < 0.4:
                self.raise_fear()

    def event_16(self):
        print("时间突然跳跃，当你们回过神时，发现蜡烛已经烧掉了一大截！")
        print("你们失去了一段时间，下一个玩家回合将被跳过")
        self.skip_player_turn = True
        if self.high_fear and self.hand_cards and random.random() < 0.5:
            lost = self.hand_cards.pop()
            print(f"在时间跳跃中，你们失去了{card_str(lost)}的记忆")

    def event_17(self):
        print("油腻的触须状物从玩家的影子中伸出，试图缠绕束缚！")
        if not self.alive:
            return
        p = random.choice(self.alive)
        print(f"{p['name']} 被寄生触手盯上了！")
        self.last_action = "挣脱触手"
        if not self.check_success(player_idx=self.players.index(p)):
            p["restricted"] = True
            self.hurt(p, health=1)
            print(f"{p['name']} 被触手束缚并伤害，下回合只能探索")
        else:
            print(f"{p['name']} 成功挣脱了触手")

    def event_18(self):
        print("天花板上睁开一只巨大的、布满血丝的眼睛，冷漠地注视着一切！")
        d = self.dmg(1, 2)
        self.check_all(fail=lambda p, i: (self.hurt(p, sanity=d), print(f"{p['name']} 与全视之眼对视，失去{d}点理智")))
        print("在全视之眼的注视下，古宅知晓你们的一切行动")
        self.eye_of_mansion = True
        self.eye_duration = 2

    def event_19(self):
        print("所有的声音瞬间消失，包括你们自己的心跳声和呼吸声！")
        self.silence_mode = True
        self.silence_duration = 2
        print("在接下来的两个回合中，所有玩家无法进行语言交流")
        if self.alive:
            p = random.choice(self.alive)
            self.grant_item(p, "镇静剂")
            print("寂静里有人摸到一管没标签的药水。")

    def event_20(self):
        print("你们瞬间目睹了古宅中曾发生的一起关键悲剧事件的幻象！")
        scene = random.choice(TRAGEDIES)
        print(f"你们看到了: {scene}")
        self.add_journal(scene)
        d = self.dmg(1, 2)

        def ok(p, i):
            print(f"{p['name']} 从幻象中了解到了一些古宅的秘密")
            card = self.draw_to_hand()
            if card:
                print(f"{p['name']} 获得了{card_str(card)}作为洞察奖励")

        self.check_all(
            fail=lambda p, i: (self.hurt(p, sanity=d), print(f"{p['name']} 被幻象震撼，失去{d}点理智")),
            ok=ok,
        )

    def event_21(self):
        print("古宅的木质结构开始疯狂生长，封堵门廊，创造新的通道！")
        if not self.explored_rooms:
            return
        n = self.return_rooms(random.randint(1, min(2, len(self.explored_rooms))))
        print(f"{n}个房间被生长的木材封堵了")
        if self.mansion_deck:
            room = self.mansion_deck.pop()
            self.explored_rooms.append(room)
            print(f"出现了新的房间: {card_str(room)}「{room_title(room)}」")
        random.shuffle(self.mansion_deck)

    def event_22(self):
        print("古宅的低语在你们之间播种猜疑，你们开始怀疑彼此的动机！")
        self.trust_crisis = True
        self.trust_crisis_duration = 2
        print("在接下来的两个回合中，玩家之间不能共享信息")
        if self.high_fear:
            for p in self.alive:
                if random.random() < 0.3:
                    self.hurt(p, sanity=1)
                    print(f"{p['name']} 因猜疑而失去1点理智")

    def event_23(self):
        print("房间内的重力方向突然改变，持续几秒！所有未固定的物体都飘浮起来。")
        d = self.dmg(1, 2)

        def fail(p, i):
            self.hurt(p, health=d)
            p["stunned"] = True
            print(f"{p['name']} 受到{d}点伤害并被撞晕，下回合无法行动")

        self.check_all(
            last_action="适应重力变化",
            fail=fail,
            ok=lambda p, i: print(f"{p['name']} 成功适应了重力变化"),
        )

    def event_24(self):
        print("门外传来一位玩家亲友的呼救声，惟妙惟肖，令人难以分辨真伪！")
        if not self.alive:
            return
        target = random.choice(self.alive)
        print(f"声音模仿的是{target['name']}的亲友！")
        self.last_action = "分辨真伪"
        if not self.check_success(player_idx=self.players.index(target)):
            print(f"{target['name']} 相信了呼救声，打开了门...")
            print("门外什么亲友都没有，只有一个可怕的存在！")
            d = self.dmg(1, 2)
            self.hurt_alive(sanity=d, health=0, msg="{name} 受到惊吓，失去{sanity}点理智")
        else:
            print(f"{target['name']} 识破了模仿者的诡计，没有上当")
            self.grant_item(target, random.choice(["钥匙", "护身符"]))

    def event_25(self):
        print("玩家们的恐惧凝聚成一个短暂的黑色人形，在房间内一闪而过！")
        if not self.alive:
            return
        weakest = min(self.alive, key=lambda x: x["sanity"])
        d = self.dmg(2, 3)
        self.hurt(weakest, sanity=d)
        print(f"{weakest['name']} 的恐惧被具象化，失去{d}点理智")
        for p in self.alive:
            if p is not weakest:
                self.hurt(p, sanity=1)
                print(f"{p['name']} 受到恐惧辐射，失去1点理智")

    def event_26(self):
        print("古宅似乎从你们身上吸取了生命力，你们感到异常虚弱！")
        self.hurt_alive(sanity=1, health=1, msg="{name} 被吸取生命力，失去{sanity}点理智和{health}点生命")

    def event_27(self):
        print("古宅的力量强制交换了玩家之间的某些属性！")
        if len(self.alive) < 2:
            print("只有一个人时，交换无法完成。你感到一阵错位，恢复1点生命。")
            self.heal(self.alive[0], health=1)
            return
        p1, p2 = random.sample(self.alive, 2)
        if random.random() < 0.5:
            p1["sanity"], p2["sanity"] = p2["sanity"], p1["sanity"]
            print(f"{p1['name']} 和 {p2['name']} 的理智值被交换了")
        else:
            p1["health"], p2["health"] = p2["health"], p1["health"]
            print(f"{p1['name']} 和 {p2['name']} 的生命值被交换了")

    def event_28(self):
        print("地板上出现一个通往绝对黑暗的洞口，从中散发出刺骨的寒意和呜咽声！")
        if not self.alive:
            return
        p = random.choice(self.alive)
        print(f"{p['name']} 感觉被洞口吸引，慢慢靠近...")
        self.last_action = "抵抗洞口吸引"
        if not self.check_success(player_idx=self.players.index(p)):
            d = self.dmg(1, 2)
            self.hurt(p, health=d)
            p["stunned"] = True
            print(f"{p['name']} 被吸入洞口，受到{d}点伤害并被困住一回合")
        else:
            print(f"{p['name']} 抵抗了洞口的吸引，但洞口中传出的低语仍在回响")
            self.hurt(p, sanity=1)
            print(f"{p['name']} 失去1点理智")
            if random.random() < 0.5:
                self.grant_item(p, "旧日记")

    def event_29(self):
        print("你们短暂地感受到了古宅那古老、冰冷、毫无人性的意识！")
        if not self.alive:
            return
        p = random.choice(self.alive)
        print(f"{p['name']} 与古宅之心建立了连接，可以问一个关于古宅的是非问题")
        input("请输入你的问题（古宅只会回答是或否）: ")
        truth = random.choice(["是", "否"])
        print(f"古宅之心的回答: {truth}")
        if yn("付出1点最大理智，换取一条真实日志？(y/n): "):
            self.lose_max_sanity(p)
            if self.core_secrets:
                self.add_journal(K_SECRETS[self.core_secrets[0]["suit"]]["hint"])
            print(f"{p['name']} 因接触古宅之心而永久失去了1点最大理智值")
        else:
            print("你及时切断了联系，只留下一阵耳鸣。")

    def event_30(self):
        print("古宅展示了它真正的力量！一首胜利的、扭曲的华尔兹音乐在宅中响起。")
        self.hurt_alive(sanity=2, health=2)
        print("所有存活玩家失去2点理智和2点生命")
        if self.high_fear:
            print("古宅的力量进一步增强了！")
            p = random.choice(self.alive) if self.alive else None
            if p:
                self.lose_max_sanity(p)
                print(f"{p['name']} 永久失去1点最大理智值")
        if self.alive and random.random() < 0.5:
            self.grant_item(random.choice(self.alive), "圣水")
            print("华尔兹停拍的瞬间，有人握紧了一小瓶圣水。")

    def play_game(self):
        self.setup_game()
        turn = 0
        while not self.game_over:
            print(f"\n{'=' * 20} 第 {turn + 1} 回合 {'=' * 20}")
            for i in range(self.num_players):
                if not self.game_over:
                    self.player_turn(i)
            if not self.game_over:
                self.mansion_turn()
            turn += 1
            if self.high_fear and not self.game_over:
                print("\n【恐惧侵蚀】古宅的恶意持续侵蚀着你们...")
                self.hurt_alive(sanity=1, msg="{name} 失去1点理智")
                self.check_player_status()
            if turn >= 18 and not self.game_over:
                print("宅邸的夜晚没有尽头，但你们已经撑过了最长的守夜。")
                print("大门在晨雾中出现了一道缝。")
                if len(self.hand_cards) >= 3:
                    self.victory = True
                    self.ending_note = "你们没能完全读懂秘密，但活着离开了。"
                else:
                    self.ending_note = "黎明赶走了古宅，你们狼狈地逃了出去。"
                    self.victory = True
                self.game_over = True

        ending = (
            "\n恭喜！你们成功逃离了古宅！"
            if self.victory
            else "\n古宅获得了胜利...你们将永远成为它的一部分"
        )
        print(ending)
        if self.ending_note:
            print(self.ending_note)
        print(f"总共经历了 {self.d30_event_count} 次D30事件")
        print(f"日志中留下了 {len(self.journal)} 条记录")
        if self.journal:
            print("—— 最终日志 ——")
            for entry in self.journal:
                print(f"  · {entry}")


if __name__ == "__main__":
    try:
        num_players = int(input("请输入玩家人数 (1-4): "))
        if not 1 <= num_players <= 4:
            print("玩家人数必须在1-4之间，使用默认值2")
            num_players = 2
    except ValueError:
        print("输入无效，使用默认玩家人数2")
        num_players = 2
    try:
        HorrorMansionGame(num_players).play_game()
    except Exception as e:
        print(f"游戏发生错误: {e}")
        print("重新启动游戏...")
        HorrorMansionGame(2).play_game()
