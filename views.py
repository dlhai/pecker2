#encoding:utf8
import json
from model import *
from flask import Blueprint
main = Blueprint('main', __name__)
 
@main.route('/login')
def login():
    return '{"login":"sss","result":404}\n'

