# Software Studio Project

## Prerequesites
- Docker
- Python and pip

## Deploying app
The ./ss-services.sh script is used to perform the startup tasks for the project

First, download the required dependencies for startup
```
cd Software-Studio
pip install -r requirements.txt
```

Now you can start by loading the database schema into the database with the following command
```
./ss-services.sh load
```

Then, use the webapp_config module to create a webapp config file
```
python webapp_config.py
```

Then, the app can be started with using
```
./ss-services.sh start
```

To stop the app, use
```
./ss-services.sh stop
```

To clear the data (database, image store) use this command. Remember to use the load option after this command to reload the schema.
```
./ss-services.sh clear
```