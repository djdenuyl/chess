"""
Main entrypoint for gunicorn

author: David den Uyl (djdenuyl@gmail.nl)
date: 2023-03-17
"""
from app import App
from os import environ


app = App().dash.server


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))
