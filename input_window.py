from tkinter import *
from tkinter import ttk
import urllib.request
from bs4 import BeautifulSoup

def get_commit_id(*args):
    try: 
        alljoyn_page = 'https://cgit.allseenalliance.org/core/alljoyn.git/commit/?h='+branch.get()
        alljoyn_git = BeautifulSoup(urllib.request.urlopen(alljoyn_page).read(), "lxml")
        commit_id.set(alljoyn_git.find('table', {"summary" : "commit info"}).findChild('tr').findNextSibling('tr').findNextSibling('tr').findChild('td').get_text())
    except Exception as e:
        print(e)

root = Tk()
root.title("Test Window")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

branch = StringVar()
commit_id = StringVar()

branch_entry = ttk.Entry(mainframe, width=7, textvariable=branch)
branch_entry.grid(column=2, row=1, sticky=(W,E))

ttk.Label(mainframe, textvariable=commit_id).grid(column=2, row=2, sticky=(W,E))
ttk.Button(mainframe, text="Get", command=get_commit_id).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Branch").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Has commit ID: ").grid(column=1, row=2, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

branch_entry.focus()
root.bind('<Return>', get_commit_id)

root.mainloop()
