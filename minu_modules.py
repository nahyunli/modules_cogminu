import eland as ed
import pandas as pd
import os
from os import sep
import operator
import numpy as np
from statsmodels import robust

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

def mad_detector (dataframe, condition_list, dependent_var_name, thresh=2.5, verbose=False):
    """
    get the median absolute deviation and the 2.5 cutoff for a given group of floats

    :param dataframe: the dataframe
    :param condition_list: (list of strings) a list of index names to 'group by'
    :param dependent_var_name: (string) index name of RT variable
    :param thresh: (fload) default is 2.5 mad
    :param verbose: default False. If True, prints all mad values and 2.5 mad threshold values.
    :return: ma(float): median absolute deviation for the group by median values.
             mad_up(float): the upperlimit for outlier RT rejection
    """
    print("")
    print('^_^ Running Mad_detector !!!')

    ma = dataframe.groupby(condition_list)[dependent_var_name].mad()

    ma = ma.to_frame()
    ma = ma.reset_index()
    #rint(ma)

    for x in range(0, len(ma)):
        i1 = str(condition_list[0])
        i2 = str(condition_list[1])
        id1= ma[i1][x]
        id2= ma[i2][x]
        tempp = dataframe.loc[(dataframe[i1] == id1) & (dataframe[i2] == id2)]
        md = tempp[[dependent_var_name]].apply(robust.mad)

        ma.at[x, dependent_var_name] = md.values[0]

    me = dataframe.groupby(condition_list)[dependent_var_name].median()
    me = me.to_frame()
    me = me.reset_index()

    # print(ma)
    # print(me)

    mad_up = me[dependent_var_name] + (ma[dependent_var_name] * thresh)
    print(mad_up)
    ma['rt'] = mad_up
    print(ma)
    if verbose == True:
        print("")
        print("Printing MAD:")
        print(ma)
        print("")
        print("Printing MAD Upper limit:")
        print(mad_up)
    print('')
    print('Returning MAD and' + str(thresh) +' MAD threshold values per group')
    return mad_up, ma

def sd_detector (dataframe, condition_list, dependent_var_name, thresh=2.5, verbose=False):
    """
    get the median absolute deviation and the 2.5 cutoff for a given group of floats

    :param dataframe: the dataframe
    :param condition_list: (list of strings) a list of index names to 'group by'
    :param dependent_var_name: (string) index name of RT variable
    :param thresh: (fload) default is 2.5 mad
    :param verbose: default False. If True, prints all mad values and 2.5 mad threshold values.
    :return: ma(float): median absolute deviation for the group by median values.
             mad_up(float): the upperlimit for outlier RT rejection
    """
    print("")
    print('^_^ Running sd_detector !!!')

    ma = dataframe.groupby(condition_list)[dependent_var_name].std()
    ma = ma.to_frame()
    ma = ma.reset_index()
    mo = dataframe.groupby(condition_list)[dependent_var_name].std()

    me = dataframe.groupby(condition_list)[dependent_var_name].mean()
    me = me.to_frame()
    me = me.reset_index()

    # print(ma)
    # print(me)

    mad_up = me[dependent_var_name] + (ma[dependent_var_name] * thresh)
    mad_down = me[dependent_var_name] + (ma[dependent_var_name] * -thresh)
    ma['rt_upper'] = mad_up
    ma['rt_lower'] = mad_down
    if verbose == True:
        print("")
        print("Printing stadard deviations:")
        print(mo)
        print("")
        print("Printing SD Upper and Lower limit:")
        print(ma)
        print("")
        print("Printing Group Averages")
        print(me)
    print('')
    print('Returning SD and ' + str(thresh) +' SD threshold values per group')
    return mo, ma, me

