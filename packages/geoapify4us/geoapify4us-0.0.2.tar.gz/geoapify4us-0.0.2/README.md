# Geoapify4us
This is therepository to help using Geoapify website APIs to make maps or geojson files.

>**Note**
>This is the personal trial to publisthe first python package on PyPi.
>You can send me such email or message to let me know the problem or advice to improve this package.

## How to use?
Firstly, you need to get your own API key from 'Geoapify.com'
And please check the needed variables before you use this.
The variables for each method are as follows:

### single_isoline(lat, lon, cal_type, cal_mode, search_range, apiKey, filename)

>The variables are lattitude, longitude, type of calculation, moving mode, range of isoline map, APIkey, outputfilename.

ex) single_isoline(lat = 37.3, lon = 127.1, cal_type = 'distance', cal_mode = 'walk', search_range = 30, apiKey = 'YOUR_API_KEY', filename = 'output')


### multi_isoline(lat, lon, cal_type, cal_mode, search_range, apiKey, filename)

>The variables are lattitude, longitude, type of calculation, moving mode, multiple ranges of isoline map, APIkey, outputfilename.

ex) multi_isoline(lat = 37.3, lon = 127.1, cal_type = 'distance', cal_mode = 'walk', search_range = '5, 10, 15', apiKey = 'YOUR_API_KEY', filename = 'output')


>**Note**
>It can be modified after the package update.

