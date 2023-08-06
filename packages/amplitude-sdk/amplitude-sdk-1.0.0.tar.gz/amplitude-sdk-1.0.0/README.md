Amplitude Python SDK
====================

SDK for Amplitude API: https://developers.amplitude.com/docs


Requirements
------------

* >=Python 3.7.5

Installation
------------
```
    pip install amplitude_sdk
```

Goal
----

To provide a python API client for Amplitude API.
(More clients to be implemented)

HTTP API V2 - to be implemented
Batch Event Upload API - to be implemented
Identify API - to be implemented
Attribution API - to be implemented
Behavioral Cohorts API - ```list_cohorts, download_cohort, create_cohorts, modify_membership ```
Chart Annotations API - to be implemented
Dashboard REST API - to be implemented
Export API - to be implemented
Group Identify API - to be implemented
Releases API - to be implemented
SCIM API - to be implemented
Taxonomy API - to be implemented
User Privacy API - to be implemented
User Profile API - to be implemented

Code sample
-----------

Requesting Behavioral Cohorts API

```python

  from amplitude_sdk import BehavioralCohortsClient
  b = BehavioralCohortsClient(
  api_key='xxxxxxx',
  secret='yyyyyyyy')
  b.list_cohorts()
```

Result from response type: forecast and forecastHourly
```python
    {'cohorts': [{'appId': 6666666,
    'archived': False,
    'definition': {'version': 2,
    'countGroup': 'User',
    'cohortType': 'UNIQUES',
    'andClauses': [{'negated': False,
      'orClauses': [{'type': 'event',
        'time_type': 'rolling',
        'time_value': 30,
        'offset': 0,
        'interval': 1,
        'type_value': 'customer-purchase',
        'operator': '>=',
        'operator_value': 2,
        'group_by': [],
        'metric': None,
        'event_props': [{'group_type': 'User',
          'filter_type': 'event',
          'type': 'orderMethod',

```

Contributors
------------

* Paulo Kuong ([@pkuong](https://github.com/paulokuong))
