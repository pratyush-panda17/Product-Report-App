import pandas as pd
import xlsxwriter
import database

global cols 
cols = ('Client','Brand','Product','Variant','SKU(ml)','No. of Pieces',
        'Total Batch Size (Kg)','Ingredient','Weight (Kg)')

def makeExcelSheet(data,path):
    global cols
    report = xlsxwriter.Workbook(path)
    sheet = report.add_worksheet("Sheet 1")

    f1=report.add_format({'bg_color':'black'})

    index =0
    for column in cols:
        sheet.set_column(index,index,20)
        sheet.write(0,index,column)
        index+=1

    index = 1
    for row in data:
        if(row[0]!="----------------------"):
            sheet.write_row(index,0,row)
        else:
            for i in range(len(cols)):
                sheet.write(index,i,"",f1)
        index+=1 
    report.close()



def insertInDb(products):
    for pdt in products:
        ingredients = ""
        weights = ""
        for i in range(9,len(pdt)):
            if i%2==1:
                ingredients = ingredients + str(pdt[i])+","
            else:
                weights = weights + str(pdt[i])+","
        database.addOne((str(pdt[0]),str(pdt[1]),str(pdt[2]),str(pdt[3]),str(pdt[4]),str(pdt[5]),
                         str(pdt[6]),str(pdt[7]),str(pdt[8]),ingredients[0:len(ingredients)-1],weights[0:len(weights)-1]))    

def getData(path):
    data = pd.read_excel(path)
    products = []
    for i in range(1,len(data.index)):
        row = []
        for column in data.columns:
            entry = data.loc[i,column]
            if pd.isna(entry):
                break
            row.append(entry)
        if len(row)>=11:
            products.append(row)
    insertInDb(products)

def percentToDecimal(x):
    return float(x[0:len(x)-1])/100.0

def getNumbers(product):
    overflow = float(product[6])
    sku = float(product[5]) 
    rd = float(product[7])
    wastage = percentToDecimal(product[8])
    return ((overflow,sku,rd,wastage))



