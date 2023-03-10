from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_cors import CORS
import os
import json
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/createVideotheque", methods=['POST'])
def create_videotheque():
    try:
        #print(type(request))
        
        isExist = os.path.exists('videotheque/'+request.form['filename']+'.json')
        #print(isExist)
        if(isExist):
            data = {'Info': 'File already exists'}
            #return jsonify({'Info': 'File already exists!'})
            return Response('{"warning": "Videotheque already exists"}',status=400,mimetype="application/json")
            #return redirect('http://127.0.0.1:5000/')
        else:
            #print('----------------Isexist------------------------>:',isExist)
            filename = request.form['filename']
            prenomP = request.form['prenomP']
            nomP = request.form['nomP']
            items = {'proprietaire': {"nom": nomP, "prenom": prenomP}, 'films': []}
            with open(f'videotheque/{filename}.json', 'w') as f:
                json.dump(items, f, indent=4)
            # file = open(f'{filename}', 'w')
            # file.writelines(items)
            #dataL = sessionStorage.setItem('filename', filename)
            #print(dataL)
            #print('-------------------------------------------->:',filename)

            #return redirect('http://127.0.0.1:5000/home')
            #return jsonify({'Sucess': 'File Created and writed!'})
            return Response('{"success": "File created"}',status=201,mimetype="application/json")
    except Exception as e:
        return jsonify({'Error': 'Invalid request'})


@app.route("/api/deleteVideotheque/<filename>", methods=['DELETE'])
def delete_videotheque(filename):
    try:
        #filename = request.json['filename']
        os.remove('videotheque/'+filename)
        return Response('{"success": "File deleted successfully!"}',status=201,mimetype="application/json")
        #return "<p>File Deleted!</p>"
    except Exception as e:
        return jsonify({'Error': 'Invalid request'})


@app.route("/api/getAllMovies/<filename>", methods=['GET'])
def get_data(filename):
    with open(f'videotheque/{filename}', 'r') as f:
        data = json.load(f)
        #for i in data:
        #    print(i)
        #print(data)
        return Response(json.dumps(data), status=200, mimetype="application/json")


@app.route("/api/addFilms/<filename>", methods=['POST'])
def add_data(filename):
    try:
        acteurs = list(map(
            lambda fullName: get_person_infos_from_fullname(fullName),
            request.form['acteurs'].split('-')))
        
        titre = request.form['titre']
        annee = request.form['annee']
        nomR = request.form['nomR']
        prenomR = request.form['prenomR']
        #acteurs = request.json['acteurs']

        print('Mes acteurs---------->', acteurs)
        print('Type acteurs---------->', type(acteurs))
        
        with open(f'videotheque/{filename}', 'r') as f:
            data = json.load(f)
            #print(data['films'])

        listFilms = data['films']
        films = {
                    "titre": titre,
                    "annee": annee,
                    "realisateur": {"nom": nomR, "prenom": prenomR},
                    "acteurs": acteurs
        },
        
        listFilms += films

        with open(f'videotheque/{filename}', 'w') as f:
            json.dump(data, f, indent=4)

        return Response('{"success": "Movie added"}', status=201, mimetype="application/json")
    except Exception as e:
        #print(e)
        return jsonify({'Error': 'Invalid request'})


@app.route("/api/searchmovie/<filename>", methods=['POST'])
def found_movie(filename):
    try:
        movie = request.form['title']
        with open(f'videotheque/{filename}', 'r') as f:
            data = json.load(f)
        searchResultByTitle = [i for i in data['films'] if i['titre'] == movie][0]
        if searchResultByTitle:
            print('Case title')
            print(searchResultByTitle)
            return Response(json.dumps(searchResultByTitle), status=200, mimetype="application/json")
        else:
            searchResultByActor = [i for i in data['films'] if i['acteurs']['nom'] == movie][0]
            if searchResultByActor:
                print('Case actor')
                print(searchResultByActor)
                return Response(json.dumps(searchResultByActor), status=200, mimetype="application/json")
            else:
                print('No DATA...')
                return Response('{"Info": "No data!"}',status=404,mimetype="application/json")
                #return Response(json.dumps(searchResultByActor), status=200, mimetype="application/json")
    except Exception as e:
        return jsonify({'Error': 'Invalid request'})


