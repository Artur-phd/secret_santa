import sqlite3 
from configurate.functions import db_connect


class CreateProfil():
    def add_in_db(self, user_id, name, team_name, wishes, status):
        self.wishes = wishes
        self.user_id = user_id
        self.name = name
        self.team_name = team_name
        self.status = status
        level = None



        lo = db_connect(db_name='players_data.sql', request="SELECT level FROM levels WHERE id = '%s'" % (user_id), do='get')
        if len(lo) == 0: 
            db_connect(db_name='players_data.sql', request="INSERT INTO levels (id, level) VALUES ('%s', 1)" % (user_id), do='post') 
            level = 1
        else:
            level = lo[0][0]
        db_connect(db_name='players_data.sql', request="INSERT INTO users (user_id, name_user, level, team, wishes, status_game, game_rools) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (user_id, name, level, team_name, wishes, status, 'No'), do='post') 

       
        