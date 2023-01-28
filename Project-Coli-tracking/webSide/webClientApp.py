from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json
from itertools import starmap
import re

app = Flask(__name__)
app.secret_key='Secret Key'

host='http://10.0.3.207:9000/api'

@app.route('/',methods=['POST', 'GET'])
def getObjectByID():
    if request.method=='GET':
        return render_template('pageClient.html')

    if request.method=='POST':
        idu = request.form['id']
        idC = ''.join(idu)
        id = int(idC)
        print('id==============>:',id)
        print('type id==============>:', type(id))
        print('type idt==============>:', type(idC))
        payload = {
            'id': id,
        }
        r = requests.post(host+'/getOCByID',data=payload)
        data = json.loads(r.content.decode())
        print(data)
        print('type data', type(data))
        return render_template('pageClient.html', data=data)


if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=int('8000'))
