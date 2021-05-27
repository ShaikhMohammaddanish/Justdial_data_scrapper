'''
 
feel free to connect with me 
watsapp 9426951412
face book :- https://www.facebook.com/danish.shaikh.509

===>>> Danish Shaikh  <<<===

'''


from bs4 import BeautifulSoup
import urllib
import request
import urllib.request
import requests
import csv



def innerHTML ( element ) :
    return element.decode_contents ( formatter = "html" )


def get_name ( body ) :
    return body.find ( 'span', { 'class' : 'jcn' } ).a.string


def which_digit ( html ) :
    mappingDict = { 'icon-ji' : 9,
                    'icon-dc' : '+',
                    'icon-fe' : '(',
                    'icon-hg' : ')',
                    'icon-ba' : '-',
                    'icon-lk' : 8,
                    'icon-nm' : 7,
                    'icon-po' : 6,
                    'icon-rq' : 5,
                    'icon-ts' : 4,
                    'icon-vu' : 3,
                    'icon-wx' : 2,
                    'icon-yz' : 1,
                    'icon-acb' : 0,
                    }
    return mappingDict.get ( html, '' )


def get_phone_number ( body ) :
    i = 0
    phoneNo = "No Number!"
    try :

        for item in body.find ( 'p', { 'class' : 'contact-info' } ) :
            i += 1
            if (i == 2) :
                phoneNo = ''
                try :
                    for element in item.find_all ( class_ = True ) :
                        classes = [ ]
                        classes.extend ( element [ "class" ] )
                        phoneNo = str ( (which_digit ( classes [ 1 ] )) )
                except :
                    pass
    except :
        pass
    body = body [ 'data-href' ]
    soup = BeautifulSoup ( body, 'html.parser' )
    for a in soup.find_all ( 'a', { "id" : "whatsapptriggeer" } ) :
        # print (a)
        phoneNo = str ( a [ 'href' ] [ -10 : ] )

    return phoneNo [ 1 : ]


def get_rating ( body ) :
    rating = 0.0
    text = body.find ( 'span', { 'class' : 'star_m' } )
    if text is not None :
        for item in text :
            rating += float ( item [ 'class' ] [ 0 ] [ 1 : ] ) / 10

    return rating


def get_rating_count ( body ) :
    text = body.find ( 'span', { 'class' : 'rt_count' } ).string

    # Get only digits
    rating_count = ''.join ( i for i in text if i.isdigit ( ) )
    return rating_count


def get_address ( body ) :
    return body.find ( 'span', { 'class' : 'mrehover' } ).text.strip ( )


page_number = 1

#fields = [ 'Name', 'Phone', 'Rating', 'Rating Count', 'Address' ]
#phone +=

out_file = open ( 'justdialdata.csv', 'w' )
csvwriter = csv.writer ( out_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL )
csvwriter.writerow ( fields )

service_count = 1

url_part = input ( "give url \n" )
url = f"{url_part}-%s" % (page_number)
print ( url )

for i in range ( 1, 4 ) :
    url = f"{url_part}-%s" % (page_number)
    print ( url )
    req = urllib.request.Request ( url, headers = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)" } )
    page = urllib.request.urlopen ( req )
    # page=urllib2.urlopen(url)
    soup = BeautifulSoup ( page.read ( ), "html.parser" )
    services = soup.find_all ( 'li', { 'class' : 'cntanr' } )

    # Iterate through the 10 results in the page
    for service_html in services :

        # Parse HTML to fetch data
        dict_service = [ ]
        name = get_name ( service_html )
        print ( name ) ;
        phone = get_phone_number ( service_html )
        rating = get_rating ( service_html )
        count = get_rating_count ( service_html )
        address = get_address ( service_html )
        if name != None :
            dict_service.append ( name )
        if phone != None :
            print ( 'getting phone number' )
            dict_service.append ( phone )
        if rating != None :
            dict_service.append ( rating )
        if count != None :
            dict_service.append ( count )
        if address != None :
            dict_service.append ( address )

        # Write row to CSV
        csvwriter.writerow ( dict_service )

        print ( "#" + str ( service_count ) + " ", dict_service )
        service_count += 1

    page_number += 1
out_file.close ( )
