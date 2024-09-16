from sqlalchemy import (
    create_engine, Integer, String, Float, ForeignKey, Text, Column, DateTime, Boolean
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


engine = create_engine('sqlite:///yes.db')
Base = declarative_base()


#Below is all the tables that I'll ever needs
#still only giving this half the data
#need to get those in soon meh.

class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    map = Column(String, nullable=False)
    teams = Column(String, nullable=False)

    players = relationship('Player', back_populates='match')
    roundinfo = relationship('RoundInformation', back_populates='match')


class RoundInformation(Base):
    __tablename__ = 'round_information'

    id = Column(Integer, primary_key=True)
    TeamAName = Column(String, nullable=False)
    TeamBName = Column(String, nullable=False)
    EconA = Column(Integer, nullable=False)
    EconB = Column(Integer, nullable=False)
    TypeofBuyA = Column(String, nullable=False)
    TypeofBuyB = Column(String, nullable=False)
    ScoreA = Column(Integer, nullable=False)
    ScoreB = Column(Integer, nullable=False)
    BombPlanted = Column(Boolean, nullable=False)
    PlayerPlanted = Column(String, nullable=False)
    RoundEndReason = Column(String, nullable=False)
    SideWon = Column(String, nullable=False)

    match_id = Column(Integer, ForeignKey('match.id'))
    match = relationship('Match', back_populates='roundinfo')

    round_kill = relationship('RoundKill', back_populates='roundinformation')


class RoundKill(Base):
    __tablename__ = 'round_kill'

    id = Column(Integer, primary_key=True)  # Add a primary key
    #TimeofKill = Column(DateTime, nullable=False)
    Killer = Column(String, nullable=False)
    KillerId = Column(Integer, nullable=False)
    VictId = Column(Integer, nullable=False)
    Victim = Column(String, nullable=False)
    Assistor = Column(String, nullable=False)
    KillerTeamString = Column(String, nullable=False)
    VictimTeamString = Column(String, nullable=False)
    #VictFlshDur = Column(DateTime, nullable=False)
    #VictDmgTaken = Column(Integer, nullable=False)
    AttDmgTaken = Column(Integer, nullable=False)
    IsHeadshot = Column(Boolean, nullable=False)
    IsFlashed = Column(Boolean, nullable=False)
    #Dist = Column(Integer, nullable=False)
    #KillerWeapon = Column(Integer, nullable=False)
    KillerTeam = Column(Integer, nullable=False)
    VictimTeam = Column(Integer, nullable=False)

    roundinformation_id = Column(Integer, ForeignKey('round_information.id'))
    roundinformation = relationship('RoundInformation', back_populates='round_kill')

class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match.id'), nullable=False)
    steam_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    impact = Column(Float)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    headshots = Column(Integer)
    hspercent = Column(Float)
    ADR = Column(Float)
    KSAST = Column(Integer)
    kdratio = Column(Float)
    firstkill = Column(Integer)
    firstdeath = Column(Integer)
    fkdiff = Column(Integer)
    round2k = Column(Integer)
    round3k = Column(Integer)
    round4k = Column(Integer)
    round5k = Column(Integer)
    totaldmg = Column(Integer)
    tradekills = Column(Integer)
    tradedeaths = Column(Integer)
    ctkills = Column(Integer)
    tkills = Column(Integer)
    effflashes = Column(Integer)
    avgflsduration = Column(Float)
    avgdist = Column(Float)
    totaldist = Column(Float)
    flashthrown = Column(Integer)
    clanname = Column(String)
    totalultildmg = Column(Integer)
    avgkillsrnd = Column(Float)
    avgdeathsrnd = Column(Float)
    avgassistrnd = Column(Float)
    roundsurvived = Column(Integer)
    roundtraded = Column(Integer)

    # Relationships
    match = relationship('Match', back_populates='players')
    weapon_kills = relationship(
        "PlayerWeaponKills",
        back_populates="player",
    )
    player_weaponkills = relationship("PlayWeaponKills", back_populates="player")

class PlayerWeaponKills(Base):
    __tablename__ = "player_weapon_kills"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("player.id"))
    weapon_id = Column(String)
    kills = Column(Integer)
    player_steam = Column(Integer, ForeignKey("player.steam_id"))

    # Relationship
    player = relationship('Player', back_populates='weapon_kills')
    player_steamid = relationship('Player', back_populates='weapons')



Base.metadata.create_all(engine)

