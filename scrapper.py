from bs4 import BeautifulSoup
import requests
import json
import re
import pandas as pd

query="web developer"
def indeedParser(q):
    list =[]
    baseURL="https://www.indeed.com/jobs?q="
    q=q.replace(' ','+')
    url=baseURL+q
    source =requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    jobs = soup.find_all('div', {"class": "jobsearch-SerpJobCard"})
    for job in jobs:
        try:
            title = job.find('a', {"class": "jobtitle"})
            link ="https://www.indeed.com/"+ title.attrs["href"]
            salery = job.find("span", {"class": "salaryText"})
            summaryDiv = job.find("div", class_="summary")
        except:
            pass

        titleText = " " if isinstance(title, type(None)) else title.text.strip(' \n')
        salaryText = " " if isinstance(salery, type(None)) else salery.text.strip(' \n')
        summaryDiv = summaryDiv.text.strip(' \n')
        x = {
            "title": titleText,
            "salery": salaryText,
            "summary": summaryDiv,
            "link": link,
            "site":"indeed.com"
        }
        list.append(x)
    y = json.dumps(list)
    return y

def stackOverflowParser(q):
    list =[]
    baseURL="https://stackoverflow.com/jobs?q="
    q=q.replace(' ','+')
    url=baseURL+q
    source =requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    listResults=soup.find_all('div',{"data-jobid":re.compile('\d{6}')})
    for job in listResults:
        try:
            title = job.find('div', {"class":"-title"}).find('h2')
            link ="https://stackoverflow.com/"+ title.find('a').attrs["href"]
            salery = job.find("span", {"class": "-salary"})
            summaryDiv = job.find("div", class_="-perks")
        except:
            pass
        titleText = " " if isinstance(title, type(None)) else title.text.strip('\r\t\n ')
        salaryText = " " if isinstance(salery, type(None)) else salery.text.strip(' \r\t\n').replace("\n","").replace("\r","")
        summaryText =" " if isinstance(summaryDiv, type(None)) else "".join(summaryDiv.text.strip(' \r\t\n').replace("\n","").replace("\r","")).split(sep="                                   ")
        x = {
            "title": titleText,
            "salery": salaryText,
            "summary": summaryText,
            "link": link,
            "site":"stackoverflow.com"
        }
        list.append(x)
    y = json.dumps(list)
    return y

""" print(stackOverflowParser(query))
print(indeedParser(query))
 """
""" with open("json.json","w") as jsonData:
    jsonData.write(stackOverflowParser(query)) """
dfStack =pd.read_json(stackOverflowParser(query))
dfIndeed =pd.read_json(indeedParser(query))
df=dfStack.append(dfIndeed)
""" df.to_excel("jobs.xls") """
df.to_csv("jobs.csv")