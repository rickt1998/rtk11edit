from collections import defaultdict

# 0xFF = index 255 maps to white
colour_map = {
    0x00: 0x2828E8, 0x01: 0x387800, 0x02: 0xD00028, 0x03: 0x8C662A, 0x04: 0x200070, 0x05: 0x5A5A5A, 0x06: 0x20DEE0, 0x07: 0xDAD23A, 0x08: 0xF69CB2, 0x09: 0xA0D488,
    0x0A: 0x1E1E1E, 0x0B: 0xF26C20, 0x0C: 0xA286AC, 0x0D: 0x5C1646, 0x0E: 0x900018, 0x0F: 0x8AC832, 0x10: 0xC4447A, 0x11: 0x8692BA, 0x12: 0xC2E088, 0x13: 0x009A7A,
    0x14: 0x463A00, 0x15: 0x423A80, 0x16: 0x9C9C9C, 0x17: 0x746442, 0x18: 0x005490, 0x19: 0xAA2C50, 0x1A: 0xF25E52, 0x1B: 0xFFFA88, 0x1C: 0xF89820, 0x1D: 0xA89870,
    0x1E: 0x942C78, 0x1F: 0x780094, 0x20: 0x86461E, 0x21: 0x007150, 0x22: 0xF79A64, 0x23: 0x12495C, 0x24: 0x8A80AC, 0x25: 0x008FC4, 0x26: 0x00A63C, 0x27: 0xF03450,
    0x28: 0xDCB06C, 0x29: 0xFFF416, 0x2A: 0x80CA87, 0x2B: 0x8EECEC, 0x2C: 0x80A6CC, 0x2D: 0x006FA9, 0x2E: 0xB8700C, 0x2F: 0x6EB8A7, 0x30: 0x20E020, 0x31: 0xE020DE,
    0xFF: 0xFFFFFF
}

city_map = {
    0x00: "Xiang Ping",
    0x01: "Bei Ping",
    0x02: "Ji",
    0x03: "Nan Pi",
    0x04: "Ping Yuan",
    0x05: "Jin Yang",
    0x06: "Ye",
    0x07: "Bei Hai",
    0x08: "Xia Pi",
    0x09: "Xiao Pei",
    0x0A: "Shou Chun",
    0x0B: "Pu Yang",
    0x0C: "Chen Liu",
    0x0D: "Xu Chang",
    0x0E: "Ru Nan",
    0x0F: "Luo Yang",
    0x10: "Wan",
    0x11: "Chang An",
    0x12: "Shang Yong",
    0x13: "An Ding",
    0x14: "Tian Shui",
    0x15: "Wu Wei",
    0x16: "Jian Ye",
    0x17: "Wu",
    0x18: "Hui Ji",
    0x19: "Lu Jiang",
    0x1A: "Chai Sang",
    0x1B: "Jiang Xia",
    0x1C: "Xin Ye",
    0x1D: "Xiang Yang",
    0x1E: "Jiang Ling",
    0x1F: "Chang Sha",
    0x20: "Wu Ling",
    0x21: "Gui Yang",
    0x22: "Ling Ling",
    0x23: "Yong An",
    0x24: "Han Zhong",
    0x25: "Zi Tong",
    0x26: "Jiang Zhou",
    0x27: "Cheng Du",
    0x28: "Jian Ning",
    0x29: "Yun Nan",
    0x2A: "Hu",
    0x2B: "Hu Lao gate",
    0x2C: "Tong Gate",
    0x2D: "Han Gu gate",
    0x2E: "Wu gate",
    0x2F: "Yang Ping",
    0x30: "Jian Ge",
    0x31: "Jia Meng",
    0x32: "Pei Shui",
    0x33: "Mian Zhu",
    0x34: "An Ping port",
    0x35: "Gao Tang",
    0x36: "Xi He",
    0x37: "Bai Ma",
    0x38: "Chang Yang",
    0x39: "Lin Ji",
    0x3A: "Hai Ling",
    0x3B: "Jiang Duo",
    0x3C: "Ru Xu",
    0x3D: "Dun Qiu",
    0x3E: "Guan Du",
    0x3F: "Meng Jin",
    0x40: "Jie Xian",
    0x41: "Xin Feng",
    0x42: "Xia Feng",
    0x43: "Fang Ling",
    0x44: "Wu Hu",
    0x45: "Hu Lin",
    0x46: "Qu A",
    0x47: "Ju Zhang",
    0x48: "Wan Kou",
    0x49: "Jiu Jiang",
    0x4A: "Lu Kou",
    0x4B: "Bou Yang",
    0x4C: "Lu Ling",
    0x4D: "Xia Kou",
    0x4E: "Hu Yang",
    0x4F: "Zhong Lu",
    0x50: "Wu Lin",
    0x51: "Han Jin",
    0x52: "Jiang Jin",
    0x53: "Lu Xian",
    0x54: "Dong Tine",
    0x55: "Gong An",
    0x56: "Wu Xian",
    0xFF: "Not Available",
    0xFFFF: "Not Available",
}


officer_status_map = {
    0x00: "Sovereign",
    0x01: "Viceroy",
    0x02: "Prefect",
    0x03: "Officer",
    0x04: "Free officer",
    0x05: "Prisoner",
    0x06: "Under aged",
    0x07: "Searchable",
    0x08: "Dead",
    0xff: "Not available",
}

