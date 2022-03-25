#!/usr/bin/env python
# coding: utf-8
# Copyright : Kshitij Raj Sharma @ 2021

# Reading an excel file using Python
import csv
import os
from datetime import datetime
if os.path.isdir('sqm2rop_outputs') is False :
    os.mkdir('sqm2rop_outputs')


def sqm2rop(sqm):
    rop_d=sqm/508.74
    ropani=int(rop_d)
    aana_d=(rop_d-ropani)*16
    aana= int(aana_d)
    paisa_d=(aana_d-aana)*4
    paisa = int(paisa_d)
    dam_d= (paisa_d-paisa)*4
    dam= round(dam_d)
    return validate_param(ropani, aana, paisa , dam)


def validate_param(ropani,aana,paisa,dam):
    if dam >= 4 :
        add_paisa=dam/4 
        paisa=int(paisa+add_paisa)
        dam=round(dam-(dam/4)*4)
    if paisa >= 4 :
        add_aana=paisa/4 
        aana=int(aana+add_aana)
        paisa=int(paisa-(paisa/4)*4)
    if aana >= 16 :
        add_rop=aana/16 
        ropani=int(ropani+add_rop)
        aana=int(aana-(aana/16)*16)

    return ropani, aana, paisa , dam
    
def process(in_column,reader):
    for row in reader:
        try:
            sqm = float(row[in_column])
        except:
            break 
        ropani,aana,paisa,dam = sqm2rop(sqm)
        row.append(ropani)
        row.append(aana)
        row.append(paisa)
        row.append(dam)
        csv_writer.writerow(row)

def converter(user_sqm=None):
    if user_sqm is None:
        user_sqm=float(input("Input SQM to convert: \n"))
    result=sqm2rop(user_sqm)
    print("\nRopani Aana Paisa Dam")
    print(result)

#Debug : 
#         print(ropani,aana,paisa,dam)
#         if ropani!= int(float(row[2])) or aana != int(float(row[3])) or paisa != int(float(row[4])) or dam != int(float(row[5])):
#             print(sqm)
#             print(ropani,aana,paisa,dam)
#             print(int(row[2]),int(row[3]),int(row[4]),int(row[5]))

if __name__ == '__main__':
    # Give the location of the file
    choice = int(input(" Choose Options : \n 1) Enter CSV \n 2) Enter SQM \n 3) Ropani Decimal to Aana and SQM \n"))
    
    if choice == 1:
        path = input("Input Path of File (with trailing \): \n")
        filename= input("Name of file : \n")
        outfilename= input("Output name of file : \n")

        loc = r''+path+filename+'.csv'
        # loc =r'C:\Users\Kshitiz\OneDrive\Desktop\purja.csv'
        # filename='purja'
        if os.path.isfile(loc) is False :
            raise ValueError("File doesnot exist at "+loc)
        ouputfilelocation=input("Output file location (with trailing \): \n")
        out=r''+ouputfilelocation+'re_'+outfilename+'.csv'
        # if os.path.isfile(loc) :
        #     os.remove(out)
        # out=r'sqm2rop_outputs\test.csv'

        with open(loc,'r', encoding="utf8") as fin,     open(out,'w',  encoding="utf-8") as fout:
            reader=csv.reader(fin)
            csv_writer=csv.writer(fout)
            
            # list to store the names of columns
            list_of_column_names = []
        
            # loop to iterate through the rows of csv
            for row in reader:
        
                # adding the first row
                list_of_column_names.append(row)
                row.append('Ropani')
                row.append('Aana')
                row.append('Paisa')
                row.append('Dam')
                csv_writer.writerow(row)
        
                # breaking the loop after the
                # first iteration itself
                break
            print(list_of_column_names[0])
            in_column= input("Enter Column Name containing Square meter : \n")
            # in_column='purja_Sqm'
            if  not in_column in list_of_column_names[0]:
                raise ValueError('Input Column name doesnot exist')
            in_column_index=list_of_column_names[0].index(in_column)
            process(in_column_index,reader)
            print("Success ! File created at : "+out)
    elif choice == 2:
        converter()
    elif choice == 3: 
        user_ropani_decimal=float(input("Input Ropani Decimal: \n"))
        decmal2sqm=user_ropani_decimal*508.74
        converter(decmal2sqm)
    else:
        print("bad value provided")
        exit()



