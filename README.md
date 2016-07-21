This is a python Restful service based on flask.

## How to use
***
  First copy this repo into your disk.
  ```bash
   git@gitlab.zte.com.cn:tlcop-sh/swagger-monkey-python-flask.git
  ```
  Then be sure you have installed python 2.7.8, this project is based on this version.
  pip is highly recommended to be install. because when you install flask by pip,it can install libraries which flaskdepends on automatically.
  - install pip
  ```bash
  python setup.py install
```
  - install falsk by pip
  ```bash
  pip install flask
  ```
  
  Finally execute this service by running run.sh in linux or run.bat in windows.
  
  Port exposed is 5000
  
  When excuting service the second time, it is necessary to comment out the first line, this line is used to initialize sqlite db.
  
## Rest APIs
***
    PATH:
         /urls
    METHOD:
         GET DELETE POST

    PATH:
         /urls/{key}
    METHOD:
         GET DELETE PUT
