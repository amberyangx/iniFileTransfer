import configparser
import pandas as pd 
import os
from tkinter import *
import datetime
import glob
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo

#initialize a list for inputfile storage 
inputFile =[]

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

        signCount = config['sign']['signCount'] #get the sign count field

        #initialize variables
        header = ['Sign Name','Dispatch Interval', 'AmberAlertTime','AmberAlertImportance','WindMeterName','WindMeterImportance','LiftBridgeName','LiftBridgeImportance',\
                'BorderCrossingName','BorderCrossingImportance','BorderCrossingVehType','AmberAlertActivationTimeout','LiftBridgeActivationTimeout','WindMeterActivationTimeout','BorderCrossingActivtnTimeout',\
                'DczName','HwyDirRef','AmberAlertsEnabled','WindMetersEnabled','LiftBridgesEnabled','BorderCrossingEnabled','TrafficFlowEnabled','MajorCongestionEnabled','SingleRoadwayEnabled']


        #If signCount != 0    
        if int(signCount) > 0:
            lst = list(config['sign'].keys())
            lst.pop(0)
            signNumber = []
            source =[]
            for x in range(int(signCount)):
                signNumber.append(str(x+1))  #signNumber = ['1','2','3','4','5','6','7']
            for j in range(24):
                keys = lst[j::24] #get the keys for the same header
                eachCategory = []
                for h in keys:
                    eachCategory.append(config['sign'][h])
                source.append(eachCategory) 
            #get all the information needed 
            dictionary = {k:v for k,v in zip(header,source)} #match the header to the data by zipping 

            #get a full dict excluding the FTM number
            full_dict = {'Sign Number':signNumber} #initialize a dict using sign number 
            full_dict.update(dictionary) #update the full_dict by adding dictionary (all the info)
            #make the dict to a dataframe 
            full_dict_df = pd.DataFrame(full_dict) #dataframe exclude FTM column      
            
        else:    
            full_dict_df = pd.DataFrame(columns = header,index=range(1))


        #insert the FTM column to the beginning of the full_dict dataframe 
        full_dict_df.insert(loc=0,column='FTM',value = FTMnumber)
                
        #dataframe to csv
        full_dict_df.to_csv('OUTPUT-ftmMwMc as of '+datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')+'.csv',index=False)
    except KeyError:
        showerror(title='Error',message= 'Unable to read the source file, upload again!')
    except ValueError:
        showerror(title='Error', message = 'Unable to read the source file, check the source file!')
    except:
        showerror(title='Error', message= 'Unable to transfer the file!')
  
#Clear output csv files with the same name
def clear():
    try:
        for f in glob.glob('OUTPUT-ftmMwMc as of*.csv'):
            os.remove(f)
    except:
        showerror(title='Error',message='Unable to clear the CSV file!')   

def combine():
    try:
        all_filenames = [i for i in glob.glob('OUTPUT-ftmMwMc as of*.csv')]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        combined_csv.fillna({'FTM':'N/A'},inplace=True)
        combined_csv.to_csv('Combined-OUTPUT-ftmMwMc as of '+datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')+'.csv',index = False)
    except:
        showerror(title='Error',message='Unable to combine the CSV files!')
         

#upload file button
upload_btn = Button(window, text='Upload ftmMwMc.ini file', command= load_file)
upload_btn.pack(pady=15)

#run button 
run_btn = Button(window, text='Transfer Now', command= runTransfer)
run_btn.pack(pady=15)

#combine files button
combine_btn =Button(window, text='Combine all ftmMwMc output files', command= combine)
combine_btn.pack(pady=15)

#clear files button
clear_btn = Button(window, text='Clear all ftmMwMc single output CSV files', command = clear)
clear_btn.pack(pady=15)

window.mainloop()

