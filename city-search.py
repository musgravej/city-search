import requests
import configparser
from xml.etree import ElementTree


def city_lookup(zipcode):
    """
    Get list of City, State, ZIP when searching by ZIP code
    writes a tab-delimited file named city-st-zip.txt
    :param zipcode: zipcode as string
    :returns console output and tab-delimited file named city-st-zip.txt
    """

    url_query = (('http://production.shippingapis.com/'
                  'ShippingAPITest.dll?API=CityStateLookup'
                  '&XML=<CityStateLookupRequest '
                  'USERID="{userid}"><ZipCode ID="0">'
                  '<Zip5>{zip5}</Zip5></ZipCode>'
                  '</CityStateLookupRequest>').format(userid=userid, 
                                                      zip5=zipcode[:5]))

    response = requests.get(url_query)
    root = ElementTree.fromstring(response.content)

    for element in root.findall('*'):
        try:
            city = element.find('City').text
            state = element.find('State').text
            zip_reslt = element.find('Zip5').text
        except AttributeError:
            city = "n/a"
            state = ""
            zip_reslt = zipcode

        print("{0}\t{1}\t{2}".format(zip_reslt, city, state))


def init_api():
    global userid
    global password

    config = configparser.ConfigParser()
    config.read('config.ini')

    userid = config['api-credentials']['userid']
    password = config['api-credentials']['password']


def main():

    for zipcode in ['50201', '000', '90001', '40201', '98801', 
                    '12123']:

        city_lookup(zipcode)


if __name__ == '__main__':
    init_api()
    main()
