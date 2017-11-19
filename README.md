# SamsungNotification
Checks Samsungcareers page &amp; Codeground page for new changes

# Dev Stacks used
- Python3
- Selenium Webdriver
- Twilio SMS API

# Setup
```
sudo apt-get update
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
# optional from here. Use venv if you want to prevent version mixups of selenium and pyvirtualdisplay.
# Note : Selenium 3.0.0, pyvirtualdisplay 0.2.1, chrome64_54.0.2840.71 are compatible. Any other versions tend to have problems.
virtualenv /var/venv  
source /var/venv/bin/activate
pip install selenium==3.0.0  
pip install pyvirtualdisplay==0.2.1
```

# How to use
Unfortunately, the script is highly personalized due to the tricky nature of navigating volatile minor websites.  
If you want to use it for your own purposes, you'll have to set up a personal twilio account to get a sid and token values.  
Also, you'll have to modify all the methods except basic wrapped ones like get_page(), start_driver() and the like so that it clicks the right elements and checks for correct conditionals.  
However, the main browser navigation code will be useful if you need to navigate through javascript rendered websites.  
The code and setup conditions were greatly referenced from a [medium article](https://medium.com/@hoppy/how-to-test-or-scrape-javascript-rendered-websites-with-python-selenium-a-beginner-step-by-c137892216aa).
