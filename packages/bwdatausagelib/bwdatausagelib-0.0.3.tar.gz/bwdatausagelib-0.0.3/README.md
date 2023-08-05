A Package for API services and utilities for sim data usage

##Notes
- Clone the repository
- Create the virtual env and install the dependencies
```
py -m venv .venv
pip install -r requirements.txt
```
```
-  Run tests 
```
pytest -s
```
- Download the build package for local development
```
py -m pip install build
```

- Build the package to be used as an import to main script
```
py -m build
```

- To install from local folder, change to the root directory of the main script and install the package
```
py -m pip install ../bwdatausagelib/dist/bwdatausagelib-0.0.1.tar.gz
```

- upload to pypi using twine
```
twine upload dist/* --config-file .pypirc
```


**GlobalSimTable**
- The API service will check for the api queries on a table `GlobalSimsTable` to refill the queue each time it is below the set limit. This table will store all the entities that containing the Sim Provider and ICCID.
- `GlobalSimTable` must be created at the storage that is binded to the Azure function as set in Application Setting `AzureWebJobsStorage`