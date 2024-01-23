import requests
import json

def getdata(start_date, end_date, rows, page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://vds.issgovernance.com/vds/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    params = {
        'customerID': 'MjU0',
        # 'fromDate': '2023-01-01',
        # 'toDate': '2023-09-30',
        'fromDate': start_date,
        'toDate': end_date,
        'liveSiteYN': '1',
        'random': '0.49761613755807876',
        'locale': 'en',
        'MeetingTypeList': '',
        'CountryList': '',
        'VotedList': '',
        '_search': 'false',
        'nd': '1705577300279',
        'rows': rows,
        'page': page,
        'SortByColumn': 'CompanyName',
        'OrderBy': 'asc',
    }

    response = requests.get('https://vds.issgovernance.com/vds/api/getVdsData/14', params=params, headers=headers)
    return response.json()['data']



def getCompanydata(MultipleFundIDs, MeetingId):
    cookies = {
        'BIGipServervds2-app.prod.us.issapps.com_8330': '2483286538.35360.0000',
        'BIGipServervds.issgovernance.com_8120': '889319946.47135.0000',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://vds.issgovernance.com/vds/',
         'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    params = {
        'customerID': 'MjU0',
        'fromDate': '',
        'toDate': '',
        'fundValue': MultipleFundIDs,
        'liveSiteYN': '1',
        'meetingID': MeetingId,
        'random': '0.956757217578498',
        'locale': 'en',
        '_search': 'false',
        'nd': '1705577418341',
        'rows': '2000',
        'page': '1',
        'SortByColumn': 'Proposal',
        'OrderBy': 'asc',
    }

    response = requests.get('https://vds.issgovernance.com/vds/api/getVdsData/7', params=params, cookies=cookies, headers=headers)

    return response.json()['data']


data = getdata('2023-01-01', '2023-09-30', 20, 1)
ResultData = []
for i in data:
    dataDict = {"CompanyName": i['CompanyName'], "Ticker": i['Ticker'], "Country": i['Country'], "SecurityID": i['SecurityID'], "MeetingDate": i['MeetingDate'], "MeetingType": i['MeetingType'], "FundName": i['FundName'], "MultipleFundIDs": i['MultipleFundIDs'], "MeetingID": i['MeetingID'] }
    print(dataDict)
    companyData = getCompanydata(dataDict['MultipleFundIDs'], dataDict['MeetingID'])
    print(companyData)