officer_ranks_map = {
    0x00: "Prime Minister",
    0x01: "Chief Minister",
    0x02: "Chief Officer",
    0x03: "SeniorMinister",
    0x04: "Minister",
    0x05: "Guard Captain",
    0x06: "Horse Captain",
    0x07: "Marshal",
    0x08: "Chancellor",
    0x09: "Sub-chancellor",
    0x0a: "Court Officer",
    0x0b: "Guard Officer",
    0x0c: "E Off. (conquest)",
    0x0d: "S Off. (conquest)",
    0x0e: "W Off. (conquest)",
    0x0f: "N Off. (conquest)",
    0x10: "Secretary General",
    0x11: "Chief Secretary",
    0x12: "Undersecretary",
    0x13: "Chief Administrator",
    0x14: "E Off(subjugation)",
    0x15: "S Off. (subjugation)",
    0x16: "W Off. (subjugation)",
    0x17: "N Off. (subjugation)",
    0x18: "Jnr Minister",
    0x19: "Chief of Records",
    0x1a: "Finance Advisor",
    0x1b: "Jnr Prefect",
    0x1c: "E Off. (defense)",
    0x1d: "S Off. (defense)",
    0x1e: "W Off. (defense)",
    0x1f: "N Off. (defense)",
    0x20: "Security Chief",
    0x21: "Commandant",
    0x22: "Records Officer",
    0x23: "Fellow",
    0x24: "E Commander",
    0x25: "W Commander",
    0x26: "Fore Commander",
    0x27: "Rear Commander",
    0x28: "Snr Advisor",
    0x29: "City Officer",
    0x2a: "Attendant",
    0x2b: "Records Secretary",
    0x2c: "Off. (strategy)",
    0x2d: "Off. (defense)",
    0x2e: "Off. (prisoners)",
    0x2f: "Off. (negotiaton)",
    0x30: "Senior Secretary",
    0x31: "Secretary",
    0x32: "Jnr Secretary",
    0x33: "Sima",
    0x34: "E Sub-officer",
    0x35: "S Sub-officer",
    0x36: "W Sub-officer",
    0x37: "N Sub-officer",
    0x38: "Administrator",
    0x39: "Treasury Officer",
    0x3a: "Armory Officer",
    0x3b: "Snr Guard",
    0x3c: "Gatekeeper",
    0x3d: "Guard",
    0x3e: "Lieutenant",
    0x3f: "2nd Lieutenant",
    0x40: "Senior Officer",
    0x41: "Negotiator",
    0x42: "Chief Retainer",
    0x43: "Retainer",
    0x44: "Officer",
    0x45: "Officer",
    0x46: "Officer",
    0x47: "Officer",
    0x48: "E Retainer",
    0x49: "W Retainer",
    0x4a: "Agric. Advisor",
    0x4b: "Vassal",
    0x4c: "Officer",
    0x4d: "Officer",
    0x4e: "Officer",
    0x4f: "Officer",
    0x50: "None",
}

growth_ability_map = {
    0x00: "Maintain + Long",
    0x01: "Maintain + Short",
    0x02: "Precocious + Short",
    0x03: "Precocious + Long",
    0x04: "Normal + Short",
    0x05: "Normal + Long",
    0x06: "Late Bloomer + Long",
    0x07: "Late Bloomer + Short",
    0x08: "Open"
}

skill_map = {
    0x5e: "Nanman ties",
    0x63: "Spousal support",
    0x62: "Prayer",
    0x61: "Feng shui",
    0x60: "Benevolent rule",
    0x5f: "Suppression",
    0x5d: "Shanyue ties",
    0x5c: "Qiang ties",
    0x5b: "Wuwan ties",
    0x5a: "Levy",
    0x59: "Taxation",
    0x58: "Sustenance",
    0x57: "Wealth",
    0x56: "Negotiator",
    0x55: "Enlister",
    0x54: "Pedagogy",
    0x53: "Shipbuilding",
    0x52: "Invention",
    0x51: "Breeding",
    0x50: "Efficacy",
    0x4f: "Fame",
    0x4e: "Colonization",
    0x4d: "Fortification",
    0x4c: "Stirring music",
    0x4b: "Gladdened heart",
    0x4a: "Clear thought",
    0x49: "Indomitable",
    0x48: "Integrity",
    0x47: "Black arts",
    0x46: "Sorcery",
    0x45: "Siren",
    0x44: "Counter plan",
    0x43: "Intensify",
    0x42: "Chain reaction",
    0x41: "Augment",
    0x40: "focus",
    0x3f: "Divine potency",
    0x3e: "Divine fire",
    0x3d: "Insight",
    0x3c: "Detection",
    0x3b: "Covert plan",
    0x3a: "Cunning",
    0x39: "Agile mind",
    0x38: "Trickery",
    0x37: "Disconcertion",
    0x36: "Poison tongue",
    0x35: "Fire assault",
    0x34: "Escort",
    0x33: "Vehemence",
    0x32: "Bowmanship",
    0x31: "Stampede",
    0x30: "Puissance",
    0x2f: "Divine waters",
    0x2e: "Divine forge",
    0x2d: "Divine cavalry",
    0x2c: "Divine bows",
    0x2b: "Divine pikes",
    0x2a: "Divine spears",
    0x29: "Divine right",
    0x28: "God\'s command",
    0x27: "Valiant general",
    0x26: "Admiral",
    0x25: "Cavalry general",
    0x24: "Archer general",
    0x23: "Pike general",
    0x22: "Spear general",
    0x21: "Escape route",
    0x20: "Providence",
    0x1f: "Aegis",
    0x1e: "Resolute",
    0x1d: "Iron wall",
    0x1c: "Indestructible",
    0x1b: "Fortitude",
    0x1a: "Assistance",
    0x19: "White riders",
    0x18: "Range",
    0x17: "Exterminate",
    0x16: "Beguile",
    0x15: "Plunder",
    0x14: "Masterful",
    0x13: "Capture",
    0x12: "Entrap",
    0x11: "Siege",
    0x10: "Critical ambush",
    0x0f: "Close combat",
    0x0e: "Marine raid",
    0x0d: "Raid",
    0x0c: "Chain attack",
    0x0b: "Promotion",
    0x0a: "Majesty",
    0x09: "Sweep asunder",
    0x08: "Antidote",
    0x07: "Transport",
    0x06: "Traverse",
    0x05: "Seamanship",
    0x04: "Propulsion",
    0x03: "Foced gallop",
    0x02: "Forced march",
    0x01: "Fleetness",
    0x00: "Flying general",
    0xff: "None",
}

character_map = {
    0x00:  "Timid",
    0x01:  "Cool",
    0x02:  "Bold",
    0x03:  "Reckless",
}

voice_map = {
    0x00: "Timid",
    0x01: "Cool",
    0x02: "Bold",
    0x03: "Reckless",
    0x04: "Female Cool",
    0x05: "Female Bold",
    0x06: "Lu Bu",
    0x07: "Zhuge Liang",
}

