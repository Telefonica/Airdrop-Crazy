from subprocess import Popen, PIPE
from time import sleep
import json
import qrcode


def create_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.show()

def detect_ngrok():
    r = Popen(["curl", "http://localhost:4040/api/tunnels"], stdout=PIPE, stderr=PIPE)
    try:
        output_raw = r.stdout.read().decode()
        output = json.loads(output_raw)
        url = output["tunnels"][0]["public_url"]
        create_qr(url)
    except Exception as e:
        print(e)
        raise