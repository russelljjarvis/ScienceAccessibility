sudo apt-get update
sudo apt-get install --fix-missing
sudo apt-get install -y octave
sudo pip install octave_kernel
#ipython notebook
# In the notebook interface, select Octave from the 'New' menu
#http://nbviewer.jupyter.org/github/Calysto/octave_kernel/blob/master/octave_kernel.ipynb
ipython qtconsole --kernel octave
ipython console --kernel octave
