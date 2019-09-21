# coding: utf-8
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    

    @app.route("/")
    def ola_bolinhas():
        return "Hello World! ",200


    return app