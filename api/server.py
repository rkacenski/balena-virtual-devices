# import ptvsd
# ptvsd.enable_attach(address=('0.0.0.0', 6001))

from flask import Flask, request, jsonify
app = Flask(__name__)

app.config['DEBUG'] = True


import docker
client = docker.from_env()

import os
host_path = os.environ['DOCKER_HOST_PATH']

@app.route('/')
def status():
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
@app.route('/stop/<string:id>')
def stop(id):
    container = client.containers.get(id)
    container.stop()
    return 'stopped: ' + id


@app.route('/create/<string:container_name>')
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
    config_json = f'{host_path}/config.json'

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

    

if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )