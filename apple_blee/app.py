# called application because gunicorn search application variable
from src import application

if __name__ == '__main__':
    application.run(threaded=True)