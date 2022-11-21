from re import search
from flask import Flask, flash, redirect, render_template, request, jsonify, make_response, session, url_for
from flask_mysqldb import MySQL
import yaml
import numpy as np
import keras
from keras.preprocessing import image
import json
from json import JSONEncoder
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import random
from flask_bcrypt import bcrypt
import pandas as pd
from PIL import Image

app = Flask(__name__)

# model = keras.models.load_model('model_v1.h5')

# class NumpyArrayEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return JSONEncoder.default(self, obj)

# def predict_image(path):
#     img = image.load_img(path, target_size=(224, 224))
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     images = np.vstack([x])
#     classes = model.predict(images, batch_size=32)
#     return classes

# def dictionary(result):
#     if result[0][0] == 1:
#         return {"result":"narrow brown spot"}
#     if result[0][1] == 1:
#         return {"result":"brown spot"}
#     if result[0][2] == 1:
#         return {"result":"healthy"}
#     if result[0][3] == 1:
#         return {"result":"backterial leaf blight"}
#     if result[0][4] == 1:
#         return {"result":"leaf blast"}
#     if result[0][5] == 1:
#         return {"result":"leaf scald"}

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
            "SELECT username FROM users WHERE username = %s", [username])
        if validateUsername > 0:
            return jsonify({"message": "Username already exists"})

        # hashed_password = Bcrypt.generate_password_hash('qwerty',passwordstring)

        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)",
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
        curl.execute("SELECT * FROM users WHERE username = %s", (username,))
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
        try:
            jeniskopi = request.form['addname']
            harga = request.form['addprice']
            jumlah = request.form['addquantity']

            if jeniskopi == "":
                return "Jenis Kopi tidak boleh kosong"
            elif harga == "":
                return "Harga tidak boleh kosong"
            elif jumlah == "":
                return "Jumlah tidak boleh kosong"

            
            if request.method == 'POST':
                mycursor = mysql.connection.cursor()
                # mycursor.execute(
                #     "SELECT COUNT(1) FROM hasil_panen WHERE product_name = %s;", [jeniskopi])
                # if mycursor.fetchone()[0]:
                #     return "Jenis Kopi sudah ada"
                # else:
                mycursor.execute(
                    "INSERT INTO hasil_panen(jenis_kopi, harga, kuantitas) Values(%s,%s,%s)", (jeniskopi, harga, jumlah))
                mysql.connection.commit()
                mycursor.close()
                flash(jeniskopi + ', ' + harga + ', ' +
                      jumlah + ', Successfully saved!')
                return "Success add data"
            else:
                return "Method undefined"
        except Exception as e:
            flash(e)
            return JSONEncoder(
                            data={
                                "message": "Failed to add data",
                                "error": e    })



@app.route('/pencatatan/search', methods=['POST'])
def search():

    try:
        jeniskopi = request.form['carikopi']
        if jeniskopi == "":
            flash('Harap isi kolom pencarian ')
            return render_template('index.html')
        else:
            if request.method == 'POST':
                mycursor = mysql.connection.cursor()
                if request.method == 'POST':
                    mycursor.execute(
                        "SELECT COUNT(1) FROM hasil_panen WHERE product_name = %s;", [jeniskopi])
                    if mycursor.fetchone()[0]:
                        mycursor.execute(
                            "SELECT * FROM hasil_panen WHERE product_name = %s;", [jeniskopi])
                        prod = mycursor.fetchall()
                        flash(jeniskopi + ' Ditemukan!')
                        return render_template('index.html', jeniskopis=prod)
                    else:
                        flash('Tidak ada jenis kopi tersebut ' + jeniskopi)
                    return render_template('index.html')
                else:
                    flash('Tidak ada jenis kopi tersebut ' + jeniskopi)
                    return render_template('index.html')
            else:
                return render_template('index.html')

    except Exception as e:
        flash(e)
        return render_template('index.html')


