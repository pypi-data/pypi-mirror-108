# Cowin Tracker

Python API wrapper for CoWin, to help citizens register themselves for the vaccination drive by booking an appointment at the nearby vaccination centres

This wrapper is meant to enable folks to build their own versions of a system to lookup for vaccine availablity either
in a district or in a particular pin code.

# Install

`pip install taranvir-cowin-api-services`

# Usage

The wrapper currently covers four endpoints used by the CoWin portal specified below.

## Initialize

```python
from cowin_api import CoWinAPI

cowin = CoWinAPI()
```

## Get all the available states

Returns the list of states in which vaccine drive is being conducted. This also returns the `state_id` which would be
required in the subsequent requests.

```python
from cowin_api import CoWinAPI

cowin = CoWinAPI()
states = cowin.get_states()
print(states)
```

---
## Get all the available districts

Returns the list of districts in a particular states in which vaccine drive is being conducted. This also returns
the `district_id` which would be required in the subsequent requests.

In this method, you would need to pass the `state_id` retrieved from the previous method.

```python
from cowin_api import CoWinAPI

state_id = '<give state_id here>'
cowin = CoWinAPI()
districts = cowin.get_districts(state_id)
print(districts)

```

## Get all the centers available using the district_id

Use this method to lookup for centers based on a `district_id` or a list of `district_ids`. This method is broader than
searching by pin code as it covers the whole district.

In this method, you would need to pass the `district_id` retrieved from the previous methods. By default, the method
looks-up for slots with today's date. For any other dates pass the date in DD-MM-YYYY format.

```python
from cowin_api import CoWinAPI

district_id = '<give the district_id here>'
date = '<Give the date here>'  # Optional. Takes today's date by default
min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_limit

cowin = CoWinAPI()
available_centers = cowin.get_availability_by_district(district_id, date, min_age_limit)
print(available_centers)
```

---

## Get all the available centers using a pin code

Use this method to lookup for centers based on a `pin_code` or a list of `pin_codes`. By default, the method looks-up
for slots with today's date. For any other dates pass the date in DD-MM-YYYY format.

```python
from cowin_api import CoWinAPI

pin_code = "<give pincode here>"
date = '<give date here>'  # Optional. Default value is today's date
min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_limit

cowin = CoWinAPI()
available_centers = cowin.get_availability_by_pincode(pin_code, date, min_age_limit)
print(available_centers)
```

---
# Contributions

Contributions are always welcome!

Feel free to modify according to your requirement.

---

# License:

MIT License
