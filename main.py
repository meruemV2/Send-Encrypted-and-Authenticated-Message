"""

Name: Jerry Laplante
Date: 03/10/2021
Assignment: Module 8: Send Authenticated Message to Boss
Due Date: 003/10/2021
About this project:Build a small scale real-world application that incorporates the principles of secure computing
including cryptography, network security, and data protection.
All work below was performed by Jerry Laplante

"""
# imports
from flask import Flask, render_template, request, session, flash, jsonify
import sqlite3 as sql
import hmac, hashlib
import os
import string, base64
import Encryption
import pandas as pd
import socket
import socketserver

app = Flask(__name__)


# home page routes to home.html
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        nm = session['name']
        nm = str(Encryption.cipher.decrypt(nm))
        return render_template('home.html', name=nm)


# enter new routes to agent.html only in logged in and admin (level 1)
@app.route('/enternew')
def new_agent():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin') == True:
        return render_template('agent.html')
    else:
        msg = "page not found"
        return render_template("result.html", msg=msg)


@app.route('/boss')
def boss():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        nm = session['name']
        nm = str(Encryption.cipher.decrypt(nm))
        return render_template('boss.html', name=nm)


# routine to handle sending encrypted and authenticated messages to boss
@app.route('/boss', methods=['POST'])
def send_message():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            # error checking
            msg = request.form['message']
            if len(msg) < 1 or msg.isspace():
                msg = "You can not enter in an empty message"
                return render_template("result.html", msg=msg)
            else:
                try:
                    msg = request.form['message']
                    nm = session['name']
                    nm = str(Encryption.cipher.decrypt(nm))

                    with sql.connect("Agent_table.db") as con:
                        con.row_factory = sql.Row
                        cur = con.cursor()

                    sql_select_query = """select * from SecretAgent where AgentName = ?"""
                    cur.execute(sql_select_query, nm)

                    row = cur.fetchone();
                    aId = int(row['AgentId'])

                    with sql.connect("Message_table.db") as con:
                        cur = con.cursor()

                    cur.execute("INSERT INTO MessageAgent ('AgentId','Message') "
                                "VALUES  (?,?)", (aId, msg))

                    con.commit()
                    
                    body = bytes(msg, encoding='utf-8')
                    bodyEncrypted = Encryption.cipher.encrypt(body)
                    secret = b'1234'
                    computedSig = hmac.new(secret, body,
                                           digestmod=hashlib.sha3_512).digest()
                    sentMessage = bodyEncrypted + computedSig

                    # msg = str(Encryption.cipher.encrypt(bytes(msg, 'utf-8')).decode("utf-8"))

                    HOST, PORT = "localhost", 8888
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Connect to server and send data
                    sock.connect((HOST, PORT))

                    sock.sendall(bytes(sentMessage, "utf-8"))

                    sock.close()

                    msg = "Message successfully sent to boss"

                    return render_template("result.html", msg=msg)
                except sock.error as e:
                    msg = "Error - Message NOT sent to boss:", e
                finally:
                    return render_template("result.html", msg=msg)



