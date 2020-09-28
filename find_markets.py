# Sam Bernstein, 5/8/15
"""

Prompts the user for their coordinates (latitude and longitude)
and a maximum distance.  Finds and prints the names of all farmers’
markets within that distance, along with the distance to those markets,
as the crow flies. The user can then select a market by entering a
number corresponding to the market to get more information about it.
From there a menu of categories will be printed and indexed with numbers
such that the user can enter a number to retrieve and print any of the
following: its address and location, when its open, the URL of the
market’s website, or a report of what types of goods are sold there.
At any point the user will be able to break out to either the coordinate
and maximum distance entry level or the market selection level
by entering -2 or -1, respectively.

"""
import statistics
import csv
import math

printing = False
def p_dev(*argv): # p_dev = development printing. A printing function that can be toggled for debugging.
    if printing:
        p = ''
        for obj in argv:
            p += str(obj)
        print(p)
    
# state abbr. conversion dictionary
abbr_to_state = { 
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

for key in abbr_to_state:
    abbr_to_state[key] = abbr_to_state[key].lower() # this is the laziest and easiest way to make the dict lower case and compatible with inputs
    
state_to_abbr = {abbr_to_state[key] : key for key in abbr_to_state } # reverse of above, for converting in other direction

p_dev(abbr_to_state)
p_dev()
p_dev(state_to_abbr)


# read and store coordinates into one dict. Keys: zip code or city/state
location_coords = {}

geo_file = open('zipcode.csv', "r")

n = 0
for line in geo_file:
    
    if line != '\n' and n > 0: #there are some empty lines in the file, and the first line is the column categories
        line_data = line.strip().split(',')

        # get rid of quotation marks encapsulating each value
        for i in range(len(line_data)): 
            new = ''
            for c in line_data[i]:
                if c != '"':
                    new += c
            line_data[i] = new

        zip_code = int(line_data[0])
        # store latitude and longitude as tuples
        location_coords[zip_code] = (float(line_data[3]), float(line_data[4])) # key is zip code
        location_coords[(line_data[1].lower()+', '+abbr_to_state[line_data[2]]).lower()] = (float(line_data[3]), float(line_data[4])) #"city, state" is key
        
    n += 1

geo_file.close()

####   End purely geographic data storing part ####



#### Read every line of the market data file and store the info for each market in a Market object.
#### Store every Market object in 3 dicts, for accessing via ZIP code, city/state, or raw coordinates
"""
its address and location, when its open,
the URL of the market’s website,
or a report of what types of goods are sold there.
"""
# , MarketName, Website, street, city, County, State, zip, Season1Date, Season1Time, Season2Date, Season2Time, Season3Date, Season3Time, Season4Date, Season4Time, x, y, Location, Credit, WIC, WICcash, SFMNP, SNAP, Bakedgoods, Cheese, Crafts, Flowers, Eggs, Seafood, Herbs, Vegetables, Honey, Jams, Maple, Meat, Nursery, Nuts, Plants, Poultry, Prepared, Soap, Trees, Wine, updateTime
class Market():

    def __init__(self, MarketName, website, street, city, county, state, zip_code, x, y, seasons_date_time, goods, location, updateTime, n):
        
        self.name = MarketName
        
        self.street = street
        self.city = city
        self.county = county
        self.state = state

        try:
            self.zip_code = int(zip_code)
        except ValueError:
            self.zip_code = None

        if x == '' or y == '':
            self.coords = (None, None)
        else:
            self.coords = (float(y), float(x))

        self.goods = []
        for item in goods:
     
            if item[1] == 'Y':
                self.goods.append([item[0],'Yes'])  # list of lists: [['name of product', 'Yes'], ['name of product','No']]
            else:
                self.goods.append([item[0], 'No'])

        if 1000 < n < 1004:
            p_dev()
            p_dev(self.goods)
            
        
        self.seasons = seasons_date_time # list of lists: [[date, time], [date, time]]

        # more info
        self.URL = website
        self.location = location
        self.last_update = updateTime
        

    def calc_straight_dist(self, input_coords): # coords is a (lat, long) tuple
        valid = True
        
        for val in self.coords:
            if val == None or val == '':
                valid = False

        for val in input_coords:
            if val == None or val == '':
                valid = False
            
        if valid:

            a1 = math.radians(input_coords[0])
            b1 = math.radians(input_coords[1])

            a2 = math.radians(self.coords[0])
            b2 = math.radians(self.coords[1])

            r_earth = 3963.1676 # in miles
            
            return math.acos(math.cos(a1)*math.cos(b1)*math.cos(a2)*math.cos(b2) + math.cos(a1)*math.sin(b1)*math.cos(a2)*math.sin(b2) + math.sin(a1)*math.sin(a2)) * r_earth
        
        return 100000000000000000000 # if coordinates of market are not known, make sure it is not within the maximum distance entered
            

    def print_info(self, index, input_coords = [None, None]): # for when first found and presented to the user as an option
        valid = True
        
        for val in self.coords:
            if val == None or val == '':
                valid = False

        for val in input_coords:
            if val == None or val == '':
                valid = False

        if valid:
            print(str(index)+". "+self.name+ " : "+str(round(self.calc_straight_dist(input_coords), 2))+" miles")
        else:
            print(str(index)+". "+self.name+ " : in your city or ZIP")

    def print_location(self):
        print(self.name+":")
        print(self.street+"\n"+self.city+", "+state_to_abbr[self.state.lower()]+" "+str(self.zip_code))
        if self.coords[0] != None:
            print("(latitude, longitude) = "+str(self.coords[0])+", "+str(self.coords[1]))

    def print_when_open(self):
        something_there = False
        something_here = False
        final = ''
        print("Market open during the following times:")
        for season in self.seasons:
            something_here = False
            if not(season[0] == '' and season[1] == '') or (season[0] == None and season[1] == None):
                something_here = True
                for field in range(2):
                    if season[field] != '' and season[field] != None:
                        final += str(season[field])
                        if field == 0:
                            final += ", "
                        something_there = True
            if something_here:
                final += "\n"

        final = final[:len(final)-2:] # gets rid of excess final new line "\n" at the end
        if something_there:
            print(final)
        else:
            print("No information found about when the market is open.")
                

    def print_goods(self):
        print("Does this market have")
        for item in self.goods:
            print(item[0].ljust(11),"-",item[1])

    def print_misc(self):
        print(self.URL)
        if self.location.strip() != '':
            print("Location info: "+self.location)
        print("Information last updated",self.last_update)

    def info_dict(self, index):
        if index == 1:
            self.print_location()
        if index == 2:
            self.print_when_open()
        if index == 3:
            self.print_goods()
        if index == 4:
            self.print_misc()
            
        print()

        

field_index = {}
index_list = []

goods_index = []

all_markets = []

markets_by_zip = {}
markets_by_city = {}
markets_by_coords = {}

market_zips = []

market_file = open('US Farmers Market Data.csv', newline='', encoding='latin-1')
##raw_market_data = market_file.readlines()

n = 0
for row in csv.reader(market_file):

    if n == 0: # store field info for columns from first row
        j = 0
        
        for field in row:
            field_index[field] = j
            index_list.append(field)
            j += 1

        p_dev()
        p_dev(field_index)
        p_dev()
        p_dev(index_list)

    else:
        
        def get(field): 
            global field_index
            return row[field_index[field]]
        # the function above makes the retrieval below easier
        MarketName = get('MarketName')
        website = get('Website')
        street = get('street')
        city = get('city')
        county = get('County')
        state = get('State')
        zip_code = get('zip')            
        x = get('x')
        y = get('y')

        seasons_date_time = [[row[i], row[i+1]] for i in range(field_index['Season1Date'], field_index['Season4Time'] + 1, 2) ]

        goods = []
        for i in range(field_index['Bakedgoods'], field_index['Wine'] + 1, 1):
            goods.append([index_list[i], row[i]])

##        goods = [[index_list[i], row[i]] for i in range(field_index['Bakedgoods'], field_index['Wine'] + 1) ]

        
        if 1000 < n < 1004:
            p_dev("\n"+str(n)+"\n")
            p_dev(goods)

        location = get('Location')
        updateTime = get('updateTime')
                         
        # store the current Market object as "market"
        market = Market(MarketName=MarketName, website=website, street=street, city=city, county=county,state=state,zip_code=zip_code,x=x,y=y,seasons_date_time=seasons_date_time,goods=goods,location=location,updateTime=updateTime, n=n) 

        all_markets.append(market)
        # store each market object in dict accessible by each of the three types of geographic data
        if market.zip_code in markets_by_zip: # if already in dictionary, add market to the list           
            markets_by_zip[market.zip_code].append( market )
        else:
            markets_by_zip[market.zip_code] = [market] # if ZIP code not already in dictionary, add market to new list

        city_state_key = (market.city+", "+market.state).lower()
        if city_state_key in markets_by_city:
            markets_by_city[city_state_key].append(market)
        else:
            markets_by_city[city_state_key] = [market]
            
        markets_by_coords[market.coords] = market

        if zip_code != '':
            market_zips.append(zip_code)
        
    n += 1

p_dev()
p_dev("All zips: ",len(market_zips)    )
count = 0
for f in markets_by_zip:
    count += len(markets_by_zip[f])
p_dev("All markets in dict:", count)
p_dev()

market_file.close()
"""
print(field_index)
print()
print(index_list)
print(len(all_markets))
"""
#####  End data storage and organization part, begin UI part #####

max_distance = 0
search_results = []
user_location = ''
results_index = 1

search = ''

info_type = '' # info type values: 'zip', 'coords

print("This program allows you to search for nearby farmers markets by accessing a database of all farmers markets in the United States.")
print("First enter geographically locating information in one of the following forms:")
print("1. city, state (e.g. los angeles, CA)\n2. ZIP code (e.g. 90210)\n3. latitude, longitude (e.g. 34.014556, -118.015495)")
print("Note: for longitudes, 118 W is equivalent to -118, and for latitudes, 34 N is equivalent to 34.", end =' ')
print("You must input the coordinates without letters.")
print("If at any point you would like to exit the program, enter -2. If at any point you would like to break out of a retrieval loop, enter -1.")


def display_market_info(market):

    for f in range(1,5):
        market.info_dict(f)

    return -1


def select_market(input_location, info_type, max_distance, first):
    search_results = []
    
    input_coords = [None, None] # coordinates that are entered by user or are found from city or zip code. Default to None
    
    if info_type == 'zip':
        try:
            for m in markets_by_zip[input_location]:
                search_results.append(m) # add all markets in same zip code to search results
        except KeyError:
            print("KEY ERROR WITH ZIP CODE INPUT")

        try:
            input_coords = location_coords[input_location]
        except KeyError:
            pass

        p_dev("input_coords found: ", input_coords)

    elif info_type == 'city':
        try:
            for m in markets_by_city[input_location]:
                search_results.append(m)

        except (KeyError, ValueError) as e:
            print("city reading error:  " + str(e))

        try:
            input_coords = location_coords[input_location]
        except KeyError:
            pass

    if info_type == 'coords':
        input_coords = input_location

    # find markets within max_distance
    for m in all_markets:
        if m.calc_straight_dist(input_coords) < max_distance:
            search_results.append(m)
    

    # print all search results
    if len(search_results) == 0:
        print("Your search did not find any farmers markets.")
        return -1
    elif first or len(search_results) < 4:
        if len(search_results) == 1:
            print("\nOnly one market found:")
            
        for f in range(len(search_results)): # this loop prints all the search results for the user
            search_results[f].print_info(f+1, input_coords)
        print()
        first = False

    if len(search_results) != 1:
        while True:
            try:
                selection = input("Select a market by number: ")
                print()
                selection = int(selection)

                if selection == -1:
                    return -1
                elif selection == -2:
                    return -2

                selection = selection - 1
                if 0 <= selection <= len(search_results) - 1:
                    break
                else:
                    print("Market number entry out of range. Please pick an indexed number shown.")
                
            except ValueError:
                print("Not a valid number. Please enter an indexed integer shown.")
    else:
        selection = 0
            
    while True:
        status = display_market_info(search_results[selection])

        if len(search_results) == 1:
            return -1
        elif status == -1:
            break
        elif status == -2:
            return -1
        elif status <= -3:
            return -2

    return 0
    
def enter_location():

    if printing:

        all_multiples = []
        for key in markets_by_zip:
            if len(markets_by_zip[key]) > 3:
                all_multiples.append(key)

        print(all_multiples)
    
    
    while True:
        info_type = '' # reset info type for new search
        final_search = []
        error_message = '\n'
        
        print()
        search = input("Enter a location:")

        if ',' in str(search): # either city/state or coordinates

            first_half = ''
            for c in search:
                if c != ',':   # gets all characters up to first comma
                    first_half += c
                else:
                    p_dev("it broke out at the comma")
                    break

            l_first = len(first_half)
            
            skip = 0
            for i in range(l_first, len(search)):
                if search[i] == ',' or search[i] == ' ':
                    skip += 1
                else:
                    break

            
            second_half = search[l_first + skip::] # get second half of the entry
            
            p_dev("First half:")
            p_dev(first_half)
            p_dev("Second half:")
            p_dev(second_half)

            try:
                latitude = float(first_half)  # try coordinates                
                longitude = float(second_half)

                final_search = (latitude, longitude)
##                final_search.append(latitude)
##                final_search.append(longitude)
                info_type = 'coords'
                break
                

            except ValueError:
                pass

            try: # try city, state
                city = first_half.lower()
                state = second_half.lower()

                p_dev(city+", "+state)

                if not(state.upper() in abbr_to_state or state in state_to_abbr):
                    error_message += "Could not interpret the state you entered."
                    raise ValueError("Couldn't find entered state in dicts.")
                    
                elif state.upper() in abbr_to_state:
                    state = abbr_to_state[state.upper()]
                    p_dev("It got to the abbrevation to state conversion part.", state)
                
                final_search = city+", "+state

                if final_search not in location_coords and final_search not in markets_by_city:
                    error_message += "Could not understand the city you entered."
                    raise ValueError("Words")
        
                info_type = 'city'
                break

            except ValueError:
                pass

        try:
            zip_c = search
            if len(search) > 5:
                zip_c = search[0:5]
                p_dev("Was more than 5 chars, now: ", zip_c)
                
            final_search = int(zip_c) # simple zip code

            p_dev("it got past int conversion")
            if final_search <= -1:
                return -1


            if final_search not in location_coords and final_search not in markets_by_zip:
                error_message = 'Could not match the entered zip code with any actual zip codes.'
                raise ValueError("zip code not found")

            
            p_dev("Search converted to int: ", search)

            info_type = 'zip'
            break

            ### check if there's a zip code match and add market to search_results
            
        except ValueError:
            pass

        if error_message == '\n':        
            print("\nYour search could not be understood. If you are searching by city and state or by coordinates, make sure to use one separating comma.")
        else:
            print(error_message)
            
    while True:
        max_distance_input = input("Enter a maximum distance to the search results, in miles: ")

        try:
            max_distance = float(max_distance_input)

            try:
                choice = int(max_distance_input)

                if -3 <= choice <= -1:
                    return -1
            except ValueError:
                pass

            if max_distance < 0:
                print("\nI'm sorry, but in this reality distances cannot be negative. Please try again.\n")
            elif max_distance < 0.003:
                print("You do not live in a farmers market, and if you did you wouldn't be searching for that one. Please enter another number.")
            else:
                break
            
        except ValueError:
            print("Your entry cound not be understood. Please enter a positive number.")

    first = True
    while True:
        status = select_market(final_search, info_type, max_distance, first)
        first = False
        if status == -1:
            break
        elif status <= -2:
            return -1
    return 0


while True:
    if enter_location() <= -1: 
        break


print("Program exited.")



"""
References:

http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/
http://stackoverflow.com/questions/12752313/unicodedecodeerror-in-python-3-when-importing-a-csv-file
docs.python.org

Coordinate distance formula:
http://mathforum.org/library/drmath/view/51711.html


"""











