from slc
USER root

RUN apt-get update
RUN apt-get install --fix-missing



RUN apt-get update

# Install octave this installs octave

RUN apt-get install --force-yes -y \
  bison \
  build-essential \
  cmake \
  cmake-curses-gui \
  flex \  
  g++ \
  imagemagick \
  libxi-dev \
  libxi6 \
  libxmu-dev \
  libxmu-headers \
  libxmu6 \  
  unzip \
  graphviz \
  xpdf \
  liboctave-dev

RUN sudo apt-get -y install gnuplot rlwrap ipython

  

# Fetch Octave forge packages
RUN mkdir /home/octave


# Build octave configure file
RUN echo more off >> /etc/octave.conf
RUN echo save_default_options\(\'-7\'\)\; >> /etc/octave.conf
RUN echo graphics_toolkit gnuplot >> /etc/octave.conf

USER jovyan

# Command for build
# docker build --no-cache -t="simexp/octave:3.8.1" .

# Command to run bash (don't start octave)
# docker run -i -t --rm --name octavebash -v $HOME:$HOME --user $UID:$GID simexp/octave:3.8.1 /bin/bash -c "export HOME=$HOME; cd $HOME; source /opt/minc-itk4/minc-toolkit-config.sh; exec bash"

# Command to run octave as command line
# docker run -i -t --rm --name octavecli -v $HOME:$HOME --user $UID:$GID simexp/octave:3.8.1 /bin/bash -c "export HOME=$HOME; cd $HOME; source /opt/minc-itk4/minc-toolkit-config.sh; octave"

# Command to run octave as GUI
# docker run -i -t --rm --name octavegui  -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -v $HOME:$HOME --user $UID:$GID simexp/octave:3.8.1 /bin/bash -c "export HOME=$HOME; cd $HOME; source /opt/minc-itk4/minc-toolkit-config.sh; octave --force-gui"