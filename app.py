from flask import Flask
from flask import render_template
from flask import session, redirect, url_for, request
from bson.objectid import ObjectId
import config
from utils import is_logged
from mongo import db as db
import pymongo
from threading import Thread

# S C R I P T S
import script.ntbscan
import script.nmap

app = Flask(__name__)


@app.route('/')
def index():
    if is_logged(session) :
        return redirect(url_for('computers'))
    else:
        return redirect(url_for('login'))

@app.route('/scan/')
@app.route('/scan/<id>')
def scan(id=None):
    if is_logged(session) :
        if len(str(id)) == 24 and id != None:
            computer = db.computers.find_one({"_id" : ObjectId(id)})
            thread = Thread(target = script.nmap.nmapscan, args = (db,computer['ip']))
            thread.start()
            info = "Scan of %s start" % computer['ip']
            return redirect(url_for('computers', info=info))
        else:
            thread = Thread(target = script.ntbscan.nbtscan, args = (db,) )
            thread.start()
            info = "Scan of netbios network start"
            return redirect(url_for('computers', info=info))
    else:
        return redirect(url_for('login'))


@app.route('/nmap/')
@app.route('/nmap/<id>')
def nmap(id=None):
        if id :
            computer = db.computers.find_one({"_id" : ObjectId(id)})
            return """
            <a href="%s">Return</a><br/>
             Hostname : %s <br/>
             IP : %s <br/>
             Mac : %s <br/>
             <hr>
             <b>Nmap</b> <br/>
             <code>
              %s
             </code>
             <hr>
             <a href="%s">Return</a><br/>
             """ % ( url_for('computers'),computer['hostname'],computer['ip'], \
                    computer['mac'], computer['nmap'], url_for('computers'))
        else :
            return "KO"


@app.route('/comment/', methods=['POST', 'GET'])
def comment():
    if is_logged(session) :
        if request.method == 'POST':
            db.computers.update({"_id": ObjectId(request.form['id'])}, { "$set": {"comment" : request.form['comment']}})
            return redirect(url_for('computers'))
    else:
        return redirect(url_for('login'))

@app.route('/computers/', methods=['POST', 'GET'])
@app.route('/computers/<id>')
def computers(id=None):
    if is_logged(session) :
        info = False
        if id :
            db.computers.update({"_id": ObjectId(id)}, { "$set": {"check" : True }})
        if request.method == 'POST':
              computer = {}
              computer["hostname"] = request.form['hostname']
              computer["ip"] = request.form['ip']
              computer["mac"] = ""
              db.computers.insert(computer)
        if request.method == 'GET' :
            if request.args.get('info') :
                info =request.args.get('info')
            if request.args.get('del') :
                id = request.args.get('del')
                db.computers.remove({"_id" : ObjectId(id)})
                info = "Computer remove!"
        computers = db.computers.find().sort([("ip", pymongo.ASCENDING)])
        return render_template('computers.html', computers=computers, info=info)


    else:
        return redirect(url_for('login'))




@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == config.USER and request.form['password'] == config.Password :
            session['username'] = request.form['username']
            session['type'] = "admin"
            session['login'] = True
        return redirect(url_for('index'))
    return '''
        <!-- Yes of course the supervisor it's running -->
        Welcome to Stupid scan  ! <br/> <br/>
        default : admin / admin
        <div style="width:100%;text-align:center">
        <form action="" method="post">
        <label>User</label><br/>
           <input type=text name=username><br/>
        <label>Password</label><br/>
          <input type=password name=password><br/><br/>

         <input type=submit value=Login>
        </form>
        </div>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    # set the secret key.  keep this really secret:
    app.secret_key = 'change_me!'
    if config.DEBUG :
        app.debug = True
    app.run(host="0.0.0.0") # Bind l'adresse plublic