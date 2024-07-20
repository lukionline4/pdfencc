from flask import Flask, request, jsonify, abort, render_template, redirect, url_for, session, send_file
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from Cryptodome.Cipher import AES
import base64
import os
import io
from bson import ObjectId

app = Flask(__name__)
app.config["SECRET_KEY"] = "pdfenc"  # Ganti dengan kunci rahasia Anda
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"  # Ganti dengan URI MongoDB Anda
mongo = PyMongo(app)

# Fungsi enkripsi dengan AES
def encrypt_file(file_data, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded_data = pad_data(file_data)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

# Fungsi dekripsi dengan AES
def decrypt_file(encrypted_data, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_data)
    return unpad_data(decrypted_data)

# Fungsi untuk padding data
def pad_data(data):
    block_size = AES.block_size
    padding_length = block_size - (len(data) % block_size)
    padded_data = data + bytes([padding_length] * padding_length)
    return padded_data

# Fungsi untuk menghilangkan padding data
def unpad_data(data):
    padding_length = data[-1]
    return data[:-padding_length]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = mongo.db.users.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return "Invalid username or password", 401

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if mongo.db.users.find_one({"username": username}):
            return "User already exists", 400

        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({"username": username, "password": hashed_password})
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/index")
def index():
    if "username" in session:
        return render_template("index.html")
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files.get("file")
        key = request.form.get("key")

        if not file or not key:
            return "File and key are required", 400

        file_data = file.read()
        encrypted_data = encrypt_file(file_data, key)
        mongo.db.files.insert_one({
            "username": session["username"],
            "filename": file.filename,
            "encrypted_file": base64.b64encode(encrypted_data).decode("utf-8")
        })

        encrypted_file_stream = io.BytesIO(encrypted_data)
        encrypted_file_stream.seek(0)

        return send_file(
            encrypted_file_stream,
            as_attachment=True,
            download_name=f"encrypted_{file.filename}"
        )
    
    return render_template("upload.html")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files.get("file")
        key = request.form.get("key")

        if not file or not key:
            return "File and key are required", 400

        encrypted_data = file.read()
        try:
            decrypted_data = decrypt_file(encrypted_data, key)
        except Exception as e:
            return f"Decryption failed: {str(e)}", 400

        decrypted_file_stream = io.BytesIO(decrypted_data)
        decrypted_file_stream.seek(0)

        return send_file(
            decrypted_file_stream,
            as_attachment=True,
            download_name=f"decrypted_{file.filename}"
        )
    
    return render_template("decrypt.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
