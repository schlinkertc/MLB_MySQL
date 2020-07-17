"""
    For now: 
        Gathers GamePks, calls the API, and inserts first 50 games of the 2019 regular season
    End Game:
        For first time users to create the database schema and download a determined number of games
"""

from database import db
from database.api_call import get_pks

db.meta.create_all()

pks = get_pks(2019)
already_added = [x['game_pk'] for x in db.query('select game_pk from game')]
to_Add = list(set(pks)-set(already_added))

[db.insert_game(pk) for pk in to_Add]