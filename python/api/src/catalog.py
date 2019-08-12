#!/usr/bin/env python3
"""
API GW with Swagger
- https://github.com/noirbizarre/flask-restplus
"""
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from factory import api


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

api.init_app(app)

app.run(debug=True)