def stai_calculator (df_of_items, mode, question_index, response_index, verbose=False):
    """
    Automatically Calculates STAI scores of 1 participant
    :param df_of_items:
    :param question_index:
    :param response_index:
    :param verbose:
    :return:
    """
    if mode == 'state':
        reverse = [1, 2, 5, 8, 10, 11, 15, 16, 19, 20]
    elif mode == 'trait':
        reverse = [1, 3, 6, 7, 10, 13, 14, 16, 19]

    convert = [4,3,2,1]
    s = 0

    question_list = df_of_items[question_index].tolist()
    response_list = df_of_items[response_index].tolist()

    if verbose == True:
        print('')
        print("Printing the Question List")
        print(questions_list)

    for i, j in enumerate(question_list):
        if (i+1) in reverse:
            if response_list[i] == 1: s = s+4
            elif response_list[i] == 2: s = s+3
            elif response_list[i] == 3: s = s+2
            elif response_list[i] == 4: s = s+1
        else:
            s = s+response_list[i]

    if s < 38: category = "no-low"
    elif s > 44: category = "high"
    else: category = "moderate"

    return s, category

def cesd_calculator (df_of_items, question_index, response_index, verbose=False):
    """
    Automatically Calculates STAI scores of 1 participant
    :param df_of_items:
    :param question_index:
    :param response_index:
    :param verbose:
    :return:
    """
    question_list = df_of_items[question_index].tolist()
    response_list = df_of_items[response_index].tolist()

    if verbose == True:
        print('')
        print("Printing the Question List")
        print(question_list)

    reverse = [4, 8, 12, 16]
    da_list = [3,6,14,17,18]
    pa_list = [4,12,16]
    sc_list = [2,5,7,11,13,20]
    ip_list = [15,19]
    s = 0
    da_sub = 0
    pa_sub = 0
    sc_sub = 0
    ip_sub = 0
    for i, j in enumerate(question_list):
        if (i+1) in reverse:
            if response_list[i] == 0: s = s+3
            elif response_list[i] == 1: s = s+2
            elif response_list[i] == 2: s = s+1
            elif response_list[i] == 3: s = s
        else:
            s = s+response_list[i]

    for i, j in enumerate(question_list):
        if (i+1) in da_list:
            da_sub = da_sub+response_list[i]
        elif (i+1) in pa_list:
            if response_list[i] == 0: pa_sub = pa_sub+3
            elif response_list[i] == 1: pa_sub = pa_sub+2
            elif response_list[i] == 2: pa_sub = pa_sub+1
            elif response_list[i] == 3: pa_sub = pa_sub
        elif (i+1) in sc_list:
            sc_sub = sc_sub + response_list[i]
        elif (i+1) in ip_list:
            ip_sub = ip_sub + response_list[i]

    if s <= 15: category = "Mild"
    elif s >= 24: category = "Severe"
    else: category = "Moderate"

    return s, category, da_sub, pa_sub, sc_sub, ip_sub

def phq9_calculator (df_of_items, question_index, response_index, verbose=False):
    """
    Automatically Calculates STAI scores of 1 participant
    :param df_of_items:
    :param question_index:
    :param response_index:
    :param verbose:
    :return:
    """
    s = 0

    question_list = df_of_items[question_index].tolist()
    response_list = df_of_items[response_index].tolist()

    if verbose == True:
        print('')
        print("Printing the Question List")
        print(questions_list)

    for i, j in enumerate(question_list):
        s = s+(response_list[i]-1)

    if   s in [0,1,2,3,4]:               category = "none"
    elif s in [5,6,7,8,9]:               category = "Severe"
    elif s in [10,11,12,13,14]:          category = "mild"
    elif s in [15,16,17,18,19]:          category = "moderately severe"
    elif s in [20,21,22,23,24,25,26,27]: category = "severe"

    return s, category

def remove_rt_outlier(df, labels, dep_var, t):
    # df input the dataframe for outlier removal
    # put list of header names of the dataframe. First header should always be the id.
    # For dependent variable input string of the dependent variable header name.
    # For t determine the cut off threshold for MAD
    names = mm.name_extractor(df, dep_var[0])
    mads, mads_upper = mm.mad_detector(df, labels, dep_var, thresh=t, verbose=False)
    return (mads, mads_upper)

def get_multi_value (index1, index_val1,df):
    a = df.loc[(df[index1] == index_val1)]
    return a


def get_multi_value2 (index1, index_val1, index2, index_val2, df):
    a = df.loc[(df[index1] == index_val1) & (df[index2] == index_val2)]
    return a

def get_multi_value3 (index1, index_val1, index2, index_val2,  index3, index_val3, df):
    a = df.loc[(df[index1] == index_val1) & (df[index2] == index_val2)  & (df[index3] == index_val3)]
    return a
 #     return empty
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    