# pyindia_zipcode

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/THAVASIGTI/pyindia_zipcode)
[![PyPI](https://img.shields.io/pypi/v/pyindia-zipcode)](https://pypi.org/project/pyindia-zipcode)
[![Downloads](https://pepy.tech/badge/pyindia-zipcode)](https://pepy.tech/project/pyindia-zipcode)

### Find Post Office Details from PinCode, All India Post Office Pincode Data

## INSTALL

``` python
pip3 install pyindia-zipcode
```
## IMPORT PKG

``` python
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pyindia_zipcode import ZipCode
>>> 
>>> obj = ZipCode()
>>> 
```
## ZIP CODE INFO

In this `625003` zip code infomation

``` python
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pyindia_zipcode import ZipCode
>>> 
>>> obj = ZipCode()
>>> 
>>> obj.get_zipcode_info(625003)
>>> 
```
### output

``` json
[
    {
        "ID": 119891, "officename": "Alagappa Nagar S.O", 
        "pincode": "625003", "officeType": "S.O", 
        "Deliverystatus": "Non-Delivery", "divisionname": "Madurai", 
        "regionname": "Madurai", "circlename": "Tamilnadu", 
        "Taluk": "Madurai South", "Districtname": "Madurai", 
        "statename": "TAMIL NADU", "Telephone": "0452-2343894", 
        "Related Suboffice": "NA", "Related Headoffice": "Madurai H.O", 
        "longitude": "NA", "latitude": "NA"
    }, {
        "ID": 120019, "officename": "Madakkulam B.O", 
        "pincode": "625003", "officeType": "B.O", 
        "Deliverystatus": "Delivery", "divisionname": "Madurai", 
        "regionname": "Madurai", "circlename": "Tamilnadu", 
        "Taluk": "Madurai South", "Districtname": "Madurai", 
        "statename": "TAMIL NADU", "Telephone": "NA", 
        "Related Suboffice": "Palanganatham S.O", "Related Headoffice": "Madurai H.O", 
        "longitude": "NA", "latitude": "NA"
    }, {
        "ID": 120073, "officename": "Palanganatham S.O", 
        "pincode": "625003", "officeType": "S.O", 
        "Deliverystatus": "Delivery", "divisionname": "Madurai", 
        "regionname": "Madurai", "circlename": "Tamilnadu", 
        "Taluk": "Madurai South", "Districtname": "Madurai", 
        "statename": "TAMIL NADU", "Telephone": "0452-2373669", 
        "Related Suboffice": "NA", "Related Headoffice": "Madurai H.O", 
        "longitude": "NA", "latitude": "NA"
    }, {
        "ID": 120185, "officename": "Tvs Nagar S.O", 
        "pincode": "625003", "officeType": "S.O", 
        "Deliverystatus": "Non-Delivery", "divisionname": "Madurai", 
        "regionname": "Madurai", "circlename": "Tamilnadu", 
        "Taluk": "Madurai South", "Districtname": "Madurai", 
        "statename": "TAMIL NADU", "Telephone": "0452-2373669", 
        "Related Suboffice": "NA", "Related Headoffice": "Madurai H.O", 
        "longitude": "NA", "latitude": "NA"
    }
]
```

` The first digit of a PIN indicates the zone, the second indicates the sub-zone, and the third, combined with the first two, indicates the sorting district within that zone. The final three digits are assigned to individual post offices within the sorting district. `