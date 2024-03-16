import sqlite3
import random


def check_user(user_id):
    conn = sqlite3.connect('players_data.sql')
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE user_id = '%s'" % (user_id))
    user_data = cur.fetchall()
    conn.close()

    if len(user_data) != 0:
        return True
    else:
        return False

def check_name(name):
    conn = sqlite3.connect('players_data.sql')
    cur = conn.cursor()
    cur.execute("SELECT name_user FROM users")
    data = cur.fetchall()
    conn.close()
    
    for names in data:
        if name == names[0]:
            return False
    return True


def fact_end_game(user_id2):
    if check_user(user_id=user_id2) is False:
        data = db_connect(db_name='players_data.sql', request="SELECT level FROM levels WHERE id = '%s'" % (user_id2), do='get')
        if len(data) != 0:
            print('FACT IS True')
            return True
        print('FACT IS False')
        return False

def check_team(team):
    conn = sqlite3.connect('players_data.sql')
    cur = conn.cursor()
    cur.execute("SELECT status_game FROM users WHERE team = '%s'" % (team))
    data = cur.fetchall()
    conn.close()
    for team_status in data:
        if team_status[0] == 'On':
            return False
    return True





def start_play(team, rools):
    conn = sqlite3.connect('players_data.sql')
    cur = conn.cursor()
    cur.execute("SELECT name_user FROM users WHERE team = '%s'" % (team))
    user_data = cur.fetchall()
    conn.close()

    for name in user_data:
        conn = sqlite3.connect('players_data.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET recipient = '%s' WHERE name_user = '%s'" % (rools.get(name[0]), name[0]))
        user_data = cur.fetchall()

        conn.commit()
        conn.close()



#DB CONNECTION -> db_name format: "players_data.sql"
def db_connect(db_name, request, do):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(request)
    if do == 'get':
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
    elif do == 'post':
        conn.commit()
        conn.close()
    




#check status game 
def check_status_game(user_id):
    conn = sqlite3.connect('players_data.sql')
    cur = conn.cursor()
    cur.execute("SELECT status_game FROM users WHERE user_id = '%s'" % (user_id))
    data = cur.fetchall()
    conn.commit()
    conn.close()
    if data[0][0] == 'On':
        return False
    else:
        return True

def tren(user_id):
    conn = sqlite3.connect('players_data.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = '%s'" % (user_id))
    user_data_1 = cur.fetchall()
    cur.execute("SELECT name_user FROM users WHERE team = '%s'" % (user_data_1[0][4]))
    user_data_2 = cur.fetchall()
    conn.close()
    team = list()
    for name in user_data_2:
        team.append(name[0])
    return len(team)

def start_game_list(user_id):
    conn = sqlite3.connect('players_data.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = '%s'" % (user_id))
    user_data_1 = cur.fetchall()
    cur.execute("SELECT name_user FROM users WHERE team = '%s'" % (user_data_1[0][4]))
    user_data_2 = cur.fetchall()
    cur.close()
    conn.close()
    team = list()
    for name in user_data_2:
        team.append(name[0])
    return team







# START GAME 
def boom(list_team):
    ch = 0
    santa_dict = dict()
    elfs_list = list()
    santa_list = list()
    lan = len(list_team)
    try:
        while len(santa_dict) != len(list_team):
            for i in range(lan):
                elf = random.choice(list_team[i:lan])
                santa = list_team[i]
                if elf != santa and elf not in elfs_list:
                    santa_dict[santa] = elf
                    elfs_list.append(elf)
                    santa_list.append(santa)
                else:
                    while elf in elfs_list:
                        elf = list_team[ch]
                        ch += 1
                    if elf != santa and elf not in elfs_list:
                        santa_dict[santa] = elf
                        elfs_list.append(elf)
                        santa_list.append(santa)
        if len(santa_dict) != len(list_team):
            boom(list_team)
    except IndexError:
        boom(list_team)

    return santa_dict


rol = {
    'Lomar': 'Mickle',
    'Dmitry': 'Russia'
}


def rools_format_sql(rol):
    result = f''
    keys = list(rol)
    for key in keys:
        result += f'{key}: {rol.get(key)}\n'
    return result



