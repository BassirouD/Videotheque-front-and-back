from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json
from itertools import starmap
import re

app = Flask(__name__)
app.secret_key='Secret Key'

films = []
videotheques = []
selected_videotheque = ''
dataMovies = []

@app.route('/')
def inscription():
    return render_template('inscription.html')

@app.route('/createVideo', methods=['POST'])
def createVideo():
    error = None
    if request.method=='POST':
        nom = request.form['nomP']
        prenom = request.form['prenomP']
        filename = request.form['filename']
        ifPatNom = check_regex(nom)
        ifPatprenom = check_regex(prenom)
        ifPatFileName = check_regex(filename)
        lenNom = len(nom)
        lenPrenom = len(prenom)
        lenFilename = len(filename)
        print(ifPatNom)
        payload = {'nomP': nom, 'prenomP': prenom, 'filename': filename}
        
        if ifPatNom & ifPatprenom & ifPatFileName:
            if nom and prenom and filename:
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
            else:
                flash('Les champs ne doivent pas etre vide', 'error')
                return redirect('/')
        else:
            flash('Les champs ne doivent pas contenir des caractères spéciaux', 'error')
            return redirect('/')
    #print('---------------------',r)
    #print('----------form-----------', form)
    #return redirect(url_for('home'))

@app.route('/home/<filename>')
def home(filename='test'):
    global films
    global selected_videotheque
    global dataMovies
    r = requests.get('http://127.0.0.1:5001/api/getAllMovies/'+filename)
    data = json.loads(r.content.decode())
    films = data['films']
    dataMovies = data
    data['selected_videotheque'] = selected_videotheque
    return render_template('home.html', data = data)



@app.route('/detailsfilm/<movieName>')
def detailsfilm(movieName):
    global selected_videotheque
    #print(selected_videotheque)
    for film in films:
        if film['titre'] == movieName:
            data={'film':film, 'selected_videotheque':selected_videotheque}
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

@app.route('/searchmovie/<filename>',methods=['POST'])
def searchmovie(filename='test',):
    global films
    global selected_videotheque
    global dataMovies
    title = request.form['title'],
    strTitle = ''.join(title)
    print('filename: ', filename)
    print('titre: ', title)
    print('strTitle: ', strTitle)
    print('type strTitle: ', type(strTitle))
    print('type titre: ', type(title))
    if strTitle:
        payload = {
            'title': strTitle, 
        }
        url='http://127.0.0.1:5001/api/searchmovieTest/'+filename
        r = requests.post(url, data=payload)
        data = json.loads(r.content.decode())
        print('--------statuis--->:', r.status_code)
        if r.status_code == 200:
            print(data)
            return render_template('search.html', data=data)
        if r.status_code == 404:
            print('--------------404----------------------', dataMovies)
            print('---------------ici--------------------')
            r = requests.get('http://127.0.0.1:5001/api/getAllMovies/'+filename)
            #data = json.loads(r.content.decode())
            #films = data['films']
            #data['selected_videotheque'] = selected_videotheque
            flash('No data found', 'error')
            return render_template('home.html', data = dataMovies)
    else:
        flash('Le champ ne doit pas être vide', 'info')
        return render_template('home.html', data = dataMovies)




def get_person_infos_from_tuple(list1, list2):
    for nom, prenom in zip(list1, list2):
        print('Daans function---->: ',nom, prenom)
    return {'nom': nom, 'prenom': prenom}


@app.route('/updatemovie/<filename>/<titre>', methods=['GET','POST'])
def updatemovie(filename='test', titre='test'):
    #print('filename: ', filename)
    #print('titre: ', titre)
    print('---------------------------------------')
    data=request.form
    listPrenomA=data.getlist('prenomA')
    listnomA=data.getlist('nomA')
    print(listnomA)
    print(listPrenomA)
    dic = {}
    maListActeur=[]
    mesActeurs=list(map(
        lambda l1, l2: zip(l1, l2),
        listnomA, listPrenomA
    ))
    for nom, prenom in zip(listnomA, listPrenomA):
       # print(nom, prenom)
        
        maListActeur.append(nom)
        maListActeur.append(prenom)
    
    maStr=' '.join(maListActeur)

    #acteurs=list(map(lambda l1, l2: get_person_infos_from_tuple(l1,l2),listnomA, listPrenomA))
    print(maListActeur)
    print('---------------------------------------------------------------------------------------------------------------------------------')
    payload = {
        'ntitre': request.form['ntitre'], 
        'nannee': request.form['nannee'], 
        'nnomR': request.form['nnomR'], 
        'nprenomR': request.form['nprenomR']
    }
    url = 'http://127.0.0.1:5001/api/updateMovie/'+filename+'/'+titre
    r = requests.post(url, data = payload)
    flash('Film modifié avec succès', 'success')
    return redirect(url_for('home', filename=filename))


def check_regex(entree: str):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(entree) == None):
        return True
    else:
        return False