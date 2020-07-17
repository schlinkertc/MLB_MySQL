"""Define sql tables"""
from sqlalchemy import (
    Column,Integer,String,
    DateTime,Date,Boolean,Float,ForeignKey,
    ForeignKeyConstraint,PrimaryKeyConstraint
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
    __tablename__ = 'game'
    __table_args__ = {'extend_existing':True}
    
    game_pk=Column(Integer,primary_key=True)
    game_type=Column(String(1))
    game_doubleHeader=Column(String(1))
    game_id=Column(String(26))
    game_gamedayType=Column(String(1))
    game_tiebreaker=Column(String(1))
    game_gameNumber=Column(Integer)
    game_calendarEventID=Column(String(20))
    game_season=Column(String(4))
    game_seasonDisplay=Column(String(4))
    datetime_dateTime=Column(String(20))
    datetime_originalDate=Column(String(10))
    datetime_dayNight=Column(String(5))
    datetime_time=Column(String(5))
    datetime_ampm=Column(String(2))
    status_abstractGameState=Column(String(5))
    status_codedGameState=Column(String(1))
    status_detailedState=Column(String(21))
    status_statusCode=Column(String(2))
    status_abstractGameCode=Column(String(1))
    teams_away_id=Column(Integer)
    teams_home_id=Column(Integer)
    venue_id=Column(Integer)
    weather_condition=Column(String(13))
    weather_temp=Column(String(3))
    weather_wind=Column(String(18))
    review_hasChallenges=Column(Integer)
    review_away_used=Column(Integer)
    review_away_remaining=Column(Integer)
    review_home_used=Column(Integer)
    review_home_remaining=Column(Integer)
    flags_noHitter=Column(Integer)
    flags_perfectGame=Column(Integer)
    flags_awayTeamNoHitter=Column(Integer)
    flags_awayTeamPerfectGame=Column(Integer)
    flags_homeTeamNoHitter=Column(Integer)
    flags_homeTeamPerfectGame=Column(Integer)
    probablePitchers_away_id=Column(Float)
    probablePitchers_home_id=Column(Float)
    officialScorer_id=Column(Float)
    primaryDatacaster_id=Column(Float)
    secondaryDatacaster_id=Column(Float)
    status_startTimeTBD=Column(Float)
      
class Play(Base):
    __tablename__ = 'plays'
    __table_args__ = (
        PrimaryKeyConstraint('atBatIndex','playEndTime','gamePk',name='play_pk'),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['game.game_pk']
        ),
        {'extend_existing':True}
    )
    
    atBatIndex=Column(Integer)
    playEndTime=Column(String(24))
    gamePk=Column(Integer)
    
    result_type=Column(String(5))
    result_event=Column(String(28))
    result_eventType=Column(String(28))
    result_description=Column(String(402))
    result_rbi=Column(Integer)
    result_awayScore=Column(Integer)
    result_homeScore=Column(Integer)
    about_atBatIndex=Column(Integer)
    about_halfInning=Column(String(6))
    about_isTopInning=Column(Integer)
    about_inning=Column(Integer)
    about_startTime=Column(String(24))
    about_endTime=Column(String(24))
    about_isComplete=Column(Integer)
    about_isScoringPlay=Column(Integer)
    about_hasReview=Column(Float)
    about_hasOut=Column(Integer)
    about_captivatingIndex=Column(Integer)
    count_balls=Column(Integer)
    count_strikes=Column(Integer)
    count_outs=Column(Integer)
    reviewDetails_isOverturned=Column(Float)
    reviewDetails_reviewType=Column(String(2))
    reviewDetails_challengeTeamId=Column(Float)
    
