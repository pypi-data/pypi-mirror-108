# NextAPM

Monitor the Django and Flask python web application. You need https://nextapm.dev account to configure the monitor.

## Installation
Install agent module in your application
```
pip install pythonapm
```

## Instrumentation
To monitor Django application, modify the settings.py 
```
add "pythonapm.contrib.django" in the first of INSTALLED_APPS in django settings.py
```

To monitor Flask application, import following module in flask main file
```
// this should be in the first line of application main file
import pythonapm;
```

## Configuration
Configure the following environment variables, you can get it from https://app.nextapm.dev after creating monitor.

```
NEXTAPM_LICENSE_KEY
NEXTAPM_PROJECT_ID
```

## Restart/Redeploy
Restart/Redeploy your application and perform transactions