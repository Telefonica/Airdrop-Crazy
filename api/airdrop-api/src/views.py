# coding=utf-8
import hashlib
from src import app, jwt, db
from .models import Phone
from threading import Thread
from src import models
import time
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required


@app.route('/api/search', methods=['GET'])
@jwt_required
def get_results():
    hash = request.args.get('hash', '')
    phone = models.Phone.query.filter_by(hash=hash).first()
    result = phone.phone if phone else None
    response = {"phone": str(result)}

    return jsonify(
        response
    )

@app.route('/api/init', methods=['GET'])
@jwt_required
def populate_db():
    db.create_all()
    if not (models.Phone.query.get(1)):
        try:
            thread = Thread(target=generate_hashes) 
            thread.start()   
            return jsonify(
                {"ok": "Number created"}
            )
        except Exception as e:
            print(e)
            pass

    return jsonify(
        {"error": "Database already created"}
    )

def generate_number(number):
    hash = hashlib.sha256(number.encode()).hexdigest()
    phone = Phone(hash=hash, phone=number)
    db.session.add(phone)
    db.session.commit()


def generate_hashes():
    for x in range (600000000, 800000000):
        if((x % 20000000) == 0):
            print(f"{time.time()}, Number: {x}")
        number = f"34{x}"
        generate_number(number)