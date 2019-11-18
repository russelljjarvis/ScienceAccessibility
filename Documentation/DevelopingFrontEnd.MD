How to finish the tool as a dash web-app:

Move contents from website to your computer hard-drive.
```
git clone https://github.com/russelljjarvis/ScienceAccessibility.git
```
Navigate to the root directory of the Project:
```
cd ScienceAccessibility
```
Build the docker image instead of pulling it from a remote.
```
sudo docker build . -t dash_mode
```
Run what you buit:
```
docker run -p 8050:8050 dash_mode
```

Tweak the file:
```
ScienceAccessibility/OnlineApp/dash-asynchronous.py
```
Rebuild
```
sudo docker build . -t dash_mode
```
Run what you buit:
```
docker run -p 8050:8050 dash_mode
```
Test for desired output and if not desired output keep tweaking file.

Recommended, any easy to replicate minimal working example, that is a good foundation to build from.
https://arthought.com/dash-simple-deployment-with-docker/
