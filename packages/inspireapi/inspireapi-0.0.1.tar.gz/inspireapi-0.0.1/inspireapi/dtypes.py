import requests 
import json
import os 

class Insight(object):
    def __init__(self, ticker: str):
        self.ticker = ticker    
        self._get() #first, search the stocks information
        self._get_insights() #get the insight data
        self._regress_data() #parse the data and return it as a inspire.Insight object
    
    def _get(self): 
        #first, we must search the stock 
        self.search_url = f"https://inspireinsight.com/api/search?query={self.ticker}"
        search_data = requests.get(self.search_url).json() 
        self.id = search_data[0]['id']
  
    def _get_insights(self): 
        assert (hasattr(self, 'id'))
        self.request_url = f"https://inspireinsight.com/api/tickers/{self.id}"
        self.__data = requests.get(self.request_url).json()

    def _regress_data(self): #make data pretty and pythonic + remove unwanted keys 
        self.data = dict()
        self.data['impact_score'] = self.__data['impactScore']
        self.data['enviromental_score'] = self.__data['environmentalScore']
        self.data['social_score'] = self.__data['socialScore']
        self.data['governance_score'] = self.__data['governanceScore']
        
        #get the criteria 
        self.data['criterion'] = [x['criterion']['name'] for x in self.__data['esgIssueCriteriaCount']]

    def dump(self): #utility function to write full json output to file; internal for devs
        with open('dump.json', 'w+') as f: 
            f.write(json.dumps(self.__data, indent=4))

        


    
if __name__ == "__main__":
    x = Insight('F') 
