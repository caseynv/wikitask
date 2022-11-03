# install all the necessary dependencies
!pip install mwapi
!pip install pywikibot
'''
mwapi is a MIT-licensed library provides a very simple convenience wrapper around the MediaWiki API, including support for authenticated sessions. 
It requires Python 3 and that your wiki is using MediaWiki 1.15.3 or greater.'''

# import all the necessary dependencies
import requests
import json
import mwapi #importing mwapi
import re #importing regular expression
import pywikibot #import pywikibot dependencies
from pywikibot.data.sparql import SparqlQuery #import dependencies for sparql query

def get_categories_list(title, lang) -> list:
    
    """
    gets all the categories of the file using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        categories_list ([string]): list containing all the categories from the api associated with the file
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )

    params = {
            "action": "query",
            "prop":"categories",
            "titles":title,
            "clshow": "hidden", #this shows part of the categories not all changing this to !hidden shows the remaining categories
            "format": "json",
    }

    response = session.get(params) #get request for the wikiapi
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0] # gets the pageid
    categories = response_pages[page_id]['categories'] #gets values of the categories the file belongs to
    categories_list = [categories_item['title'] for categories_item in categories] # loops through the categories list from the api to get the title
    
    return categories_list

#get_categories_list('File:Açude_Cedro_-_Detalhe_do_acabamento_da_barragem_principal.jpg', lang='commons')

def get_hidden_categories_list(title, lang) -> list:
    
    """
    gets all the hidden categories of the file using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        categories_hidden_list ([string]): list containing all the hidden categories from the api associated with the file
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )

    params = {
            "action": "query",
            "prop":"categories",
            "titles":title,
            "clshow": "!hidden", #Which kind of categories to show.
            "format": "json",
    }

    response = session.get(params) #get request for the wikiapi
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0] # gets the pageid
    categories = response_pages[page_id]['categories'] #gets values of the categories the file belongs to
    categories_hidden_list = [categories_item['title'] for categories_item in categories]  # loops through the categories list from the api to get the title
    
    return categories_hidden_list

#get_hidden_categories_list('File:Açude_Cedro_-_Detalhe_do_acabamento_da_barragem_principal.jpg', lang='commons')


