First, you need to setup some tools/ environments, and then once the project is setup, there are some data initialization steps

A. Setup Tools/Environment:
We need to do three things to get going:
1. Make sure you have the right verison of python installed
2. Make sure you have the right packages setup in a virtual environment designed to ensure all code is compatible
3. Pull the project from github
4. Setup an IDE to make development easier

Step 1:First, make sure you have python 3 installed. Download the Anaconda bundle here, which includes python 3,
       and some other tools we'll use:
       https://www.anaconda.com/products/individual

Step 2: To download this from github, go to your terminal command prompt and type: https://github.com/Mike-Huntress/Intership2020.git
        -This will create a copy of project in your local directory.
        -Set the working directory to the newly checkouted out code with:
         cd [put the path to the newly checked out code here]
        -Once you've done that, you should create your own development branch to work on with:
         git checkout -b bondSignal_[FirstnameLastname]
        -When it comes time to share your code, you can commit with these commands:
         git commit -m "Your commit message"   , followed by
         git push   , which will push your code to the github server on your new branch

Step 3: To make sure your local version of python and the associated packages are compatible with utilities we've
        made to make this work easier, you're going to need to spin up a python virtual environment with pipenv,
        a virtual environment and package manager. As part of your Anaconda download, a piece of package management
        software called pip was installed that we're going to run from your terminal/ command line. We're going to
        it to fetch some other tools that will help manage our packages more cleanly. Run this in the terminal/command line:

        sudo -H pip install -U pipenv
        cd [path to the project we just cloned in step 2]
        pipenv install
        pipenv shell

        This will return some text, including a directory path, e.g.:
        /Users/michaelhuntress/.local/share/virtualenvs/BWInternship2020-qGgbmmCS/bin/activate

        Save this path. This new "virtual environment" is a container that will house the right interpreter (python version),
        and associated packages to use in this project. It's out of here we're going to run out code.

Step 4: Next, we're going to go get an IDE (integrated development environment), which will make it easier to write
        code in. There are many, and you're welcome to use a different one, but I like this one, PyCharm
        https://www.jetbrains.com/pycharm/download/#section=mac

        Download the community version.

        -Once you've done this, open an existing project from the directory where we cloned the porject code.
        -Now we need to tell it to run the python interpreter out of the virtual environemnt we created in step 3:
          -Go to Preferences -> Project -> Project Interpreter
          -Select the * button, click "add local", and then in the directory menu that appears select the directory
         path the terminal/command line returned to you in step 3, e.g. /Users/michaelhuntress/.local/share/virtualenvs/BWInternship2020-qGgbmmCS/bin/activate

        - You can check this is working by running any script in pyCharm. At the top of the pyCharm terminal will
          show the interpreter and the file run. E.g.:
          /Users/michaelhuntress/.local/share/virtualenvs/BWInternship2020-qGgbmmCS/bin/python3.6 /Users/michaelhuntress/PycharmProjects/BWInternship2020/BasicSetup/CountryMetaData.py

          So here, for instance, I see it's running out of my virtual environment.






B. Data Initialization Steps
You need to perform a few initial setup steps.You'll need to:
1. Write your data stream (Eikon) credentials to a local file
2. Create a country metadata file that will also be stored locally (you'll use this over and over)
3. Pull an initial batch of data and write to a local file where you can quickly and easily pull from
4. Make sure you can run Jupyter notebooks from within PyCharm




Step 1: Write credentials to local file
You should have received an Eikon/DataStream username and password. Open up Credentials.py in the
the BasicSetup package and fill out the parameters for "Your Username" and "Your Password" with the
appripriate information.
e.g.:
DataSourceCredentials().addCredentials("datastream", "Your Username", "Your Password")

You should see a folder called .ConfigKeys get written to your user directory with a file called user.config.ini in it.
Once you do this you won't need to worry about passing your username and password to the Eikon/DataStream API to
fetch data again

Step 2: Create country metadata file
Open the CountryMetaData.py file in the BasicSetpu package and run this. That's all you need to do, and you only need to do it once. This
will write a local folder to your user directory called  .dataLib with a file called countryMetaData.ini

Step 3: Fetch data from Eikon/DataStream API and build your data library
While you can add data later, you've been set up with a base set of data. Open the 0_SignalDataLibrary.py file
from the SampleSignal package and run  this. This will fatch and save a temporary version of the data to your
user directory under a series of folders nested under the .dataLib folder created above.

Step 4: Make sure you can run Jupyter notebooks from within PyCharm
Although there are lots of potential ways you might use an IDE, a combination I like (and thus will impose upon you),
is the PyCharm IDE used in conjunction with a jupyter notebook to serve as a scratch pad. You can open them up in parallel
windows and run the jupyter notebook out of PyCharm in a pretty nice side by side experiances.

First, go to your terminal/command line and enter "jupyter notebook". If you installed Anaconda this should instantiate the
locally hosted jupyter notebook and give you a link and token to access that notebook:
e.g.:
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8889/?token=9a30c4ba98a483ae652282dfa41a8e56e0e560b8d96beb22

Copy this link and open up the DataBrowser.ipynb file in the SampleSignal package. Hit the green arrow to "run cell". It'll open a
dialogue box asking for a token. Copy your URL with the embedded token in this window and hit ok. Now your jupyter notebook in
Pycharm should be working. Run a couple cells in the file to make sure this is true.

A thing I like doing is splitting the python window into a horizontal pane. Right click the "DataBrowser.ipynb" tab at the top of your
PyCharm window and hit "Split Horizontally". You should now have split windows with the notebook off to the right.


