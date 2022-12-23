from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json

app = Flask(__name__)
app.secret_key='Secret Key'

films = []
videotheques = []
selected_videotheque = ''

@app.route('/')
def inscription():
    print(requests.get)
    return render_template('inscription.html')

@app.route('/createVideo', methods=['POST'])
def createVideo():
    if request.method=='POST':
        payload = {'nomP': request.form['nomP'], 'prenomP': request.form['prenomP'], 'filename': request.form['filename']}
    
        r = requests.post('http://127.0.0.1:5001/api/createVideotheque',data=payload)

        #print('------R----------', r.status_code)

        if r.status_code == 201:
            flash('Vidéothèque créée avec success')
            return redirect(url_for('getAllVideotheque'))
            #return redirect(url_for('home', filename=payload['filename']))
        else:
            resp=json.loads(r.content.decode())
            flash(resp['warning'])
            return redirect('/')
    #print('---------------------',r)
    #print('----------form-----------', form)
    #return redirect(url_for('home'))

@app.route('/home/<filename>')
def home(filename='test'):
    global films
    global selected_videotheque
    r = requests.get('http://127.0.0.1:5001/api/getAllMovies/'+filename)
    data = json.loads(r.content.decode())
    films = data['films']
    data['selected_videotheque'] = selected_videotheque
    
    return render_template('home.html', data = data)



@app.route('/detailsfilm/<movieName>')
def detailsfilm(movieName):
    global selected_videotheque
    #print(selected_videotheque)
    for film in films:
        if film['titre'] == movieName:
            data={'film':film, 'selected_videotheque':selected_videotheque}
            print('data--->:',data)
            return render_template('detailsfilm.html', data = data)

def get_person_infos_from_fullname(fullname:str):
    firstName, lastname = fullname.split(' ')
    return {'nom': lastname, 'prenom': firstName}

@app.route('/addmovie/<filename>', methods=['GET','POST'])
def addmovie(filename='test'):
    global selected_videotheque
    if request.method == 'POST':
        #acteurs = list(map(
            #lambda fullName: get_person_infos_from_fullname(fullName),
            #request.form['acteurs'].split('-')))
        #print(acteurs)
        #print('Type acteurs', type(acteurs))
        payload = {
            'titre': request.form['titre'], 
            'annee': request.form['annee'], 
            'nomR': request.form['nomR'],
            'prenomR': request.form['prenomR'],
            'acteurs': request.form['acteurs']
        }
        r = requests.post('http://127.0.0.1:5001/api/addFilms/' + selected_videotheque,data=payload)

        #headers = {'accept': 'application/json'}
        #r = requests.post('http://127.0.0.1:5001/api/addFilms/' + selected_videotheque,json=acteurs)
        #print(r.content)
        return redirect(url_for('home', filename=selected_videotheque))
    if request.method == 'GET':
        return render_template('addmovie.html', selected_videotheque=selected_videotheque)


@app.route('/getAllVideotheque')
def getAllVideotheque():
    global videotheques
    r = requests.get('http://127.0.0.1:5001/api/getAllVideotheque')
    #print(r.content.decode())
    data = json.loads(r.content.decode())
    videotheques = data
    return render_template('allVideotheque.html', data=data)

@app.route('/select_videotheque/<videotheque>')
def select_videotheque(videotheque=''):
    global videotheques
    global selected_videotheque

    if(videotheque in videotheques):
        selected_videotheque = videotheque
    return redirect(url_for('home', filename=videotheque))


@app.route('/deletevideotheque/<filename>')
def deletevideotheque(filename):
    #print('filename: ',filename)
    r = requests.delete('http://127.0.0.1:5001/api/deleteVideotheque/'+filename)
    #print('r--->:',r)
    return redirect(url_for('getAllVideotheque'))

@app.route('/deletemovie/<filename>/<titre>')
def deletemovie(filename, titre):
    #print('filename: ', filename)
    #print('titre: ', titre)
    r = requests.delete('http://127.0.0.1:5001/api/deleteMovie/' + filename+ '/' + titre)
    #print('r--->:',r)
    return redirect(url_for('home', filename=filename))


@app.route('/updatemovie/<filename>/<titre>', methods=['GET','POST'])
def updatemovie(filename='test', titre='test'):
    print('filename: ', filename)
    print('titre: ', titre)
    payload = {
        'ntitre': request.form['ntitre'], 
        'nannee': request.form['nannee'], 
        'nnomR': request.form['nnomR'], 
        'nprenomR': request.form['nprenomR']
    }
    print('payload----->:',payload)
    url='http://127.0.0.1:5001/api/updateMovie/'+filename+'/'+titre
    print('url-->',url)
    r = requests.post(url, data = payload)
    print('r--->:',r.content)
    return redirect(url_for('home', filename=filename))
