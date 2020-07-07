import configparser
import pandas as pd 
import os
import datetime
import glob
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo


#create the tkinter window
window = Tk()

#define the size of the window
window.geometry('400x300')

#Prevent the window from getting resized
window.resizable(True,True)

#define the title of the window
window.title('Configuration File Format Transfer')

#load input file
def load_file(event=None):
    global inputFile
    inputFile = askopenfilename(parent=window,initialdir=os.getcwd())
    if inputFile:
        try:
            showinfo(title='Selected file:',message = inputFile) #show selected file
        except:
            showerror(title='Error',message="Unable to load the source file!")
    return inputFile

#Transfer function
def runTransfer():
    try:
        #Create a config 
        config =  configparser.ConfigParser(strict=False)
    
        #read the input .ini file
        path = os.path.abspath(os.getcwd()) #get the working directory 
        os.chdir(path) #go to the working directory 

        #extract FTM for each file
        dirname =os.path.dirname(inputFile)
        if 'cfg_FTM' in dirname:
            FTMnumber = dirname.split('cfg_FTM')[-1] #get the FTM number from cfg_FTM7
        else:
            FTMnumber= 'N/A' #if no cfg_FTM, FTM number is N/A

        #parse input file one by one
        config.read(inputFile)
        signCount = config['general']['signCount'] #get the sign count field

        if int(signCount) != 0:
            #get the signs section names
            new_df = pd.DataFrame()
            i=0
            for key in config.sections():
                if 'sign' in key.lower():
                    df = pd.DataFrame(dict(config.items(key)),index=[i])
                    i+=1
                    new_df=new_df.append(df)
            new_df.insert(loc=0,column='FTM',value = FTMnumber)
            new_df.to_csv('OUTPUT-ftmMwMd as of'+datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')+'.csv',index = False)       

        else: 
            new_df = pd.DataFrame(data=[FTMnumber],columns=['FTM'])
            new_df.to_csv('OUTPUT-ftmMwMd as of '+datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')+'.csv',index = False)
    except KeyError:
        showerror(title='Error',message= 'Unable to read the source file, upload again!')
    except ValueError:
        showerror(title='Error', message = 'Unable to read the source file, check the source file!')
    except:
        showerror(title='Error',message='Unable to transfer the source file!')

#Clear output csv files with the same name
def clear():
    try:
        for f in glob.glob('OUTPUT-ftmMwMd as of*.csv'):
            os.remove(f)
    except:
        showerror(title='Error',message='Unable to clear the CSV file!')   

def combine():
    try:
        all_filenames = [i for i in glob.glob('OUTPUT-ftmMwMd as of*.csv')]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        combined_csv.fillna({'FTM':'N/A'},inplace=True)
        combined_csv.to_csv('Combined-OUTPUT-ftmMwMd as of '+datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')+'.csv',index = False)
    except:
        showerror(title='Error',message='Unable to combine the CSV files!')

#upload file button
upload_btn = Button(window, text='Upload ftmMwMd.ini file', command= load_file)
upload_btn.pack(pady=15)

#run button 
run_btn = Button(window, text='Transfer Now', command= runTransfer)
run_btn.pack(pady=15)

#combine files button
combine_btn =Button(window, text='Combine all ftmMwMd output files', command= combine)
combine_btn.pack(pady=15)

#clear files button
clear_btn = Button(window, text='Clear all ftmMwMd single output CSV files', command = clear)
clear_btn.pack(pady=15)

window.mainloop()

