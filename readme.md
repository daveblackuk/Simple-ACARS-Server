# SIMPLE ACARS server

* Allows local connectivity testing for clients
* Supports CDPLC, TELEX, PROGRESS, POSREQ, POSITION, POLL and PEEK message types
* Based: on [https://www.hoppie.nl/acars/system/tech.html](https://www.hoppie.nl/acars/system/tech.html)
* Endpoint: http://localhost:5050/acars/system/connect.html
* Display the database contents: http://localhost:5050/dump

## Local Installation

* Ensure Python3 and PIP3 installed
* Install requirements: pip3 install -r requirements.txt
* Run the server python server.py
* No logon required

## Docker Container

* Docker build -t "acars" .
* docker run -it --name acars -p 5050:5050 acars

## CURL Examples

replace  localhost with your docker container's IP address if required

Telex: curl "http://localhost:5050/acars/system/connect.html?logon=gFR54Fr&from=KXXY&to=KLM123&type=telex&packet=hello_world"

CPDLC:  curl "http://localhost:5050/acars/system/connect.html?logon=gFR54Fr&from=KXXY&to=KLM123&type=cpdlc&&packet=/data2/2321/1/Y/WILCO

Poll:  curl "http://localhost:5050/acars/system/connect.html?logon=gFR54Fr&from=KLM123&to=SERVER&type=poll"

Peek: **curl "http://localhost:5050/acars/system/connect.html?logon=gFR54Fr&from=KLM123&to=SERVER&type=peek
