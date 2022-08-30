import pandas as pd
import os
from os import sep
import numpy as np

def pd_print_all():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

def csv_compiler(root_folder, verbose=False):
    """
    Enter a directory coontaining .csv files in the same format.
    Returns dataframe of compiled .csv files
    verbose default is False.
    If true, it prints the name of the files in the directory.
    """
    print()
    print('^o^ Running csv_compiler !!!')
    print('')
    print('Reading csv. files in ' + root_folder)
    print('This may take a while')
    file_list = os.listdir(root_folder)
    if verbose==True:
        print('printing file list in directory ' + root_folder + ': \n' + str(file_list))
        print("")
    for i, j in enumerate(file_list):
        data = pd.read_csv((root_folder+sep+file_list[i]), sep=',', header=0)
        # print(i)
        if i == 0:
            temp = data

        elif i > 0:
            temp=temp.append(data, sort=True)

    # print(temp)
    print('Returning compiled dataframe')
    print("")
    return (temp)

def name_extractor (dataframe, fieldname, verbose=False):
    """
    Extract unique names from a dataframe
    :param dataframe: the dataframe
    :param fieldname: the column index name that you want to extract the unique names.
    :return: (list) a list of unique names
    """
    name_list = (dataframe[fieldname].unique()).tolist()
    print("")
    print("Unique Values from '" + fieldname + "' are extracted")
    if verbose==True:
        print("")
        print("Printing the unique values")
        print(name_list)
    return name_list

def get_multi_value (index1, index_val1,df):
    a = df.loc[(df[index1] == index_val1)]
    return a

def get_multi_value2 (index1, index_val1, index2, index_val2, df):
    a = df.loc[(df[index1] == index_val1) & (df[index2] == index_val2)]
    return a

def get_multi_value3 (index1, index_val1, index2, index_val2,  index3, index_val3, df):
    a = df.loc[(df[index1] == index_val1) & (df[index2] == index_val2)  & (df[index3] == index_val3)]
    return a

def check_remove(before, after):
    num_removed = len(before) - len(after)
    print("removing " + str(num_removed))

 #     return empty
def myMAD(x):
    med = np.median(x)
    x = abs(x - med)
    MAD = np.median(x)
    return MAD
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    