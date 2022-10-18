import requests
import urllib.parse
import sys
import config
import argparse
import time

parser = argparse.ArgumentParser(description="Github code scrapper")
parser.add_argument("-r","--Req", type = str, metavar='', help="Searched code, avoid the spaces in the code search part", default="exec( language:php")
parser.add_argument("-n","--Page_num", type = int, metavar='', help="Page number of the search", default=1)
parser.add_argument("-p", "--Per_page",type = int, metavar='', help="Number of result per page", default=40)
args=parser.parse_args()

headers = {
        "Authorization": f"Token {config.access_token}"
    }

out_file = open("top_raw_results","w+")

in_file=open("top_repo_results.txt","r")

#writes all urls in out_file
repos=in_file.readlines()
print("starting filling url file from top repos...")
for repo in repos:
    request=args.Req.strip()+f" repo:{repo.strip()}"
    full_request = {'q': request}
    # request to the github api search code
    request_enc = urllib.parse.urlencode(full_request)
    api_repo_req = f"https://api.github.com/search/code?{request_enc}&page={args.Page_num}&per_page={args.Per_page}"
    try :
        resp_repo = requests.get(api_repo_req, headers=headers,timeout=3)
    except :
        pass
    if (resp_repo.status_code != 200):
        print("request access fail")
        print(resp_repo.text)
        sys.exit(1)        
    data = resp_repo.json()
    if "message" in data :
        print("Fast as fuck boi",data)
        sys.exit(2)
    #building the list of github code urls
    urls_list = []
    for item in  data["items"] :
        urls_list.append(item["url"])
    #getting all raw urls in out_file
    for url in urls_list:
        try :
            r = requests.get(url,headers=headers, timeout=4)
            out_file.write(r.json()["download_url"]+"\n")
        except : 
            print("Error requesting raw url")
            pass
        
    time.sleep(3)


out_file.close()
in_file.close()