@app.route('/pencatatan/delete', methods=['POST'])
def delete():
    try:
        namee = request.form['prodsname']
        if namee == "":
            return render_template('index.html')
        else:
            if request.method == 'POST':
                mycursor = mysql.connection.cursor()
                if request.method == 'POST':
                    mycursor.execute(
                        "SELECT COUNT(1) FROM hasil_panen WHERE product_name = %s;", [namee])
                    if mycursor.fetchone()[0]:
                        mycursor.execute(
                            "DELETE FROM hasil_panen WHERE product_name = %s;", [namee])
                        mycursor.commit()
                        mycursor.close()
                        mycursor.close()
                        flash('Berhasil Menghapus!')
                        return render_template('index.html')
                    else:
                        flash(
                            'Product ' + request.form['prodsname'] + 'Tidak ada dalam list')
        return render_template('index.html')
    except Exception as e:
        flash(e)
        return render_template('index.html')


@app.route('/pencatatan/update', methods=['POST'])
def update():
    try:
       name_prod = request.form['namess']
       price = request.form['pricee']
       quantt = request.form['quantityy']
       if name_prod == "":
           return render_template('index.html')
       elif price == "":
           return render_template('index.html')
       elif quantt == "":
           return render_template('index.html')
       else:
           if request.method == 'POST':
               mycursor = mysql.connection.cursor()
               if request.method == 'POST':
                   mycursor.execute(
                       "SELECT COUNT(1) FROM hasil_panen WHERE product_name = %s;", [name_prod])
                   if mycursor.fetchone()[0]:
                       mycursor.execute(
                           "SELECT * FROM hasil_panen WHERE product_name = %s;", [name_prod])
                       produ = mycursor.fetchall()
                       flash(name_prod + ' Ditemukan!')
                       for row in produ:
                           b = row[3]
                           if int(b)+int(quantt) < 0:
                               flash('Tidak cukup')
                               return render_template('index.html')
                           else:
                               sum = int(b) + int(quantt)
                               mycursor.execute("UPDATE hasil_panen SET price='" + price + "' , quantity='" + str(
                                   sum) + "' WHERE product_name='" + name_prod + "'")
                               mycursor.commit()
                               mycursor.close()
                               mycursor.close()
                               flash('Berhasil Diupdate')
                               return render_template('index.html')
                   else:
                       flash('Tidak ada jenis kopi tersebut ' + name_prod)
                   return render_template('index.html')
    except Exception as e:
        flash(e)
        return render_template('index.html')

        
# @app.route("/penyakit", methods=['POST'])
# def predict():
#     if request.method == 'POST':
#         penyakitDetails = request.form
#         latitude = penyakitDetails['latitude']
#         longitude = penyakitDetails['longitude']
#         img = request.files['image']
#         createdAt = datetime.now()
#         updatedAt = datetime.now()

#         splitfile = os.path.splitext(img.filename)
#         fileName = splitfile[0] + str(random.randint(1,1000)) + splitfile[1]
#         img.save("./static/" + fileName)
#         url = os.path.join('static/', fileName)
#         img_path = url

#         p = predict_image(img_path)
#         print(p)
#         result = dictionary(p)

#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO penyakits(indikasi, latitude, longitude, createdAt, updatedAt, image, url) VALUES (%s, %s, %s, %s, %s, %s, %s)", (result['result'], latitude, longitude, createdAt, updatedAt, fileName, url))
#         mysql.connection.commit()
#         cur.close()
#         return {
#             "status": 200,
#             "message": "Penyakit berhasil diprediksi",
#             "data": result
#         }

