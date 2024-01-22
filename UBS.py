import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def sendmail(recipient_email, update, notebook_name, erorUpdate, attachment_path):

    sender_email = 'deepakpythonwork@gmail.com'
    sender_password = 'uzed ghqu tkxz mjxf '
    email_template_path = "index.html"
    with open(email_template_path, "r") as template_file:
        email_template = template_file.read()
    email_template = email_template.replace("{row number}", str(update))
    email_template = email_template.replace("{notebook}", str(notebook_name))
    email_template = email_template.replace("{bug}", str(erorUpdate))
    subject = 'Update ' + ' ' + str(notebook_name)  


    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(email_template, 'html'))
    with open(attachment_path, "rb") as attachment_file:
        attachment = MIMEApplication(attachment_file.read(), _subtype="xlsx")
        attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path)
        message.attach(attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  
        server.login(sender_email, sender_password)  
        server.sendmail(sender_email, recipient_email, message.as_string()) 

        
import requests, json, os
import pandas as pd
from openpyxl import load_workbook
def getdata(start_date, end_date, rows, page):
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
        # 'Cookie': 'BIGipServervds2-app.prod.us.issapps.com_8330=2483286538.35360.0000; BIGipServervds.issgovernance.com_8120=889319946.47135.0000',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    params = {
        'customerID': 'MjU0',
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://vds.issgovernance.com/vds/',
        # 'Cookie': 'BIGipServervds2-app.prod.us.issapps.com_8330=2483286538.35360.0000; BIGipServervds.issgovernance.com_8120=889319946.47135.0000',
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

    response = requests.get('https://vds.issgovernance.com/vds/api/getVdsData/7', params=params, headers=headers)

    return response.json()['data']
def getTotalrow(start_date, end_date, rows, page):
     TRow= getdata(start_date, end_date, rows, page)[0]['TotalRows']
     return TRow
 
 
start_date = '2023-01-01'
end_date = '2023-12-31'
#processed  2709 of 18655 rows
file_name= 'UBS.xlsx'
rows = getTotalrow(start_date, end_date, 20, 1)
print(f"Total rows {rows}")
rowProcessed=0
data = getdata(start_date, end_date, rows, 1)
try:
    for i in range(2709, len(data)):
        dataDict = {"CompanyName": data[i]['CompanyName'], "Ticker": data[i]['Ticker'], "Country": data[i]['Country'], "SecurityID": data[i]['SecurityID'], "MeetingDate": data[i]['MeetingDate'], "MeetingType": data[i]['MeetingType'], "FundName": data[i]['FundName'], "MultipleFundIDs": data[i]['MultipleFundIDs'], "MeetingID": data[i]['MeetingID'] }
        print(f"processed  {i + 1} of {rows} rows" )
        companyData = getCompanydata(dataDict['MultipleFundIDs'], dataDict['MeetingID'])
        DataSheet = pd.DataFrame(companyData)
        if os.path.exists(file_name):
            rowProcessed=i
            df = pd.read_excel(file_name)
            df = df.append(DataSheet, ignore_index= True)
            df.to_excel(file_name, index=False)
        else:
            DataSheet.to_excel(file_name, index=False)
    sendmail("rohit45deepak@gmail.com", rowProcessed, "UBS", "Done file check", file_name)
    sendmail("eleanorpwilli@gmail.com", rowProcessed, "UBS", "Done file check", file_name)
except Exception as e:
    sendmail("rohit45deepak@gmail.com", rowProcessed, "UBS", e, file_name)
    sendmail("eleanorpwilli@gmail.com", rowProcessed, "UBS", e, file_name)
