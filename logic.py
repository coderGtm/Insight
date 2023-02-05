from pathlib import Path
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
        filePath = str(Path(filePath).parent)
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
    tables = getTableNames(cursor)
    #get num of rows in each table
    numOfRows = getNumOfRowsInAllTables(cursor, tables)
    # show tables
    ui.showTablesFrame(root, tables, numOfRows, cursor)

def getTableNames(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return tables

def getNumOfRowsInAllTables(cursor, tables):
    numOfRows = []
    for table in tables:
        tableName = table[0]
        cursor.execute("SELECT COUNT(*) FROM {0};".format(tableName))
        numOfRows.append(cursor.fetchall()[0][0])

    return numOfRows

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