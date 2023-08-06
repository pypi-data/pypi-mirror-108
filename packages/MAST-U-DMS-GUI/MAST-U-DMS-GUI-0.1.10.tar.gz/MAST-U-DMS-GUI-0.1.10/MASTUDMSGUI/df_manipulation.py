import numpy as np
import pandas as pd
import concurrent.futures
import time
import matplotlib.pyplot as plt

def calibration(wavelength,centre_wavelength):
    '''Determines the correct offset needed based on the centre wavelength and applies it to the wavelength values

    Parameters
    ----------
    wavelength : list
    The wavelength values that correspond to each value data point
    centre_wavelength : int
    The value for the wavelength at the centre, but also tells use what datafile to use for calibration

    Returns
    -------
    result
    The new wavelength list with the offset applied
    '''

    result=[]
    #dictionary of all the offsets
    calibration_values = {380:4.3875,
                          400: 4.5683333,
                          420: 4.5466667,
                          440: 4.54666667,
                          460: 4.76,
                          500: 0,
                          540: 4.73,
                          580: 4.78666667,
                          620: 5.015,
                          660: 4.46,
                          700: 4.5125,
                          740: 4.853333333,
                          780: 4.8725,
                          820: 4.98,
                          860: 4.945}
    offset = calibration_values[centre_wavelength]
    #applying the offset
    for i in wavelength:
        i -= offset
        result.append(i)
    return(result)

#trims down the data to only what is needed
def trimming(df):
    '''Trims down the input data to only have the needed columns and gives them helpful column labels

    Parameters
    ----------
    df : DataFrame
    an input data frame of 5 columns with variable labels for those columns. The only important ones are the
    sets, pixel and value in the 2nd, 4th and 5th columns

    Returns
    -------
    needed:
    returns a DataFrame with labels columns of "set", "pixel", "value".
    '''

    #allows for the correct columns regardless of index number
    lst = df.columns
    needed = df[[lst[1], lst[3], lst[4]]]
    # giving proper titles to the columns
    needed.columns = ["set", "pixel", "value"]
    #print(needed)
    return needed

#creates a list of values for s1(t-1)/s1(t0)
def crt_smear_correct(data_2,data_1):
    '''takes in a set of 2D data and creates a 2D superlist of the correct smear values for the dataset

    Parameters
    ----------
    data :  2D list
    a 2D list of data values

    Returns
    -------
    smr_cor_lst
    returns a 2D super list of smear values corresponding to the input data
    '''
    smr_cor_lst = []
    minor_lst = []
    count = 0
    count_2 = 0
    #I don't like for loops okay, I'll change it if you ask nicely
    while count < len(data_2):
        #print(data_2)
        while count_2 < len(data_2[0]):
            #setting the value equal to 1 if there is no previous value to interpolate from
            if data_1 == "N/A":
                smear_correct = 1
                minor_lst.append(smear_correct)
                count_2 += 1
            elif data_2[count][count_2] == 0:
                smear_correct = 1
                minor_lst.append(smear_correct)  # Adding points to the list
                count_2 += 1
            else: #performs the corrct calculation and adds it to the sublist
                smear_correct = data_1[count][count_2] / data_2[count][count_2]
                if smear_correct > 4 or smear_correct < 0.25: #if the change is silly it just changes the correction to 1
                    smear_correct = 1
                minor_lst.append(smear_correct) #Adding points to the list
                count_2 += 1
        smr_cor_lst.append(minor_lst)
        minor_lst = []
        count += 1
        count_2 = 0
    return smr_cor_lst  #currently keeping it as return a list with sublists but could be changed to an array in the future

#Takes in the 2D data and converts it into 1D data that the other functions can accept
def two_d_correction(input, N, smear_ratios):
    '''Takes in a 2D data input and outputs a 2D data input with smearing correction.
    Uses a couple of functions along the way

    Parameters
    ----------
    input : list
    a 2D list of data values
    N : integer
    N is number of pixels per fibre
    smear_ratios: list
    A 1D list of the ratios between values in different dimensions that will be inputted into the correction matrix

    Returns
    -------
    final_df
    returns  a super list of 2D corrected data with the 1D data within the sublists
    '''

    count = 0
    final_df = []
    N_list = [N] * len(input)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # creates a real data value for every input data value
        current_real = executor.map(create_and_apply_correction, input, N_list, smear_ratios)
    #        current_real = create_and_apply_correction(current_data, N, current_smear) #uses the 1D correction applying function
    #        final_df.append(current_real)  #creates a master list of all the correct data values
    #        count += 1
    returned = []
    for x in current_real:
        returned.append(x)
    return returned

