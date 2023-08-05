# Google API Connection Wrapper

[![PyPI Latest Release](https://img.shields.io/pypi/v/googlewrapper.svg)](https://pypi.org/project/googlewrapper/)

General Connector Classes for Google Products 

__Links to their respective sections__

 - <a href=https://github.com/jaceiverson/google-wrapper#google-analytics>Google Analytics</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-search-console>Google Search Console</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-calendar>Google Calendar</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-big-query>Google Big Query</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-page-speed-insights>Google PageSpeed API</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#gmail>Gmail</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-sheets>Google Sheets</a>

# STEPS
 1) <a href=https://github.com/jaceiverson/google-wrapper#Acquire-Google-Credentials-from-API-Console>Acquire Google Credentials from API Console</a>
 2) <a href=https://github.com/jaceiverson/google-wrapper#installation>Install this pacakge</a>
 3) <a href=https://github.com/jaceiverson/google-wrapper#establish-your-connection>Create Connection in Python</a>
 4) <a href=https://github.com/jaceiverson/google-wrapper#product-specific-methods>Use wrapper to make API calls</a>


## Acquire Google Credentials from API Console

First we will need to get our own Google Project set up so we can get our credentials. If you don't have experience, you can do so here <a href=https://console.cloud.google.com/apis/dashboard>Google API Console</a>

After you have your project set up, oAuth configured, and the optional service account (only for Google Big Query connections), you are good to install this package.

Make sure to download your oAuth credentials and save them to your working directory as 'client_secret.json'.

## Installation

```
pip install googlewrapper
```


## Establish your Connection
Use the Connection class found in connect.py to asisgn credentials. 

'client_secret.json' should be in the working directory, if not, please declare the path while initializing the class. See the example below for both versions.
```
from googlewrapper.connect import Connection

#in working directory
google_connection = Connection()

#declare path in class
google_connection = Connection(file/path/to/client_secret.json)
```

Once we have our connection object, we wil need to declare the scope of our access. You can do this by accessing the following class methods:

| Google Service       | Module     | Authentication Type | Credential File |
| :------------- | :----------: | :----------: | :----------: |
|  Analytics | .ga()   | oAuth | client_secret.json | 
| Search Console   | .gsc() | oAuth |  client_secret.json | 
| Calendar   | .cal() | oAuth | client_secret.json | 
| Big Query   | .gbq() | Service Account | gbq-sa.json |
| PageSpeed  | n/a | API Key | n/a | 
| Gmail   | .gmail() | oAuth | client_secret.json | 
| Sheets   | .gs() | oAuth | client_secret.json | 

Note, you can change the file path for authenticating Google Big Query by passing in the Service Account json in the gbq method

```
gbq_connection = Connection().gbq(file/path/to/service_account.json)
```
After authentication has taken place, a folder will be created in your cwd named _credentials_. The respective authentication scopes will be stored there so you don't have to authenticate everytime. Each token is stored with the Google property name as a .dat file.

#### One Line Connection
It is possible to just use one line when connecting. This can be done by calling the Connection class and immediately calling the scope that you want access to. See below.
```
from googlewrapper.connect import Connection

ga_auth = Connection().ga()
```

## Product Specific Methods
Now that we have our credential object, we are ready to call the api. We will walk through examples for the different products
### Google Analytics
#### Initialize 
```
from googlewrapper.connect import Connection
from googlewrapper.ga import GoogleAnalytics

ga_auth = Connection().ga()
ga = GoogleAnalytics(ga_auth)
```
#### Methods
#### Examples

### Google Search Console
#### Initialize 
```
from googlewrapper.connect import Connection
from googlewrapper.gsc import GoogleSearchConsole

gsc_auth = Connection().gsc()
gsc = GoogleSearchConsole(gsc_auth)
```
#### Methods
#### Examples
```
#assign the constant variables
sites = list_of_sites

gsc.set_sites(sites)
gsc.set_start_date(day)
gsc.set_end_date(day)
gsc.set_branded(branded_list)
gsc.set_dimensions(dim_list)

#call the api
data = gsc.get_data()
```
### Google Calendar
#### Initialize 
```
from googlewrapper.connect import Connection
from googlewrapper.cal import GoogleCalendar

cal_auth = Connection().cal()
cal = GoogleCalendar(cal_auth)
```
#### Methods
```
.set_default(cal_id)
```
 - Assigns which calendar will be used to create and find events
```
.find_event(str)
```
   - Searches for an event in your calendar by name 
   - Returns <a href=https://developers.google.com/calendar/v3/reference/events/list#response>events list response object</a>
```
.get_event(eventId:str)
```
   - Returns the <a href=https://developers.google.com/calendar/v3/reference/events#resource>event object</a> of the eventId you passed in
 
```
.all_events(num_events,min_date)
```
   - Params
     - num_events
       - Is the number of events you'd like to return
       - defaults to 250
     - min_date
       - the starting point will only search forward in time from this date
       - defaults to the current date and time 
   - Returns
     - <a href=https://developers.google.com/calendar/v3/reference/events/list#response>events list response object</a>

```
.update_event(new_event,send_updates)
```
   - Params
     - new_event
       - event formated json to update
     - send_updates: str
       - if you want to send the updates
       - see <a href=https://developers.google.com/calendar/v3/reference/events/update#parameters>Google's Docs</a> for more info
       - defaults to 'all'
   - Returns the <a href=https://developers.google.com/calendar/v3/reference/events#resource>updated event object</a>
#### Examples 
```
my_event = cal.find_event('Team Meeting')
```

### Google Big Query
#### Initialize 
```
from googlewrapper.connect import Connection
from googlewrapper.gbq import GoogleBigQuery

gbq_auth = Connection().gbq()
gbq = GoogleBigQuery(gba_auth)
```
Remember that Google Big Query authenticates from a service account, be sure to include the gbq-sa.json file in your path, or pass in the pass to the .gbq() method.
#### Methods
#### Examples 

### Google PageSpeed Insights
#### Initialize 
```
from googlewrapper.pagespeed import PageSpeed

page_speed = PageSpeed(API_KEY)
```
#### Methods
#### Examples 

### Gmail
#### Initialize 
```
from googlewrapper.connect import Connection
from googlewrapper.gmail import Gmail

gmail_auth = Connection().gmail()
mail = Gmail(gmail_auth)
```
#### Methods
#### Examples 

### Google Sheets
#### Initialize 
```
from googlewrapper.connect import Connection
from googlewrapper.gs import GoogleSheets

gs_auth = Connection().gs()
gs = GoogleSheets(gs_auth)
```
##### Methods
#### Examples 
