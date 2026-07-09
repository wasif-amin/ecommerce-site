from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:21070212w@localhost:5432/ecommercesite'