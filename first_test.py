from tkinter import *
from tkinter import ttk
import urllib.request
from bs4 import BeautifulSoup
from jira import JIRA

my_bugs = []
recent_bugs = []

def get_commit_id(*args):
    try: 
        #Clean list of bugs:
        for bug in my_bugs:
            my_bugs.remove(bug)
    except Exception as e:
        print(e)
    try:
        for bug in recent_bugs:
            recent_bugs.remove(bug)
    except Exception as e:
        print(e)
    try: 
        alljoyn_page = 'https://cgit.allseenalliance.org/core/alljoyn.git/commit/?h='+branch.get()
        ajtcl_page = 'https://cgit.allseenalliance.org/core/ajtcl.git/commit/?h='+branch.get()
        test_page = 'https://cgit.allseenalliance.org/core/test.git/commit/?h='+branch.get()
        alljoyn_git = BeautifulSoup(urllib.request.urlopen(alljoyn_page).read(), "lxml")
        ajtcl_git = BeautifulSoup(urllib.request.urlopen(ajtcl_page).read(), "lxml")
        test_git = BeautifulSoup(urllib.request.urlopen(test_page).read(), "lxml")
        ajn_id = alljoyn_git.find('table', {"summary" : "commit info"}).findChild('tr').findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        ajn_id = ajn_id[:ajn_id.find(" ")]
        tcl_id = ajtcl_git.find('table', {"summary" : "commit info"}).findChild('tr').findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        tcl_id = tcl_id[:tcl_id.find(" ")]
        tst_id = test_git.find('table', {"summary" : "commit info"}).findChild('tr').findNextSibling('tr').findNextSibling('tr').findChild('td').get_text()
        tst_id = tst_id[:tst_id.find(" ")]
        ajn_commit_id.set(ajn_id)
        tcl_commit_id.set(tcl_id)
        tst_commit_id.set(tst_id)
    except Exception as e:
        print(e)

    # Get Jira Bugs
    jira = JIRA('https://jira.allseenalliance.org', basic_auth=('tyler_gilbert', 'gonnabegood'))
    assigned_issues = jira.search_issues('project=ASACORE and issuetype=Bug and assignee=currentUser() and status!=Closed')
    if not assigned_issues:
        my_bugs_list.set("None")
    else:
        for bug in assigned_issues:
            my_bugs.append(bug.key+": "+bug.fields.summary)
        my_bugs_list.set(tuple(my_bugs))
    recently_logged = jira.search_issues('project=ASACORE and issuetype=Bug and created>=-1w')
    if not recently_logged:
        recent_bugs_list.set("None")
    else:
        for bug in recently_logged:
            recent_bugs.append(bug.key+": "+bug.fields.summary)
        recent_bugs_list.set(tuple(recent_bugs))

root = Tk()
root.title("IoT Lab Info")

mainframe = ttk.Frame(root, padding="2 8 8 28")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=2)
mainframe.columnconfigure(2, weight=2)
mainframe.rowconfigure(8, weight=2)

branch = StringVar()
ajn_commit_id = StringVar()
tcl_commit_id = StringVar()
tst_commit_id = StringVar()
my_bugs_list = StringVar(value=my_bugs)
recent_bugs_list = StringVar(value=recent_bugs)

ttk.Label(mainframe, text="Branch").grid(column=2, row=1, sticky=E)
branch_entry = ttk.Entry(mainframe, width=7, textvariable=branch)
branch_entry.grid(column=2, row=2, sticky=E)

ttk.Label(mainframe, text="AllJoyn Core:").grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, textvariable=ajn_commit_id).grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="AllJoyn Thin Core:").grid(column=1, row=4, sticky=E)
ttk.Label(mainframe, textvariable=tcl_commit_id).grid(column=2, row=4, sticky=W)
ttk.Label(mainframe, text="Test Tools:").grid(column=1, row=5, sticky=E)
ttk.Label(mainframe, textvariable=tst_commit_id).grid(column=2, row=5, sticky=W)

ttk.Button(mainframe, text="Get", command=get_commit_id).grid(column=2, row=6, sticky=E)

ttk.Label(mainframe, text="My Bugs").grid(column=1, row=7, sticky=W)
assigned_list = Listbox(mainframe, listvariable=my_bugs_list, height=7)
assigned_list.grid(column=1, row=8, sticky=(N, E, S, W))
assigned_scroll = ttk.Scrollbar(mainframe, orient=HORIZONTAL, command=assigned_list.yview)
assigned_scroll.grid(column=1, row=9, sticky=(W, E)) 
assigned_list['xscrollcommand'] = assigned_scroll.set
ttk.Label(mainframe, text="Recent Bugs").grid(column=2, row=7, sticky=W)
recent_list = Listbox(mainframe, listvariable=recent_bugs_list, height=7)
recent_list.grid(column=2, row=8, sticky=(N, E, S, W))
recent_scroll = ttk.Scrollbar(mainframe, orient=HORIZONTAL, command=recent_list.xview)
recent_scroll.grid(column=2, row=9, sticky=(W, E))
recent_list['xscrollcommand'] = recent_scroll.set


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

branch_entry.focus()
root.bind('<Return>', get_commit_id)

root.mainloop()
