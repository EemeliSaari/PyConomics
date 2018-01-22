import json
import os
import sys
import sqlite3
from functools import partial

from flask import Flask, jsonify, render_template, request, abort


ROUTES = dict()
def route(route=None):
    def subfunc(func):
        ROUTES[route] = func
        return func
    return subfunc


class Server(Flask):
    """Simple backend server inherited from Flask"""

    def __init__(self, database, *args, **kwargs):
        """
        Constructor for the class

        :param database: DataBase object
        """
        if not args:
            kwargs.setdefault('import_name', __name__)

        # Init the Flask app
        Flask.__init__(self, *args, **kwargs)

        # Map all the routes
        for route, func in ROUTES.items():
            part_func = partial(func, self)
            part_func.__name__ = func.__name__
            self.route(route)(part_func)

        self.__database = database

    @route('/')
    def index(self):
        """Renders the html page"""
        return render_template('index.html')
    
    @route('/data/<string:symbol>')
    def get_stock(self, symbol):
        """Returns symbols price date in json format"""
        try:
            return jsonify(self.__database.get_stock(symbol))
        except sqlite3.OperationalError:
            return abort(404)