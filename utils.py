import cryptocode
import datetime

from models.User import User
from main import SUPERMEGASECRET

def create_user(data):
    room = cryptocode.encrypt(data["email"], SUPERMEGASECRET)

    return User(username=data["username"], email=data["email"],
                    password=data["password"], first_name=data["first_name"], last_name=data["last_name"], role=data["role"], room=room)


def decrypt_room(room):
    return cryptocode.decrypt(room, SUPERMEGASECRET)

def encrypt_room(room):
    return cryptocode.encrypt(room, SUPERMEGASECRET)

def date_converter(date):
    date = datetime.fromtimestamp(date)

    return date.strftime("%m/%d/%Y, %H:%M:%S")

def get_user_by_id(id):
    return User.query.filter_by(id=id).first()