tone_map = {
    0x00: "Female Barbarian",
    0x01: "Female Reckless",
    0x02: "Female Dignified",
    0x03: "Xiao Qiao/Da Qiao",
    0x04: "Female Frank",
    0x05: "Zhang Fei",
    0x06: "Barbarian",
    0x07: "Guan Yu",
    0x08: "Frank",
    0x09: "Dignified",
    0x0a: "Pompus",
    0x0b: "Reckless",
    0x0c: "Humble",
    0x0d: "Courteous",
    0x0e: "Polite",
    0x0f: "Normal",
}

court_importance_map = {
    0x00: "Ignore",
    0x01: "Normal",
    0x02: "Important",
}

weapon_model_map = defaultdict(lambda: "Default", {
    0x01: "Serpent Spear",
    0x02: "Blue Dragon",
    0x03: "Sky Scorcher",
    0x04: "Arrow",
    0x05: "Fan",
})

horse_model_map = defaultdict(lambda: "Default", {
    0x01: "Red Hare",
    0x02: "Hex Mark",
    0x03: "Shadow Runner",
    0x04: "Gray Lightning",
})


action_map = defaultdict(lambda: "Default", {
    0x68: "Available",
    0x20: "Available",
    0xC8: "Available",
})

affinity_map = {
    0x00: "C",
    0x01: "B",
    0x02: "A",
    0x03: "S",
}

use_map = {
    0x00: "Ability",
    0x01: "Performance",
    0x02: "Fame",
    0x03: "Righteousness",
    0x04: "Arbitrary"
}

debate_map = {
    0x00: "Fact",
    0x01: "Logic",
    0x02: "Time"
}

strategy_map = {
    0x2C: "Endless Might",
    0x00: "National Desires",
    0x01: "Local Desires",
    0x02: "State Desires",
    0x03: "Maintain"
}

campaign_map = {
    0x00: "Countryside",
    0x01: "Impromptu Strategy",
    0x02: "Sea is Home"
}

item_type_map = {
    0x00: "Elite Horse",
    0x01: "Sword",
    0x02: "Long Spear",
    0x03: "Throwing Knife",
    0x04: "Bow",
    0x05: "Writings",
    0x06: "Imperial Seal",
    0x07: "Bronze Pheasant",
    0xFF: "Not Available",
}

title_map = {
    0x00: "Emperor",
    0x01: "Regent",
    0x02: "Duke",
    0x03: "Baron",
    0x04: "Grand General",
    0x05: "Field Marshal",
    0x06: "General",
    0x07: "Governor",
    0x08: "Lt. Governor",
    0x09: "None",
    0xFF: "Not Available",
}

country_map = defaultdict(lambda: "Vacant", {
    0x00: "Wei",
    0x01: "Wu",
    0x02: "Shu",
    0x03: "Ji",
    0x04: "Cheng",
    0x05: "Yellow Turbans",
    0x06: "Han",
    0x07: "Xia",
    0x08: "Chang",
    0x09: "Zhou",
    0x0a: "Qin",
    0x0b: "Xin",
    0x0c: "Yan",
    0x0d: "Zhao",
    0x0e: "Qi",
    0x0f: "Ji",
    0x10: "Lu",
    0x11: "Cao",
    0x12: "Xue",
    0x13: "Xu",
    0x14: "Song",
    0x15: "Chen",
    0x16: "Su",
    0x17: "Han",
    0x18: "Gu",
    0x19: "Zheng",
    0x1a: "Xu",
    0x1b: "Yu",
    0x1c: "Liang",
    0x1d: "Liang",
    0x1e: "Cai",
    0x1f: "Tang",
    0x20: "Deng",
    0x21: "Shen",
    0x22: "Sui",
    0x23: "Chu",
    0x24: "Yue",
    0x25: "Wuwan",
    0x26: "Qiang",
    0x27: "Shanyue",
    0x28: "Nanman",
    0x29: "Bandit",
    0xFF: "Not Available",
})

