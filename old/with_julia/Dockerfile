FROM russelljarvis/science_accessibility:slc

USER root

# Install some Debian package
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-setuptools     \
    python3-wheel          \
    python3-pip            \
    less                  \
    nano                  \
    sudo                  \
    git                   \
    npm                   \
  && rm -rf /var/lib/apt/lists/*

# install Jupyter via pip
RUN pip3 install notebook

# install ipywidgets
RUN pip3 install ipywidgets  && \
    jupyter nbextension enable --sys-prefix --py widgetsnbextension


RUN sudo /opt/conda/bin/conda install --channel conda-forge appmode



RUN jupyter nbextension     enable --py --sys-prefix appmode && \
    jupyter serverextension enable --py --sys-prefix appmode
# Launch Notebook server
EXPOSE 8888
CMD ["jupyter-notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token=''"]
