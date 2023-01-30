from tkinter import filedialog
import sqlite3
import ui

def selectFile(root):
    prevFilePath = getPrevFilePath()
    filePath = filedialog.askopenfilename(initialdir=prevFilePath, title="Select a Database",filetypes=(("Database Files","*.sqlite3"),("All Files","*.*")))
    if (filePath == () or filePath == ""):
        return
    saveFilePath(filePath)
    openDB(root, filePath)

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

def openDB(root, filePath):
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
    ui.showTablesFrame(root, tables, cursor)

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