

import csv
import statistics

# read and store coordinates into one dict. Keys: zip code or city/state
"""
its address and location, when its open,
the URL of the market’s website,
or a report of what types of goods are sold there.
"""
# , MarketName, Website, street, city, County, State, zip, Season1Date, Season1Time, Season2Date, Season2Time, Season3Date, Season3Time, Season4Date, Season4Time, x, y, Location, Credit, WIC, WICcash, SFMNP, SNAP, Bakedgoods, Cheese, Crafts, Flowers, Eggs, Seafood, Herbs, Vegetables, Honey, Jams, Maple, Meat, Nursery, Nuts, Plants, Poultry, Prepared, Soap, Trees, Wine, updateTime
class Market():

    def __init__(self, MarketName, website, street, city, county, state, zip_code, x, y, seasons_date_time, goods, location, updateTime):
        # basic info
        self.name = MarketName
        
        self.street = street
        self.city = city
        self.county = county
        self.state = state

        self.zip_code = zip_code

        self.coords = (y, x)

        self.goods = []
        for item in goods:
            self.goods.append([item[0], 'No']) # list of lists: [['name of product', 'Yes'], ['name of product','No']]
            if item[1].upper() == 'Y':
                self.goods[-1][1] == 'Yes' 
            
        self.seasons = seasons_date_time # list of lists: [[date, time], [date, time]]

        # more info
        self.URL = website
        self.location = location
        self.last_update = updateTime
        

    def calc_linear_dist(self, coords): # coords is a (lat, long) tuple
        pass

    def print_info(self, index, coords): # for when first found and presented to the user as an option
        print(str(index)+". "+self.name+ " : "+str(calc_linear_dist(coords)))

    def print_location(self):
        print(self.street+", \n"+self.city+", "+self.state+" "+self.zip_code)

    def print_when_open(self):
        pass

    def print_URL(self):
        print(self.URL)

    def print_goods(self):
        pass

    def print_misc(self):
        pass
    
    

field_index = {}
index_list = []

goods_index = []

all_markets = []

markets_by_zip = {}
markets_by_city = {}
markets_by_coords = {}
    
market_file = open('US Farmers Market Data.csv', newline='', encoding='latin-1')
##raw_market_data = market_file.readlines()

n = 0
for row in csv.reader(market_file):

    if n == 0:
        j = 0
        
        for field in row:
            field_index[field] = j
            index_list.append(field)
            j += 1
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

        goods = [[index_list[i], row[i]]   for i in range(field_index['Bakedgoods'], field_index['Wine']) ]       

        location = get('Location')
        updateTime = get('updateTime')
                         
        # store the current Market object as "market"
        market = Market(MarketName=MarketName, website=website, street=street, city=city, county=county,state=state,zip_code=zip_code,x=x,y=y,seasons_date_time=seasons_date_time,goods=goods,location=location,updateTime=updateTime) 

        all_markets.append(market)
        # store each market object in dict accessible with each of the three types of geographic data
        markets_by_zip[market.zip_code] = market
        markets_by_city[(market.city+", "+market.state).lower()] = market
        markets_by_coords[market.coords] = market
        
 
    n += 1

market_file.close()

print(field_index)
print()
print(index_list)
print(len(all_markets))


