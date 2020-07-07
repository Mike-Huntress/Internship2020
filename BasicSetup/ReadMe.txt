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


