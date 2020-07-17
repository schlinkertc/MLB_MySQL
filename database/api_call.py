import statsapi as mlb

def get_pks(season):
    season = mlb.get('season',{'sportId':1,'seasonId':season})['seasons'][0]
    start = season['seasonStartDate']
    end = season['seasonEndDate']
    schedule = mlb.get(
        'schedule',
        {'startDate':start,
         'endDate':end,
         'sportId':1}
    )

    pks = []
    for date in schedule['dates']:
        for game in date['games']:
            pks.append(game['gamePk'])

    pks = list(reversed(pks))
    return pks

def add_playFKs(dictionary,play,game):
    for fk in ['atBatIndex','playEndTime']:
        dictionary[fk]=play[fk]
        dictionary['gamePk']=game['gamePk']
        
def parse(input_dict,nested_lists=None):
    out={}
    if dict not in [type(x) for x in input_dict.values()]:
        return input_dict
    else:
        for k,v in input_dict.items():
            if type(v) in [str,int,float,bool]:
                out[k]=input_dict[k]
            elif type(v)==dict:
                nested_dict = v
                # if nested dict has an 'id', use it as a foreign key
                # exepct in the cause of the 'game' table which has a pk field
                if 'id' in nested_dict.keys() and 'pk' not in nested_dict.keys():
                    out[f"{k}_id"]=nested_dict['id']
                else:
                    for key,value in nested_dict.items():
                        out[f"{k}_{key}"]=value
            elif type(v)==list:
                if nested_lists != None:
                    nested_lists.append({k:v})
        return parse(out,nested_lists)

class Game():
    def __init__(self,gamePk):
        """Call the mlb API and parse results into flat dictionaries for DB insert."""
        # call the api 
        game = mlb.get('game',{'gamePk':gamePk})
        
        # players
        self.players = []
        players = game['gameData'].pop('players')
        for playerId in players.keys():
            self.players.append(parse(players[playerId]))
        
        # team / player stats
        #self.teams = []
        self.game_players = []
        self.team_stats = []
        self.team_records = []
        for home_away in ['away','home']:
            team = game['liveData']['boxscore']['teams'][home_away]
            players = team.pop('players')
            for playerId in players.keys():
                player = players[playerId]
                # add foreign keys to player / game records
                player['team_id']=team['team']['id']
                player['gamePk']=game['gamePk']
                self.game_players.append(parse(player))
            team_stats = team.pop('teamStats')
            team_stats['team_id']=team['team']['id']
            team_stats['gamePk']=game['gamePk']
            self.team_stats.append(parse(team_stats))
            #self.teams.append(parse(team))
        
        # game
        gm = parse(game['gameData'])
        #gm.update(game['gameData']['game'])
        setattr(self,'game',gm)
        
        # teams / team records 
        self.teams = []
        self.team_records = []
        teams = game['gameData']['teams']
        for home_away in ['home','away']:
            team = teams[home_away]
            team_record = parse(team.pop('record'))
            team_record['teamId']=team['id']
            team_record['gamePk']=game['gamePk']
            self.team_records.append(team_record)
            self.teams.append(parse(team))
        
        # venue
        self.venue = parse(game['gameData']['venue'])
        
        # plays and play events 
        parsed_plays = []
        game_play_events = []
        matchups = []
        self.pitches = []
        self.actions = []
        self.movements = []
        self.credits = []
        for play in game['liveData']['plays']['allPlays']:
            matchup = play.pop('matchup')
            add_playFKs(matchup,play,game)
            matchups.append(matchup)
            
            nested_play_details = []
            play_events = []
            
            parsed_plays.append(parse(play,nested_lists=nested_play_details))
            
            
            for element in nested_play_details:
                for value in element.values():
                    if type(value)==list and len(value)>0:
                        if type(value[0])==dict:
                            for x in value:
                                play_event = parse(x,nested_play_details)
                                # add FKs to trace back to the play
                                add_playFKs(play_event,play,game)
                                if play_event.get('isPitch'):
                                    self.pitches.append(play_event)
                                if play_event.get('type')=='action':
                                    self.actions.append(play_event)
                                if 'movement_isOut' in list(play_event.keys()):
                                    self.movements.append(play_event)
                                if 'credit' in list(play_event.keys()):
                                    self.credits.append(play_event)
                                play_events.append(play_event)
                                
            game_play_events.append(play_events)
            
        for play in parsed_plays:
            play['gamePk']=game['gamePk']
        
        setattr(self,'plays',parsed_plays)
        #setattr(self,'play_events',game_play_events)
        
        # dealing with matchups
        parsed_matchups = []
        game_matchup_stats = []
        for matchup in matchups:
            # pop out hot cold stats
            # these are such a pain to parse I might just calculate them myself
            for stats in ['batterHotColdZoneStats','pitcherHotColdZoneStats']:
                if stats in matchup.keys():
                    game_matchup_stats.append(matchup.pop(stats))
            parsed_matchups.append(parse(matchup))
                            
        setattr(self,'matchups',parsed_matchups)
    
    def __repr__(self):
        return self.game['game_id']