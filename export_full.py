import sqlite3
import csv

conn = sqlite3.connect('gamedb.sqlite')
cur = conn.cursor()
  
def select_columns(table_name):
    table_script = 'SELECT * FROM ' + table_name
    cur.execute(table_script)
    columns = [table_name + '.' + desc[0] for desc in cur.description]
    return(columns)
    
game_cols = [col for col in select_columns('Game') if all(tuple(key not in col for key in ('score','id')))]
drive_cols = ['Drive.series', 'Drive.drive_end']
play_cols = select_columns('Play')
selected_cols = tuple(game_cols + drive_cols + play_cols)

cur.execute('DROP VIEW IF EXISTS Full_Export;')
script = 'CREATE VIEW Full_Export AS SELECT ' + selected_cols[0]
for col in selected_cols[1:]:
    script = script + ', ' + col

script = script + ''' 
        FROM Game INNER JOIN Drive ON Game.id = Drive.game_id
        INNER JOIN Play ON Drive.id = Play.drive_id;
        '''
cur.execute(script)
cur.execute('SELECT * FROM Full_Export')
fields = [desc[0] for desc in cur.description]
plays = cur.fetchall()

filename = input('What team are you scouting?') + '.csv'
with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file, lineterminator = '\n')
    csv_writer.writerow(fields)
    csv_writer.writerows(plays)