#taking the master list creating the correction matrix (currently only the basic version, need to add in s1(t-1)/s1(t0)
def create_and_apply_correction(input, N, smear_ratios):
    '''Takes in a set of 1D data, creates a correction matrix for it and then applies that matrix to it
    (currently not sure if this thing actually works correctly, will need actual unsmeared data to compare)

    Parameters
    ----------
    input : list
    A 1D list of the data values to be smear corrected
    N :
    N is the number of pixels per fibre
    smear_ratios: list
    A 1D list of the ratios between values in different dimensions that will be inputted into the correction matrix

    Returns
    -------
    real_values:
    A list of the real values for the data with smear correction applied
    '''

    major_lst = []
    minor_lst = []
    t_ss = 0.0000012
    texp = 0.008
    row = 0
    column = 0
    #making the coloumn only be as long as N
    while column < len(input):
        count = 0
        #making the rows only be as long as N
        while row < len(input):
            #making the identity matrix
            if count == column:
                minor_lst.append(1)
                count += 1 #counting how far along the row we are
                row += 1 #giving the exit condition
            elif count < column:
                minor_lst.append((((N) * t_ss) / texp) * (smear_ratios))  #adding the value to the list
                count += 1
                row += 1
            else:
                minor_lst.append(((N)*t_ss)/texp)  #adding the value to the list
                count += 1
                row += 1
        major_lst.append(minor_lst) #appends the individual rows into a list for the matrix
        minor_lst = []
        row = 0 #resets the rwo so it starts at the beginning
        column += 1 #counts how far along the columns we are
    major_lst = pd.DataFrame(major_lst)
    input = pd.DataFrame(input) #converting into data frames to allow for matrix multiplication
    correction_inverse = np.linalg.inv(major_lst) #inverting the correction matrix
    real_values = correction_inverse.dot(input) #multiplying the input data by the inverse of the correction matrix for the real data
    real_values = real_values.tolist() #turning it back into a list
    return real_values

#creates a dataframe of the means and stds with their corresponding pixels
def means_and_stds(needed):
    '''Takes an Dataframe input and finds the mean and standard deviation of values with the same pixel value

    Parameters
    ----------
    needed : Dataframe
    A dataframe with 3 or 2 columns. The first "set" (optional) says what set of data is on.
    2nd is "pixel" and says which pixel the "value" corresponds to.
    3rd is "value" which contains the value for a pixel, all values on the same pixel are grouped together

    Returns
    -------
    final data:
    Returns a 3 column dataframe with the pixels in the first, the means the 2nd and the standard devision in the 3rd
    The rows of data correspond to one another. E.g. the 1st row has pixel 1 and the mean and stds for values on pixel 1
    '''

    # setting up values for later in program
    means = []
    stds = []
    pixel_list = []
    pixel = 1
    # creating a loop to make a list of the mean and standard deviations.
    while pixel < 1025:
        # selecting a row
        data = needed[needed.pixel == pixel]
        # converting to a list
        data = data['value'].values
        # appending to the main list of means and std the current mean and std
        means.append(np.mean(data))
        stds.append(np.std(data))
        pixel_list.append(pixel)
        # implementing a counting system
        pixel += 1
    #return means, stds, pixel

    #recreating a dataframe using the pixel, means and stds list
    final_data = pd.DataFrame(pixel_list)
    final_data["1"] = (means)
    final_data["2"] = (stds)
    final_data.columns = ['Pixel', 'Means', 'Standard Deviations']
    return(final_data)

#creates a dataframe of the means and stds with their corresponding pixels
def test_means_and_stds(needed):
    '''Takes an Dataframe input and finds the mean and standard deviation of values with the same pixel value

    Parameters
    ----------
    needed : Dataframe
    A dataframe with 3 or 2 columns. The first "set" (optional) says what set of data is on.
    2nd is "pixel" and says which pixel the "value" corresponds to.
    3rd is "value" which contains the value for a pixel, all values on the same pixel are grouped together

    Returns
    -------
    final data:
    Returns a 3 column dataframe with the pixels in the first, the means the 2nd and the standard devision in the 3rd
    The rows of data correspond to one another. E.g. the 1st row has pixel 1 and the mean and stds for values on pixel 1
    '''

    # setting up values for later in program
    means = []
    stds = []
    pixel_list = []
    pixel = 0
    final_data = []
    # creating a loop to make a list of the mean and standard deviations.
    while pixel < 1024:
        for i in needed:
            pixel_list.append(i[pixel])
        print(pixel_list)
        print(sum(pixel_list))
        print(len(pixel_list))
        avg = sum(pixel_list) / len(pixel_list)
        pixel += 1
        pixel_list = []
        final_data.append(avg)
    return(final_data)


def test_resample(data, current_sample_rate, desired_sample_rate):
    ''' I accidentally copy and pasted the mean and stds description into this so I don't currently know what it does
    good luck, I will update it as I figure it out myself

    data: list/superlist
    I believe this takes an entire fibres worth of data and then resamples it as stated previously

    current_sample_rate: integer
    Is the current sample rate  that it is being compared to

    desired_sample_rate: integer
    Is the desired sample rate that will need to be converted towards


    return Total_data: ?

    Is the fibres total data returned at the new resampling I believe, current formatting unknown
        '''

    #creating a ratio between the current sample rate and the desired rate
    reference = current_sample_rate / desired_sample_rate

