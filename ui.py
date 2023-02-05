import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logic

def clearView(view):
    for widget in view.winfo_children():
        widget.destroy()

def showHomeFrame(root):
    # discard old frame
    clearView(root)
    # set Title
    root.title("Insight")
    # create frame
    homeFrame = tk.Frame(root)
    homeFrame.pack()
    # create label
    titleLabel = tk.Label(homeFrame,text="Insight", font=("Helvetica",50)).pack(padx=50,pady=20)
    subTitleLabel = tk.Label(homeFrame,text="Database Viewer", font=("Terminal",20)).pack(padx=50,pady=10)
    # create button
    openExplorerBtn = tk.Button(homeFrame,text="SELECT FILE", command=lambda: logic.selectFile(root), font=("Berlin",25)).pack(padx=50,pady=20)

def showTablesFrame(root, tables, numOfRows, cursor):
    # discard old frame
    clearView(root)
    #set title
    root.title("Insight | Tables")
    # create frame
    tablesFrame = tk.Frame(root)
    tablesFrame.pack()
    # create label
    tablesLabel = tk.Label(tablesFrame,text="Tables", font=("Arial",30)).pack(pady=20)
    # show tables in treeview widget with titles Sr no, Table Name, Rows Count
    tablesTree = ttk.Treeview(tablesFrame)
    tablesTree["columns"]=("one","two")
    tablesTree.column("#0", minwidth=50, stretch=tk.NO)
    tablesTree.column("one", minwidth=100, stretch=tk.NO)
    tablesTree.column("two", minwidth=50, stretch=tk.NO)
    tablesTree.heading("#0",text="Sr no",anchor=tk.W)
    tablesTree.heading("one", text="Table Name",anchor=tk.W)
    tablesTree.heading("two", text="Rows Count",anchor=tk.W)
    tablesTree.pack(padx=20)
    # add data to treeview
    for i in range(len(tables)):
        tablesTree.insert("", i, text=i+1, values=(tables[i][0],numOfRows[i]))

    tablesTree.bind("<Double-1>",lambda event: showTableDataFrame(root, tables, tablesTree, cursor, numOfRows))

    # create button to go back to home frame
    backBtn = tk.Button(tablesFrame,text="Back", font=("Courier",20), command=lambda: showHomeFrame(root)).pack(pady=20)

def showTableDataFrame(root, tables, tablesTree, cursor, numOfRows):
    # get currently selected table
    try:
        selectedTable = tablesTree.item(tablesTree.focus())["values"][0]
    except IndexError:
        messagebox.showerror("No Table Selected", "Double-click a table to open it.")
        return
    except ValueError:
        messagebox.showerror("No Tables present.", "This Database is empty.")
    # discard old frame
    clearView(root)
    #set title
    root.title("Insight | {0}".format(selectedTable))
    # create frame
    tableDataFrame = tk.Frame(root)
    tableDataFrame.pack()
    # create label
    tableDataLabel = tk.Label(tableDataFrame,text=selectedTable, font=("Arial",30)).pack(pady=20)
    columnNames = logic.getColumnNames(selectedTable, cursor)
    data = logic.getTableData(selectedTable, cursor)
    # show table data in treeview widget with column names
    tableDataTree = ttk.Treeview(tableDataFrame)
    tableDataTree["columns"]=columnNames
    tableDataTree.column("#0", width=0, stretch=tk.NO)
    for i in range(len(columnNames)):
        tableDataTree.column(columnNames[i], minwidth=50, stretch=tk.NO)
        tableDataTree.heading(columnNames[i], text=columnNames[i],anchor=tk.W)
    tableDataTree.pack(padx=20)
    # add data to treeview
    for i in range(len(data)):
        tableDataTree.insert("", i, text=i+1, values=data[i])

    tk.Label(tableDataFrame, text="Double-click on a row to expand it.", font=("System",10)).pack(pady=20)

    tableDataTree.bind("<Double-1>",lambda event: showRowDetails(tableDataTree, data, columnNames))

    # create button to go back to tables frame
    backBtn = tk.Button(tableDataFrame,text="Back", font=("Courier",20), command=lambda: showTablesFrame(root, tables, numOfRows, cursor)).pack(pady=20)

def showRowDetails(tableDataTree, data, columnNames):
    # get currently selected row
    try:
        selectedRowIndex = int(tableDataTree.item(tableDataTree.focus())["text"])-1
    except IndexError:
        messagebox.showerror("No Row Selected", "Double-click a row to expand it.")
        return
    except ValueError:
        messagebox.showerror("No Rows present", "This relation is empty.")
        return

    rowString = ""
    for i in range(len(columnNames)):
        colString = "{0}: {1}".format(columnNames[i], data[selectedRowIndex][i])
        rowString += colString
        rowString += "\n---------------------\n"

    messagebox.showinfo("Expanded Row", rowString)