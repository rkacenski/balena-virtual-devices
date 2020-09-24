# Details

WIP... Simple interface to run BalenaOS and attach to a application on BalenaCloud. Allowing you to create virtual devices in your application. Super helpful for end-to-end testing. Still need to add the UI and other endpoints.

## Getting Started
1. Download your config.json from BalenaCloud and add to the root of this project
2. set balena/aufs2overlay.sh to executable `chmod +x aufs2overlay.sh`
3. `docker-compose -f dev.yml build --no-cache` (rebuild also when you install new packages)
3. `docker-compose -f dev.yml up`
4. Endpoint available at localhost:5000


### Docker API
We can access the docker socket by using a volume mount on the api container. To learn more about this reference: https://medium.com/better-programming/about-var-run-docker-sock-3bfd276e12fd

### ToDo

#### Frontend
 - [x] Create base frontend (list devices, and app configs)
 - [x] Add a app config ui
 - [x] Add a device
 - [ ] Change status of the device (start, stop, delete)
 - [ ] Loaders for api calls when adding

#### API
 - [x] Save app config to disk
 - [ ] Copy and edit app config for creating a device
 - [ ] Separate routes to multi files with Blueprints
 - [ ] Start and stop devices


### Helpful hints

Basic api in python 
- https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
- https://smirnov-am.github.io/running-flask-in-production-with-docker/
