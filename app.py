from re import search
from flask import Flask, flash, redirect, render_template, request, jsonify, make_response, session, url_for
from flask_mysqldb import MySQL
import yaml
import numpy as np
import keras
from keras.preprocessing import image
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
import json
from json import JSONEncoder
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import random
from flask_bcrypt import bcrypt
import pandas as pd
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

app.config['JSON_SORT_KEYS'] = False

mysql = MySQL(app)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # return render_template("register.html")

        cur = mysql.connection.cursor()
        userDetails = request.form
        username = userDetails['username']
        passwordstring = userDetails['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(passwordstring, bcrypt.gensalt())

        validateUsername = cur.execute(
            "SELECT username FROM user WHERE username = %s", [username])
        if validateUsername > 0:
            return jsonify({"message": "Username already exists"})

        # hashed_password = Bcrypt.generate_password_hash('qwerty',passwordstring)

        cur.execute("INSERT INTO user(username, password) VALUES(%s, %s)",
                    (username, hash_password))
        mysql.connection.commit()
        cur.close()
        return 'success'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = curl.fetchone()
        curl.close()

        if user is not None and len(user) > 0:
            if bcrypt.hashpw(password, user[2].encode('utf-8')) == user[2].encode('utf-8'):
                return "Success"
            else:
                return "Gagal, username dan password tidak cocok"
        else:
            return "Username tidak ditemukan"
    else:
        return "Method undefined"


@app.route('/pencatatan/insert', methods=['POST'])
def insert():
    # try:
    jeniskopi = request.form['addname']
    harga = request.form['addprice']
    jumlah = request.form['addquantity']
    waktu = datetime.now()

    if jeniskopi == "":
        return "Jenis Kopi tidak boleh kosong"
    elif harga == "":
        return "Harga tidak boleh kosong"
    elif jumlah == "":
        return "Jumlah tidak boleh kosong"
    elif waktu == "":
        return "Waktu tidak boleh kosong"

    if request.method == 'POST':
        mycursor = mysql.connection.cursor()
        mycursor.execute(
            "SELECT COUNT(1) FROM hasil_panen WHERE jenis_kopi = %s;", [jeniskopi])
        if mycursor.fetchone()[0]:
            return "Jenis Kopi sudah ada"
        else:
            mycursor.execute(
                "INSERT INTO hasil_panen(jenis_kopi, harga, kuantitas, waktu) Values(%s,%s,%s,%s)", (jeniskopi, harga, jumlah, waktu))
            mysql.connection.commit()
            mycursor.close()
            flash(jeniskopi + ', ' + harga + ', ' +
                  jumlah + ',' + str(waktu) + ' Successfully saved!')
            return "Success add data"
    else:
        return "Method undefined"

        # except Exception as e:
        #     flash(e)
        #     return JSONEncoder(
        #                     data={
        #                         "message": "Failed to add data",
        #                         "error": e    })


@app.route('/pencatatan/search', methods=['POST'])
def search():

    # try:
    jeniskopi = request.form['carikopi']
    if jeniskopi == "":
        # flash('Harap isi kolom pencarian ')
        return "Harap isi kolom pencarian"
    else:
        if request.method == 'POST':
            mycursor = mysql.connection.cursor()
            if request.method == 'POST':
                mycursor.execute(
                    "SELECT COUNT(1) FROM hasil_panen WHERE jenis_kopi = %s;", [jeniskopi])
                if mycursor.fetchone()[0]:
                    mycursor.execute(
                        "SELECT * FROM hasil_panen WHERE jenis_kopi = %s;", [jeniskopi])
                    prod = mycursor.fetchall()
                    flash(jeniskopi + ' Ditemukan!')
                    return "Ditemukan"
                else:
                    flash('Tidak ada jenis kopi tersebut ' + jeniskopi)
                return "Tidak ada jenis kopi tersebut"
            else:
                flash('Tidak ada jenis kopi tersebut ' + jeniskopi)
                return 'tidak ada jenis kopi tersebut'
        else:
            return 'Method undefined'

    # except Exception as e:
    #     flash(e)
    #     return render_template('index.html')


@app.route('/pencatatan/delete', methods=['DELETE'])
def delete():
    # try:
    jeniskopi = request.form['prodsname']
    if jeniskopi == "":
        return "Harap isi kolom penghapusan"
    else:
        if request.method == 'DELETE':
            mycursor = mysql.connection.cursor()
            if request.method == 'DELETE':
                mycursor.execute(
                    "SELECT COUNT(1) FROM hasil_panen WHERE jenis_kopi = %s;", [jeniskopi])
                if mycursor.fetchone()[0]:
                    mycursor.execute(
                        "DELETE FROM hasil_panen WHERE jenis_kopi = %s;", [jeniskopi])
                    mysql.connection.commit()
                    mycursor.close()
                    flash('Berhasil Menghapus!')
                    return 'Berhasil Menghapus!'
                else:
                    flash(
                        'Jenis Kopi' + request.form['prodsname'] + 'Tidak ada dalam list')
    return 'Method undefined'
    # except Exception as e:
    #     flash(e)
    #     return render_template('index.html')


@app.route('/pencatatan/update', methods=['PUT'])
def update():
    # try:
    jeniskopi = request.form['addname']
    harga = request.form['addprice']
    jumlah = request.form['addquantity']
    timee = datetime.now()

    if jeniskopi == "":
        return 'Jenis kopi tidak boleh kosong'
    elif harga == "":
        return "Harga tidak boleh kosong"
    elif jumlah == "":
        return "Jumlah tidak boleh kosong"
    elif timee == "":
        return "Waktu tidak boleh kosong"
    else:
        if request.method == 'PUT':
            mycursor = mysql.connection.cursor()
            if request.method == 'PUT':
                mycursor.execute(
                    "SELECT COUNT(1) FROM hasil_panen WHERE jenis_kopi = %s;", [jeniskopi])
                if mycursor.fetchone()[0]:
                    mycursor.execute(
                        "SELECT * FROM hasil_panen WHERE jenis_kopi = %s;", [jeniskopi])
                    produ = mycursor.fetchall()
                    print(produ)
                    flash(jeniskopi + ' Ditemukan!')
                    for row in produ:
                        b = row[0]
                        if int(b)+int(jumlah) < 0:
                            flash('Tidak cukup')
                            return 'Tidak cukup'
                        else:
                            sum = int(b) + int(jumlah)
                            mycursor.execute("UPDATE hasil_panen SET harga='" + harga + "' , kuantitas ='" +
                                             jumlah + "' , waktu ='" + str(timee) + "' WHERE jenis_kopi='" + jeniskopi + "'")
                            mysql.connection.commit()
                            mycursor.close()
                            mycursor.close()
                            flash('Berhasil Diupdate')
                            return 'Berhasil di Update'
                else:
                    flash('Tidak ada jenis kopi tersebut ' + jeniskopi)
                return 'Tidak ada jenis kopi tersebut '
    # except Exception as e:
    #     flash(e)
    #     return render_template('index.html')


# LOAD MODEL

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test the model on random input data.
input_shape = input_details[0]['shape']
input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)

# predicting images

def predict_image(path):
    img = load_img(path, target_size=(256, 256))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    prediction = np.argmax(output_data)
    return prediction

def dictionary(prediction):
    if prediction == 0:
        return {"nama_penyakit" :"Healthy",
                "ciri": "Healthy",
                "deskripsi": "blablablalblab",
                "penanganan": "nananana"
                }
    elif prediction == 1:
        return {"nama_penyakit" :"Miner",
                "ciri": "Miner",
                "deskripsi": "blablablalblab",
                "penanganan": "nananana"
                }
    elif prediction == 2:
        return {"nama_penyakit" :"Phoma",
                "ciri": "Phoma",
                "deskripsi": "blablablalblab",
                "penanganan": "nananana"
        }
    else:
        return {
            "nama_penyakit": "Rust",
            "ciri": "Rust",
            "deskripsi": "blablablalblab",
            "penanganan" : "nananana"
        }


# untuk menambahkan data
@app.route("/penyakit", methods=['POST'])
def predict():
    if request.method == 'POST':
        penyakitDetails = request.form
        latitude = penyakitDetails['latitude']
        longitude = penyakitDetails['longitude']
        img = request.files['image']

        splitfile = os.path.splitext(img.filename)
        fileName = splitfile[0] + str(random.randint(1, 1000)) + splitfile[1]
        img.save("./static/" + fileName)
        url = os.path.join('static/', fileName)
        img_path = url

        p = predict_image(img_path)
        print(p)
        result = dictionary(p)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO penyakit(nama_penyakit, ciri, deskripsi, penanganan, latitude, longitude,  image, url) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)",
                    (result['nama_penyakit'], result['ciri'], result['deskripsi'], result['penanganan'], latitude, longitude, fileName, url))
        mysql.connection.commit()
        cur.close()
        return {
            "status": 200,
            "message": "Penyakit berhasil diprediksi",
            "data": result
        }

