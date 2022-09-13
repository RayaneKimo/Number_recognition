from flask import Flask, send_from_directory, render_template, request, url_for
from flask_restful import Api, Resource, reqparse, request
from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
import sklearn
import pickle
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import SubmitField
import base64
import cv2 as cv
import os
from PIL import Image
import numpy as np

# app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app=Flask(__name__)

CORS(app) #comment this on deployment
# api = Api(app)
svm_model = pickle.load(open('model_pkl',"rb"))
app.config['SECRET_KEY']='JKSDFKJBSDBKJSCCS'
app.config['UPLOADED_PHOTOS_DEST']="photos"
photos= UploadSet('photos',IMAGES)
configure_uploads(app,photos)

class UploadForm(FlaskForm):
    photo = FileField( 
        validators =[ 
            FileAllowed(photos, 'Only images are allowed'), 
            FileRequired("File field should not be empty")
            ]
            )
    submit = SubmitField('Upload')

def GaussianBlurGrisLvlReduct(image):
    image = cv.GaussianBlur(image,(7,7),0.2).astype(np.uint8)
    image = np.reshape(np.round(image*(3/255))*(255/3),(1,784))
    return image


@app.route('/photos/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)
 

@app.route('/', methods=['GET','POST'])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        filename=photos.save(form.photo.data)
        file_url= url_for('get_file', filename=filename) #1st name of the view #2nd filename
        # load_img_rz = np.array(Image.open(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)).resize((28, 28)))
        img = cv.imread(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
        img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        resized = np.array(cv.resize(img_gray, [28,28], interpolation=cv.INTER_AREA))
        resized=GaussianBlurGrisLvlReduct(resized)
        print(svm_model.predict(resized))
        data=file_url
    else :
        file_url = None
        data= None
    return render_template('home.html',form=form, file_url=file_url, data=data)

# @app.route('/SVM_api', methods=['POST'])
# def predict():
#  data=request.files.get("image","")
#  print(data)
# @app.route("/", defaults={'path':''})
# def serve(path):
#     return send_from_directory(app.static_folder,'index.html')

# @app.route('/upload', methods=['POST'])
# def fileUpload():
#     file = request.files['file']
#     response="Succesful upload"
#     return response

# api.add_resource(HelloApiHandler, '/flask/hello')

if __name__ =="__main__" :
    app.run(debug=True)