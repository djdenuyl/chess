"""
Created on %(date)s

@author: David den Uyl (ddenuyl@bebr.nl)
"""
from app import App
from os import environ


app = App().dash


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(environ.get("PORT", 8080)))
