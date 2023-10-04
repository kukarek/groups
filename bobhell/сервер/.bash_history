sudo apt update
sudo apt upgrade
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
python3.9 --version
sudo apt install python3.9-distutils
apt install curl
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.9 get-pip.py
sudo apt install python3.9-venv
python3.9 -m venv desktop
source desktop/bin/activate
python -V
pip -V
pip install --upgrade pip
pip install aiogram
pip install requests
pip install pillow
python pooling.py
pip uninstall aiogram
pip install --force-reinstall -v "aiogram==2.23.1"
python pooling.py
