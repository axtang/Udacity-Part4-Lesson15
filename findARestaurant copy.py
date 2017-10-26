from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "W420GTMB3YROTK0IGPPQTSCV2JHHQV4UHRHKJKJC23KSFHFF"
foursquare_client_secret = "0FTWK1B30ZOMRALJVLKPJAL02VGGIEEO5VB1RZTHJZ5CWKVB"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20171026&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))
	h= httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])

	#3. Grab the first restaurant
	if result['response']['venues']:
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id']
		venue_name = restaurant['name']
		venue_address = restaurant['location']['formattedAddress']
		address = ""
		for i in venue_address:
			address += i + ""
		venue_address = address

		#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20171026&client_secret=%s' % (venue_id, foursquare_cliend_id, foursquare_client_secret))
		result = json.loads(h.request(url,'GET')[1])
		
		#5. Grab the first image
		if result['response']['photos']['items']:
			firstpic = result['response']['photo']['items'][0]
			prefix = firstpic['prefix']
			suffix = firstpic['suffix']
			imageURL = prefix = "300x300" + suffix

		#6. If no image is available, insert default a image url
		else:
			imageURL = "https://vice-images.vice.com/images/content-images-crops/2016/07/19/spirited-away-ghibli-miyazaki-15th-15-year-anniversary-best-animation-hannah-ewens-body-image-1468945005-size_1000.jpg?output-quality=75"

		#7. Return a dictionary containing the restaurant name, address, and image url	
		restaurantInfo = {'name': venue_name, 'address': venue_address, 'image': imageURL}
		print ("Restaurant Name: %s" % restaurantInfo['name'])
		print ("Restaurant Address: %s" % restaurantInfo['address'])
		print ("Image: %s \n" % restaurantInfo['image'])
		return restaurantInfo
	else:
		print ("No Restaurants Found for %s" % location)
		return "no Restaurants Found"

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
