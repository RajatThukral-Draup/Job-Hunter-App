from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
# from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime, date
from utils import extractPdfText
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)

MASTER_RESUME_NAMES = []
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'draup17*#IT'
app.config['MYSQL_DB'] = 'job_hunter_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
# mysql = MySQL(app)

# Index
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/uploader')
def uploader():
    return render_template('uploader.html')


@app.route('/questionnaire',methods=['GET'])
def questionnaire_resp():
    return render_template('/questionnaire.html')


@app.route('/analyzed_jobs')
def analyzed_jobs():
    if MASTER_RESUME_NAMES:
        resume_name = MASTER_RESUME_NAMES[-1]
    else:
        resume_name = '------.pdf'

    return render_template('jobs.html',resume_name=resume_name)

@app.route('/upload_resume',methods=['GET','POST'])
def uploading_resume():
    file_data = request.files['file']
    file_name = file_data.filename
    MASTER_RESUME_NAMES.append(file_name)
    extract_text = extractPdfText(fileObject=file_data)
    return render_template('/questionnaire.html')


@app.route('/upload_qa',methods=['GET','POST'])
def upload_qa():
    qa = request.form
    qa_responses = qa.to_dict(flat=False)['qa[]']
    qa_responses = [i.split('_')[-1] for i in qa_responses]

    return render_template('/questionnaire.html')

