from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, NumberObject, TextStringObject
import os
#import pypdftk

import pdfrw
from pdfrw import PdfWriter, PdfReader
import pypdftk
import pandas as pd
#import simple_form as sf

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import magenta, pink, blue, green, black, white

import threading




def create_simple_form(cols, name, max_len):
    
    c = canvas.Canvas(name + '.pdf')
    
    c.setFont("Courier", 20)
    c.drawCentredString(300, 790, 'Template')
    c.setFont("Courier", 14)
    form = c.acroForm
    
    labelY = 780
    formY = 765
    numCols = len(cols)

    for i in range(numCols):
        labelY = labelY - 50
        formY = formY - 50
        c.drawString(10, labelY, cols[i] + ":")
        form.textfield(name=cols[i], tooltip=cols[i],
                    x=110, y=formY,
                    fillColor=white,
                    width=300, maxlen=max_len,
                    textColor=black, forceBorder=True)   

        if (i+1) % 14 == 0:
            c.showPage()
            labelY = 780
            formY = 765


    """
    c.drawString(10, 650, 'First Name:')
    form.textfield(name='fname', tooltip='First Name',
                   x=110, y=635, borderStyle='inset',
                   borderColor=magenta, fillColor=pink, 
                   width=300, maxlen=5000,
                   textColor=blue, forceBorder=True)
    
    c.drawString(10, 600, 'Last Name:')
    form.textfield(name='lname', tooltip='Last Name',
                   x=110, y=585, borderStyle='inset',
                   borderColor=green, fillColor=magenta, 
                   width=300,
                   textColor=blue, forceBorder=True)
    
    c.drawString(10, 550, 'Address:')
    form.textfield(name='address', tooltip='Address',
                   x=110, y=535, borderStyle='inset',
                   width=400, forceBorder=True)
    
    c.drawString(10, 500, 'City:')
    form.textfield(name='city', tooltip='City',
                   x=110, y=485, borderStyle='inset',
                   forceBorder=True)
    
    c.drawString(250, 500, 'State:')
    form.textfield(name='state', tooltip='State',
                   x=350, y=485, borderStyle='inset',
                   forceBorder=True)
    
    c.drawString(10, 450, 'Zip Code:')
    form.textfield(name='zip_code', tooltip='Zip Code',
                   x=110, y=435, borderStyle='inset',
                   forceBorder=True)

    """
    
    c.save()


def create_record_pdf(startRecord, endRecord, df, name):
        if startRecord > endRecord:
                return None

        for i in range(startRecord, endRecord + 1):
                #Convert each record(row) to a mapping
                #print(name)
                #print(i)
                mapping = df[i:].to_dict('records')[0]
                pypdftk.fill_form(pdf_path=name+".pdf", datas=mapping, out_file=name+"_record{}.pdf".format(i), flatten=False)

        #print("All 'record pdfs' from {} to {} for ".format(startRecord,endRecord) + name + " are created.")


def begin(df_dict, num_of_threads = 2, max_len = 1000):

        thrds = []
        for key in df_dict:
                #Template creation with column names
                curr_df = df_dict.get(key)
                df_cols = list(curr_df.columns)
                
                create_simple_form(df_cols, key, max_len)
                #Template ready

                startRow = 0
                lastRow = curr_df.shape[0] - 1
                numRows = curr_df.shape[0]
                
                binSize = int(numRows / num_of_threads)

                #Create concurrent threads
                
                for i in range(num_of_threads):
                        if i == num_of_threads - 1:
                                thrds.append(threading.Thread(target=create_record_pdf, args=(startRow, lastRow, curr_df, key)))
                                break

                        endRow = min(startRow + binSize - 1, lastRow)
                        thrds.append(threading.Thread(target=create_record_pdf, args=(startRow, endRow, curr_df, key)))
                        startRow = endRow + 1



        for t in thrds:
                t.start()

        for t in thrds:
                t.join()

        print("Complete!")





