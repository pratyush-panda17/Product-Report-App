from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import database
import functionality

def window_event(event):
    if root.attributes('-fullscreen'):
        data.config(height=31)
    else:
        data.config(height=25)

def focusNext(event):
    wid = root.focus_get()
    par =wid.winfo_parent()
    if(par == '.!labelframe2.!labelframe'):
        row = wid.grid_info()["row"]
        col = wid.grid_info()["column"]
        if event.keysym == 'Down' and row == 0:
            generator.winfo_children()[1].focus_set()
            generator.winfo_children()[1].selection_range(0,END)

        if event.keysym == 'Up' and row == 1:
            generator.winfo_children()[0].focus_set()
            generator.winfo_children()[0].selection_range(0,END)

def insertInExcel(values,btls):
    (ovf,sku,rd,wstg) = functionality.getNumbers(values)
    btc_sz = btls * (ovf + sku) * rd * (1 + float(wstg))/1000
    info = (values[0],values[1],values[2],values[3],values[5],
           int(btls),btc_sz,values[9][0],btc_sz*float(values[10][0]))
    data.insert("",'end',values=info)

    for i in range(1,len(values[9])):
        tup = ("","","","","","","",values[9][i],btc_sz*float(values[10][i]))
        data.insert("",'end',values=tup)
    l = "----------------------"
    lines = (l,l,l,l,l,l,l,l,l)
    data.insert("",'end',values=lines)

def getReport():
    pName = productName.get()
    if pName=="":
        messagebox.showinfo(title="Error",message="Please enter a product name")

    else:
        product = database.search(pName)
        if product == None:
            messagebox.showinfo(title="Error",message="Record does not exist")

        btls = bottles.get()
        if product !=None and not btls.isdigit():
            messagebox.showinfo(title="Error",message="The number of bottles must be a natural number")

        if product != None and btls.isdigit():
             insertInExcel(product,float(btls))

def clearAllExcel():
    for row in data.get_children():
        data.delete(row)

def uploadFile():
    root.filename = filedialog.askopenfilename(initialdir="/",title="Select File",
                                           filetypes=(("excel files","*.xlsx"),))
    if root.filename !="":
        functionality.getData(root.filename)

def downloadReport():
    excel_data =[]
    for child in data.get_children():
        excel_data.append(data.item(child)["values"])
    if excel_data==[]:
        messagebox.showinfo(title="",message="No generated reports")
    else:
            save_file = filedialog.asksaveasfilename(defaultextension=".xlsx",initialdir="",title="Save File",
                                                 filetypes=(("Excel Files","*.xlsx"),))
            if save_file:
                functionality.makeExcelSheet(excel_data,save_file)

#----------------------------------------------GUI--------------------------------------------------#
root = Tk()
root.title("Report Generator")

#-----------------------------EXCEL SHEET VIEWER----------------------------------#

data_section = ttk.LabelFrame(root,style="TLabelframe")
data_section.grid(row=0,column=0,columnspan=2,padx=(45,25),pady=15,sticky=N)

data_frame = ttk.Frame(data_section)
data_frame.grid(row=0,column=0,columnspan=2)

yscrollbar = ttk.Scrollbar(data_frame)
yscrollbar.pack(side=RIGHT,fill=Y)

cols = ('Client','Brand','Product','Variant','SKU(ml)',
        'No. of Pieces','Total Batch Size (Kg)','Ingredient','Weight (Kg)')

data = ttk.Treeview(data_frame, yscrollcommand=yscrollbar.set, columns=cols,
                    show='headings')

data.column("Client",width=170,stretch=False)
data.heading("Client",text="Client")


for column in cols[1:]:
    data.column(column,width=150,stretch =False)
    data.heading(column,text=column)

data.pack()

yscrollbar.config(command=data.yview)

excelClearAllBtn = ttk.Button(data_section, text = "Clear All",command=clearAllExcel)
excelClearAllBtn.grid(row=1,column=1,sticky=E,padx=20)

#-----------------------------EXCEL SHEET VIEWER----------------------------------#

#----------------------------------REPORT GUI--------------------------------------#

report = ttk.LabelFrame(root,style="TLabelframe")
report.grid(row=1,column=1,sticky=(N,W))

#----------------Generate Report---------------#

generator = ttk.LabelFrame(report)
generator.grid(row=1,column=0,columnspan=2,padx=10,pady=10,sticky=(N))

productName = ttk.Entry(generator)
bottles = ttk.Entry(generator, text = "Enter Number of Bottles",width=20)
get_report_btn = ttk.Button(generator,text="Get Report",width=10, command=getReport)

productName.grid(row=0,column=0)
productName.insert(0,"Product Name")

bottles.grid(row=1,column=0,pady=10)
bottles.insert(0,"No. of bottles")

get_report_btn.grid(row=2,column=0)

#----------------Generate Report---------------#

upload_fileBtn = ttk.Button(report,text="Upload File",command = uploadFile)
upload_fileBtn.grid(row=2,column=0,padx=10,pady=10)
download_reportBtn = ttk.Button(report,text="Download Report",command=downloadReport)
download_reportBtn.grid(row=2,column=1,padx=10,pady=10)


#----------------------------------REPORT UI--------------------------------------#

root.bind('<Up>',lambda event: focusNext(event))
root.bind('<Down>',lambda event: focusNext(event))
root.bind("<Configure>", window_event)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

root.mainloop()
#----------------------------------------------GUI--------------------------------------------------#