from flask import Flask
import json
import base64
import os 
import uuid
import re
import numpy as np

from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    # import pdb ; pdb.set_trace()
    data = request.form

    trace_points = json.loads(data['path'])
    label = str( ((int(data['imgClass']) -1) % 20) + 1)
    # A life hack -- Strip the "geraba" before chewing the chat
    image = re.sub('^data:image/.+;base64,', '', data['img']).decode('base64') 

    ## check if directory exists 
    dir_ = 'images/{}/'.format(label)
    path_dir = 'paths/{}/'.format(label)
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    
    
    filename = str(uuid.uuid4())
    path_filename = str(uuid.uuid4())


    # Write the image to file 
    with open('{}{}.png'.format(dir_, filename), "w+") as f:
        f.write(image)
    
    # Write the path to file 
    with open('{}{}.npz'.format(path_dir, path_filename), 'w+') as f:
        np.save(f, np.array(trace_points))

    return 'Upload successful'