import paho.mqtt.client as paho
import sys
import json
import os

class Package:
    def __init__(self, package_id):
        self.package_id = package_id
        self.tracking_session = TrackingSession(package_id)
        self.connector = Connector()
        self.mobile_app = MobileApp()


listOC = []
listSession = []

def initalistion(package_id):
    global listOC
    global listSession
    myObect = ObjectConnecte(package_id)
    session = TrackingSession(package_id)
    listOC.append(myObect)
    listSession.append(session)

class ObjectConnecte:
    def __init__(self, package_id):
        self.package_id = package_id
        self.tracking_session = TrackingSession(package_id)
        #self.connector = Connector()
        #self.mobile_app = MobileApp()

class TrackingSession:
    def __init__(self, package_id):
        # Create a new tracking session for the given package
        self.package_id = package_id
        self.server.create_tracking_session(package_id)
    
    def update(self, location):
        # Update the tracking session with the latest location information
        self.server.update_tracking_session(self.package_id, location)
    
    def close(self):
        # Close the tracking session and archive the data
        self.server.close_tracking_session(self.package_id)

class Server:
    def create_tracking_session(self, package_id):
        # Create a new tracking session for the package in the database
        tracking_session = TrackingSession(package_id)
        self.db.add(tracking_session)
    
    def update_tracking_session(self, package_id, location):
        # Update the tracking session with the latest location information
        tracking_session = self.db.get(package_id)
        tracking_session.update(location)
    
    def close_tracking_session(self, package_id):
        # Close the tracking session and archive the data
        tracking_session = self.db.get(package_id)
        tracking_session.close()
        self.db.remove(tracking_session)

def onMessage(client, userdata, msg):
    #print(msg.topic + ': ' + msg.payload.decode())
    mon_topic=msg.topic
    message=msg.payload.decode()
    if msg.topic == 'UProd':
        data_load = json.loads(message)
        print('Nouveau coli: ', message)
        add_sessions(data_load)
        print('id coli: ', data_load['id'])
        print('location coli: ', data_load['location'])
    if msg.topic == 'en01':
        data_load = json.loads(message)
        update_session(data_load['id'], data_load['location'])
    if msg.topic == 'en02':
        data_load = json.loads(message)
        update_session(data_load['id'], data_load['location'])
    if msg.topic == 'en03':
        data_load = json.loads(message)
        update_session(data_load['id'], data_load['location'])
    if msg.topic == 'endSession':
        print('typeDara:',type(message))
        convertData=int(message)
        print('typeDara---->:',type(convertData))
        delete_session(convertData)
        print('Coli dans: ', convertData)

def tostart():
    createDatabase()
    client = paho.Client()
    client.on_message = onMessage
    if client.connect('127.0.0.1', 5000, 60) != 0:
        print('Could no connect to MQTT Broker')
        sys.exit(-1)
    
    client.subscribe('UProd')
    client.subscribe('en01')
    client.subscribe('en02')
    client.subscribe('en03')
    client.subscribe('endSession')


    try:
        print('Press CTRL to exit...')
        client.loop_forever()
    except:
        print('Disconnecting from broker')
    
    
    client.disconnect()

def createDatabase():
    try:
        isExist = os.path.exists('database/sessions.json')
        if not isExist:
            data = {'sessions': []}
            with open('database/sessions.json', 'w') as f:
                json.dump(data, f, indent=4)
    except Exception as e:
        print(e)

def add_sessions(data):
    with open('database/sessions.json', 'r') as f:
        all_data = json.load(f)

    all_sessions = all_data['sessions']
    all_sessions.append(data)
    #all_sessions += data

    with open('database/sessions.json', 'w') as f:
        json.dump(all_data, f, indent=4)

def update_session(id, location):
    with open('database/sessions.json', 'r') as f:
        all_data = json.load(f)
    
    all_sessions = all_data['sessions']
    sessionfound = [i for i in all_sessions if i['id'] == id][0]
    sessionfound['location'] = location

    with open('database/sessions.json', 'w') as f:
        json.dump(all_data, f, indent=4)

def delete_session(id: int):
    print('dans delete:',id)
    with open('database/sessions.json', 'r') as f:
        all_data = json.load(f)
    f.close()
    
    all_sessions = all_data['sessions']
    sessionfound = [i for i in all_sessions if not (i['id'] == id)]
    all_data['sessions'] = sessionfound

    print(sessionfound)

    with open('database/sessions.json', 'w') as f:
        json.dump(all_data, f, indent=4)


tostart()