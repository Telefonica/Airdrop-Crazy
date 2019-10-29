from src import application, socketio
from utils.ngrok_detect import detect_ngrok


if __name__ == '__main__':
    try:
        detect_ngrok()
        socketio.run(application)
    except Exception as e:
        print("Error setting the server, ngrok may be down")
