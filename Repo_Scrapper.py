import requests
import urllib.parse
import sys
import config
import argparse

parser = argparse.ArgumentParser(description="Github code scrapper")
parser.add_argument("-r","--Req", type = str, metavar='', help="Searched code, avoid the spaces in the code search part", default="exec( language:php")
parser.add_argument("-n","--Page_num", type = int, metavar='', help="Page number of the search", default=1)
parser.add_argument("-p", "--Per_page",type = int, metavar='', help="Number of result per page", default=50)
parser.add_argument("-t", "--Top_selected",type = int, metavar='', help="Number of selected repos", default=50)
args=parser.parse_args()


out_file=open("top_repo_results.txt","w+")

request = {'q': (args.Req).strip()}

# request to the github api search code
request_enc = urllib.parse.urlencode(request)

api_repo_req = f"https://api.github.com/search/repositories?{request_enc}&page={args.Page_num}&per_page={args.Per_page}&sort=stars"


headers = {
    "Authorization": f"Token {config.access_token}"
}

#Getting search results
response_repo = requests.request("GET", api_repo_req, headers=headers)

#Test if request was successful and if request rate is not exceeded
if (response_repo.status_code != 200):
    print("request access fail")
    print(response_repo.text)
    sys.exit(1)

#Retrieving names of top repos requested
data = response_repo.json()
repo_names_list=[]
print("len of items :",len(data["items"]))
index = 0
for item in  data["items"] :
    index+=1
    repo_names_list.append(item["full_name"])
    out_file.write(item["full_name"]+"\n")
    if (index >= args.Top_selected):
        break

print(len(repo_names_list))
out_file.close()
