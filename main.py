import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import sqlite3

# logic
def selectFile():
    prevFilePath = getPrevFilePath()
    filePath = filedialog.askopenfilename(initialdir=prevFilePath, title="Select a Database",filetypes=(("Database Files","*.sqlite3"),("All Files","*.*")))
    if (filePath == () or filePath == ""):
        return
    saveFilePath(filePath)
    openDB(filePath)

def saveFilePath(filePath):
    with open("filePath.txt", "w") as f:
        f.write(filePath)

def getPrevFilePath():
    try:
        with open("filePath.txt", "r") as f:
            filePath = f.read()
            return filePath
    except:
        return ""

def openDB(filePath):
    # connect to database
    conn = sqlite3.connect(filePath)
    if (conn == None):
        print("Error: Could not connect to database")
        return
    cursor = conn.cursor()
    # get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # show tables
    showTablesFrame(tables, cursor)

def getColumnNames(tableName, cursor):
    cursor.execute("PRAGMA table_info(" + tableName + ")")
    columns = cursor.fetchall()
    columnNames = []
    for column in columns:
        columnNames.append(column[1])

    return columnNames
    
def getTableData(tableName, cursor):
    cursor.execute("SELECT * FROM " + tableName)
    data = cursor.fetchall()
    return data
    

# gui
def clearView(view):
    for widget in view.winfo_children():
        widget.destroy()

def showHomeFrame():
    # discard old frame
    clearView(root)
    # create frame
    homeFrame = tk.Frame(root)
    homeFrame.pack()
    # create label
    homeLabel = tk.Label(homeFrame,text="DB Viewer").pack()
    # create button
    openExplorerBtn = tk.Button(homeFrame,text="Select File", command=selectFile).pack()

def showTablesFrame(tables, cursor):
    # discard old frame
    clearView(root)
    # create frame
    tablesFrame = tk.Frame(root)
    tablesFrame.pack()
    # create label
    tablesLabel = tk.Label(tablesFrame,text="Tables").pack()
    # show tables in treeview widget with titles Sr no, Table Name, Rows Count
    tablesTree = ttk.Treeview(tablesFrame)
    tablesTree["columns"]=("one","two")
    tablesTree.column("#0", width=50, minwidth=50, stretch=tk.NO)
    tablesTree.column("one", width=100, minwidth=100, stretch=tk.NO)
    tablesTree.column("two", width=100, minwidth=100, stretch=tk.NO)
    tablesTree.heading("#0",text="Sr no",anchor=tk.W)
    tablesTree.heading("one", text="Table Name",anchor=tk.W)
    tablesTree.heading("two", text="Rows Count",anchor=tk.W)
    tablesTree.pack()
    # add data to treeview
    for i in range(len(tables)):
        tablesTree.insert("", i, text=i+1, values=(tables[i][0],i+1))

    # create button to open the currently selected table in a new frame
    openTableBtn = tk.Button(tablesFrame,text="Open Table", command=lambda: showTableDataFrame(tables, tablesTree, cursor)).pack()

    # create button to go back to home frame
    backBtn = tk.Button(tablesFrame,text="Back", command=showHomeFrame).pack()

def showTableDataFrame(tables, tablesTree, cursor):
    # get currently selected table
    selectedTable = tablesTree.item(tablesTree.focus())["values"][0]
    # discard old frame
    clearView(root)
    # create frame
    tableDataFrame = tk.Frame(root)
    tableDataFrame.pack()
    # create label
    tableDataLabel = tk.Label(tableDataFrame,text=selectedTable).pack()
    columnNames = getColumnNames(selectedTable, cursor)
    data = getTableData(selectedTable, cursor)
    # show table data in treeview widget with column names
    tableDataTree = ttk.Treeview(tableDataFrame)
    tableDataTree["columns"]=columnNames
    tableDataTree.column("#0", width=0, stretch=tk.NO)
    for i in range(len(columnNames)):
        tableDataTree.column(columnNames[i], width=100, minwidth=100, stretch=tk.NO)
        tableDataTree.heading(columnNames[i], text=columnNames[i],anchor=tk.W)
    tableDataTree.pack()
    # add data to treeview
    for i in range(len(data)):
        tableDataTree.insert("", i, text=i+1, values=data[i])

    # create button to go back to tables frame
    backBtn = tk.Button(tableDataFrame,text="Back", command=lambda: showTablesFrame(tables, cursor)).pack()




# start gui in main
if __name__ == "__main__":
    root = tk.Tk()
    showHomeFrame()
    root.mainloop()