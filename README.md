#Create a virtual environment
python3 -m venv env

#Activate the virtual environment in linux
source env/bin/activate 

#Activate the virtual environment in windows
env\Scripts\activate

#Readme to install fastapi and requirements.txt
pip install -r requirements.txt

#init fastapi
uvicorn app.main:app --reload --port 8080

#run tests
pytest

#run tests with coverage
pytest --cov=app

