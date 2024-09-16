from main import *

def queryThis():
    stmt = session.query(Player).filter(Player.steam_id == 76561198214009861).all()

    allStats =  {
        "kills" : 0,
        "deaths" : 0,
        "assists" : 0,
        "matches": [],
        "firstKill": 0,
        "firstDeath": 0,
        "headshots":0,
        "ctkills":0,
        "tkills":0,
        "weaponStats": [],
    }

    for stats in stmt:
        allStats["matches"].append(stats.match_id)
        allStats["kills"] += stats.kills
        allStats["deaths"] += stats.deaths
        allStats["assists"] += stats.assists
        allStats["firstKill"] += stats.firstkill
        allStats["firstDeath"] += stats.firstdeath
        allStats["headshots"] += stats.headshots
        allStats["ctkills"] += stats.ctkills
        allStats["tkills"] += stats.tkills

        weaps = session.query(PlayerWeaponKills).filter(PlayerWeaponKills.player_steam_id == 76561198214009861).all()

        for i in weaps:
            allStats["weaponStats"].append({
                "wepName": wepNames(int(i.weapon_id)),
                "kills": i.kills
            })
            print(i.weapon_id)

    print(allStats)

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