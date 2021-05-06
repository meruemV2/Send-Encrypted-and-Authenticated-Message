import sqlite3
import Encryption

'Encryption.py'
# create new db
conn = sqlite3.connect('Agent_table.db')

# create Cursor to execute queries
cur = conn.cursor()

# drop table from database
try:
    conn.execute('''Drop table SecretAgent''')
    # save changes
    conn.commit()
    print('SecretAgent table dropped.')
except:
    print('SecretAgent table did not exist')

# Create table SecretAgent
cur.execute('''CREATE TABLE SecretAgent(AgentId INTEGER PRIMARY KEY 
NOT NULL, AgentName TEXT NOT NULL, AgentAlias TEXT NOT NULL, 
AgentSecurityLevel INTEGER NOT NULL, LoginPassword TEXT NOT NULL);''')

# save changes
conn.commit()
print('SecretAgent Database created...')

# 1
# encrypt data AgentName, AgentAlias, and LoginPassword
AN = str(Encryption.cipher.encrypt(b'James Bond').decode("utf-8"))
AA = str(Encryption.cipher.encrypt(b'007').decode("utf-8"))
LP = str(Encryption.cipher.encrypt(b'pass123').decode("utf-8"))
cur.execute("Insert Into SecretAgent ('AgentName','AgentAlias','AgentSecurityLevel','LoginPassword')"
            " Values (?, ?, ?,?)", (AN, AA, 3, LP))
conn.commit()

# 2
# encrypt data AgentName, AgentAlias, and LoginPassword
AN = str(Encryption.cipher.encrypt(b'Kim Smith').decode("utf-8"))
AA = str(Encryption.cipher.encrypt(b'Smiley').decode("utf-8"))
LP = str(Encryption.cipher.encrypt(b'pass123').decode("utf-8"))
cur.execute("Insert Into SecretAgent ('AgentName','AgentAlias','AgentSecurityLevel','LoginPassword')"
            " Values (?, ?, ?,?)", (AN, AA, 1, LP))
conn.commit()

# 3
# encrypt data AgentName, AgentAlias, and LoginPassword
AN = str(Encryption.cipher.encrypt(b'Tom Hatfield').decode("utf-8"))
AA = str(Encryption.cipher.encrypt(b'Baldy').decode("utf-8"))
LP = str(Encryption.cipher.encrypt(b'pass123').decode("utf-8"))
cur.execute("Insert Into SecretAgent ('AgentName','AgentAlias','AgentSecurityLevel','LoginPassword')"
            " Values (?, ?, ?,?)", (AN, AA, 2, LP))
conn.commit()

# 4
# encrypt data AgentName, AgentAlias, and LoginPassword
AN = str(Encryption.cipher.encrypt(b'Dr. Evil').decode("utf-8"))
AA = str(Encryption.cipher.encrypt(b'E').decode("utf-8"))
LP = str(Encryption.cipher.encrypt(b'pass123').decode("utf-8"))
cur.execute("Insert Into SecretAgent ('AgentName','AgentAlias','AgentSecurityLevel','LoginPassword')"
            " Values (?, ?, ?,?)", (AN, AA, 3, LP))
conn.commit()

# 5
# encrypt data AgentName, AgentAlias, and LoginPassword
AN = str(Encryption.cipher.encrypt(b'Number 2').decode("utf-8"))
AA = str(Encryption.cipher.encrypt(b'Two').decode("utf-8"))
LP = str(Encryption.cipher.encrypt(b'pass123').decode("utf-8"))
cur.execute("Insert Into SecretAgent ('AgentName','AgentAlias','AgentSecurityLevel','LoginPassword')"
            " Values (?, ?, ?,?)", (AN, AA, 2, LP))
conn.commit()

# 6
# encrypt data AgentName, AgentAlias, and LoginPassword
AN = str(Encryption.cipher.encrypt(b'Mini me').decode("utf-8"))
AA = str(Encryption.cipher.encrypt(b'MM').decode("utf-8"))
LP = str(Encryption.cipher.encrypt(b'pass123').decode("utf-8"))
cur.execute("Insert Into SecretAgent ('AgentName','AgentAlias','AgentSecurityLevel','LoginPassword')"
            " Values (?, ?, ?,?)", (AN, AA, 1, LP))
conn.commit()

# iterate over the rows and print values
for row in cur.execute('SELECT * FROM SecretAgent;'):
    print(row)

#########

# create new db
conn = sqlite3.connect('Message_table.db')

# create Cursor to execute queries
cur = conn.cursor()

# drop table from database
try:
    conn.execute('''Drop table MessageAgent''')
    # save changes
    conn.commit()
    print('MessageAgent table dropped.')
except:
    print('MessageAgent table did not exist')

# Create table SecretAgent
cur.execute('''CREATE TABLE MessageAgent(MessageId INTEGER PRIMARY KEY 
NOT NULL, AgentId INTEGER NOT NULL, Message TEXT NOT NULL);''')

# save changes
conn.commit()
print('MessageAgent Database created...')

# 1
cur.execute('''Insert Into MessageAgent ('AgentId','Message') 
Values ('1', 'TEST 1');''')

conn.commit()

# 2
cur.execute('''Insert Into MessageAgent ('AgentId','Message') 
Values ('2', 'TEST 2');''')

conn.commit()
# 3
cur.execute('''Insert Into MessageAgent ('AgentId','Message') 
Values ('2', 'TEST 2 AGAIN');''')

conn.commit()
# 4
cur.execute('''Insert Into MessageAgent ('AgentId','Message') 
Values ('3', 'I am from Mars');''')

conn.commit()
# 5
cur.execute('''Insert Into MessageAgent ('AgentId','Message') 
Values ('1', 'Life is hard sometimes');''')

conn.commit()
# 6
cur.execute('''Insert Into MessageAgent ('AgentId','Message') 
Values ('3', 'TESTING 1 2 3');''')

conn.commit()

# iterate over the rows and print values
for row in cur.execute('SELECT * FROM MessageAgent;'):
    print(row)

# close database connection
# conn.close()
print('Connection closed.')