class Pitch(Base):
    __tablename__ = 'pitches'
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['game.game_pk']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.atBatIndex','plays.playEndTime'],
            name='pitch_play'
        ),
        {'extend_existing':True})
    
    gamePk=Column(Integer,primary_key=True)
    
    atBatIndex=Column(Integer,primary_key=True)
    playEndTime=Column(String(24),primary_key=True)
    
    index=Column(Integer,primary_key=True)
    
    details_call_code=Column(String(2))
    details_call_description=Column(String(25))
    details_description=Column(String(25))
    details_code=Column(String(2))
    details_ballColor=Column(String(22))
    details_trailColor=Column(String(22))
    details_isInPlay=Column(Integer)
    details_isStrike=Column(Integer)
    details_isBall=Column(Integer)
    details_type_code=Column(String(2))
    details_type_description=Column(String(18))
    details_hasReview=Column(Integer)
    count_balls=Column(Integer)
    count_strikes=Column(Integer)
    pitchData_startSpeed=Column(Float)
    pitchData_endSpeed=Column(Float)
    pitchData_strikeZoneTop=Column(Float)
    pitchData_strikeZoneBottom=Column(Float)
    pitchData_coordinates_aY=Column(Float)
    pitchData_coordinates_aZ=Column(Float)
    pitchData_coordinates_pfxX=Column(Float)
    pitchData_coordinates_pfxZ=Column(Float)
    pitchData_coordinates_pX=Column(Float)
    pitchData_coordinates_pZ=Column(Float)
    pitchData_coordinates_vX0=Column(Float)
    pitchData_coordinates_vY0=Column(Float)
    pitchData_coordinates_vZ0=Column(Float)
    pitchData_coordinates_x=Column(Float)
    pitchData_coordinates_y=Column(Float)
    pitchData_coordinates_x0=Column(Float)
    pitchData_coordinates_y0=Column(Float)
    pitchData_coordinates_z0=Column(Float)
    pitchData_coordinates_aX=Column(Float)
    pitchData_breaks_breakAngle=Column(Float)
    pitchData_breaks_breakLength=Column(Float)
    pitchData_breaks_breakY=Column(Float)
    pitchData_breaks_spinRate=Column(Float)
    pitchData_breaks_spinDirection=Column(Float)
    pitchData_zone=Column(Float)
    pitchData_typeConfidence=Column(Float)
    pitchData_plateTime=Column(Float)
    pitchData_extension=Column(Float)
    pfxId=Column(String(13))
    playId=Column(String(36))
    pitchNumber=Column(Integer)
    startTime=Column(String(24))
    endTime=Column(String(24))
    isPitch=Column(Integer)
    type=Column(String(5))
    hitData_launchSpeed=Column(Float)
    hitData_launchAngle=Column(Float)
    hitData_totalDistance=Column(Float)
    hitData_trajectory=Column(String(15))
    hitData_hardness=Column(String(6))
    hitData_location=Column(String(2))
    hitData_coordinates_coordX=Column(Float)
    hitData_coordinates_coordY=Column(Float)
    details_runnerGoing=Column(Float)
    reviewDetails_isOverturned=Column(Float)
    reviewDetails_reviewType=Column(String(2))
    reviewDetails_challengeTeamId=Column(Float)

class Action(Base):
    __tablename__ = 'actions'
    __table_args__ = (
        PrimaryKeyConstraint('playEndTime','atBatIndex','index','gamePk',name='action_pk'),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['game.game_pk'],
            name='action_game'
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.atBatIndex','plays.playEndTime'],
            name='action_play'
        ),
        {'extend_existing':True})
    
    atBatIndex=Column(Integer)
    gamePk=Column(Integer)
    playEndTime=Column(String(24))
    index=Column(Integer)
    
    details_description=Column(String(207))
    details_event=Column(String(28))
    details_eventType=Column(String(28))
    details_awayScore=Column(Integer)
    details_homeScore=Column(Integer)
    details_isScoringPlay=Column(Integer)
    details_hasReview=Column(Integer)
    count_balls=Column(Integer)
    count_strikes=Column(Integer)
    count_outs=Column(Integer)
    startTime=Column(String(24))
    endTime=Column(String(24))
    isPitch=Column(Integer)
    type=Column(String(6))
    player_id=Column(Integer)
    position_code=Column(String(2))
    position_name=Column(String(17))
    position_type=Column(String(10))
    position_abbreviation=Column(String(2))
    battingOrder=Column(String(3))
    actionPlayId=Column(String(36))
    umpire_id=Column(Float)
    base=Column(Float)
    reviewDetails_isOverturned=Column(Float)
    reviewDetails_reviewType=Column(String(2))
    reviewDetails_challengeTeamId=Column(Float)
    injuryType=Column(String(8))
    
class Credit(Base):
    
    __tablename__ = 'credits'
    __table_args__ = (
#         PrimaryKeyConstraint(
#             'playEndTime','atBatIndex',
#             'credit','player_id','credit_id',
#             'gamePk',
#             name='credit_pk'),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['game.game_pk'],
            name='credit_game'
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.atBatIndex','plays.playEndTime'],
            name='credit_play'
        ),
        ForeignKeyConstraint(
            columns=['player_id'],
            refcolumns=['players.id'],
            name='credit_player'
        ),
        {'extend_existing':True})
    
    # requires autoincrement Primary Key because of duplicate values that arise 
    # in an unassisted double play
    credit_id = Column(Integer,primary_key=True) # autoincrement by default
    
    player_id=Column(Integer)
    position_code=Column(String(1))
    position_name=Column(String(11))
    position_type=Column(String(10))
    position_abbreviation=Column(String(2))
    credit=Column(String(20))
    atBatIndex=Column(Integer)
    gamePk=Column(Integer)
    playEndTime=Column(String(24))

