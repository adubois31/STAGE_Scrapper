import requests
import urllib.parse
import sys
import config
import argparse

parser = argparse.ArgumentParser(description="Github code scrapper")
parser.add_argument("-r","--Req", type = str, metavar='', help="Searched code, avoid the spaces in the code search part", default="exec( language:php")
parser.add_argument("-n","--Page_num", type = int, metavar='', help="Page number of the search", default=1)
parser.add_argument("-p", "--Per_page",type = int, metavar='', help="Number of result per page", default=50)
args=parser.parse_args()


out_file=open("raw_page1_results.txt","a+")

request = {'q': (args.Req).strip()}

# request to the github api search code
request_enc = urllib.parse.urlencode(request)

api_req = f"https://api.github.com/search/code?{request_enc}&page={args.Page_num}&per_page={args.Per_page}"

headers = {
  "Authorization": f"Token {config.access_token}"
}

#Getting search results
response = requests.request("GET", api_req, headers=headers)

#Test if request was successful and if request rate is not exceeded
if (response.status_code != 200):
  print("request access fail")
  print(response.text)
  sys.exit(1)
elif ("message" in response.text):
  print("exceeded request rate, try later")
  sys.exit(2)

#Retrieving urls of each file code
data = response.json()
urls_list=[]
print("len of items :",len(data["items"]))
for item in data["items"] :
  urls_list.append(item["url"])

#retrieving the urls to the raw files 
raw_urls=[]
for url_elem in urls_list :
  resp=requests.get(url_elem,headers=headers)
  if (resp.status_code != 200):
    print("Error request for a raw url")
    pass
  out_file.write(resp.json()["download_url"]+"\n")
  raw_urls.append(resp.json()["download_url"])

print(len(raw_urls))
out_file.close()