def get_metadata_item(title, lang) -> str:
    
    """
    metadata of the file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        all metadata and their values as strings
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang), #lang can vary depending on the api and language working with eg lang can be fr, as, commons, en etc
        user_agent="Outreachy round fall 2022"
    )

    params = {
            "action": "query",
            "prop":"imageinfo", #Returns file information and upload history. from the api https://commons.wikimedia.org/w/api.php?action=help&modules=query
            "titles":title,
            "iiprop":"metadata", #Which file information to get eg metadata, size, dimension, mime
            "iimetadataversion":"latest", #Version of metadata to use. If latest is specified, use latest version. Defaults to 1 for backwards compatibility
            "format": "json",
    }

    response = session.get(params)
    response_imageinfo = response['query']['pages']  #selects the query -> pages dictionary from the api response
    page_id = list(response_imageinfo.keys())[0] #automates how to extract information using the pageid than manually entering it
    imageinfo = response_imageinfo[page_id]['imageinfo']
    
    for response_value in imageinfo:
        response_item = response_value['metadata'] #selects the metadata dictionary
        for metadata_value in response_item: #loops through this list
            if type(metadata_value['value']) == list: #some of the metadata further have a list of dictionaries that give more information
                for i in range (len(metadata_value['value'])-1): # looping through this list and extracting these informations
                    print(metadata_value["name"], '-> ', metadata_value['value'][i]['name'], '->', metadata_value['value'][i]['value'])
                    
            else: #conditional when the value of the metadata is not a list
                print(metadata_value["name"], '-> ', metadata_value['value'])
            
            
#get_metadata_item('File:Açude_Cedro_-_Detalhe_do_acabamento_da_barragem_principal.jpg', lang='commons')

def get_summary_data(title, lang) -> str:
    
    """
    summary data of te file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string):+  the particular wikipedia api needed eg en, fr, commons

    Returns:
        DateTimeOriginal|Categories|License|LicenseUrl|ImageDescription|Credit|GPSLatitude|GPSLongitude
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )

    params = {
            "action": "query",
            "prop":"imageinfo",
            "titles": title,
            "iiprop":"extmetadata",
            "format": "json",
    }

    response = session.get(params) #get request for the wikiapi
    response_pages = response['query']['pages'] 
    page_id = list(response_pages.keys())[0]  # gets the pageid
    imageinfo = response_pages[page_id]['imageinfo']
    
    for response_item in imageinfo:
        response_metadata = response_item['extmetadata']
        
        print(title)
        
        print("DateTimeOriginal", '-> ', response_metadata["DateTimeOriginal"]['value'])
        print("DateTime", '-> ', response_metadata["DateTime"]['value'])
        print('Categories', '-> ', response_metadata['Categories']['value'])
        print('License', '-> ', response_metadata['License']['value'])
        
        try:  #the artist difer for different artist some are embedded in a link others are not
            artist_value = re.findall(r"<a\b[^>]*>([^<]+)<\/a>", response_metadata["Artist"]['value']) # regex to extract the artist name from anchor html tags
            print("Artist", '-> ', artist_value[0])
        except:
            artist_value = re.findall(r"<span[^>]*>(.*?)</span>", response_metadata["Artist"]['value']) # regex to extract the image description from anchor html tags
            print("Artist", '-> ', artist_value[0])
        
        try: #the license url is absent for some files in commons
            print('LicenseUrl', '-> ', response_metadata['LicenseUrl']['value'])
        except:
            continue
            
        try: #the credit value difer for different artist some are embedded in a link others are not
            credit_value = re.findall(r"<span\b[^>]*>([^<]+)<\/span>", response_metadata["Credit"]['value']) # regex to extract the credit from span html tags
            print("Credit", "-> ", credit_value[0])
        except:
            print("Credit", "-> ", response_metadata["Credit"]['value'])
            
        try: #the imagedescription difer for different artist some are embedded in a link others are not
            image_value = re.findall(r"(.*?)<a\b[^>]*>([^<]+)<\/a>", response_metadata["ImageDescription"]['value']) # regex to extract the image description from anchor html tags
            print("ImageDescription", "-> ", image_value[0][0], image_value[0][1])
        except:
            print("ImageDescription", "-> ", response_metadata["ImageDescription"]['value'])
        
        try: #some files do not have camera location
            print("GPSLatitude", '-> ', response_metadata["GPSLatitude"]['value'])
            print("GPSLongitude", '-> ', response_metadata["GPSLongitude"]['value'])
        except KeyError:
            continue 
        
        
#get_summary_data('File:Açude_Cedro_-_Detalhe_do_acabamento_da_barragem_principal.jpg', lang='commons')

