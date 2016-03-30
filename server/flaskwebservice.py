#!/bin/usr/env python3
# -*- coding: utf-8 -*-
# -*- mode: python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://iqms:iqtest@iqtest'
db = SQLAlchemy(app)


class Arinvt(db.Model):
    # __table__ = db.Model.metadata.tables['arinvt']
    __table__ = 'arinvt'

    id = db.Column(db.Integer, primary_key=True)
    itemno = db.Column(db.String)
    descrip = db.Column(db.String)
