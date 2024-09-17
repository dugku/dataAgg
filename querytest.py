import math

from main import *

class PlayerStats:
    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.name = ""
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.matches = []
        self.firstKill = 0
        self.firstDeath = 0
        self.headshots = 0
        self.headshotPercent = 0
        self.ctkills = 0
        self.tkills = 0
        self.weaponStats = {
            "EqUnknown": 0, "EqP2000": 0, "EqGlock": 0, "EqP250": 0,
            "EqDeagle": 0, "EqFiveSeven": 0, "EqDualBerettas": 0,
            "EqTec9": 0, "EqCZ": 0, "EqUSP": 0, "EqRevolver": 0,
            "EqMP7": 0, "EqMP9": 0, "EqBizon": 0, "EqMac10": 0,
            "EqUMP": 0, "EqP90": 0, "EqMP5": 0, "EqSawedOff": 0,
            "EqNova": 0, "EqMag7": 0, "EqXM1014": 0, "EqM249": 0,
            "EqNegev": 0, "EqGalil": 0, "EqFamas": 0, "EqAK47": 0,
            "EqM4A4": 0, "EqM4A1": 0, "EqScout": 0, "EqSG556": 0,
            "EqAUG": 0, "EqAWP": 0, "EqScar20": 0, "EqG3SG1": 0,
            "EqZeus": 0, "EqBomb": 0, "EqKnife": 0, "EqDecoy": 0,
            "EqMolotov": 0, "EqIncendiary": 0, "EqFlash": 0,
            "EqSmoke": 0, "EqHE": 0, "EqWorld": 0
        }

    def addkill(self, num):
        self.kills += num

    def adddeath(self, num):
        self.deaths += num

    def addassist(self, num):
        self.assists += num

    def addmatch(self, num):
        self.matches.append(num)

    def addfirstkill(self, num):
        self.firstKill += num

    def addfirstdeath(self, num):
        self.firstDeath += num

    def addheadshot(self, num):
        self.headshots += num

    def addheadshotpercent(self):
        if self.kills > 0:  # Prevent division by zero
            self.headshotPercent = math.floor((self.headshots / self.kills) * 100)

    def addctkill(self, num):
        self.ctkills += num

    def addtkill(self, num):
        self.tkills += num

    def addweaponstats(self, name, num):
        self.weaponStats[name] += num
def queryThis():
    stmt = session.query(Player).filter(Player.steam_id == 76561198214009861).all()
    weapon = session.query(PlayerWeaponKills).filter(PlayerWeaponKills.player_steam_id == 76561198214009861).all()




    sweet = getStats(stmt, weapon)

    for i in sweet:
        print(i.name)
        print(f"Kills:{i.kills} Deaths:{i.deaths} Assists:{i.assists} Headshots:{i.headshots}")
        print(f"headshot Percent{i.headshotPercent} firstkill:{i.firstKill} firstdeath:{i.firstDeath}")
        print(f"ctkills {i.ctkills} tkills {i.tkills}")

        for i,x in i.weaponStats.items():

            if x == 0:
                continue

            print(f"Weapon Name:{i} Kill: {x}")

def getStats(playerObj, weaponObj):
    player_stats_lst = []

    for stats in playerObj:
        player = PlayerStats(stats.steam_id)

        player.addkill(stats.kills)  # Use the correct method names
        player.adddeath(stats.deaths)
        player.addassist(stats.assists)
        player.addmatch(stats.match)
        player.addfirstkill(stats.firstkill)
        player.addfirstdeath(stats.firstdeath)
        player.addheadshot(stats.headshots)
        player.addheadshotpercent()
        player.addctkill(stats.ctkills)
        player.addtkill(stats.tkills)

        for wepstat in weaponObj:
            weaponName = wepNames(int(wepstat.weapon_id))
            player.addweaponstats(weaponName, wepstat.kills)

        player_stats_lst.append(player)

    return player_stats_lst

def wepNames(wepId):
    equipment_types = {
        0: "EqUnknown",

        1: "EqP2000",
        2: "EqGlock",
        3: "EqP250",
        4: "EqDeagle",
        5: "EqFiveSeven",
        6: "EqDualBerettas",
        7: "EqTec9",
        8: "EqCZ",
        9: "EqUSP",
        10: "EqRevolver",

        101: "EqMP7",
        102: "EqMP9",
        103: "EqBizon",
        104: "EqMac10",
        105: "EqUMP",
        106: "EqP90",
        107: "EqMP5",

        201: "EqSawedOff",
        202: "EqNova",
        203: "EqMag7",  # Mag7 and Swag7 share the same ID
        204: "EqXM1014",
        205: "EqM249",
        206: "EqNegev",

        301: "EqGalil",
        302: "EqFamas",
        303: "EqAK47",
        304: "EqM4A4",
        305: "EqM4A1",
        306: "EqScout",  # Scout and SSG08 share the same ID
        307: "EqSG556",  # SG556 and SG553 share the same ID
        308: "EqAUG",
        309: "EqAWP",
        310: "EqScar20",
        311: "EqG3SG1",

        401: "EqZeus",
        402: "EqKevlar",
        403: "EqHelmet",
        404: "EqBomb",
        405: "EqKnife",
        406: "EqDefuseKit",
        407: "EqWorld",
        408: "EqZoneRepulsor",
        409: "EqShield",
        410: "EqHeavyAssaultSuit",
        411: "EqNightVision",
        412: "EqHealthShot",
        413: "EqTacticalAwarenessGrenade",
        414: "EqFists",
        415: "EqBreachCharge",
        416: "EqTablet",
        417: "EqAxe",
        418: "EqHammer",
        419: "EqWrench",
        420: "EqSnowball",
        421: "EqBumpMine",

        501: "EqDecoy",
        502: "EqMolotov",
        503: "EqIncendiary",
        504: "EqFlash",
        505: "EqSmoke",
        506: "EqHE",
    }

    return equipment_types[wepId]

queryThis()