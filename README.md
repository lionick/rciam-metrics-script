# rciam-metrics
A Python-based tool for exporting metrics to file (Prometheus format) and save them to a database:
- Registered Users from CoManage
- Total Logins from proxystatistics
- Total Api requests from nginx logs

## Installation
```
git clone https://github.com/rciam/rciam-metrics.git
cd rciam-metrics
cp config.py.example config.py
vi config.py
```

Create a Python virtualenv, install dependencies, and run the script
```
virtualenv -p python3 .venv
source .venv/bin/activate
(venv) pip3 install -r requirements.txt
(venv) python3 -m Utils.install
(venv) python3 exportStats.py
🍺
```

## License
Licensed under the Apache 2.0 license, for details see LICENSE.



