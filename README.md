#### Flask server with postgres database
Basic solution to upload expense reports, and calculate month by month expenses for that file

For now, its not as tightly packaged as I would like it to be. Using fabric to set up a few things and to run server. Ideally we would want something like a vagrant box to be provisioned to have all the dependencies neatly packagaed.

Pre reququisites:
* Postgres needs to be running before the app is run
* python 2.7 needs to be installed


#### To setup

```sh
$fab setup_postgres
```
This will create a postgres user/database. The same credentials will be used by the flask app to connect to postgres

Then do a
```sh
$fab install_packages
```
This will create a virtaul environment in this directory, and install all the required packages from requirements.txt in there

Finally, to finally run the server, just do a
```sh
$fab run_server
```

#### To test the server

```
http://localhost:5000/upload
http://localhost:5000/all
```