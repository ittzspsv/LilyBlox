import requests
from bs4 import BeautifulSoup

class FruitValues():
    def __init__(self):
        self.rarity = ["", "common", "uncommon", "rare", "legendary", "mythical", "gamepass", "limited"]

    def _get_fruit_data(self, url):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com",
    }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            fruit_names = []
            name_elements = soup.select("h1.text-2xl.font-semibold")
            for name in name_elements:
                fruit_names.append(name.get_text(strip=True))

            fruit_values = []
            value_elements = soup.select("h2.text-2xl.contents")
            for value in value_elements:
                text = value.get_text(strip=True)
                if "," in text:
                    fruit_values.append(text)

            fruit_demand = []
            demand_elements = soup.select("h2.text-2xl.contents")
            for demand in demand_elements:
                text = demand.get_text(strip=True)
                if "/" in text:
                    fruit_demand.append(text)

            fruit_demand_type = []
            demand_type_elements = soup.select("h1.text-sm.font-medium")
            for demand_type in demand_type_elements:
                fruit_demand_type.append(demand_type.get_text(strip=True))

            while len(fruit_values) < len(fruit_names):
                fruit_values.append("Unknown")
            while len(fruit_demand) < len(fruit_names):
                fruit_demand.append("Unknown")
            while len(fruit_demand_type) < len(fruit_names):
                fruit_demand_type.append("Unknown")

            fruit_data = {}
            for name, value, demand, demand_type in zip(fruit_names, fruit_values, fruit_demand, fruit_demand_type):
                fruit_data[name] = {"Value": value, "Demand": demand, "Demand Type": demand_type}
            return fruit_data
        else:
            return "Failed to retrieve the webpage."

    def FetchFruitDetail(self, fruit_name):
        '''RETURNS THE DETAIL OF FRUIT SUCH AS Fruit Name, Fruit Value, Demand, Demand Type in a tuple'''
        for rarity_type in self.rarity:
            url = f'https://bloxfruitsvalues.com/{rarity_type}'
            fruit_data = self._get_fruit_data(url)

            if isinstance(fruit_data, dict) and fruit_name.title() in fruit_data:
                details = fruit_data[fruit_name.title()]
                return fruit_name.title(), details['Value'], details['Demand'], details['Demand Type']

        return f"Fruit '{fruit_name}' not found."
    
    def FetchFruitDetails_DictionaryType(self, fruit_name):
        '''RETURNS THE DETAIL OF FRUIT SUCH AS Fruit Name, Fruit Value, Demand, Demand Type in a dictionary type'''
        for rarity_type in self.rarity:
            url = f'https://bloxfruitsvalues.com/{rarity_type}'
            fruit_data = self._get_fruit_data(url)

            if isinstance(fruit_data, dict) and fruit_name.title() in fruit_data:
                details = fruit_data[fruit_name.title()]
                return {"FruitName" : fruit_name.title(), "Value" : details['Value'], "Demand" : details['Demand'], "Demand Type" : details['Demand Type']}
            
class Stock():
    def __init__(self):
        self.url = "https://fruityblox.com/stock"
        pass

    def _get_stock(self, stock_filter):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            fruit_names = [name.get_text(strip=True) for name in soup.select("h3.font-medium")]

            fruit_values = []
            value_elements = soup.select("span.text-sm.font-medium")
            for value in value_elements:
                text = value.get_text(strip=True)
                if "$" in text:
                    fruit_values.append(text)

            stock_types = [stock.get_text(strip=True) for stock in soup.select("span.text-xs.text-gray-400")]


            while len(fruit_values) < len(fruit_names):
                fruit_values.append("Unknown")
            while len(stock_types) < len(fruit_names):
                stock_types.append("Unknown")

            data = {}

            for name, value, stock_type in zip(fruit_names, fruit_values, stock_types):
                if stock_filter.lower() in stock_type.lower():
                    if name in data:
                        data[name]["Stock Type"].append(stock_type)

                    else:
                        data[name] = {"Value": value, "Stock Type": [stock_type]}

            return data
        else:
            return "Failed to scrape web data"
        
    def get_normal_stock(self):
        return self._get_stock("normal")
    
    def get_mirage_stock(self):
        return self._get_stock("mirage")