@app.route("/api/searchmovieTest/<filename>", methods=['POST'])
def found_movie_test(filename):
    try:
        movie = request.form['title']
        print(movie)
        with open(f'videotheque/{filename}', 'r') as f:
            data = json.load(f)
        #searchResultByTitle = [i for i in data['films'] if i['titre'] == movie][0]
        testList = list(filter(lambda movieList: movieList['titre'] == movie, data['films']))
        
        if testList:
            print('Case title')
            return Response(json.dumps(testList), status=200, mimetype="application/json")
        if len(testList) == 0:
            #return Response('{"Info": "No data!"}',status=404,mimetype="application/json")
            films = data["films"]
            matching_films = []

            for film in films:
                for actor in film["acteurs"]:
                    if actor["nom"] == movie or actor["prenom"] == movie:
                        matching_films.append(film)
                        
            #return Response(json.dumps(matching_films), status=200, mimetype="application/json")
            if matching_films:
                return Response(json.dumps(matching_films), status=200, mimetype="application/json")
            else:
                print('No DATA...')
                return Response('{"Info": "No data!"}',status=404,mimetype="application/json")
                    #return Response(json.dumps(searchResultByActor), status=200, mimetype="application/json")
    except Exception as e:
        return jsonify({'Error': 'Invalid request'})



@app.route("/api/deleteMovie/<filename>/<titre>", methods=['DELETE'])
def delete_movie(filename, titre):
    print('filename: ', filename)
    print('titre: ', titre)
    try:
        #titre = request.json['titre']
        if titre != "":
            with open(f'videotheque/{filename}', 'r') as f:
                data = json.load(f)
            f.close()

            listFilms = data['films']

            deletedict = [i for i in listFilms if not (i['titre'] == titre)]

            data['films'] = deletedict

            print(deletedict)

            with open(f'videotheque/{filename}', 'w') as f:
                json.dump(data, f, indent=4)

            return Response('{"success": "Movie deleted"}', status=201, mimetype="application/json")
            #return jsonify({'Success': 'Movie deleted'})
        else:
            return jsonify({'Error': 'Champ ne doit pas ??tre vide'})
    except Exception as e:
        return jsonify({'Error': 'Invalid request'})


@app.route("/api/updateMovie/<filename>/<titre>", methods=['POST'])
def update_movie(filename, titre):
    print('filename: ', filename)
    print('titre: ', titre)
    try:
        #title = request.form['title']
        acteurs = list(map(
            lambda fullName: get_person_infos_from_fullname(fullName),
            request.form['acteurs'].split('-')))
        print('mesActeurs',acteurs)
        ntitre = request.form['ntitre']
        nannee = request.form['nannee']
        nnomR = request.form['nnomR']
        nprenomR = request.form['nprenomR']
        with open(f'videotheque/{filename}', 'r') as f:
            data = json.load(f)
        f.close()
        listFilms = data['films']
        datafound = [i for i in data['films'] if i['titre'] == titre][0]
        datafound['titre'] = ntitre
        datafound['annee'] = nannee
        datafound['realisateur']['nom'] = nnomR
        datafound['realisateur']['prenom'] = nprenomR
        datafound['acteurs']=acteurs

        with open(f'videotheque/{filename}', 'w') as f:
            json.dump(data, f, indent=4)

        #return datafound
        return Response('{"success": "Movie updated successfully!"}',status=201,mimetype="application/json")
    except Exception as e:
        return Response('{"Error": "Invalid request!"}',status=404,mimetype="application/json")
        #return jsonify({'Error': 'Invalid request'})


@app.route("/api/getAllVideotheque", methods=['GET'])
def getallvideotheque():
    try:
        videotheques = os.listdir('videotheque')
        return Response(json.dumps(videotheques), status=200, mimetype="application/json")
    except Exception as e:
        return jsonify({'Error': 'Invalid request'})


def get_person_infos_from_fullname(fullname:str):
    firstName, lastname = fullname.split(' ')
    return {'nom': lastname, 'prenom': firstName}


if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=int('5001'))