
### Setting Up the Environment (Developer)
A docker container can be downloaded from Docker hub or built locally.
```BASH
docker login your_user_name@dockerhub.com
docker pull russelljarvis/science_accessibility:slc
mkdir $HOME/data_words
docker run -it -v $HOME/data_words russelljarvis/science_accessibility:slc
```
### Running a Simple Example (User)
After Docker installation on your Operating System, run the following commands in a BASH terminal.
```BASH
docker pull russelljarvis/science_accessibility_user:latest
```
Here is a python example to search for results from academic author Richard Gerkin. When inside the docker container, issue the command:
```BASH
mkdir $HOME/data_words
docker run -v $HOME/data_words russelljarvis/science_accessibility_user "R Gerkin"
```
