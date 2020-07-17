"""Initialize database connection"""
from sqlalchemy import create_engine
import pymysql
from os import path,environ
from dotenv import load_dotenv
from .api_call import Game
from .tables import Base

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, '.env'))

class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    """
    Class for instantiating a SQL Alchemy connection.
    Credit to Medium user Mahmud Ahsan:
    https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32
    """
    DB_ENGINE = {
        'sqlite': 'sqlite:////{dbname}',
        'pymysql': 'mysql+pymysql://{username}:{password}@{hostname}/{dbname}?charset=UTF8MB4'
    }

    # Main DB Connection Ref Obj
    engine = None
    def __init__(self, dbtype, **kwargs):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(**kwargs)
            self.engine = create_engine(engine_url)
            print(self.engine)
            
            self.Base = Base
            self.meta = self.Base.metadata
            self.meta.bind=self.engine

        else:
            print("DBType is not found in DB_ENGINE")
    def __repr__(self):
        return "{dbtype} connection"
    
    def query(self,query_statement,out_type='records'):
        with self.engine.connect() as conn:
            result = conn.execute(query_statement)
            if out_type == 'records':
                out = [dict(row) for row in result]
            if out_type=='tuples':
                out = [tuple(row) for row in result]
        conn.close()
        return out
    
    def __map_toTable(self,tablename,record):
        out = {}
        for col in self.meta.tables[tablename].c:
            out[col.name]=record.get(col.name)
        return out
        
    def insert_game(self,gamePk):
        existing_games = [
            x['game_pk'] for x in self.query("select game_pk from game")
        ]
        if gamePk in existing_games:
            return f"{gamePk} already added"
        game = Game(gamePk)
        
        records_toAdd = {}
        
        # Game
        game_record = self.__map_toTable('game',game.game)
        records_toAdd['game']=game_record
        
        # Venue
        existing = self.query(
            f"select * from venue where id = {game.venue['id']}"
        )
        if len(existing)==0:
            venue_record=self.__map_toTable('venue',game.venue)
            records_toAdd['venue']=venue_record
        
        # Players
        existing = [x['id'] for x in self.query('select `id` from players')]
        game_players = [x['id'] for x in game.players]
        to_add = list(set(game_players)-set(existing))
        players_toAdd = [x for x in game.players if x['id'] in to_add]
        player_records = [
            self.__map_toTable('players',player) 
            for player in players_toAdd
        ]
        records_toAdd['players']=player_records
        
        # Teams
        team_records = []
        for team in game.teams:
            existing = self.query(
                f"select * from teams where id = {team['id']}"
            )
            if len(existing)==0:
                team_records.append(self.__map_toTable('teams',team))
        records_toAdd['teams']=team_records
        
        # Everything else
        for table in ['plays','pitches',
                      'movements','credits','matchups',
                      'actions','team_records','game_players']:
            records = []
            for record in game.__dict__[table]:
                row = {}
                for col in [x.name for x in self.meta.tables[table].c]:
                    row[col]=record.get(col)
                records.append(row)
            records_toAdd[table]=records
        
        for tablename in records_toAdd.keys():
            table = self.meta.tables[tablename]
            if type(records_toAdd[tablename])==dict:
                with self.engine.connect() as conn:
                    conn.execute(
                        table.insert().values(**records_toAdd[tablename])
                    )
                    conn.close()
            if type(records_toAdd[tablename])==list and len(records_toAdd[tablename])>0:
                with self.engine.connect() as conn:
                    conn.execute(table.insert(),records_toAdd[tablename])
                    conn.close()
        return f"{gamePk} inserted"
                
            
db = MyDatabase(
    dbtype='pymysql',
    username=environ.get('db_user'),
    password=environ.get('db_password'),
    hostname=environ.get('db_host'),
    dbname='MLB'
    
)

