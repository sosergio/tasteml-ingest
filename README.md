
cluster address: https://cloud.mongodb.com/v2/5d0342a09ccf648ca5f2e4dc
username: admin
password: khCggojq5uP5Wdey
old password: ifhK8pwM6Uhbs8C
connection string: mongodb+srv://admin:<password>@tasteml-cluster-mc39i.mongodb.net/test?retryWrites=true&w=majority

ip address needs to be whitelisted on mongodb Atlas

-- HOW TO INSTALL
install python3
and use pip3 (comes with python3) to install the following packages:
# required for interacting with MongoDb
dnspython
pymongo
# natural language toolkit
nltk
# SciPy stack
numpy scipy matplotlib ipython jupyter pandas sympy nose
# after SciPy is insalled, install scikit-learn
scikit-learn

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
