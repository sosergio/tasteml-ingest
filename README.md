
cluster address: https://cloud.mongodb.com/v2/5d0342a09ccf648ca5f2e4dc
username: admin
password: khCggojq5uP5Wdey
old password: ifhK8pwM6Uhbs8C
connection string: mongodb+srv://admin:<password>@tasteml-cluster-mc39i.mongodb.net/test?retryWrites=true&w=majority

ip address needs to be whitelisted on mongodb Atlas

-- TO GENERATE THE REQUIREMENTS.txt
install python3
pip3 freeze > requirements.txt


-- HOW TO INSTALL
install python3
# create virtual environment
python3 -m venv /path/to/new/virtual/env
# install project dependencies
pip3 install -r requirements.txt

Libraries installed contain:
# required for interacting with MongoDb
dnspython
pymongo
# natural language toolkit
nltk
# SciPy stack
numpy scipy matplotlib ipython jupyter pandas sympy nose
# after SciPy is insalled, install scikit-learn
scikit-learn

# run an interactive GUI to download NLTK packages
import nltk
nltk.download()
import nltk
nltk.download("stopwords")

# downloads the NLTK's small collection of web text includes content from a Firefox discussion forum, conversations overheard in New York, the movie script of Pirates of the Carribean, personal advertisements, and wine reviews.
nltk.download('webtext') 

# Pandas takes data (like a CSV or TSV file, or a SQL database) and creates a Python object with rows and columns called data frame that looks very similar to table in a statistical software (think Excel or SPSS for example
import numpy as np
import pandas as pd

# install multiple packages at once ()
pip3 install -U numpy scipy matplotlib ipython jupyter pandas sympy nose
pip3 install -U scikit-learn
pip3 install -U requests

-- VISUAL STUDIO CODE
install python extension for linting, debugging
choose as python provider the right version

-- HOW TO RUN
open the terminal in the folder
python3 run.py

** if you get an error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
http://api.mongodb.com/python/current/examples/tls.html#troubleshooting-tls-errors
macOS users using Python 3.6.0 or newer downloaded from python.org may have to run a script included with python to install root certificates:
open "/Applications/Python <YOUR PYTHON VERSION>/Install Certificates.command"