def get_all_files_data(title, lang) -> str:
    
    """
    summary data of te file on the homepage using api: https://commons.wikimedia.org/w/api.php

    Args:
        title (string): the title of the commons file
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        DateTimeOriginal|Categories|License|LicenseUrl|ImageDescription|Credit|GPSLatitude|GPSLongitude
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )

    params = {
            "action": "query",
            "prop":"imageinfo",
            "titles": title,
            "iiprop":"extmetadata|commonmetadata|size|dimensions|mime|mediatype", #the type of file information to get
            "format": "json",
    }


    response = session.get(params)
    response_pages = response['query']['pages'] 
    
    page_id = list(response_pages.keys())[0]  # automates the pageid for each file/a file 
    imageinfo = response_pages[page_id]['imageinfo'] # retrieves the value of item imageinfo
    
    for response_item in imageinfo: #loops through the imageinfo list
        for response_item_keys in list(response_item.keys()): #automate the keys of the response_item dictionary to get the values
            
            if type(response_item[response_item_keys]) == list: #conditional statement if the values is a list
                for response_item_nestedkeys in response_item[response_item_keys]: #loop through this list
                    if type(response_item_nestedkeys['value']) == list:  #conditional statement if the value of the above list is a list
                        for nested_keys in response_item_nestedkeys['value']: #loop through this list
                            print(response_item_nestedkeys['name'], '-> ', nested_keys['name'], '-> ', nested_keys['value'])
                    else:
                        print(response_item_nestedkeys['name'], ' -> ', response_item_nestedkeys['value'])
                    
            elif isinstance(response_item[response_item_keys], dict): #conditional statement if the values is a dictionary
                for response_itemkeys in list(response_item[response_item_keys].keys()): #automate the keys of the response_itemkeys dictionary to get the values
                    if response_itemkeys == 'ImageDescription': #conditional statement if the dictionary value is a ImageDescription inorder to use this particular regex to extract image description
                        try: #the imagedescription difer for different artist
                            image_value = re.findall(r"(.*?)<a\b[^>]*>([^<]+)<\/a>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the image description from anchor html tags
                            print("ImageDescription", "-> ", image_value[0][0], image_value[0][1])

                        except:
                            print("ImageDescription", "-> ", response_item[response_item_keys][response_itemkeys]['value'])
                            
                    elif response_itemkeys == 'Artist': #conditional statement if the dictionary value is an artist inorder to use this particular regex to extract artist name
                        try: #the artist difer for different artist
                            artist_value = re.findall(r"<a\b[^>]*>([^<]+)<\/a>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the artist from anchor html tags
                            print("Artist", '-> ', artist_value[0])
                        except:
                            artist_value = re.findall(r"<span\b[^>]*>([^<]+)<\/span>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the artist from anchor html tags
                            print("Artist", '-> ', artist_value[0])
                    
                    elif response_itemkeys == 'Credit': #conditional statement if the dictionary value is a credit property inorder to use this particular regex to extract credit
                        try: #the credit difer for different artist
                            credit_value = re.findall(r"<span\b[^>]*>([^<]+)<\/span>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the credit from span html tags
                            print("Credit", "-> ", credit_value[0])
                        except:
                            credit_value = re.findall(r"(.*?)<a\b[^>]*>([^<]+)<\/a>", response_item[response_item_keys][response_itemkeys]['value']) # regex to extract the credit from span html tags
                            print("Credit", "-> ", credit_value[0][0], credit_value[0][1])
                            
                    else:
                        print(response_itemkeys, ' -> ', response_item[response_item_keys][response_itemkeys]['value'])
                        
            else:
                print(response_item_keys, ' -> ', response_item[response_item_keys])
    
#get_all_files_data('File:Açude_Cedro_-_Detalhe_do_acabamento_da_barragem_principal.jpg', lang='commons')

def get_all_files_subcat(cat_title, lang='commons') -> list:
    
    """
    files/images of wikidata item for subcategory

    Args:
        cat_title (string): the title/name of the category of interest
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
         files_list ([string]): the title of the files/images of wikidata item for category(subcategory) for each wikidata id in a category
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )
    params_1 = {
                "action": "query",
                "generator":"categorymembers", #Get information about all categories used in the page
                "gcmlimit": 500,
                "gcmtitle": cat_title,
                "gcmnamespace": 6,
                "format": "json",
        }
    
    response = session.get(params_1)
    pageids = list(response['query']['pages'].keys())
    
    files_list=[]
    for pageid in pageids:
        files = response['query']['pages'][str(pageid)]['title']
        files_list.append(files)
    return files_list

#get_all_files_subcat('Category:2021 in São Paulo (state)', lang='commons')

