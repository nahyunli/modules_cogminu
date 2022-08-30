
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
        print(question_list)

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
        print(question_list)

    for i, j in enumerate(question_list):
        s = s+(response_list[i]-1)

    if   s in [0,1,2,3,4]:               category = "none"
    elif s in [5,6,7,8,9]:               category = "Severe"
    elif s in [10,11,12,13,14]:          category = "mild"
    elif s in [15,16,17,18,19]:          category = "moderately severe"
    elif s in [20,21,22,23,24,25,26,27]: category = "severe"

    return s, category


    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    