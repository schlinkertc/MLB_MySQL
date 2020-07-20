# TO DO: 
## add a parent class to prevent repetition of init and refresh methods

import pandas as pd
from . import db
import os
import joblib

data_path = os.path.abspath(os.curdir)+'/data'

class NextPitchQuery():
    
    saved_filename = "nextPitch"
    
    def __init__(self):
        saved_data_path = f"{data_path}/{self.saved_filename}.pkl"
        try: 
            self.data = joblib.load(saved_data_path)
        except FileNotFoundError:
            self.data = self._executeQuery()        
        
    def _executeQuery(self):
        # query pitches and plays seperately
        pitch_q = """
        SELECT
            p.gamePk,
            p.atBatIndex,
            p.playEndTime,
            p.pitchNumber,
            lag(p.count_balls,1) OVER(
                                PARTITION BY gamePk, atBatIndex, playEndTime
                                ORDER BY pitchNumber) as balls,
            lag(p.count_strikes,1) OVER(
                                PARTITION BY gamePk, atBatIndex, playEndTime
                                ORDER BY pitchNumber) as strikes,

            lag(p.details_call_description,1) OVER(
                                    PARTITION BY gamePk, atBatIndex, playEndTime
                                    ORDER BY pitchNumber) as previous_result,
            lag(p.pitchData_zone,1) OVER(
                                    PARTITION BY gamePk, atBatIndex, playEndTime
                                    ORDER BY pitchNumber) as previous_pitchZone,
            lag(p.details_type_description,1) OVER(
                                    PARTITION BY gamePk, atBatIndex, playEndTime
                                    ORDER BY pitchNumber) as previous_pitchType,
            p.details_type_description as pitchType
        FROM
            pitches p
        WHERE
            p.gamePk
            IN
            (SELECT 
                game_pk
            FROM
                game
            WHERE
                game_type = 'R');
        """

        playMatchup_q = """
        SELECT
            plays.atBatIndex,
            plays.playEndTime,
            plays.gamePk,
            m.batter_id,
            m.pitcher_id,
            m.splits_pitcher,
            m.splits_batter,
            lag(m.splits_menOnBase,1) OVER(
                                    PARTITION BY gamePk
                                    ORDER BY atBatIndex) as menOnBase,
            lag(plays.count_outs,1) OVER(
                                    PARTITION BY gamePk
                                    ORDER BY atBatIndex) as outs,
            plays.about_halfInning as halfInning,
            plays.about_inning as inning,
            plays.result_awayScore,
            plays.result_homeScore,
            plays.result_rbi
        FROM
            plays
        INNER JOIN
            matchups m
            ON
                plays.atBatIndex=m.atBatIndex
                and
                plays.playEndTime=m.playEndTime
                and
                plays.gamePk=m.gamePk
        """
        
        pitch_results = db.query(pitch_q)

        playMatchup_results = db.query(playMatchup_q)

        pitches = pd.DataFrame.from_records(pitch_results)
        playMatchups = pd.DataFrame.from_records(playMatchup_results)

        pitches_matchups = pitches.join(
            playMatchups.set_index(
                ['gamePk','playEndTime','atBatIndex']
            ),
            on=['gamePk','playEndTime','atBatIndex']
        )
        
        return pitches_matchups
    
    def _refresh(self):
        saved_data_path = f"{data_path}/{self.saved_filename}.pkl"
        data = self._executeQuery()
        data.to_pickle(saved_data_path)
        print(f"data refreshed and saved at {saved_data_path}")
        
class Pitches():
    
    saved_filename = "Pitches"
    saved_data_path = f"{data_path}/{saved_filename}.pkl"
    
    def __init__(self):
        try: 
            self.data = joblib.load(self.saved_data_path)
        except FileNotFoundError:
            self.data = self._executeQuery()   
    
    def _executeQuery(self):
        q = """
        SELECT 
            p.gamePk,
            p.atBatIndex,
            p.playEndTime,
            p.pitchNumber,
            p.pitchData_endSpeed as endSpeed,
            p.pitchData_startSpeed as startSpeed,
            p.pitchData_breaks_breakLength as breakLength,
            p.pitchData_breaks_breakAngle as breakAngle,
            p.pitchData_zone as zone,
            p.details_type_description as pitchType,
            p.details_call_description as result,
            p.hitData_launchSpeed,
            p.hitData_launchAngle,
            p.hitData_totalDistance,
            p.hitData_hardness,
            p.hitData_location,
            m.batter_id,
            m.pitcher_id
        FROM
            pitches p
        INNER JOIN
            matchups m
            ON
                p.atBatIndex=m.atBatIndex
                and
                p.playEndTime=m.playEndTime
                and
                p.gamePk=m.gamePk
        WHERE
            p.details_type_description != 'Automatic Ball'
            AND
            p.gamePk 
            IN
            (SELECT 
                game_pk
            FROM
                game
            WHERE
                game_type = 'R')
            AND
                p.details_type_description NOT IN ('Automatic Ball','Knuckle Ball', 'Eephus','Forkball')
            AND 
                p.details_type_description IS NOT NULL;
        """
        
        df = pd.DataFrame.from_records( db.query(q) )
        df.to_pickle(self.saved_data_path)
        return df
    
    def _refresh(self):
        data = self._executeQuery()
        data.to_pickle(self.saved_data_path)
        print(f"data refreshed and saved at {self.saved_data_path}")