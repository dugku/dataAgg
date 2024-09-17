import re

from sqlalchemy import (
    create_engine, Integer, String, Float, ForeignKey, Text, Column, DateTime,
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import json
import os
from tables import *
"""
This entire solution is trivial in a sense
Because I was doing this in fastAPI at first
But it was duplicating some of the players
So I just wrote this up since it would've been easier to deal with.
"""

Session = sessionmaker(bind=engine)
session = Session()

#Reads the json file from the data folder
def readJsonFiles(filepath):
    count = 0

    for _, v in enumerate(filepath):
        with open(v, 'r', encoding="utf8") as f:
            data = json.load(f)

            match_data = data.get("Match")
            if not isinstance(match_data, dict):
                print(f"No valid 'Match' data in file {v}.")
                continue

            rounds = match_data.get("rounds", [])
            if not isinstance(rounds, list):
                print(f"No valid 'rounds' data in file {v}.")
                continue

            # Filter out rounds where 'KillARound' is None or not a dict
            valid_rounds = []
            for index, round_data in enumerate(rounds):
                if not isinstance(round_data, dict):
                    print(f"Round {index} is invalid or None.")
                    continue
                kill_a_round = round_data.get("KillARound")
                if kill_a_round is None:
                    print(f"Round {index} has KillARound set to null or missing.")
                    continue
                elif not isinstance(kill_a_round, dict):
                    print(f"Round {index} has unexpected KillARound type: {type(kill_a_round)}")
                    continue
                # If all checks pass, add the round to the valid rounds list
                valid_rounds.append(round_data)

            # Update the data with only valid rounds
            data["Match"]["rounds"] = valid_rounds

            # Check if there are any valid rounds before processing
            if not valid_rounds:
                print(f"No valid rounds to process in file {v}.")
                continue

            dataBaseStuff(data)

def num_sort(value):
    parts = re.findall(r'\d+', value)

    return int(parts[0]) if parts else 0

def getFilePaths(dirPath):
    filepaths = [os.path.join(dirPath, f) for f in os.listdir(dirPath) if f.endswith('.json')]

    # Sort filepaths numerically by the numeric part of the filename
    filepaths_sorted = sorted(filepaths, key=num_sort)
    readJsonFiles(filepaths_sorted)

#does database magic stuff
def dataBaseStuff(data):
    #assigns the stuff for the match
    match_info = data['Match']

    match = Match (
        map=match_info['maps'],
        teams=match_info['teams'],
    )
    session.add(match)
    session.flush()

    for rounds in match_info['rounds']:
            round = RoundInformation (
                TeamAName=rounds['TeamNameA'],
                TeamBName=rounds['TeamNameB'],
                EconA=rounds['EconA'],
                EconB=rounds['EconB'],
                TypeofBuyA=rounds['TypeofBuyA'],
                TypeofBuyB=rounds['TypeofBuyB'],
                ScoreA=rounds['ScoreA'],
                ScoreB=rounds['ScoreB'],
                BombPlanted=rounds["BombPlanted"],
                PlayerPlanted=rounds['PlayerPlanted'],
                RoundEndReason=rounds['RoundEndedReason'],
                SideWon=rounds['SideWon'],
                match_id=match.id
            )

            session.add(round)
            session.flush()

            for key, roundKill in rounds['KillARound'].items():
                rKill = RoundKill(
                    Killer=roundKill['Killer'],
                    Victim=roundKill['Victim'],
                    KillerId=roundKill['KillerId'],
                    VictId=roundKill['VictId'],
                    Assistor=roundKill['Assistor'],
                    KillerTeamString=roundKill['KillerTeamString'],
                    VictimTeamString=roundKill['VictimTeamString'],
                    AttDmgTaken=roundKill['AttackerHealth'],
                    IsHeadshot=roundKill['IsHeadshot'],
                    IsFlashed=roundKill['IsFlashed'],
                    KillerTeam=roundKill['KillerTeam'],
                    VictimTeam=roundKill['VictTeam'],
                    roundinformation_id=round.id
                )
                session.add(rKill)

    #Get player data yikes really big
    for _, players in match_info["players"].items():
       player = Player(
           match_id=match.id,
           name=players["name"],
           steam_id=players["steamid"],
           kills=players["kills"],
           deaths=players["deaths"],
           assists=players["assists"],
           headshots=players["headshots"],
           hspercent=players["hspercent"],
           ADR=players["ADR"],
           KSAST=players["KSAST"],
           kdratio=players["kdratio"],
           firstkill=players["firstkill"],
           firstdeath=players["firstdeath"],
           fkdiff=players["firstdeath"] - players["firstkill"],
           round2k=players["round2k"],
           round3k=players["round3k"],
           round4k=players["round4k"],
           round5k=players["round5k"],
           totaldmg=players["totaldmg"],
           totalultildmg=players["totalultildmg"],
           avgkillsrnd=players["avgkillsrnd"],
           avgdeathsrnd=players["avgdeathsrnd"],
           avgassistrnd=players["avhassistrnd"],
           roundsurvived=players["roundsurvived"],
           roundtraded=players["roundtraded"],
           tradekills=players["tradekills"],
           ctkills=players["ctkills"],
           tkills=players["tkills"],
           effflashes=players["effflahses"],
           avgflsduration=players["avgflsduration"],
           avgdist=players["avgdist"],
           totaldist=players["totaldist"],
           flashthrown=players["flashthrown"],
           clanname=players["clananme"],
           tradedeaths=players["tradedeaths"],
           impact=players["impact"],
       )
       session.add(player)
       session.flush()
       #Weapon kill stuff easy to understand.
       #you don't understand? Too bad!
       for weapon_id, kills in players.get('weapons', {}).items():
           weapon_kill = PlayerWeaponKills(
               player_id=player.id,
               weapon_id=weapon_id,
               kills=kills,
               player_steam_id=player.steam_id
           )
           session.add(weapon_kill)
    session.commit()

#These two methods below are for testing since we need to test don't we?
def dropall():
    Base.metadata.drop_all(engine)
    print("dropped")

def createTabs():
    Base.metadata.create_all(engine)
    print("created")

dropall()

createTabs()

getFilePaths("C:\\Users\\Mike\\Desktop\\dataAgg\\stuff")
