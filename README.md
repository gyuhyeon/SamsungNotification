sudo apt-get install libpango1.0-0  
sudo apt-get -f install  
wget -c "https://www.slimjet.com/chrome/download-chrome.php?file=lnx%2Fchrome64_54.0.2840.71.deb"  
sudo dpkg -i download-chrome.php?file=lnx%2Fchrome64_54.0.2840.71.deb  
sudo rm download-chrome.php?file=lnx%2Fchrome64_54.0.2840.71.deb  
sudo apt-get install -y -f  
sudo mkdir /var/chromedriver  
cd /var/chromedriver  
wget "http://chromedriver.storage.googleapis.com/2.25/chromedriver_linux64.zip"  
unzip chromedriver_linux64.zip  
sudo apt-get -y install python3-pip python3-dev build-essential libssl-dev libffi-dev xvfb  
pip3 install --upgrade pip  
virtualenv /var/venv  
pip install selenium==3.0.0  
pip install pyvirtualdisplay==0.2.1 
