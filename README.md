
cluster address: https://cloud.mongodb.com/v2/5d020fdbcf09a2dda67c5ac0#clusters/detail/tasteml-db
username: admin
password: ifhK8pwM6Uhbs8C
connection string: mongodb+srv://admin:<password>@tasteml-db-gndd2.mongodb.net/test?retryWrites=true&w=majority

-- HOW TO INSTALL
install python3
and use pip3 (comes with python3) to install the following packages:
dnspython
pymongo
nltk

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
