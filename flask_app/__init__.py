from flask import Flask, session
DB = 'users2' #!CHANGE DB NAME IF 
app = Flask(__name__)
app.secret_key = "shhhhhh"
