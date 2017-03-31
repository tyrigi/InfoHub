import urllib.request
from bs4 import BeautifulSoup

branch='RB16.10'
alljoyn_page = 'https://cgit.allseenalliance.org/core/alljoyn.git/commit/?h='+branch
ajtcl_page = 'https://cgit.allseenalliance.org/core/ajtcl.git/commit/?h='+branch
test_page = 'https://cgit.allseenalliance.org/core/test.git/commit/?h='+branch

attempts=0
while True:
    try: 
        alljoyn_git = BeautifulSoup(urllib.request.urlopen(alljoyn_page, 'lxml').read())
        ajtcl_git = BeautifulSoup(urllib.request.urlopen(ajtcl_page, 'lxml').read())
        test_git = BeautifulSoup(urllib.request.urlopen(test_page, 'lxml').read())
        ajn_commit = alljoyn_git.find('table', {"summary" : "commit info"}).findChild('tr')
        ajn_commit = ajn_commit.findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        tcl_commit = ajtcl_git.find('table', {"summary" : "commit info"}).findChild('tr')
        tcl_commit = tcl_commit.findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        tst_commit = test_git.find('table', {"summary" : "commit info"}).findChild('tr')
        tst_commit = tst_commit.findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        ajn_commit_id = ajn_commit[:ajn_commit.find(" ")]
        tcl_commit_id = tcl_commit[:tcl_commit.find(" ")]
        tst_commit_id = tst_commit[:tst_commit.find(" ")]
        print("AllJoyn Core: ",ajn_commit_id)
        print("Thin Core: ",tcl_commit_id)
        print("Test Tools: ",tst_commit_id)
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
