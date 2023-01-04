import mechanicalsoup
import requests
from multiprocessing import cpu_count,Pool
import json
from concurrent.futures import ThreadPoolExecutor
import time,os

url1 = "https://api.synopticlabs.org/v2/stations/timeseries?stid=TWB{}&vars=precip_accum_fifteen_minute,precip_accum_five_minute,pressure,relative_humidity,soil_temp,soil_moisture,solar_radiation,air_temp,wind_direction,wind_gust,wind_speed&units=english&start=20{}01011200&end=20{}12311200&token=f626b8d4c80242d39ecceaa253c41aff"
years = [["16", "17"], ["18", "19"], ["20", "21"], ["22", "22"]]

class parseMeso:


    ##
    ## Get Stations from the API
    ##
    def get_station_id(self,url:str):
        
        station_id_list = []

        response = requests.get(url)
        json_response = response.json()

        for data in json_response:
            station_id_list.append(data['stationId'])

        return station_id_list

    ##
    ## NOT USED
    ##
    def parse_data_products_mesonet(self,station):

        browser = mechanicalsoup.Browser()
        url = 'https://www.texmesonet.org/DataProducts/CustomDownloads'
        page = browser.get(url)
        html_page = page.soup
        #print(html_page.select('div'))
        region = html_page.select('select')[0]
        region.select('option')[0]["value"] = 'Station'

        data_type = html_page.select('select')[1]
        data_type.select('option')[2]["value"] = 'Timeseries'

        #print(html_page.select('span'))
        start_date = html_page.find_all("div", {"class": "col50 field-container"})[2]
        start_date.select('input')[0]["value"] = '11/28/2022'
        
        end_date = html_page.find_all("div", {"class": "col50 field-container"})[3]
        end_date.select('input')[0]["value"] = '12/05/2022'
        
        station = html_page.find_all("div", {"class": "col50 field-container"})[4]
        station.select('input')[0]["value"] = 'Headwaters Ranch'

        interval = html_page.select('select')[3]
        interval.select('option')[0]["value"] = 'Daily'

        units = html_page.select('select')[5]
        units.select('option')[0]["value"] = 'US / Customary'

        #resp = browser.submit_selected()

        browser_state = mechanicalsoup.StatefulBrowser()
        browser_state.open(url)
        browser_state.select_form()
        print(browser_state.get_current_form().print_summary())

        #profile_page = browser.submit()

    def multi_parse_mesonet(self):

        links = []
        
        station_id_list = self.get_station_id('https://www.texmesonet.org/api/Stations')
        
        for i in range(len(station_id_list)):
            id_val = str(station_id_list[i])
            id_val = '0' + id_val if len(id_val) == 1 else id_val
            for year in years:
                links.append([url1.format(id_val, year[0], year[1]),id_val,year[0],year[1]])

        ##
        ## Multi-threadin to improve performance.
        ##
        with ThreadPoolExecutor(max_workers=20) as p:
            p.map(self.extract_links,links)

    def extract_links(self,url:list):
        absolute_path = os.path.dirname(__file__)
        relative_path = 'output_data'
        full_path = os.path.join(absolute_path, relative_path)
        x = requests.get(url[0])
        data = x.json()
        #print(data)
        #print(url[1], url[2], x.status_code)
        #path = "C:\Users\Nachiket Deo\LiquidPrep-ML\data-engineering\output_data
        
        with open(r'..\data-{}-{}-{}.json'.format(url[1], url[2], url[3]), 'w') as f:
            json.dump(data, f)



def main():
    
    start_time = time.perf_counter()
    pm = parseMeso()
    #pm.get_station_id('https://www.texmesonet.org/api/Stations')
    pm.multi_parse_mesonet()
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    # print stats
    print(f'Total execution time: {execution_time} secs')
    #p.parse_data_products_mesonet(24)    
    #print("Hello World!")

if __name__ == "__main__":
        main()
