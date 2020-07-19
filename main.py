"""
Gathers gamePks and inserts into the
"""

from database import db
from database.api_call import get_pks

db.meta.create_all()

seasons = [2019]

pks = []
for season in seasons:
    pks.extend(get_pks(season))

already_added = [x['game_pk'] for x in db.query('select game_pk from game')]
to_Add = list(set(pks)-set(already_added))

if len(to_Add)>0:
    [db.insert_game(pk) for pk in to_Add]
