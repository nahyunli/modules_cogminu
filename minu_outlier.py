from statsmodels import robust
from .minu_utils import get_multi_value, get_multi_value2
from .minu_utils import myMAD
import numpy as np

def mad_detector (dataframe, condition_list, dependent_var_name, thresh, verbose=False):
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
    print("")
    mad_each_group = dataframe.groupby(condition_list)[dependent_var_name].apply(myMAD)
    mad_each_group = mad_each_group.to_frame()
    mad_each_group = mad_each_group.reset_index()

    #print(mad_each_group)
    print("Calculating median and cutoff for each group")
    mean_each_group = dataframe.groupby(condition_list)[dependent_var_name].median()
    mean_each_group = mean_each_group.to_frame()
    mean_each_group = mean_each_group.reset_index()

    mad_up = mean_each_group[dependent_var_name] + (mad_each_group[dependent_var_name] * thresh)
    mad_down = mean_each_group[dependent_var_name] - (mad_each_group[dependent_var_name] * thresh)

    mean_each_group["up"] = mad_up
    mean_each_group["down"] = mad_down
    mean_each_group["mad"] = mad_each_group.rt
    return mean_each_group

def sd_detector (dataframe, condition_list, dependent_var_name, thresh, verbose=False):
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

def remove_outlier(limit, dataframe, condition_list, dependent_var_name, tail):
    length = len(condition_list)

    for row in dataframe.iterrows():
        row_index = row[0]
        t_dv = row[1][dependent_var_name]
        
        # print(the_dictionary[row_index])

        if length == 1:
            t_iv = row[1][condition_list[0]]
            threshs = get_multi_value(condition_list[0], t_iv, limit)

            up_thresh = threshs['up'].values[0]
            down_thresh = threshs['down'].values[0]

        elif length == 2:
            t_iv_1 = row[1][condition_list[0]]
            t_iv_2 = row[1][condition_list[1]]
            threshs = get_multi_value2(condition_list[0], t_iv_1, condition_list[1], t_iv_2, limit)

            up_thresh = threshs['up'].values[0]
            down_thresh = threshs['down'].values[0]

        if tail == 'twotail':
            if t_dv >= up_thresh:
                dataframe.at[row_index, 'trim'] = 'bad'
            elif t_dv <= down_thresh:
                dataframe.at[row_index, 'trim'] = 'bad'
            else:
                dataframe.at[row_index, 'trim'] = 'good'
                
        elif tail == 'onetail':
            if t_dv >= up_thresh:
                dataframe.at[row_index, 'trim'] = 'bad'
            else:
                dataframe.at[row_index, 'trim'] = 'good'

    removed = dataframe[dataframe['trim'] == 'good']

    # check how many were removed
    num_removed=len(dataframe) - len(removed)
    print ("removed" + str(num_removed))
    return dataframe, removed

def calculateMahalanobis(data=None, cov=None):
    y_mu = data - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(y_mu, inv_covmat)
    mahal = np.dot(left, y_mu.T)
    return mahal.diagonal()