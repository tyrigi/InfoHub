import urllib.request
from bs4 import BeautifulSoup

branch="RB16.10"

attempts=0
while True:
    try: 
        soup = BeautifulSoup(urllib.request.urlopen('https://cgit.allseenalliance.org/core/alljoyn.git/commit/?h='+branch, "lxml").read())
        commit = soup.find('table', {"summary" : "commit info"}).findChild('tr').findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        commit_id = commit[:commit.find(" ")]
        print(commit_id)
    except Exception as e:
        print(e)
        attempts+=1
        if (attempts == 4):
            break
    try:
        if (commit_id != None):
            break
    except:
        continue
