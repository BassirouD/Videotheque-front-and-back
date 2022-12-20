from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def inscription():
    return render_template('inscription.html')

@app.route('/createVideo', methods=['POST'])
def createVideo():
    print('hiiiiiiiiiiiiiiiiiii')
    if request.method=='POST':
        print('++++++++++++++++++++++++-----:', request.form)


    r = requests.post('http://127.0.0.1:5002/api/createVideotheque')
    
    print('---------------------',r)
    print('----------form-----------', form)
    return redirect(url_for('home'))

@app.route('/home')
def home():
    r = requests.get('http://127.0.0.1:5002/api/getAllMovies/test')
    data = json.loads(r.content)

    print(data['proprietaire'])

    return render_template('home.html', data = data)