officer_map = defaultdict(lambda: "Unknown", {
    0x0000: "Ahui Nan",
    0x0001: "Wei Zhao",
    0x0002: "Yi Ji",
    0x0003: "Yin Shang",
    0x0004: "Yin Damu",
    0x0005: "Yin Mo",
    0x0006: "Yu Jin",
    0x0007: "Yu Quan",
    0x0008: "Wei Guan",
    0x0009: "Yuan Yi",
    0x000a: "Yuan Yin",
    0x000b: "Yan Yu",
    0x000c: "Yuan Huan",
    0x000d: "Yuan Xi",
    0x000e: "Yan Xing",
    0x000f: "Yan Rou",
    0x0010: "Yuan Shu",
    0x0011: "Yuan Shang",
    0x0012: "Yuan Shao",
    0x0013: "Yan Xiang",
    0x0014: "Yuan Tan",
    0x0015: "Yan Pu",
    0x0016: "Yuan Yao",
    0x0017: "Wang Wei",
    0x0018: "Wang Yi",
    0x0019: "Wang Yun",
    0x001a: "Wang Ji",
    0x001b: "Wang Qui",
    0x001c: "Wang Kuang",
    0x001d: "Wang Ye",
    0x001e: "Wang Jing",
    0x001f: "Wang Kang",
    0x0020: "Wang Hun",
    0x0021: "Wang Can",
    0x0022: "Wang Xiu",
    0x0023: "Wang Rong",
    0x0024: "Wang Su",
    0x0025: "Wang Jun",
    0x0026: "Wang Xiang",
    0x0027: "Ou Xing",
    0x0028: "Wang Shuang",
    0x0029: "Wang Zhong",
    0x002a: "Wang Chang",
    0x002b: "Wang Tao",
    0x002c: "Wang Dun",
    0x002d: "Wang Ping",
    0x002e: "Wang Fu",
    0x002f: "Wang Men",
    0x0030: "Wang Ling",
    0x0031: "Wang Lei",
    0x0032: "Wang Lang",
    0x0033: "Wen Hui",
    0x0034: "He Yan",
    0x0035: "Kuai Yue",
    0x0036: "Kuai Liang",
    0x0037: "Jia Hua",
    0x00c8: "Wu Can",
    0x00c9: "Hu Zhi",
    0x00ca: "Wu Zhi",
    0x00cb: "Hu Cheer",
    0x00cc: "Hu Zun",
    0x00cd: "Hu Zhen",
    0x00ce: "Gu Tan",
    0x00cf: "Wu Tugu",
    0x00d0: "Hu Ban",
    0x00d1: "Wu Ban",
    0x00d2: "Hu Fen",
    0x00d3: "Gu  Yong",
    0x00d4: "Wu Lan",
    0x00d5: "Hu Lie",
    0x00d6: "Cui Yan",
    0x00d7: "Cai Yan",
    0x00d8: "Cai He",
    0x00d9: "Cai Shi",
    0x00da: "Cai Zhong",
    0x00db: "Cai Mao",
    0x00dc: "Cui Lin",
    0x00dd: "Zuo Yi",
    0x00de: "Ze Rong",
    0x00df: "Shi Shuo",
    0x00e0: "Shi Zuan",
    0x00e1: "Sima Yi",
    0x00e2: "Sima Yan",
    0x00e3: "Sima Shi",
    0x00e4: "Sima Zhao",
    0x00e5: "Sima Zhou",
    0x00e6: "Sima Fu",
    0x00e7: "Sima Wang",
    0x00e8: "Sima You",
    0x00e9: "Sima Lang",
    0x00ea: "Xie Jing",
    0x00eb: "Che Zhou",
    0x00ec: "Sha Moke",
    0x00ed: "Zhu Yi",
    0x00ee: "Zhou Xin",
    0x00ef: "Zhou Ang",
    0x00f0: "Zhou Zhi",
    0x00f1: "Zhou Cang",
    0x00f2: "Zhou Tai",
    0x00f3: "Zhou Tai",
    0x00f4: "Zhou Fang",
    0x00f5: "Zhou Yu",
    0x00f6: "Zhu Huan",
    0x00f7: "Zhu Ju",
    0x00f8: "Zhu Rong",
    0x00f9: "Zhu Jun",
    0x00fa: "Zhu Ran",
    0x00fb: "Zhu Zhi",
    0x00fc: "Zhu Bao",
    0x00fd: "Zhu Ling",
    0x00fe: "Xun Yu",
    0x00ff: "Chunyu Qiong",
    0x0191: "Zhang Hua",
    0x0192: "Zhang Kai",
    0x0193: "Zhang Jiao",
    0x0194: "Zhang Ji",
    0x0195: "Zhang Xiu",
    0x0196: "Zhang Qiu",
    0x0197: "Zhang Yi",
    0x0198: "Zhang Xun",
    0x0199: "Zhang Hu",
    0x019a: "Zhang Hong",
    0x019b: "Zhang Yue",
    0x019c: "Zhao Guang",
    0x019d: "Zhao Hong",
    0x019e: "Zhang Ji",
    0x019f: "Zhang Xiu",
    0x01a0: "Zhang Ji",
    0x01a1: "Zhang Zun",
    0x01a2: "Zhang Chunhua",
    0x01a3: "Zhang Zhao",
    0x01a4: "Zhang Song",
    0x01a5: "Zhang Shao",
    0x01a6: "Zhang Cheng",
    0x01a7: "Zhang Ren",
    0x01a8: "Diao Chan",
    0x01a9: "Zhang Ti",
    0x01aa: "Zhao Tong",
    0x01ab: "Zhang Te",
    0x01ac: "Zhang Nan",
    0x01ad: "Zhang Nan",
    0x01ae: "Zhang Miao",
    0x01af: "Zhao Fan",
    0x01b0: "Zhang Fei",
    0x01b1: "Zhang Bu",
    0x01b2: "Zhang Bao",
    0x01b3: "Zhang Bao",
    0x01b4: "Zhang Mancheng",
    0x01b5: "Zhang Yang",
    0x01b6: "Zhang Yi",
    0x01b7: "Zhang Liao",
    0x01b8: "Zhang Liang",
    0x01b9: "Zhao Lei",
    0x01ba: "Zhang Lu",
    0x01bb: "Chen Heng",
    0x01bc: "Chen Ying",
    0x01bd: "Chen Ji",
    0x01be: "Chen Gong",
    0x01bf: "Chen Jiao",
    0x01c0: "Chen Qun",
    0x01c1: "Chen Gui",
    0x01c2: "Chen Qian",
    0x01c3: "Chen Shou",
    0x01c4: "Chen Shi",
    0x01c5: "Chen Zhen",
    0x01c6: "Chen Tai",
    0x01c7: "Chen Deng",
    0x01c8: "Chen Dao",
    0x025a: "Lu Xun",
    0x025b: "Li Yan",
    0x025c: "Li Ru",
    0x025d: "Li Su",
    0x025e: "Li Sheng",
    0x025f: "Li Kan",
    0x0260: "Li Tong",
    0x0261: "Li Dian",
    0x0262: "Li Fu",
    0x0263: "Li Feng",
    0x0264: "Li Feng",
    0x0265: "Li Feng",
    0x0266: "Liu Yan",
    0x0267: "Liu He",
    0x0268: "Liu Kui",
    0x0269: "Liu Qi",
    0x026a: "Liu Yu",
    0x026b: "Liu Xun",
    0x026c: "Liu Xian",
    0x026d: "Liu Zan",
    0x026e: "Liu Shi",
    0x026f: "Liu Xun",
    0x0270: "Liu Zhang",
    0x0271: "Liu Shao",
    0x0272: "Liu Cheng",
    0x0273: "Liu Chen",
    0x0274: "Liu Xuan",
    0x0275: "Liu Chan",
    0x0276: "Liu Cong",
    0x0277: "Liu Dai",
    0x0278: "Liu Du",
    0x0279: "Liu Ba",
    0x027a: "Liu Pan",
    0x027b: "Liu Bei",
    0x027c: "Liu Biao",
    0x027d: "Liu Fu",
    0x027e: "Liu Ping",
    0x027f: "Liu Pi",
    0x0280: "Liu Feng",
    0x0281: "Liu Ye",
    0x0282: "Liu Yao",
    0x0283: "Liu Lue",
    0x0284: "Lu Weihuang",
    0x0285: "Liao Hua",
    0x0286: "Liang Xing",
    0x0287: "Liang Gang",
    0x0288: "Liang Xi",
    0x0289: "Liang Xu",
    0x028a: "Ling Cao",
    0x028b: "Ling Tong",
    0x028c: "Liao Li",
    0x028d: "Lu Kai",
    0x028e: "Lu Ju",
    0x028f: "Lu Qian",
    0x0290: "Lu Kuang",
    0x0291: "Lu Xiang",
    0x0038: "Hua He",
    0x0039: "Jia Kui",
    0x003a: "He Yi",
    0x003b: "Hua Xin",
    0x003c: "Jia Xu",
    0x003d: "Guo Yi",
    0x003e: "Guo Yuan",
    0x003f: "Guo Jia",
    0x0040: "E Huan",
    0x0041: "Guo Si",
    0x0042: "Yue Jiu",
    0x0043: "Huo Jun",
    0x0044: "Hao Zhao",
    0x0045: "Yue Jin",
    0x0046: "Yue Chen",
    0x0047: "Guo Tu",
    0x0048: "Guo Ma",
    0x0049: "Hao Meng",
    0x004a: "Guo Youzhi",
    0x004b: "Huo Yi",
    0x004c: "Guo Huai",
    0x004d: "Xiahou Wei",
    0x004e: "Xiahou Yuan",
    0x004f: "Xiahou En",
    0x0050: "Xiahou He",
    0x0051: "Xiahou Hui",
    0x0052: "Xiahou Xuan",
    0x0053: "Xiahou Shang",
    0x0054: "Xiahou De",
    0x0055: "Xiahou Dun",
    0x0056: "Xiahou Ba",
    0x0057: "Xiahou Mao",
    0x0058: "Xiahou Lingnu",
    0x0059: "Jia Chong",
    0x005a: "He Zhi",
    0x005b: "He Jin",
    0x005c: "He Qi",
    0x005d: "Jia Fan",
    0x005e: "Hua Man",
    0x005f: "Hua Xiong",
    0x0060: "Guan Yi",
    0x0061: "Han Yin",
    0x0062: "Guan Yu",
    0x0063: "Huan Jie",
    0x0064: "Guan Hai",
    0x0065: "Guanqiu Jian",
    0x0066: "Guanqiu Xiu",
    0x0067: "Guanqiu Dian",
    0x0068: "Han Juzi",
    0x0069: "Han Xuan",
    0x006a: "Han Hao",
    0x006b: "Guan Xing",
    0x006c: "Guan Suo",
    0x006d: "Han Sui",
    0x006e: "Han Song",
    0x006f: "Guan Jing",
    0x0070: "Han Xian",
    0x0071: "Kan Ze",
    0x0072: "Han Zhong",
    0x0073: "Guan Tong",
    0x0100: "Xun Yi",
    0x0101: "Xun Xu",
    0x0102: "Xun Chen",
    0x0103: "Xun You",
    0x0104: "Jiao Yi",
    0x0105: "Zhong Yu",
    0x0106: "Jiang Wan",
    0x0107: "Zhong Hui",
    0x0108: "Jiang Gan",
    0x0109: "Jiang Yiqu",
    0x010a: "Xiao Qiao",
    0x010b: "Jiang Qin",
    0x010c: "Jiang Ji",
    0x010d: "Qiao Zhou",
    0x010e: "Jiang Shu",
    0x010f: "Jiao Chu",
    0x0110: "Xiang Chong",
    0x0111: "Shao Ti",
    0x0112: "Jiang Ban",
    0x0113: "Jiang Bin",
    0x0114: "Zhong Yao",
    0x0115: "Zhongli Mu",
    0x0116: "Xiang Lang",
    0x0117: "Xu Rong",
    0x0118: "Zhuge Ke",
    0x0119: "Zhuge Qiao",
    0x011a: "Zhuge Jin",
    0x011b: "Zhuge Jun",
    0x011c: "Zhuge Xu",
    0x011d: "Zhuge Shang",
    0x011e: "Zhuge Jing",
    0x011f: "Zhuge Zhan",
    0x0120: "Zhuge Dan",
    0x0121: "Zhuge Liang",
    0x0122: "Xu Huang",
    0x0123: "Xu Shi",
    0x0124: "Xu Zhi",
    0x0125: "Xu Shu",
    0x0126: "Xu Sheng",
    0x0127: "Xu Miao",
    0x0128: "Shen Ying",
    0x0129: "Shen Yi",
    0x012a: "Xin Xianying",
    0x012b: "Cen Hun",
    0x012c: "Zhen Shi",
    0x012d: "Xin Chang",
    0x012e: "Shen Dan",
    0x012f: "Shen Pei",
    0x0130: "Xin Pi",
    0x0131: "Xin Ping",
    0x0132: "Qin Mi",
    0x0133: "Qin Lang",
    0x0134: "Sui Yuanjin",
    0x0135: "Sui Gu",
    0x0136: "Zou Shi",
    0x0137: "Zou Jing",
    0x0138: "Zou Dan",
    0x0139: "Cheng Yi",
    0x013a: "Cheng Gongying",
    0x013b: "Sheng Man",
    0x01c9: "Chen Biao",
    0x01ca: "Chen Wu",
    0x01cb: "Chen Lan",
    0x01cc: "Chen Lin",
    0x01cd: "Cheng Yu",
    0x01ce: "Cheng Yuanzhi",
    0x01cf: "Ding Yi",
    0x01d0: "Cheng Yin",
    0x01d1: "Ding Yuan",
    0x01d2: "Cheng Pu",
    0x01d3: "Cheng Wu",
    0x01d4: "Cheng Bing",
    0x01d5: "Ding Feng",
    0x01d6: "Ding Feng",
    0x01d7: "Dian Wei",
    0x01d8: "Tian Kai",
    0x01d9: "Tian Xu",
    0x01da: "Tian Chou",
    0x01db: "Tian Feng",
    0x01dc: "Dian Man",
    0x01dd: "Tian Yu",
    0x01de: "Teng Yin",
    0x01df: "Dong Yun",
    0x01e0: "Dong He",
    0x01e1: "Deng Ai",
    0x01e2: "Dang Jun",
    0x01e3: "Dong Jui",
    0x01e4: "Tao Qian",
    0x01e5: "Deng Xian",
    0x01e6: "Deng Zhi",
    0x01e7: "Tang Zi",
    0x01e8: "Dong Xi",
    0x01e9: "Teng Xiu",
    0x01ea: "Tao Jun",
    0x01eb: "Dong Cheng",
    0x01ec: "Dong Zhao",
    0x01ed: "Dong Zhuo",
    0x01ee: "Deng Zhong",
    0x01ef: "Dong Chao",
    0x01f0: "Dong TuNa",
    0x01f1: "Tang Bin",
    0x01f2: "Dong Min",
    0x01f3: "Deng Mao",
    0x01f4: "Du Ji",
    0x01f5: "Du Yu",
    0x01f6: "Ning Sui",
    0x01f7: "Pei Yuanshao",
    0x01f8: "Pei Xiu",
    0x01f9: "Ma Yunlu",
    0x01fa: "Ma Wan",
    0x01fb: "Ma Xiu",
    0x01fc: "Ma Jun",
    0x01fd: "Bo Cai",
    0x01fe: "Ma Zun",
    0x01ff: "Ma Su",
    0x0200: "Ma Dai",
    0x0201: "Ma Zhong",
    0x0202: "Ma Zhong",
    0x0203: "Ma Chao",
    0x0204: "Ma Tie",
    0x0292: "Lu Dai",
    0x0293: "Lu Fan",
    0x0294: "Lu Bu",
    0x0295: "Lu Meng",
    0x0296: "Lu Lingqi",
    0x0297: "Lun Zhi",
    0x0298: "Leng Bao",
    0x0299: "Lou Gui",
    0x029a: "Lou Xuan",
    0x029b: "Lu Su",
    0x029c: "Lu Shu",
    0x029d: "Lu Zhi",
    0x02bc: "Emperor Ling",
    0x02bd: "Emperor Shao",
    0x02be: "Emperor Xian",
    0x02bf: "Yu Ji",
    0x02c0: "Hua Tuo",
    0x02c1: "Guan Lu",
    0x02c2: "Xu Shao",
    0x02c3: "Zuo Ci",
    0x02c4: "Sima Hui",
    0x02c5: "Mi Heng",
    0x02c6: "Huang Chengyan",
    0x02c7: "Qiao Xuan",
    0x02c8: "North Star",
    0x02c9: "South Star",
    0x02ca: "Thief",
    0x02cb: "Civil Official",
    0x02cc: "Soldier",
    0x02cd: "Male",
    0x02ce: "Female",
    0x02cf: "Old Man",
    0x02d0: "Child",
    0x02d1: "Wuwan Chief",
    0x02d2: "Wuwan Officer",
    0x02d3: "Qiang Chief",
    0x02d4: "Qiang Officer",
    0x02d5: "Shanyue Chief",
    0x02d6: "Shanyue Officer",
    0x02d7: "Nanman Chief",
    0x02d8: "Nanman Officer",
    0x02d9: "Zhang Rang",
    0x02da: "Jian Shuo",
    0x02db: "Baby",
    0x02dc: "Messenger",
    0x02dd: "Nobleman",
    0x02de: "Doctor",
    0x02df: "Aeromancer",
    0x02e0: "Empress",
    0x02e1: "Old Man",
    0x02e2: "Old Woman",
    0x02e3: "Wizard",
    0x02e4: "Miscreant",
    0x02e5: "Eunuch",
    0x02e6: "Envoy",
    0x02e7: "Officer",
    0x02e8: "Guard",
    0x0074: "Han Dang",
    0x0075: "Han De",
    0x0076: "Gan Ning",
    0x0077: "Huan Fan",
    0x0078: "Han Fu",
    0x0079: "Guan Ping",
    0x007a: "Jian Yong",
    0x007b: "Yan Liang",
    0x007c: "Wei Yan",
    0x007d: "Qu Yi",
    0x007e: "Xi Zhicai",
    0x007f: "Wei Xu",
    0x0080: "Wei Miao",
    0x0081: "Wei Feng",
    0x0082: "Wei You",
    0x0083: "Niu Jin",
    0x0084: "Qiu Jian",
    0x0085: "Niu Fu",
    0x0086: "Qiu Ben",
    0x0087: "Ji Yong",
    0x0088: "Jiang Wei",
    0x0089: "Gong Zhi",
    0x008a: "Qiao Rui",
    0x008b: "Gong Du",
    0x008c: "Qiao Mao",
    0x008d: "Xu Yi",
    0x008e: "Xu Gong",
    0x008f: "Xu Jing",
    0x0090: "Xu Zhu",
    0x0091: "Xu You",
    0x0092: "Ji Ling",
    0x0093: "Jin Yi",
    0x0094: "Jinhuan Sanjie",
    0x0095: "Jin Xuan",
    0x0096: "Yu Si",
    0x0097: "Yu Fan",
    0x0098: "Xing Daorong",
    0x0099: "Xi Zheng",
    0x009a: "Yan Yan",
    0x009b: "Qian Hong",
    0x009c: "Yan Gang",
    0x009d: "Yan Jun",
    0x009e: "Qian Zhao",
    0x009f: "Yan Zheng",
    0x00a0: "Yan Baihu",
    0x00a1: "Yan Yu",
    0x00a2: "Wu Yi",
    0x00a3: "Huang Gai",
    0x00a4: "Gao Gan",
    0x00a5: "Huang Ying",
    0x00a6: "Huang Quan",
    0x00a7: "Huang Hao",
    0x00a8: "Gao Rou",
    0x00a9: "Gao Shun",
    0x00aa: "Gao Xiang",
    0x00ab: "Gao Sheng",
    0x00ac: "Huang Chong",
    0x00ad: "Hou Cheng",
    0x00ae: "Hou Xuan",
    0x00af: "Huang Zu",
    0x013c: "Shi Bao",
    0x013d: "Xue Ying",
    0x013e: "Xue Xu",
    0x013f: "Xue Cong",
    0x0140: "Quan Yi",
    0x0141: "Quan Yi",
    0x0142: "Quan Ji",
    0x0143: "Shan Jing",
    0x0144: "Quan Shang",
    0x0145: "Quan Cong",
    0x0146: "Quan Duan",
    0x0147: "Cao Yu",
    0x0148: "Cao Rui",
    0x0149: "Cao Huan",
    0x014a: "Cao Xi",
    0x014b: "Cao Xiu",
    0x014c: "Cao Xun",
    0x014d: "Song Xian",
    0x014e: "Song Qian",
    0x014f: "Cao Ang",
    0x0150: "Cao Hong",
    0x0151: "Cao Chun",
    0x0152: "Cao Zhang",
    0x0153: "Cao Zhi",
    0x0154: "Cao Zhen",
    0x0155: "Cao Ren",
    0x0156: "Cao Xing",
    0x0157: "Cao Cao",
    0x0158: "Cao Shuang",
    0x0159: "Cao Chong",
    0x015a: "Zang Ba",
    0x015b: "Cao Pi",
    0x015c: "Cao Bao",
    0x015d: "Cao Fang",
    0x015e: "Cao Mao",
    0x015f: "Cao Xiong",
    0x0160: "Ju Hu",
    0x0161: "Ju Shou",
    0x0162: "Su Fei",
    0x0163: "Zu Mao",
    0x0164: "Su You",
    0x0165: "Sun Yi",
    0x0166: "Sun He",
    0x0167: "Sun Huan",
    0x0168: "Sun Guan",
    0x0169: "Sun Ji",
    0x016a: "Sun Xiu",
    0x016b: "Sun Kuang",
    0x016c: "Sun Xin",
    0x016d: "Sun Jian",
    0x016e: "Sun Qian",
    0x016f: "Sun Quan",
    0x0170: "Sun Hao",
    0x0171: "Sun Jiao",
    0x0172: "Sun Ce",
    0x0173: "Sun Shi",
    0x0174: "Sun Xiu",
    0x0175: "Sun Jun",
    0x0176: "Sun Shao",
    0x0177: "Sun Shang Xiang",
    0x0205: "Ma Teng",
    0x0206: "Ma Miao",
    0x0207: "Ma Liang",
    0x0208: "Wan Yu",
    0x0209: "Fan Jian",
    0x020a: "Fan Shi",
    0x020b: "Pan Jun",
    0x020c: "Pan Zhang",
    0x020d: "Fan Chou",
    0x020e: "Fan Neng",
    0x020f: "Pan Feng",
    0x0210: "Fei Yi",
    0x0211: "Bei Yan",
    0x0212: "Fei Shi",
    0x0213: "Mi Shi",
    0x0214: "Mi Zhu",
    0x0215: "Mi Fang",
    0x0216: "Fei Yao",
    0x0217: "Wu Anguo",
    0x0218: "Feng Xi",
    0x0219: "Fu Jia",
    0x021a: "Fu Ren",
    0x021b: "Fu Qian",
    0x021c: "Fu Xun",
    0x021d: "Fu Tong",
    0x021e: "Wen Yang",
    0x021f: "Wen Qin",
    0x0220: "Wen Hu",
    0x0221: "Wen Chou",
    0x0222: "Wen Pin",
    0x0223: "Bian Xi",
    0x0224: "Bian Shi",
    0x0225: "Fang Yue",
    0x0226: "Pang Hui",
    0x0227: "Mang Yachang",
    0x0228: "Feng Ji",
    0x0229: "Pang Xi",
    0x022a: "BaoSanniang",
    0x022b: "Bao Xin",
    0x022c: "Fa Zheng",
    0x022d: "Pang Tong",
    0x022e: "Pang De",
    0x022f: "Bao Long",
    0x0230: "Bu Xie",
    0x0231: "Mu Shun",
    0x0232: "Puyang Xin",
    0x0233: "Mulu Duosi",
    0x0234: "Bu Zhi",
    0x0235: "Bu Chan",
    0x0236: "Man Chong",
    0x0237: "Mao Jie",
    0x0238: "Meng Huo",
    0x0239: "Meng Zong",
    0x023a: "Meng Da",
    0x023b: "Meng You",
    0x023c: "Yu She",
    0x023d: "Yang Huai",
    0x023e: "Yong Kai",
    0x023f: "Yang Yi",
    0x0240: "Yang Xin",
    0x02e9: "Bandit",
    0x02ea: "Turban Rebel",
    0x02eb: "Warrior",
    0x02ec: "Farmer",
    0x02ed: "Merchant",
    0x02ee: "Workman",
    0x02ef: "Youth",
    0x02f0: "Youth Woman",
    0x02f1: "Boy",
    0x02f2: "Girl",
    0x02f3: "Rich Man",
    0x02f4: "Craftsman",
    0x02f5: "Burglar",
    0x02f6: "Traveler",
    0x02f7: "Barmaid",
    0x02f8: "Waitress",
    0x02f9: "Fisherman",
    0x02fa: "Scholar",
    0x00b0: "Gongsun Yue",
    0x00b1: "Gongsun Yuan",
    0x00b2: "Gongsun Gong",
    0x00b3: "Gongsun Kang",
    0x00b4: "Gongsun Zan",
    0x00b5: "Gongsun Xu",
    0x00b6: "Gongsun Du",
    0x00b7: "Gongsun Fan",
    0x00b8: "Kong Zhou",
    0x00b9: "Huang Zhong ",
    0x00ba: "Gao Ding",
    0x00bb: "Gaotang Long",
    0x00bc: "Gao Pei",
    0x00bd: "Huangfu Song",
    0x00be: "Kong Rong",
    0x00bf: "Gao Lan",
    0x00c0: "Wu Yan",
    0x00c1: "Wu Ju",
    0x00c2: "Guo Yuan",
    0x00c3: "Wu Jing",
    0x00c4: "Wu Yan",
    0x00c5: "Wu Gang",
    0x00c6: "Wu Guotai",
    0x00c7: "Hu Ji",
    0x00c8: "Wu Can",
    0x0178: "Sun Zhen",
    0x0179: "Sun Jing",
    0x017a: "Sun Zhong",
    0x017b: "Sun Chen",
    0x017c: "Sun Deng",
    0x017d: "Sun Yu",
    0x017e: "Sun Yi",
    0x017f: "Sun Liang",
    0x0180: "Sun Li",
    0x0181: "Sun Lang",
    0x0182: "Sun Luban",
    0x0183: "Da Qiao",
    0x0184: "Taishi Xiang",
    0x0185: "Taishi Ci",
    0x0186: "Dailai Dongzhu",
    0x0187: "Dai Ling",
    0x0188: "King Duosi",
    0x0189: "Tan Xiong",
    0x018a: "Zhang Yun",
    0x018b: "Zhao Yun",
    0x018c: "Zhang Gu",
    0x018d: "Zhang Ying",
    0x018e: "Zhang Yan",
    0x018f: "Zhang Heng",
    0x0190: "Zhang Wen",
    0x0241: "Yang Hu",
    0x0242: "Yang Hong",
    0x0243: "Yang An",
    0x0244: "Yang Ji",
    0x0245: "Yang Chou",
    0x0246: "Yang Xiu",
    0x0247: "Yang Qiu",
    0x0248: "Yang Song",
    0x0249: "Yang Ren",
    0x024a: "Yang Zuo",
    0x024b: "Yang Zhao",
    0x024c: "Yang Bo",
    0x024d: "Yang Fu",
    0x024e: "Yang Feng",
    0x024f: "Yang Feng",
    0x0250: "Lei Tong",
    0x0251: "Lei Bo",
    0x0252: "Luo Tong",
    0x0253: "Luo Xian",
    0x0254: "Li Yi",
    0x0255: "Li Hui",
    0x0256: "Li Jue",
    0x0257: "Lu Kai",
    0x0258: "Lu Kang",
    0x0259: "Lu Ji",
})

