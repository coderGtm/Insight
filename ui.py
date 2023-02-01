import tkinter as tk
from tkinter import ttk
import logic

def clearView(view):
    for widget in view.winfo_children():
        widget.destroy()

def showHomeFrame(root):
    # discard old frame
    clearView(root)
    # create frame
    homeFrame = tk.Frame(root)
    homeFrame.pack()
    # create label
    homeLabel = tk.Label(homeFrame,text="DB Viewer").pack()
    # create button
    openExplorerBtn = tk.Button(homeFrame,text="Select File", command=lambda: logic.selectFile(root)).pack()

def showTablesFrame(root, tables, cursor):
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

    tablesTree.bind("<Double-1>",lambda event: showTableDataFrame(root, tables, tablesTree, cursor))

    # create button to open the currently selected table in a new frame
    openTableBtn = tk.Button(tablesFrame,text="Open Table", command=lambda: showTableDataFrame(root, tables, tablesTree, cursor)).pack()

    # create button to go back to home frame
    backBtn = tk.Button(tablesFrame,text="Back", command=lambda: showHomeFrame(root)).pack()

def showTableDataFrame(root, tables, tablesTree, cursor):
    # get currently selected table
    selectedTable = tablesTree.item(tablesTree.focus())["values"][0]
    # discard old frame
    clearView(root)
    # create frame
    tableDataFrame = tk.Frame(root)
    tableDataFrame.pack()
    # create label
    tableDataLabel = tk.Label(tableDataFrame,text=selectedTable).pack()
    columnNames = logic.getColumnNames(selectedTable, cursor)
    data = logic.getTableData(selectedTable, cursor)
    # show table data in treeview widget with column names
    tableDataTree = ttk.Treeview(tableDataFrame)
    tableDataTree["columns"]=columnNames
    tableDataTree.column("#0", width=0, stretch=tk.NO)
    for i in range(len(columnNames)):
        tableDataTree.column(columnNames[i], width=500, minwidth=50, stretch=tk.NO)
        tableDataTree.heading(columnNames[i], text=columnNames[i],anchor=tk.W)
    tableDataTree.pack()
    # add data to treeview
    for i in range(len(data)):
        tableDataTree.insert("", i, text=i+1, values=data[i])

    # create button to go back to tables frame
    backBtn = tk.Button(tableDataFrame,text="Back", command=lambda: showTablesFrame(root, tables, cursor)).pack()