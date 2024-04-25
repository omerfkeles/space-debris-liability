#
# Created by Omer F. Keles (ORCID: 0000-0002-3004-1191)
#

# Import necessary modules
import requests
import pandas as pd
import time

# Open and close the API token
fh = open("discosweb-token.txt")
token = fh.read()
fh.close()

# API URL for the debris object data, courtesy of the European Space Agency (ESA)
URL = "https://discosweb.esoc.esa.int"

# Create empty list "olist" to store the debris object data
# Set the page size and start with the first page
olist = []
page_number = 1

# Access the DISCOSweb API and sort in ascending order by object ID, starting with the first 100 objects in page 1
# Pull paginated data of 100 objects at a time by looping through all 704 pages of the object database (as of 4/21/2024)
# Check if the request was successful by using if statement to test whether "response.status_code" is not equal to 200 (the HTTP status code for success)
# If request is not successful, print "response.status_code" and "response.text" (which may provide more detail about what went wrong), and stop the script immediately if the "assert False" statement is reached
# Set "doc" to the result of calling the .json() method of "response", which will parse the JSON returned by the ESA server and extend (not append, which only adds a single element rather than an iterable list) the list of data to "olist"
# Add a delay of 5 seconds to the execution of the script by using the sleep() function, which avoids overwhelming the API with requests
for page_number in range(1, 705):
    response = requests.get(
        f"{URL}/api/objects",
        
        headers = {
            "Authorization": f"Bearer {token}",
            "DiscosWeb-Api-Version": "2",
                  },
        
        params = {
            "page[size]": 100,
            "page[number]": page_number,
            "sort": "id",
                 },
                           )

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        assert False 

    doc = response.json()
    olist.extend(doc["data"])

    time.sleep(5)

# Set "colnames" to the first row of "olist" via "olist[0]" and "datarows" to the first debris object onwards via "olist[0:]"
colnames = olist[0]
datarows = olist[0:]

# Set "debris_objects" equal to calling pd.DataFrame(), with arguments "columns = colnames" and "data = datarows", to convert the data into a Pandas dataframe
debris_objects = pd.DataFrame(columns = colnames, data = datarows)

# Set the index of "debris_objects" to "id" and drop extraneous columns
debris_objects.set_index("id")
debris_objects = debris_objects.drop(columns = ["type", "relationships", "links"])

# Separate the key-value pairs of the dictionaries of attributes within the rows of the "attributes" column into their own separate columns and rows
# Convert the data under the "attributes" column of "debris_objects" from a dictionary to separate columns/rows by applying pd.Series (a one-dimensional array with axis labels) to every row under "attributes"
attributes = debris_objects["attributes"].apply(pd.Series)

# Drop the original "attributes" column
debris_objects = debris_objects.drop(columns = "attributes")

# Concatenate the original "debris_objects" dataframe with the new "attributes" dataframe, adding "axis = 1" to ensure the DataFrame objects are combined horizontally along the x-axis
debris_objects = pd.concat([debris_objects, attributes], axis = 1)

# Add a "Year" column with values that consist of the first four characters of values under the COSPAR ID ("cosparId") column, signifying the year a debris object was generated for objects with known origins
debris_objects["Year"] = debris_objects["cosparId"].str[:4]

# Save the updated dataframe to a local debris_objects.csv file that will be read and analyzed in the next script
debris_objects.to_csv("debris_objects.csv", index = False)