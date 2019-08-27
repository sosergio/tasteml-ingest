# tasteml-ingest
## How to use

Install python3:

```sh
install python3
```

Install project's dependencies:

```sh
pip3 install -r requirements.txt
```

download required NLTK packages:

```sh
python3
import nltk
nltk.download("stopwords")
nltk.download('punkt')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
```

## Then
run the script:

```sh
python3 main.py
```

## Developing with VISUAL STUDIO CODE
install python extension for linting, debugging
choose as python provider the right version

** if you get an error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
http://api.mongodb.com/python/current/examples/tls.html#troubleshooting-tls-errors
macOS users using Python 3.6.0 or newer downloaded from python.org may have to run a script included with python to install root certificates:
open "/Applications/Python <YOUR PYTHON VERSION>/Install Certificates.command"
