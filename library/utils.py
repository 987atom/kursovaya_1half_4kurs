from django.contrib.auth.hashers import check_password
from .models import Reader

def authenticate_reader(username, password):
    try:
        reader = Reader.objects.get(username=username)
        if reader.password == password:  # Сравниваем пароли в открытом виде
            return reader
    except Reader.DoesNotExist:
        return None
