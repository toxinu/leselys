# -*- coding: utf-8 -*-
import hashlib
from getpass import getpass


def get_users(storage):
    return storage.get_users()


def add_user(storage):
    username = raw_input('Username: ')
    if username in get_users(storage):
        print('User already exists')
        exit(1)

    same_password = False
    while not same_password:
        password1 = getpass('Password (not showed): ')
        password2 = getpass('Password again: ')
        if password1 == password2:
            same_password = True
        else:
            print('Not same password')

    m = hashlib.md5()
    m.update(password1)
    password_md5 = m.hexdigest()

    storage.add_user(username, password_md5)
    print('User added.')
    exit(0)


def del_user(storage):
    username = raw_input('Username: ')
    if username not in get_users(storage):
        print('User not found.')
        exit(1)
    storage.remove_user(username)
    print('User removed.')
    exit(0)


def update_password(storage):
    username = raw_input('Username :')
    same_password = False
    while not same_password:
        password1 = getpass('Password (not showed): ')
        password2 = getpass('Password again: ')
        if password1 == password2:
            same_password = True
        else:
            print('Not same password')

    m = hashlib.md5()
    m.update(password1)
    password_md5 = m.hexdigest()
    storage.set_password(username, password_md5)
    print('Password updated.')
    exit(0)
