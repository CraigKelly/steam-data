# Steam Data Setup

This subdir is for gathering the data we need using freely available API's
with Python.

You should have Python 3 and `make` installed to use the `Makefile`

Please be careful with `make clean` - it will delete the Python virtual env
and all previous data, so be sure that's what you want.

## In Progress

TODO: add app id and name from csv file to record - including for success=false
TODO: games.py should pre-scan games.json, find missing appid's, and then append
TODO: above todo means our makefile would be incomplete