def get_all_files_cat(cat, lang):
    
    """
    files/images of all the subcategory in a category

    Args:
        cat_title (string): the title/name of all the files in each subcategory in a category of interest
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
         cat_file_list([string]): the title of the files/images of wikidata item for each subcategory in a category
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )
    
    params = {
            "action": "query",
            "list":"categorymembers", #Get information about all categories used in the page
            "cmtitle": cat,
            "cmtype": 'subcat', #get sub categories in a category
            "format": "json",
    }

    response = session.get(params) #get request for the wikiapi to get the category members pageid
    category_member = response['query']['categorymembers']
    
    cat_file_list=[]
    for category_item in category_member:
        cat_title = category_item['title']
        files = get_all_files_subcat(cat_title, lang='commons')
        #print(cat_title, ' -> ', files)
        cat_file_list += files
        
    return cat_file_list

#get_all_files_cat('Category:Top_contributors_of_Wiki_Loves_Monuments_2020_in_Brazil', lang='commons')

def get_wikidata(cat, lang) -> list:
    
    """
    unique wikidata item for each image in all subcategory of a category of interest

    Args:
        cat (string): the title/name of the category of interest
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
        new_wikidata_list ([string]): the unique wikidata item for each image in a category
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )
    
    params = {
            "action": "query",
            "generator":"categorymembers", #Get information about all categories used in the page
            "gcmlimit": 500,
            "gcmtitle": cat,
            "gcmnamespace": 6,
            "format": "json",
    }

    response = session.get(params) #get request for the wikiapi to get the category members pageid
    pageids = list(response['query']['pages'].keys()) #automatically get the pageids
    
    wikidata_list=[]
    for pageid in pageids:
        pageid_number = "M" + str(pageid)
        params_1 = {
            "action": "wbgetentities", #Gets the data for multiple Wikibase entities.
            "ids": str(pageid_number),
            "format": "json",
        }

        response_1 = session.get(params_1) #get request for the wikiapi to get the data/information about this pageid_number passed
        pagetitle = response_1.get('entities').get(pageid_number).get('title')
        property_depict = response_1.get('entities').get(pageid_number).get('statements').get('P180', 'XX') #P180 is the wikidata property number for depicts
        
        if "XX" not in str(property_depict):
            
            depictslist=[]
            for dict_place in range(0, len(property_depict)): #get the mainsnak dictionary
                try:
                    wikidata_num = property_depict[dict_place]['mainsnak']['datavalue']['value']['id'] #get the wikidata number 

                    params_2 = {
                        "action": "wbgetentities", #Gets the data for multiple Wikibase entities.
                        "ids": str(wikidata_num),
                        "props": "labels",
                        "languages": "en",
                        "format": "json",
                    }

                    response_2 = session.get(params_2) #get request for the wikiapi to get information about the wikidata number got
                    depicts = response_2.get('entities', 'XX').get(wikidata_num).get('labels', 'XX').get('en', 'XX') #The names of the properties to get back from each entity. Will be further filtered by any languages given.
                    
                    if "XX" not in str(depicts):
                        info = str(depicts['value']) + " (" + str(wikidata_num) + ")" #gets the depict value and their respective wikidata number
                        #depictslist.append(info)
                        wikidata_list.append(wikidata_num)
                        
                except:
                    continue 
            else:
                continue
                
        else:
            continue
            
    new_wikidata_list=[]
    for list_item in wikidata_list:
        
        if list_item not in new_wikidata_list: #further ensure the wikidata numbers in the list are unique
            new_wikidata_list.append(list_item)
            
    return new_wikidata_list
            
#get_wikidata('Category:Images_by_Prburley_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

#this function gets the label and description of selected properties(i chose properties depicted in the cultu)

def get_labels_description_subcat(cat, lang):
    
    """
    labels and description of the location, heritage, street address, and description of unique wikidata item for each image in all subcategory of a category of interest 

    Args:
        cat (string): the title/name of the category of interest
        lang(string): the particular wikipedia api needed eg en, fr, commons

    Returns:
         response_item[response_keys]['value'] (string): the value of the labels and description of the location, heritage, street address, and description for each wikidata id in a category
    """
    
    session = mwapi.Session(
        host="https://{0}.wikimedia.org/w/api.php".format(lang),
        user_agent="Outreachy round fall 2022"
    )
    
    params = {
            "action": "query",
            "list":"categorymembers", #Get information about all categories used in the page
            "cmtitle": cat,
            "cmtype": 'subcat', #get sub categories in a category
            "format": "json",
    }

    response = session.get(params) #get request for the wikiapi to get the category members pageid
    category_member = (response['query']['categorymembers']) #get the list of all the subcategories
   

    for category_item in category_member:
        
        wikidata_list = get_wikidata(category_item['title'], lang='commons')
        print('\n', category_item['title'])
        
        for wikidata_item in wikidata_list:
            
            sparql = """
            SELECT 
                 ?item ?itemLabel ?itemDescription 
                  ?locationLabel ?locationDescription  
                  ?streetLabel  
                  ?descriptionLabel 
                  ?heritageLabel
                WHERE {
                  VALUES ?item { wd:"""+wikidata_item+""" }
                  ?item wdt:P131 ?location ;
                        wdt:P1435 ?heritage .
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                  OPTIONAL {?item 
                        wdt:P6375 ?street ;
                        wdt:P973 ?description ;}
                }
            """
            
            wikiquery = SparqlQuery() #sparqlquery that allows the use of sparql queries with python
            response = wikiquery.query(sparql)
            results = response['results']['bindings'] #get list of all the response results
            
            for response_item in results:
                
                for response_keys in list(response_item.keys()):
                    print(response_keys, ' -> ', response_item[response_keys]['value'])

            