class Matchup(Base):
    __tablename__ = 'matchups'
    __table_args__ = (
        PrimaryKeyConstraint(
            'playEndTime','atBatIndex',
            'batter_id',
            'gamePk',
            name='matchup_pk'),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['game.game_pk'],
            name='matchup_game'
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.atBatIndex','plays.playEndTime'],
            name='matchup_play'
        ),
        ForeignKeyConstraint(
            columns=['batter_id'],
            refcolumns=['players.id'],
            name='matchup_batter'
        ),
        ForeignKeyConstraint(
            columns=['pitcher_id'],
            refcolumns=['players.id'],
            name='matchup_pitcher'
        ),
        {'extend_existing':True})
    

    batter_id=Column(Integer)
    batSide_code=Column(String(1))
    batSide_description=Column(String(5))
    pitcher_id=Column(Integer)
    pitchHand_code=Column(String(1))
    pitchHand_description=Column(String(5))
    splits_batter=Column(String(6))
    splits_pitcher=Column(String(6))
    splits_menOnBase=Column(String(6))
    atBatIndex=Column(Integer)
    gamePk=Column(Integer)
    playEndTime=Column(String(24))
    postOnFirst_id=Column(Float)
    postOnSecond_id=Column(Float)
    postOnThird_id=Column(Float)

class Movement(Base):
    __tablename__ = 'movements'
    __table_args__ = (
        PrimaryKeyConstraint(
            'playEndTime','atBatIndex',
            'details_runner_id','details_playIndex',
            'movement_start','movement_end',
            'gamePk',name='movement_pk'),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['game.game_pk'],
            name='movement_game'
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.atBatIndex','plays.playEndTime'],
            name='movement_play'
        ),
        ForeignKeyConstraint(
            columns=['details_runner_id'],
            refcolumns=['players.id'],
            name='movement_runner'
        ),
        ForeignKeyConstraint(
            columns=['details_responsiblePitcher_id'],
            refcolumns=['players.id'],
            name='movement_pitcher',
        ),
        {'extend_existing':True})
    
    # movement_id = Column(Integer) #autoincrement by default
    atBatIndex=Column(Integer)
    gamePk=Column(Integer)
    playEndTime=Column(String(24))
    movement_end=Column(String(5))
    movement_start=Column(String(2))
    details_runner_id=Column(Integer)
    details_playIndex=Column(Integer)
    
    movement_outBase=Column(String(2))
    movement_isOut=Column(Integer)
    movement_outNumber=Column(Float)
    details_event=Column(String(28))
    details_eventType=Column(String(28))
    details_isScoringEvent=Column(Integer)
    details_rbi=Column(Integer)
    details_earned=Column(Integer)
    details_teamUnearned=Column(Integer)
    details_movementReason=Column(String(30))
    details_responsiblePitcher_id=Column(Integer)
    
    
class Player(Base):
    __tablename__ = 'players'
    __table_args__ = {'extend_existing':True}
    
    id=Column(Integer,primary_key=True)
    fullName=Column(String(21))
    link=Column(String(21))
    firstName=Column(String(14))
    lastName=Column(String(13))
    primaryNumber=Column(String(2))
    birthDate=Column(String(10))
    currentAge=Column(Integer)
    birthCity=Column(String(28))
    birthStateProvince=Column(String(17))
    birthCountry=Column(String(18))
    height=Column(String(6))
    weight=Column(Integer)
    active=Column(Integer)
    primaryPosition_code=Column(String(2))
    primaryPosition_name=Column(String(17))
    primaryPosition_type=Column(String(10))
    primaryPosition_abbreviation=Column(String(2))
    useName=Column(String(11))
    middleName=Column(String(15))
    boxscoreName=Column(String(18))
    nickName=Column(String(27))
    gender=Column(String(1))
    isPlayer=Column(Integer)
    isVerified=Column(Integer)
    draftYear=Column(Float)
    mlbDebutDate=Column(String(10))
    batSide_code=Column(String(1))
    batSide_description=Column(String(6))
    pitchHand_code=Column(String(1))
    pitchHand_description=Column(String(6))
    nameFirstLast=Column(String(21))
    nameSlug=Column(String(28))
    firstLastName=Column(String(21))
    lastFirstName=Column(String(22))
    lastInitName=Column(String(16))
    initLastName=Column(String(15))
    fullFMLName=Column(String(30))
    fullLFMName=Column(String(31))
    strikeZoneTop=Column(Float)
    strikeZoneBottom=Column(Float)
    nameMatrilineal=Column(String(11))
    pronunciation=Column(String(29))
    nameTitle=Column(String(3))
    lastPlayedDate=Column(String(10))
    deathDate=Column(String(10))
    deathCity=Column(String(9))
    deathStateProvince=Column(String(2))
    deathCountry=Column(String(3))
    
    
