

### How to finish the tool as a dash web-app:

Move contents from website to your computer hard-drive.
```
git clone https://github.com/russelljjarvis/ScienceAccessibility.git
```

Navigate to the root directory of the Project:
```
cd ScienceAccessibility
```

# * ***1***: If I Change something on GitHub.
From inside the ScienceAccessibility directory you navigated to in the last step. Run ``` git pull origin master ``` This synchronize the website with your hard drive.

* caveat, if you have changed some file contents in the intervening time, Git wants to help you not to over write changes. 

Gits behavior assumes you never want to lose changes, but the messages it gives can be cryptic. To keep your changes and mine. Run `git add filename_you_changed_locall.py`, `git commit -m "message", `git pull origin master`, `git push origin master`

Over time you may want to sync your local code, with your own fork on Github, there are guides to help with this. Also there are Git GUIs that do all this command line busy work for you.

Build the docker image instead of pulling it from a remote.
```
sudo docker build . -t dash_mode
```
Run what you built:
```
docker run -p 8050:8050 dash_mode
```

Tweak [this file](https://github.com/russelljjarvis/ScienceAccessibility/blob/master/OnlineApp/dash-asynchronous.py) as it exists on your local hard drive remember the directory structure has been mapped faithfuly to your hard drive:
```
atom ScienceAccessibility/OnlineApp/dash-asynchronous.py
```
The link was not provided as an indication that you should edit the online file, it's provided as a navigation aid, as it's the file contents as they exist on your computer that we now care about.

Rebuild
```
sudo docker build . -t dash_mode
```
Run what you built:
```
docker run -p 8050:8050 dash_mode
```
Test for desired output and if not desired output keep tweaking file.

Recommended, any easy to replicate [minimal working example](https://arthought.com/dash-simple-deployment-with-docker/), that is a good foundation to build from.


You may also feel the need to tweak the last lines of [this file](https://github.com/russelljjarvis/ScienceAccessibility/blob/master/Dockerfile) as it exists on your local hard drive remember the directory structure has been mapped faithfuly to your hard drive:

When the app works move your changes back onto the website with:

```BASH
git add filename.py
git commit -m 'work-done'
git push origin master
```