# # @app.route("/penyakit/<int:id_penyakit>", methods=['PUT'])
# # def update(id_penyakit):
# #     if request.method == 'PUT':
# #         cur = mysql.connection.cursor()
# #         searchpenyakit = cur.execute(
# #             "SELECT * FROM penyakits WHERE id_penyakit = {}".format(id_penyakit))
# #         row_headers = [x[0] for x in cur.description]
# #         if (searchpenyakit > 0):
# #             penyakit = cur.fetchall()
# #             json_data = []
# #             for result in penyakit:
# #                 json_data.append(dict(zip(row_headers, result)))
# #             # return jsonify(json_data)
# #             if (request.files['image'].filename == ''):
# #                 fileName = json_data[0]['image']
# #             else:
# #                 img = request.files['image']
# #                 os.remove("./static/" + json_data[0]['image'])
# #                 splitfile = os.path.splitext(img.filename)
# #                 fileName = splitfile[0] + \
# #                     str(random.randint(1, 1000)) + splitfile[1]
# #                 img.save("./static/" + fileName)

#             penyakitDetails = request.form
#             latitude = penyakitDetails['latitude']
#             longitude = penyakitDetails['longitude']
#             createdAt = json_data[0]['createdAt']
#             updatedAt = datetime.now()

#             url = os.path.join('static/', fileName)
#             img_path = url

#             p = predict_image(img_path)
#             print(p)
#             result = dictionary(p)

##              cur = mysql.connection.cursor()
#             cur.execute("UPDATE penyakits SET indikasi=%s, latitude=%s, longitude=%s, createdAt=%s, updatedAt=%s, image=%s, url=%s WHERE id_penyakit=%s",
#                         (result['result'], latitude, longitude, createdAt, updatedAt, fileName, url, id_penyakit))
##              mysql.connection.commit()
#             cur.close()
#             return {
#                 "status": 204,
#                 "message": "Penyakit berhasil perbarui",
#                 "data": result
#             }

#         else:
#             return "penyakit not found"


##  @app.route('/penyakit', methods=['GET'])
# def get_penyakit():
#     cur = mysql.connection.cursor()
#     result = cur.execute("SELECT * FROM penyakits AS result")
##      row_headers = [x[0] for x in cur.description]
#     if result > 0:
#         penyakitDetails = cur.fetchall()
#         json_data = []
#         for result in penyakitDetails:
#             json_data.append(dict(zip(row_headers, result)))
#         return jsonify(json_data)
#         # return {
#         #     "status": 200,
#         #     "message": "Penyakit ditemukan",
#         #     "data": penyakitDetails
#         # }
#     return result


# @app.route('/penyakit/<int:id_penyakit>', methods=['GET'])
# def get_penyakit_by_id(id_penyakit):
#     cur = mysql.connection.cursor()
#     result = cur.execute(
#         "SELECT * FROM penyakits WHERE id_penyakit = {}".format(id_penyakit))
#     row_headers = [x[0] for x in cur.description]
#     if result > 0:
#         penyakitDetails = cur.fetchall()
#         json_data = []
#         for result in penyakitDetails:
#             json_data.append(dict(zip(row_headers, result)))

#     return jsonify(json_data)
#     # return {
#     #         "status": 200,
#     #         "message": "Penyakit ditemukan",
#     #         "data": data
#     #     }


# @app.route('/penyakit/<int:id_penyakit>', methods=['DELETE'])
# def delete(id_penyakit):
#     cur = mysql.connection.cursor()
#     searchpenyakit = cur.execute(
#         "SELECT * FROM penyakits WHERE id_penyakit = {}".format(id_penyakit))
#     row_headers = [x[0] for x in cur.description]
#     if (searchpenyakit > 0):
#         penyakit = cur.fetchall()
#         json_data = []
#         for result in penyakit:
#             json_data.append(dict(zip(row_headers, result)))
#     else:
#         return {
#             "status": 400,
#             "message": "Penyakit tidak ditemukan"
#         }

#     os.remove("./static/" + json_data[0]['image'])
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM penyakits WHERE id_penyakit={}".format(id_penyakit))
#     mysql.connection.commit()
#     cur.close()

#     return {
#         "status": 200,
#         "message": "Penyakit dihapus",
#     }


if __name__ == '__main__':
    app.secret_key = 'qwerty'
    app.run(host='0.0.0.0', port=5000)
