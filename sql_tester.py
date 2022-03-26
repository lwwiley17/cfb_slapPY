import sqlite3

conn = sqlite3.connect('gamedb.sqlite')
cur = conn.cursor()

# # Do some setup
# init_script = open('db_init.sql', 'r')
# cur.executescript(init_script.read())
# conn.commit

cur.execute('SELECT * FROM Play')
play_keys = {desc[0] for desc in cur.description if desc[0] != 'id'}
for key in play_keys:
    print(key)
    
new_key = 'rusher'
sql_type = 'VARCHAR (50)'
cur.execute('ALTER TABLE Play ADD COLUMN ? VARCHAR(50)', (new_key,))