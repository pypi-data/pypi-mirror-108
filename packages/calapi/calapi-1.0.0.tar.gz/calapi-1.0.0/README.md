# Calapi 1.0.0

A light weight python wrapper for [Google's Calendar API v3](https://developers.google.com/calendar/v3/reference) written upon [Google's API Python Client](https://github.com/google/google-api-python-client).

# Features provided by Calapi
- Documented functions and usage instructions.
- Pythonic style usage.

# Installation
To install, simply use `pip` or `easy_install`:

```bash
$ pip install calapi
```
or
```bash
$ easy_install calapi
```

# Acquire Google Oauth credentials

**1.  Create a new project on google console dashboard on below link**

https://console.cloud.google.com/apis/dashboard

**2.  Enable Google Calendar API on the below link**

https://console.cloud.google.com/apis/library/calendar-json.googleapis.com

**3.  Configure Oauth Consent Screen**

- Open Link https://console.cloud.google.com/apis/credentials/consent
- Click on "OAuth Consent screen"
- Select User Type and click create
- Provide app name, email and proceed
- Add Required scopes based on your use case
- Proceed and complete the process

**3.  Create Oauth Client ID credentials for Users consent**

- Open Link https://console.cloud.google.com/apis/credentials/consent
- Click on "+ Create Credentials"
- Select "OAuth client ID"
- Select Application Type "Web Application"
- Provide name, authorized javascript URIs, authorized redirect URIs and create
- Download the credentials

------------

# Get Started

#### Instantiate Calapi Oauth Instance

    from calapi import Oauth
    client = Oauth(
        credentials_path='./credentials.json',
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.readonly'
        ]
    )
        
#### Get Users consent for Calendar Access
**(Note: Users Consent is required for accessing user calendar)**

    # Redirect URL to which google will callback with state and code
    callback_url = 'https://yourdomain.com/api/v1/google/calendar/callback'

    # Use `oauth_consent_url` to get user's consent
    oauth_consent_url = client.get_authorization_url(redirect_uri=callback_url)

#### Fetch User's Access Token using Google's callback after users consent
**(Google will callback on provided redirect_uri)**

    # Upon Googles Oauth callback, get state & code from query params
    state = request.args.get('state')
    code = request.args.get('code')
    
    # Call this function on google's callback after users consent
    session_credentials = client.on_auth_callback(state, code)

    # Store Users session credentials in DB for performing actions on user's Calendar

#### Instantiate Session Object for user

    from calapi import Session
    session = Session(session_credentials=session_credentials)

## Using Events API 
**(Refer Google's docs: https://developers.google.com/calendar/v3/reference/events)**
**(Get all the usage information for events api using below line)**

    help(session.events)

### Create Event on Users Calendar

    # Generate query for inserting
    query = session.events.query.start(
                date_time='2021-06-03T09:00:00-07:00',
                time_zone='America/Los_Angeles'
            ).end(
                date_time='2021-06-03T09:30:00-07:00',
                time_zone='America/Los_Angeles'
            ).attendees([
                {'email': 'lp_age@example.com'},
                {'email': 'sbrin@example.com'},
            ]).summary(
                'Google I/O 2015'
            ).description(
                '800 Howard St., San Francisco, CA 94103'
            ).recurrence([
                'RRULE:FREQ=DAILY;COUNT=2'
            ]).reminders({
                'use_default': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            })
    # Insert to the calendar
    created_event = session.events.insert(query)

### Get Event using event id

    event = session.events.get(event_id)

### Update Event using event id

    query = session.events.query.summary(
                    'Updated summary Google I/O 2015'
                ).description(
                    'Updated description 800 Howard St., San Francisco, CA 94103'
                )
    resp = session.events.update(event_id, query)

### Delete Event

    resp = session.events.delete(event_id)


## Using Calendars API 
**(Refer Google's docs: https://developers.google.com/calendar/v3/reference/calendars)**

### **Get all the usage information for calendars api using below line**

    help(session.calendars)

### Create Secondary Calendar

    # Generate query for inserting
    query = session.events.query.summary(
                'calendarSummary'
            ).time_zone(
                'America/Los_Angeles'
            )
    # Insert Secondary calendar
    calendar = session.calendars.insert(query)

#### Get metadata for a calendar

    resp = session.calendars.get(calendar_id)

#### Update metadata for a calendar

    query = session.calendars.query.summary(
                        'New Summary'
                    )
    resp = session.calendars.update(query)
        

#### Delete a secondary calendar

    resp = session.calendars.delete(event_id)

## For all the apis, calapi provides all the usage information in respected help function
### **To learn about the usage for other apis, use below lines of code**


    # For Oauth usage instruction
    help(calapi.Oauth)

    # For Session usage instruction
    help(calapi.Session)

    # For ACL Api usage instruction
    help(session.acl)

    # For Calendar List Api usage instruction
    help(session.calendarlist)

    # For Calendars Api usage instruction
    help(session.calendars)

    # For Settings Api usage instruction
    help(session.settings)

    # For Colors Api usage instruction
    help(session.colors)

    # For Events Api usage instruction
    help(session.events)


**(Note: I tried to cover all the basic details which are required by each api in the docs. If there are any missing docs, please feel free to report in the issue section)**

------

## Third Party Libraries and Dependencies
The following libraries will be installed when you install the client library:
* [google-api-python-client](https://github.com/google/google-api-python-client) (Google Client Library)
* [google-auth](https://github.com/GoogleCloudPlatform/google-auth-library-python/) (Google Auth Library)
* [google-auth-oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib) (This library provides oauthlib integration with google-auth)
* [google-auth-httplib2](https://github.com/googleapis/google-auth-library-python-httplib2) (This library provides an httplib2 transport for google-auth.)

## To-Dos
- Response Object Manipulation. (This update will enable to you to generate response in Google Raw Response, Simplified Response, CSV, Panda Dataframe).
- Test cases.

## Contribute
1. Look for an open [issue](https://github.com/rakeshgunduka/calapi/issues) or create new issue to get a dialog going about the new feature or bug that you've discovered.
2. Fork the [repository](https://github.com/rakeshgunduka/calapi) on Github to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Make a pull request.