#get_labels_description_subcat('Category:Top_contributors_of_Wiki_Loves_Monuments_2020_in_Brazil', lang='commons')

# list of commons files selected

files_list = get_all_files_subcat('Category:Images_by_Ana_Beatriz_Sampaio_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

for title in files_list: #loops through the list of commons files
    print(title, ' -> ', get_categories_list(title, lang='commons'))
    print('\n')

# list of commons files selected

files_list = get_all_files_subcat('Category:Images_by_Ana_Beatriz_Sampaio_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

for title in files_list: #loops through the list of commons files
    print(title, ' -> ', get_hidden_categories_list(title, lang='commons'))
    print('\n')

# list of commons files selected

files_list = get_all_files_subcat('Category:Images_by_Ana_Beatriz_Sampaio_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

for title in files_list: #loops through the list of commons files
    get_all_files_data(title, lang='commons')
    print('\n')

# list of commons files selected

files_list = get_all_files_subcat('Category:Images_by_Ana_Beatriz_Sampaio_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

for title in files_list: #loops through the list of commons files
    get_summary_data(title, lang='commons')
    print('\n')

# list of commons files selected

files_list = get_all_files_subcat('Category:Images_by_Ana_Beatriz_Sampaio_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

for title in files_list:  #loops through the list of commons files
    get_metadata_item(title, lang='commons')
    print('\n')

# list of commons files selected

files_list = get_all_files_subcat('Category:Images_by_Ana_Beatriz_Sampaio_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

for title in files_list:  #loops through the list of commons files
    
    hidden_list = get_hidden_categories_list(title, lang='commons')
    non_hidden_list = get_categories_list(title, lang='commons')
    all_categories_list = non_hidden_list + hidden_list #get all the categories that is, the hidden plus the unhidden categories
    print(all_categories_list)
    print('\n')

files_list = get_all_files_subcat('Category:Images_by_Ana_Beatriz_Sampaio_in_Wiki_Loves_Monuments_2021_in_Brazil', lang='commons')

all_category=[]
for title in files_list:  #loops through the list of commons files
    all_categories_list = get_categories_list(title, lang='commons') + get_hidden_categories_list(title, lang='commons') #get all the categories that is, the hidden plus the unhidden categories
    all_category += all_categories_list
    
new_all_category_list=[]
for list_item in all_category: #list got from the addition of all the hidden and unhidden category list is filtered to remove category repetition
        
    if list_item not in new_all_category_list: #further ensure the categories in the list are unique to avoid repetition
        new_all_category_list.append(list_item)
for cat in all_categories_list: #looping through the list
    
    if 'Category:Pages with maps' not in cat: #category:pages with maps, amongst others have no entities so this filters it out
        try:
            info = get_labels_description_subcat(cat, lang='commons')
        except:
            continue
                
print('\n', info)



#Thoughts
'''
The function get_all_files_subcat gives a list of files in a subcategory while get_all_files_cat gives a list of all files in all the subcategory present in the category. This is to prevent hard coding any file name or subcategory. The function get_all_files_cat still goes through further filter the list to ensure no repetition of the wikidata id. Also the all_category list got from the addition of all the hidden and unhidden category list is filtered to remove category repetition.

All these functions ensures that we get all the details from a category/files with or without subcategory. The function get_labels_description_subcat is used to extract information present in the cultural property which cannot be got from the mediawiki api (iwlink gives the wikidata id) as well as the wikidata label and description and other necessary information that might be of use.
'''






















