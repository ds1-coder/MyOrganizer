ROOT_ENV=.rootenv
VIRTUAL_ENV=.venv
source $VIRTUAL_ENV/bin/activate
pip3 install -r requirements.txt
python3 app.py