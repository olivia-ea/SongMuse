"""Server"""

from views import app
from model import connect_to_db

if __name__ == '__main__':

    app.secret_key = 'SECRET'
    app.debug = True
    connect_to_db(app)
    app.run(host="0.0.0.0")
