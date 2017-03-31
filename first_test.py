from tkinter import *
from tkinter import ttk
import urllib.request
from bs4 import BeautifulSoup

def get_commit_id(*args):
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

root = Tk()
root.title("IoT Lab Info")

mainframe = ttk.Frame(root, padding="2 8 8 28")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

branch = StringVar()
ajn_commit_id = StringVar()
tcl_commit_id = StringVar()
tst_commit_id = StringVar()

ttk.Label(mainframe, text="My Bugs").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Recent Bugs").grid(column=2, row=1, sticky=W)

ttk.Label(mainframe, text="Branch").grid(column=2, row=3, sticky=E)
branch_entry = ttk.Entry(mainframe, width=7, textvariable=branch)
branch_entry.grid(column=2, row=4, sticky=E)

ttk.Label(mainframe, text="AllJoyn Core:").grid(column=1, row=5, sticky=W)
ttk.Label(mainframe, textvariable=ajn_commit_id).grid(column=2, row=5, sticky=W)
ttk.Label(mainframe, text="AllJoyn Thin Core:").grid(column=1, row=6, sticky=W)
ttk.Label(mainframe, textvariable=tcl_commit_id).grid(column=2, row=6, sticky=W)
ttk.Label(mainframe, text="Test Tools:").grid(column=1, row=7, sticky=W)
ttk.Label(mainframe, textvariable=tst_commit_id).grid(column=2, row=7, sticky=W)

ttk.Button(mainframe, text="Get", command=get_commit_id).grid(column=2, row=8, sticky=E)

#ttk.Label(mainframe, text="Has commit ID: ").grid(column=1, row=2, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

branch_entry.focus()
root.bind('<Return>', get_commit_id)

root.mainloop()
