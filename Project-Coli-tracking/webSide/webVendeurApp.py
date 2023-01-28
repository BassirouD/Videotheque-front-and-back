from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json
from itertools import starmap
import re

app = Flask(__name__)
app.secret_key='Secret Key'

host='http://10.0.3.207:9000/api'

@app.route('/')
def inscription():
    r = requests.get(host+'/getAllOC')
    data = json.loads(r.content.decode())
    print(data)
    return render_template('pagevendeur.html', data=data)


if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=int('5000'))
