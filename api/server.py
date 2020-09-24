# import ptvsd
# ptvsd.enable_attach(address=('0.0.0.0', 6001))

from flask import Flask, request, jsonify
app = Flask(__name__)

# allow access to any origin
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# run in debug mode for now
app.config['DEBUG'] = True
#set uploads folder
app.config['UPLOAD_FOLDER'] = '/code/configs'


@app.route('/')
def status():
    return jsonify({
        'status': 'online'
    })


##
# Apps
# /       -> GET list of saved apps
# /add    -> POST saves uploaded config file 
##

@app.route('/apps')
def app_list():
    data = get_json_from_files('/code/configs/apps')
    return jsonify(data)

@app.route('/apps/add', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/apps', filename))
        return jsonify({'filename': filename})

##
# Devices
# /           -> GET all running docker containers
# /create     -> POST creates the new device vm and starts it
# /stop/<id>  -> GET stops a running container by id
##

import docker
client = docker.from_env()

import os
host_path = os.environ['DOCKER_HOST_PATH']

@app.route('/devices')
def devices():
    containers = client.containers.list(all=True)
    results = []
    for c in containers:
       results.append(
           {
               'id': c.short_id,
               'status': c.status,
               'name': c.name,
               'image': c.image.tags
           }
       )
    print(results)
    return jsonify(results)


@app.route('/devices/add', methods=['POST'])
def new_device():
    data = request.json
    if 'application' in data:
        config = open(data['application'])
        config = json.load(config)
        config['initialDeviceName'] = data['device_name']
        print(config)
        f = open('/code/configs/devices/'+data['device_name']+'.json', 'w+')
        f.write( json.dumps(config) )

        create(data['device_name'])

    return jsonify({'success':'true'})


def create(container_name):
    image = 'resin/resinos:2.54.2_rev1.dev-genericx86-64-ext'
    vols = createVolumes(image, container_name)

    container = client.containers.run(
        image,
        remove = True,
        privileged = True,
        environment = ['container=docker'],
        detach = True,
        dns = [ '127.0.0.2' ],
        name = f'balena_{container_name}',
        command = "sh -c '/aufs2overlay;exec /sbin/init'",
        volumes = {
                host_path+'/balena/systemd-watchdog.conf': {
                    'bind': '/etc/systemd/system.conf.d/watchdog.conf', 'mode': 'ro'
                },
                '/lib/modules': {
                    'bind': '/lib/modules', 'mode': 'ro'
                },
                host_path+'/balena/aufs2overlay.sh': {
                    'bind': '/aufs2overlay', 'mode': 'rw'
                },
                'balena-boot-'+container_name: {
                    'bind': '/mnt/boot', 'mode': 'rw'
                },
                'balena-state-'+container_name: {
                    'bind': '/mnt/state', 'mode': 'rw'
                },
                'balena-data-'+container_name: {
                    'bind': '/mnt/data', 'mode': 'rw'
                }
            }
    )

    print(container.logs())

    return jsonify(vols)

    

def createVolumes(image, container_name):
    config_json = f'{host_path}/api/configs/devices/{container_name}.json'

    #set the 3 volume names needed
    vols = [
        'balena-boot-'+container_name,
        'balena-state-'+container_name,
        'balena-data-'+container_name
    ]

    #find or create each
    for volume in vols:
        exists = True
        try:
            client.volumes.get(volume)
            print(f'INFO: Reusing {volume} docker volume')
        except:
            exists = False

        if not exists:
            #create the volume
            print(f'INFO: Creating {volume} volume')
            client.volumes.create(volume)
            #attach the os and the config to the volume
            print(f'INFO: Mount image and config to {volume}')
            client.containers.run(image,
                remove=True,
                command='cp /config.json /mnt/boot/config.json',
                volumes = {
                    volume: {
                        'bind': '/mnt/boot', 'mode': 'rw'
                    },
                    config_json: {
                        'bind': '/config.json', 'mode': 'rw'
                    },
                }
            )

    return vols

@app.route('/devices/stop/<string:id>')
def stop(id):
    container = client.containers.get(id)
    container.stop()
    return 'stopped: ' + id

##
# Helpers
##

import glob
import json

def get_json_from_files(json_dir_name):
    contents = []

    json_pattern = os.path.join(json_dir_name, '*.json')
    file_list = glob.glob(json_pattern)
    for file in file_list:
        f = json.load( open(file) )
        f['file_name'] = file
        contents.append( f )
    return contents

    

if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )