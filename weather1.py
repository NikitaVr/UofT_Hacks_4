import urllib2
import json
f = urllib2.urlopen('http://api.wunderground.com/api/6a28c24f2553611a/geolookup/conditions/q/43.665301,-79.395720.json')
#f = urllib2.urlopen('http://api.wunderground.com/api/6a28c24f2553611a/hourly/q/CA/San_Francisco.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_c']
feels_like = parsed_json['current_observation']['feelslike_c']
print "Current temperature in %s is: %s Degrees Celsius\n" % (location, temp_f)
print "Feels like: %s Degrees Celsius \n" % (feels_like)
#for doc in parsed_json:
    #print parsed_json[doc]

f.close()
