import socketio
import subprocess
import platform
import time

# asyncio
sio = socketio.Client()

@sio.event(namespace='/win')
def connect():
    print("I'm connected!")

@sio.event(namespace='/win')
def connect_error(data):
    print("The connection failed!")

@sio.event(namespace='/win')
def disconnect():
    print("I'm disconnected!")


@sio.event(namespace='/win')
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

def main():
    while True:
        try: 
            time.sleep(1)
            sio.connect('http://192.168.0.180:5000', namespaces=["/win"])
            sio.wait()
        except KeyboardInterrupt:
            sio.disconnect()
            break
        finally:
            print("keine Verbindung")

if __name__ == '__main__':
    main()
