This is a python Restful service based on flask.

## How to use
***
  First copy this repo into your disk.
  ```bash
   git@github.com:liyueshining/swagger-parrot.git
  ```
  Then be sure you have installed python 2.7.8, this project is based on this version.
  pip is highly recommended to be install. because when you install flask by pip,it can install libraries which flaskdepends on automatically.
  - install pip
  
  ```bash
    python setup.py install
  ```
  - install falsk by pip
  ```bash
    pip install Flask
  ```
  
  - install falsk-cors by pip
  ```bash
    pip install -U flask-cors
  ```
  
  First use flask command line to initialize db as follows:
  ```python
    @app.cli.command()
    def initdb_command():
        """Initializes the database."""
        init_db()
        print('Initialized the database.')
  ```
  
  THen create initdb.sh or init.bat as follows:  and run it
  ```bash
    export FLASK_APP=service.py
    or
    set FLASK_APP=service.py
    
    flask initdb_command
  ```
  
  Finally execute this service by running run.sh in linux or run.bat in windows.
  
  Port exposed is 5000, or can be configured in app.run(host='0.0.0.0', port=5050)
  
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