ghost_officer_map = defaultdict(lambda: "Unknown", {
    0xD007: "Yuan Shao's father (Yuan Cheng I guess)",
    0xD107: "Yuan Yin's father",
    0xD207: "Yuan Shu's & Yuan Yi's father (Yuan Feng, but weren't Shu and Yi cousins?)",
    0xD307: "Wang Yun's father",
    0xD407: "Wang Ling's father",
    0xD507: "Kuai Liang's & Kuai Yue's father",
    0xD607: "Xiahou Dun's father",
    0xD707: "Xiahou De's & Xiahou Shang's father",
    0xD807: "Xiahou Yuan's father",
    0xD907: "Guanqiu Jian's & Guanqiu Xiu's father",
    0xDA07: "Han Xuan's & Han Hao's father",
    0xDB07: "Yan Baihu's & Yan Yu's father",
    0xDC07: "Gao Gan's & Gao Rou's father",
    0xDD07: "Gongsun Zan's & Gongsun Yue's father",
    0xDE07: "Gongsun Fan's father",
    0xDF07: "Cai He's & Cai Zhong's father",
    0xE007: "Cai Mao's & Cai Shi's father (I thought they were siblings of Cai He and Zhong?)",
    0xE107: "Sima Lang's, Sima Yi's & Sima Fu's father (Sima Fang I guess)",
    0xE207: "Zhou Xin's & Zhou Ang's father",
    0xE307: "Zhu Rong's & Dailai Dongzhu's father",
    0xE407: "Xun Yu's & Xun Chen's father (Xun Gun I guess)",
    0xE507: "Xun You's father",
    0xE607: "Xun Xu's father",
    0xE707: "Xiang Lang's father",
    0xE807: "Xiang Chong's father",
    0xE907: "Zhuge Jin's, Zhuge Liang's & Zhuge Jun's father (must be Zhuge Gui)",
    0xEA07: "Shen Yi's & Shen Dan's father",
    0xEB07: "Xin Ping's & Xin Pi's father",
    0xEC07: "Cao Cao's father (Cao Song)",
    0xED07: "Cao Xiu's father",
    0xEE07: "Cao Zhen's father (Cao/Qin Shao)",
    0xEF07: "Cao Ren's & Cao Chun's father (Cao Chi)",
    0xF007: "Cao Hong's father",
    0xF107: "Cao Mao's father (Cao Lin)",
    0xF207: "Sun Huan's father",
    0xF307: "Sun Shao's father",
    0xF407: "Sun Jian's & Sun Jing's father",
    0xF507: "Sun Xiu's father (General, not Emperor Sun Xiu)",
    0xF607: "Sun Jun's father",
    0xF707: "Sun Chen's father",
    0xF807: "None",
    0xF907: "Sun Xin's & Sun Zhen's father",
    0xFA07: "Zhang Jiao's, Zhang Bao's & Zhang Liang's father",
    0xFB07: "None",
    0xFC07: "Zhang Ji's father (Dong Zhuo's general)",
    0xFD07: "Zhang Xiu's father (Lord of Wan)",
    0xFE07: "Zhang Lu's & Zhang Wei's father",
    0xFF07: "Ding Feng's & Ding Feng's father",
    0x0008: "Dong Zhuo's & Dong Min's father",
    0x0108: "None",
    0x0208: "Ma Dai's father",
    0x0308: "Ma Liang's & Ma Su's father",
    0x0408: "Mi Zhu's, Mi Fang's & Mi Shi's father",
    0x0508: "Meng Huo's & Meng You's father",
    0x0608: "Yang Bo's & Yang Song's father",
    0x0708: "Lu Xun's father",
    0x0808: "Lu Kai's father (Wu general)",
    0x0908: "Liu Yao's & Liu Dai's father",
    0x0A08: "Lu Kuang's & Lu Xiang's father",
    0x0B08: "Wu Jing's & Wu Guotai's father",
    0xFFFF: "None"
})

specialty_options = {
    0: "Large City",
    1: "Spears",
    2: "Pikes",
    3: "Bows",
    4: "Horses",
    5: "Weaponry",
    6: "Navy"
}

specialty_hex = [int(n, 16) for n in [
    '000000000000',
    '010000000000',
    '000100000000',
    '000001000000',
    '000000010000',
    '000000000100',
    '000000000001'
]]

col_map = {
    'rank': officer_ranks_map,
    'status': officer_status_map,
    'title': title_map,
    'strategist': officer_map,
    'ruler': officer_map,
    'father': officer_map,
    'mother': officer_map,
    'spouse': officer_map,
    'swornbrother': officer_map,
    'likedofficer1': officer_map,
    'likedofficer2': officer_map,
    'likedofficer3': officer_map,
    'likedofficer4': officer_map,
    'likedofficer5': officer_map,
    'dislikedofficer1': officer_map,
    'dislikedofficer2': officer_map,
    'dislikedofficer3': officer_map,
    'dislikedofficer4': officer_map,
    'dislikedofficer5': officer_map,
}