# untuk mengupdate data
@app.route("/penyakit/<int:id_penyakit>", methods=['PUT'])
def updatee(id_penyakit):
    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        searchpenyakit = cur.execute(
            "SELECT * FROM penyakit WHERE id_penyakit = {}".format(id_penyakit))
        row_headers = [x[0] for x in cur.description]
        if (searchpenyakit > 0):
            penyakit = cur.fetchall()
            json_data = []
            for result in penyakit:
                json_data.append(dict(zip(row_headers, result)))
            # return jsonify(json_data)
            if (request.files['image'].filename == ''):
                fileName = json_data[0]['image']
            else:
                img = request.files['image']
                os.remove("./static/" + json_data[0]['image'])
                splitfile = os.path.splitext(img.filename)
                fileName = splitfile[0] + \
                    str(random.randint(1, 1000)) + splitfile[1]
                img.save("./static/" + fileName)

            penyakitDetails = request.form
            latitude = penyakitDetails['latitude']
            longitude = penyakitDetails['longitude']

            url = os.path.join('static/', fileName)
            img_path = url

            p = predict_image(img_path)
            print(p)
            result = dictionary(p)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE penyakit SET nama_penyakit=%s, ciri=%s, deskripsi=%s, penanganan=%s, latitude=%s, longitude=%s, image=%s, url=%s WHERE id_penyakit=%s",
                        (result['nama_penyakit'], result['ciri'], result['deskripsi'], result['penanganan'], latitude, longitude, fileName, url, id_penyakit))
            mysql.connection.commit()
            cur.close()
            return {
                "status": 204,
                "message": "Penyakit berhasil perbarui",
                "data": result
            }

        else:
            return "penyakit not found"


# untuk melihat semua data
@app.route('/penyakit', methods=['GET'])
def get_penyakit():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM penyakit AS result")
    row_headers = [x[0] for x in cur.description]
    if result > 0:
        penyakitDetails = cur.fetchall()
        json_data = []
        for result in penyakitDetails:
            json_data.append(dict(zip(row_headers, result)))
        return jsonify(json_data)
        # return {
        #     "status": 200,
        #     "message": "Penyakit ditemukan",
        #     "data": penyakitDetails
        # }
    return result


# untuk melihat data berdasarkan id
@app.route('/penyakit/<int:id_penyakit>', methods=['GET'])
def get_penyakit_by_id(id_penyakit):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM penyakit WHERE id_penyakit = {}".format(id_penyakit))
    row_headers = [x[0] for x in cur.description]
    if result > 0:
        penyakitDetails = cur.fetchall()
        json_data = []
        for result in penyakitDetails:
            json_data.append(dict(zip(row_headers, result)))

    return jsonify(json_data)
    # return {
    #         "status": 200,
    #         "message": "Penyakit ditemukan",
    #         "data": data
    #     }


# untuk menghapus data
@app.route('/penyakit/<int:id_penyakit>', methods=['DELETE'])
def deletee(id_penyakit):
    cur = mysql.connection.cursor()
    searchpenyakit = cur.execute(
        "SELECT * FROM penyakit WHERE id_penyakit = {}".format(id_penyakit))
    row_headers = [x[0] for x in cur.description]
    if (searchpenyakit > 0):
        penyakit = cur.fetchall()
        json_data = []
        for result in penyakit:
            json_data.append(dict(zip(row_headers, result)))
    else:
        return {
            "status": 400,
            "message": "Penyakit tidak ditemukan"
        }

    os.remove("./static/" + json_data[0]['image'])
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM penyakit WHERE id_penyakit={}".format(id_penyakit))
    mysql.connection.commit()
    cur.close()

    return {
        "status": 200,
        "message": "Penyakit dihapus",
    }


if __name__ == '__main__':
    app.secret_key = 'qwerty'
    app.run(host='0.0.0.0', port=5000)
