import socketio
import subprocess
import platform


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
        version = int(platform.version().split('.')[2])
        if(version >= 22621):
            subprocess.call(r'msteams')
        else:
            subprocess.call([r'C:\Users\nicow\AppData\Local\Microsoft\Teams\current\Teams.exe'])

if __name__ == '__main__':
    sio.connect('http://192.168.0.180:5000')

