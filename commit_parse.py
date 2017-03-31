import urllib.request
from bs4 import BeautifulSoup

branch = 'RB16.10'
MAX_ATTEMPTS = 4
commit_ids = []

alljoyn_page = 'https://cgit.allseenalliance.org/core/alljoyn.git/commit/?h='+branch
ajtcl_page = 'https://cgit.allseenalliance.org/core/ajtcl.git/commit/?h='+branch
test_page = 'https://cgit.allseenalliance.org/core/test.git/commit/?h='+branch
alljoyn_git = None
ajtcl_git = None
test_git = None

for attempts in range(0,MAX_ATTEMPTS):
    try:
        if (alljoyn_git == None):
            alljoyn_git = BeautifulSoup(urllib.request.urlopen(alljoyn_page).read(),"lxml")
        else:
            continue
        if (ajtcl_git == None):
            ajtcl_git = BeautifulSoup(urllib.request.urlopen(ajtcl_page).read(),"lxml")
        else:
            continue
        if (test_git == None):
            test_git = BeautifulSoup(urllib.request.urlopen(test_page).read(),"lxml")
        else:
            continue
    except Exception as e:
        print(e)

try:
    for soup in [alljoyn_git, ajtcl_git, test_git]:
        commit = soup.find('table', {"summary" : "commit info"}).findChild('tr').findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        id_string = commit[:commit.find(" ")]
        commit_ids.append(id_string+"\n")
except Exception as e:
    print(e)

with open('commits_record.txt', 'r') as file:
    commits_record = file.readlines()

if (commits_record[0] != commit_ids[0]):
    print("New AllJoyn Core version!")
    print(commit_ids[0],end='')
    commits_record[0] = commit_ids[0]
else:
    print("AllJoyn Core: ",commits_record[0],end='')

if (commits_record[1] != commit_ids[1]):
    print("New AllJoyn Thin Core version!")
    print(commit_ids[1],end='')
    commits_record[1] = commit_ids[1]
else:
    print("Thin Core:    ",commits_record[1],end='')

if (commits_record[2] != commit_ids[2]):
    print("New Test Tools version!")
    print(commit_ids[2],end='')
    commits_record[2] = commit_ids[2]
else:
    print("Test Tools:   ",commits_record[2],end='')







