import socketio
import subprocess


# asyncio
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.event
def message(data):
    print('I received a message!', data)
    if data == "zoom":
        print("starte zoom")
        subprocess.call([r'C:\Users\nicow\AppData\Roaming\Zoom\bin\Zoom.exe'])
    elif data == "teams":
        print("starte teams")
        subprocess.call([r'msteams'])
        
if __name__ == '__main__':
    sio.connect('http://192.168.0.180:5000')

