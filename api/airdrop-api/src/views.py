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
    country = request.args.get('country', '')
    db.create_all()
    if not (models.Phone.query.get(1)):
        try:
            choose_region(country)
            return jsonify({"ok": "Number created"})
        except:
            return jsonify(
                {"error": "Generation only supported for US and Spain"}
             )         
    return jsonify(
        {"error": "Database already created"}
    )


def choose_region(region):
    if(region == "us"):
        thread = Thread(target=generate_hashes_us) 
    elif(region == "es"):
        thread = Thread(target=generate_hashes_es) 
    else:
        raise Exception
    thread.start()
        

def generate_number(number):
    """Generate new entry with hash and number relationship
    
    Args:
        number (str): Phone number
    """
    hash = hashlib.sha256(number.encode()).hexdigest()
    phone = Phone(hash=hash, phone=number)
    db.session.add(phone)
    db.session.commit()


def generate_hashes_us():
    """Generate hashes from all the numbers of US
    """
    list_numbers = [209, 213, 279, 310, 323, 408, 415, 424, 442, 510, 530, 559, 562, 619, 626, 628, 650, 657, 661, 669, 707, 714, 747, 760, 805, 818, 820, 831, 858, 909, 916, 925, 949, 951, 479, 501, 870, 480, 520, 602, 623, 928, 907, 
    205, 251, 256, 334, 938, 303, 719, 720, 970, 203, 475, 860, 959, 302, 239, 305, 321, 352, 386, 407, 561, 727, 754, 772, 786, 813, 850, 863, 904, 941, 954, 229, 404, 470, 478, 678, 706, 762, 770, 912, 808, 208, 986, 217, 224, 309, 
    312, 331, 618, 630, 708, 773, 779, 815, 847, 872, 219, 260, 317, 463, 574, 765, 812, 930, 319, 515, 563, 641, 712, 316, 620, 785, 913, 270, 364, 502, 606, 859, 225, 318, 337, 504, 985, 207, 240, 301, 410, 443, 667, 339, 351, 413, 
    508, 617, 774, 781, 857, 978, 231, 248, 269, 313, 517, 586, 616, 734, 810, 906, 947, 989, 218, 320, 507, 612, 651, 763, 952, 228, 601, 662, 769, 314, 417, 573, 636, 660, 816, 406, 308, 402, 531, 702, 725, 775, 603, 201, 551, 609, 
    640, 732, 848, 856, 862, 908, 973, 212, 315, 332, 347, 516, 518, 585, 607, 631, 646, 680, 716, 718, 838, 845, 914, 917, 929, 934, 505, 575, 252, 336, 704, 743, 828, 910, 919, 980, 984, 701, 216, 220, 234, 330, 380, 419, 440, 513, 
    567, 614, 740, 937, 405, 539, 580, 918, 215, 223, 267, 272, 412, 445, 484, 570, 610, 717, 724, 814, 878, 458, 503, 541, 971, 401, 803, 843, 854, 864, 605, 423, 615, 629, 731, 865, 901, 931, 210, 214, 254, 281, 325, 346, 361, 409, 
    430, 432, 469, 512, 682, 713, 726, 737, 806, 817, 830, 832, 903, 915, 936, 940, 956, 972, 979, 385, 435, 801, 802, 276, 434, 540, 571, 703, 757, 804, 206, 253, 360, 425, 509, 564, 202, 262, 414, 534, 608, 715, 920, 304, 681, 307, 
    684, 671, 670, 787, 939, 340]
    for prefix in list_numbers:
        for number in range (0000000, 9999999):
            number = f"1{prefix}{number:07d}"
            generate_number(number)

def generate_hashes_es():
    """Generate hashes from all the numbers of Spain
    """
    for number in range (600000000, 799999999):
        number = f"34{number}"
        generate_number(number)