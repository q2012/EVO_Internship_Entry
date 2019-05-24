# First task for Evo Internship Entry

Second task is on [second brach](https://github.com/q2012/EVO_Internship_Entry/tree/second_task)

----
## Web file exchanger
Preview [on heroku](https://intense-atoll-62971.herokuapp.com/).

Done using Flask + MongoDB.

----
## Usage
Pretty staightforward: if you want to upload a file, you need to register first. Login right after, choose file with filechooser and enter day/time you want to have this file expired. After submitting, link to filepage will appear. Anyone with this link will be able to download your file before expiration date.

----
## Local deployment

You need to have python, pip, mongodb installed. 
Unzip project and run

```
pip install requirements.txt
```

Set up `MONGODB_URI` and `FLASK_APP=flaskr` as environment variable.

To run application, use 

```
flask run
```