#creating values for later
    count_pop = 0
    sent_data = []
    total_data = []
    #detects if the data is empty
    while len(data) > 0:

        #checks if the length of the data is long enough for a full averaging
        if len(data) > reference:
            while count_pop < reference: #checking that we're collecting the same number of data points (time) as the reference
                sent_data.append(data.pop(0))
                count_pop += 1
            sent_data = test_means_and_stds(sent_data)
            total_data.append(sent_data)
            sent_data = []
            count_pop = 0
        else:
            while len(data) > 0:
                sent_data.append(data.pop(0))
            sent_data = test_means_and_stds(sent_data)
            total_data.append(sent_data)

    return total_data

def resample(data, current_sample_rate, desired_sample_rate):
    ''' I accidentally copy and pasted the mean and stds description into this so I don't currently know what it does
    good luck, I will update it as I figure it out myself

    data: list/superlist
    I believe this takes an entire fibres worth of data and then resamples it as stated previously

    current_sample_rate: integer
    Is the current sample rate  that it is being compared to

    desired_sample_rate: integer
    Is the desired sample rate that will need to be converted towards


    return Total_data: ?

    Is the fibres total data returned at the new resampling I believe, current formatting unknown
        '''

    #creating a ratio between the current sample rate and the desired rate
    reference = current_sample_rate / desired_sample_rate

#creating values for later
    count_pop = 0
    sent_data = []
    total_data = []
    #detects if the data is empty
    while len(data) > 0:
        #checks if the length of the data is long enough for a full averaging
        if len(data) > reference:
            while count_pop < reference: #checking that we're collecting the same number of data points as the reference
                sent_data.append(data.pop(0))
                count_pop += 1
            sent_data = create_for_means_and_stds(sent_data)
            sent_data = means_and_stds(sent_data)
            sent_data = sent_data["Means"].values.tolist()
            total_data.append(sent_data)
            sent_data = []
            count_pop = 0
        else:
            while len(data) > 0:
                sent_data.append(data.pop(0))
            sent_data = create_for_means_and_stds(sent_data)
            sent_data = means_and_stds(sent_data)
            sent_data = sent_data["Means"].values.tolist()
            total_data.append(sent_data)


    return total_data

#Converting a list into a vertical matrix
def convert_list_matrix(lst):
    '''Converts a single list into a vertical matrix

    Parameters
    ----------
    lst : list
    The initial list to be converted

    Returns
    -------
    Matrix
    A vertical matrix made from the list
    '''
    Matrix = np.array(lst)
    Matrix = Matrix.reshape(len(lst),1)
    return Matrix

#merges lists within lists into a single large list
def merge_sublists(superlist):
    '''Merges the lists within a superlist into one singular long list

    Parameters
    ----------
    superlist : list
    contains the superlist with sublists within it

    Returns
    -------
    total:
    a large list with all the previous sublists merged in order
    '''

    total = []
    for i in superlist:
        #print(i)
        total += i
    return total

#creates sublists of the length inputted (check that the total number of entires is divisable by that number)
def create_sublists(list,length):
    '''We take a large list and break it up into a set of sublists

    Parameters
    ----------
    list : list
        This is the list that gets broken up
    length : int
        describes the legnth each sublist should be

    Returns
    -------
    sublists:
        a superlist containing sublists of the same length as the length input
    '''

    temp = list
    super_list = []
    count_2 = 0
    while count_2 < len(temp):
        sub_list = []
        count = 0
        while count < length:
            sub_list.append(temp.pop(0))
            count += 1
        super_list.append(sub_list)
        count_2 += 1

    return(super_list)

def create_pixel(data_input):
    '''creates a set and pixel values for reference and readablility of data

    Parameters
    ----------
    data_input : list
    contains a list of all the data broken up into sublists

    Returns
    -------
    time:
    returns a list for the corresponding time for each data point
    '''
    count = 0
    sub_pixel = []
    pixel = []
    while count < len(data_input):
        sub_pixel = [*range(1,(len(data_input[count]))+1)]
        pixel.append(sub_pixel)
        count += 1
    return pixel

def create_time(data_input):
    '''creates a set and pixel values for reference and readablility of data

    Parameters
    ----------
    data_input : list
    contains a list of all the data broken up into sublists

    Returns
    -------
    time:
    returns a list for the corresponding time for each data point
    '''


    count = 1
    sub_time = []
    time = []
    while count-1 < len(data_input):
        sub_time = [count]*len(data_input[count-1])
        time.append(sub_time)
        count += 1
    return time

def create_for_means_and_stds(superlist):
    time = create_time(superlist)
    pixel = create_pixel(superlist)
    time = merge_sublists(time)
    pixel = merge_sublists(pixel)
    data = merge_sublists(superlist)
    final_df = pd.DataFrame({
        'time': time,
        'pixel': pixel,
        'value': data
    })
    return final_df

def create_single_sublist(lst):
    '''
    turns a list with a single entry into a sublist of that entry for formatting purposes
    sub: lst
    the list that is operated upon

    '''
    sub = [[0]]
    sub.append(lst)
    del sub[0]
    return sub