class Team(Base):
    __tablename__ = 'teams'
    __table_args__ = {'extend_existing':True}
    
    id=Column(Integer,primary_key=True)
    name=Column(String(25))
    link=Column(String(17))
    season=Column(Integer)
    venue_id=Column(Integer)
    teamCode=Column(String(3))
    fileCode=Column(String(3))
    abbreviation=Column(String(3))
    teamName=Column(String(12))
    locationName=Column(String(13))
    firstYearOfPlay=Column(String(4))
    league_id=Column(Integer)
    division_id=Column(Float)
    sport_id=Column(Integer)
    shortName=Column(String(13))
    springLeague_id=Column(Float)
    allStarStatus=Column(String(1))
    active=Column(Integer)

    
class Venue(Base):
    __tablename__ = 'venue'
    __table_args__ = {'extend_existing':True}
    
    id=Column(Integer,primary_key=True)
    name=Column(String(28))
    link=Column(String(19))
    location_city=Column(String(14))
    location_state=Column(String(20))
    location_stateAbbrev=Column(String(2))
    location_defaultCoordinates_latitude=Column(Float)
    location_defaultCoordinates_longitude=Column(Float)
    timeZone_id=Column(String(19))
    fieldInfo_capacity=Column(Integer)
    fieldInfo_turfType=Column(String(10))
    fieldInfo_roofType=Column(String(11))
    fieldInfo_leftLine=Column(Integer)
    fieldInfo_leftCenter=Column(Float)
    fieldInfo_center=Column(Integer)
    fieldInfo_rightCenter=Column(Float)
    fieldInfo_rightLine=Column(Integer)
    fieldInfo_left=Column(Float)
    fieldInfo_right=Column(Float)
    location_country=Column(String(14))
    
class Team_Record(Base):
    __tablename__ = 'team_records'
    __table_args__ = {'extend_existing':True}
    
    id = Column(Integer,primary_key=True) # autoincrement by default
    gamesPlayed = Column(Integer)
    wildCardGamesBack = Column(String(5))
    leagueGamesBack = Column(String(5))
    springLeagueGamesBack = Column(String(5))
    sportGamesBack = Column(String(5))
    divisionGamesBack = Column(String(5))
    conferenceGamesBack = Column(String(5))
    leagueRecord_wins = Column(String(5))
    leagueRecord_losses = Column(String(5))
    leagueRecord_pct = Column(String(5))
    divisionLeader = Column(String(5))
    wins = Column(String(5))
    losses = Column(String(5))
    winningPercentage = Column(String(5))
    teamId = Column(Integer,ForeignKey('teams.id'))
    gamePk = Column(Integer,ForeignKey('game.game_pk'))
    
class Game_Players(Base):
    __tablename__ = 'game_players'
    __table_args__ = {'extend_existing':True}
    
    id = Column(Integer,primary_key=True) # autoincrement by default
    person_id = Column(Integer,ForeignKey('players.id'))
    jerseyNumber = Column(String(15))
    position_code = Column(String(15))
    position_name = Column(String(25))
    position_type = Column(String(15))
    position_abbreviation = Column(String(15))
    status_code = Column(String(15))
    status_description = Column(String(15))
    parentTeamId = Column(String(15))
    battingOrder = Column(String(15))
    gameStatus_isCurrentBatter = Column(String(15))
    gameStatus_isCurrentPitcher = Column(String(15))
    gameStatus_isOnBench = Column(String(15))
    gameStatus_isSubstitute = Column(String(15))
    team_id = Column(Integer,ForeignKey('teams.id'))
    gamePk = Column(Integer,ForeignKey('game.game_pk'))