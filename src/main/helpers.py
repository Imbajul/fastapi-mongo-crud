import os
import hashlib
import models
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status

app_conf = models.AppSettings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def setup_data_dir():
    os.makedirs(app_conf.data_dir, exist_ok=True)

def hash_password(password):
    salt = b'some_random_salt'  
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed_password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

