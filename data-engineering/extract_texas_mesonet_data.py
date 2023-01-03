import mechanicalsoup
import requests

class parseMeso:

    def get_station_id(self,url:str):
        
        station_id_list = []

        response = requests.get(url)
        json_response = response.json()

        for data in json_response:
            station_id_list.append(data['stationId'])
    
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
       


def main():
    p = parseMeso()
    p.get_station_id('https://www.texmesonet.org/api/Stations')
    #p.parse_data_products_mesonet(24)    
    #print("Hello World!")

if __name__ == "__main__":
        main()