# the new agent is added only after input has been validated
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin') == True:
        if request.method == 'POST':

            nm = request.form['AgentName']
            aa = request.form['AgentAlias']
            asl = request.form['AgentSecurityLevel']
            pwd = request.form['LoginPassword']
            validInput = True

            msg = ""
            if len(nm) < 1 or nm.isspace():
                msg = msg + "Name is empty\n"
                validInput = False

            if len(aa) < 1 or aa.isspace():
                msg = msg + "Alias is empty\n"
                validInput = False

            if len(asl) < 1 or asl.isspace() or not asl.isnumeric():
                msg = msg + "Security level must be between 1 and 10\n"
                validInput = False
            elif int(asl) > 10 or int(asl) < 1:
                msg = msg + "Security level must be between 1 and 10\n"
                validInput = False

            if len(pwd) < 1 or pwd.isspace():
                msg = msg + "Pwd is empty\n"
                validInput = False
            # finally adds to new db record
            if validInput:
                try:
                    nm = request.form['AgentName']
                    nm = str(Encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode("utf-8"))
                    aa = request.form['AgentAlias']
                    aa = str(Encryption.cipher.encrypt(bytes(aa, 'utf-8')).decode("utf-8"))
                    asl = request.form['AgentSecurityLevel']
                    pwd = request.form['LoginPassword']
                    pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

                    with sql.connect("Agent_table.db") as con:
                        cur = con.cursor()

                    cur.execute("INSERT INTO SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) "
                                "VALUES  (?,?,?,?)", (nm, aa, asl, pwd))

                    con.commit()
                    msg = "Record successfully added"
                # more error checking
                except:
                    con.rollback()
                    msg = "error in insert operation"

                finally:
                    return render_template("result.html", msg=msg)
                    con.close()
        return render_template("result.html", msg=msg)
        con.close()
    else:
        # if failed then repeat trying to login
        return render_template('login.html')


# checks to see if user is level 1 or 2 before displaying
@app.route('/list')
def list():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin') == True:
        con = sql.connect("Agent_table.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select AgentName, AgentAlias, AgentSecurityLevel, LoginPassword from SecretAgent")
        df = pd.DataFrame(cur.fetchall(), columns=['AgentName', 'AgentAlias', 'AgentSecurityLevel', 'LoginPassword']);

        # convert to an array
        index = 0
        for nm in df['AgentName']:
            nm = str(Encryption.cipher.decrypt(nm))
            df._set_value(index, 'AgentName', nm)
            index += 1
        con.close()

        index = 0
        for aa in df['AgentAlias']:
            aa = str(Encryption.cipher.decrypt(aa))
            df._set_value(index, 'AgentAlias', aa)
            index += 1
        con.close()
        return render_template("list.html", rows=df)
    # repeat for next admin level
    elif session.get('admin2') == True:
        con = sql.connect("Agent_table.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select AgentName, AgentAlias, AgentSecurityLevel, LoginPassword from SecretAgent")
        df = pd.DataFrame(cur.fetchall(), columns=['AgentName', 'AgentAlias', 'AgentSecurityLevel', 'LoginPassword']);

        # convert to an array
        index = 0
        for nm in df['AgentName']:
            nm = str(Encryption.cipher.decrypt(nm))
            df._set_value(index, 'AgentName', nm)
            index += 1
        con.close()

        index = 0
        for aa in df['AgentAlias']:
            aa = str(Encryption.cipher.decrypt(aa))
            df._set_value(index, 'AgentAlias', aa)
            index += 1
        con.close()
        return render_template("list.html", rows=df)
    # else returns user to error page
    else:
        msg = "page not found"
        return render_template("result.html", msg=msg)


# logic to ascertain a user's security level
@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        nm = request.form['AgentName']
        nm = str(Encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode("utf-8"))
        pwd = request.form['LoginPassword']
        pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

        with sql.connect("Agent_table.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = """select * from SecretAgent where AgentName = ? and LoginPassword = ?"""
            cur.execute(sql_select_query, (nm, pwd))

            row = cur.fetchone();
            if (row != None):
                session['logged_in'] = True
                session['name'] = nm
                if (int(row['AgentSecurityLevel']) == 1):
                    session['admin'] = True
                else:
                    session['admin'] = False
                if (int(row['AgentSecurityLevel']) == 2):
                    session['admin2'] = True
                else:
                    session['admin2'] = False
                if (int(row['AgentSecurityLevel']) == 3):
                    session['admin3'] = True
                else:
                    session['admin3'] = False
            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')
    except:
        con.rollback()
        flash("error in insert operation")
    finally:
        con.close()
    return home()


# logs user out
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['admin'] = False
    session['name'] = ""
    return home()


# init function
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
