import json
import os
import sys
from functools import partial

from flask import Flask, render_template, request, jsonify

ROUTES = dict()
def route(route=None):
    def subfunc(func):
        ROUTES[route] = func
        return func
    return subfunc


class Server(Flask):


    def __init__(self, database, *args, **kwargs):

        if not args:
            kwargs.setdefault('import_name', __name__)

        Flask.__init__(self, *args, **kwargs)

        for route, func in ROUTES.items():
            part_func = partial(func, self)
            part_func.__name__ = func.__name__
            self.route(route)(part_func)

        self.__database = database

    @route('/')
    def index(self):
        return render_template('index.html')
    
    @route('/data/<string:symbol>')
    def get_stock(self, symbol):

        return jsonify(self.__database.get_stock(symbol))
