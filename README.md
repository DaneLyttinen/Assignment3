# Assignment2
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