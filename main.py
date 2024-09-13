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

Base.metadata.create_all(engine)

#Reads the json file from the data folder
def readJsonFiles(dirPath):
    for i in os.listdir(dirPath):
        with open(os.path.join(dirPath, i), 'r') as f:
            data = json.load(f)
        dataBaseStuff(data)

#does database magic stuff
def dataBaseStuff(data):
    #assigns the stuff for the match
    match = Match (
        map=data['map'],
        teams=data['teams'],
    )
    session.add(match)
    session.flush()

    #Get player data yikes really big
    for _, players in data["players"].items():
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
               kills=kills
           )
           session.add(weapon_kill)
    session.commit()

#query stuff to see if this work and it does.
def queryDat():
    matches = session.query(Match).all()

    for match in matches:
        print(match.id, match.map, match.teams)
        for player in match.players:
            print(player.name, player.kills, player.deaths, player.assists, player.headshots)


#These two methods below are for testing since we need to test don't we?
def dropall():
    Base.metadata.drop_all(engine)
    print("dropped")

def createTabs():
    Base.metadata.create_all(engine)
    print("created")

dropall()

createTabs()

readJsonFiles("C:\\Users\\iphon\\PycharmProjects\\dataAgg\\MatchDat")

queryDat()