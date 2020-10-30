# Assignment3

## Description

A Web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool.

Note
Unfortunately I couldn't get a movie to link to a director
correctly and couldn't get this fixed 

Setting up a virtual environment
to set up a virtual environment follow these steps
1. Open a terminal
2. type in the command
```shell
$pip -h (if you don't have it install it)
```
3.type in 
```shell
$pip install virtualenv 
```
4. create virtualenvironment
```shell
$virtualenv website
```
5. Activate the virtual environment by running the command
```shell
$mypthon\Scripts\activate
```
**Installation via requirements.txt**

```shell
$ cd COMPSCI-235
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```
To set up a virtual environemnt in pycharm follow the steps on the jetbrains website at https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html


## Execution

**Running the application**

From the *COMPSCI-235* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

##Configuration
The *COMPSCI-235/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

Testing
Testing requires that file COMPSCI-235/tests/conftest.py be edited to set the value of TEST_DATA_PATH. You should set this to the absolute path of the COMPSCI-235/tests/data directory.

E.g.

TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'ian', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

C:\Users\ian\Documents\python-dev\COVID-19\tests\data

Please also do this in the data path in test_memory_repository.py