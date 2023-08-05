import os
import tkinter as Tk
from tkinter import filedialog
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import df_manipulation as df
import pandas as pd
import time
from matplotlib.widgets import Slider, RectangleSelector
matplotlib.use("TkAgg")
import spe2py as sls
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
from numpy import matlib

def clicking_anywhere(event):
    """
    Is where the pickers for clicking for x and y data go to.
    It containts a picker setting to select what to do with the selected x and y values.

    :param event: The x and y data that have been taken from where the user clicks
    :return:
    """
    global dict

    if dict["picker setting"] == "Zooming":
        if len(dict["picker data list"]) == 1:
            dict["picker data list"].append(event.xdata)
            dict["fig"].canvas.mpl_disconnect(dict["cid"])
            Zooming_in()
        else:
            dict["picker data list"].append(event.xdata)


    elif dict["picker setting"] == "Intergration":
        if len(dict["picker data list"]) == 1:
            dict["picker data list"].append(event.xdata)
            dict["fig"].canvas.mpl_disconnect(dict["cid"])
            intergration_window_graph()
        else:
            dict["picker data list"].append(event.xdata)


    elif dict["picker setting"] == "Comparing Ratios":
        if len(dict["picker data sub list1"]) < 1:
            dict["picker data sub list1"].append(event.xdata)
        elif len(dict["picker data sub list1"]) == 1:
            dict["picker data sub list1"].append(event.xdata)

        elif len(dict["picker data sub list1"]) == 2:
            if len(dict["picker data sub list2"]) < 1:
                dict["picker data sub list2"].append(event.xdata)
            elif len(dict["picker data sub list2"]) == 1:
                dict["picker data sub list2"].append(event.xdata)

                dict["picker data list"].append(dict["picker data sub list1"])
                dict["picker data list"].append(dict["picker data sub list2"])
                dict["fig"].canvas.mpl_disconnect(dict["cid"])
                comparing_ratios()

            else:
                print("something else has gone wrong")
        else:
            print("something has gone wrong")

    elif dict["picker setting"] == "Test":
        print(event.xdata)
        dict["fig"].canvas.mpl_disconnect(dict["cid"])
    else:
        print("no setting selected")


    #if it's the zooming in function
    #if only 1 point then just store it

    #if two points then store the second point
    #disconnect the picker
    #then call into main zooming in function with the x and y data


    #intergrations:

    #same as the zooming in picker but call the intergration function


    #comparing ratios:
    #create two different lists inside the dictionary
    # if the first list len < 2 then add the first two points to it
    # if first list len == 2 then add the second two poitns to the 2nd list
    #then append the two lists to the normal data list in the dictionary
    #then disconnect the picker
    #then call the comparing ratios


def start_clicking():
    "just a test to see if it's working"
    global dict
    dict["picker setting"] = "Test"
    dict["cid"] = dict["fig"].canvas.mpl_connect('button_press_event', clicking_anywhere)

def create_naming_window_external():
    """
    Creates a window with an entry box to name the file.
    Destroys itself on saving
    :return:
    """

    global dict

    #dict["text_window"] = Tk.Tk()
    #dict["text_window"].wm_title("Exernal Saving Window")
    #dict["text_box"] = Tk.Entry(dict["text_window"])
    #dict["text_box"].grid(column = 0, row = 0)

    #os.getenv("HOME")

    cur_dir = os.getcwd()
    os.chdir('/home')
    ""
    file_path = filedialog.asksaveasfile()
    file_path = file_path.name
    dict["file_path"] = file_path
    os.chdir(cur_dir)
    externally_save_data()
    #button_1 = Tk.Button(dict["text_window"], text = "confirm", command = externally_save_data)
    #button_1.grid(column = 1, row = 0)

def create_naming_window_internal():
    """
    Creates a window with an entry box for a name to describe the saved sets of data.
    Destroys itself on saving

    :return:
    """
    global dict

    dict["text_window"] = Tk.Tk()
    dict["text_window"].wm_title("Internal Saving Window")
    dict["text_box"] = Tk.Entry(dict["text_window"])
    dict["text_box"].grid(column = 0, row = 0)
    button_1 = Tk.Button(dict["text_window"], text = "save data", command = internally_save_data)
    button_1.grid(column = 1, row = 0)

def internally_save_data():
    """
    a button pushed, opens up a text box that allows for a string to name the entry in the dictionary.
    This then saves the selected data as the entry in it's dictionary

    :return:
    """
    global dict

    temp = dict["text_box"]
    string = temp.get()
    dict["text_window"].destroy()
    dict["saveable_data"][string] = dict["data_to_be_saved"]


def externally_save_data():
    """
    Saves the data externally of all the data that has been saved internally with a customisable file name.

    May want to see if a file browser and selection can be chosen, like with the data loader.

    :return:
    """

    global dict


    #changes current directory to the directory where the data files are
    #cur_dir = os.getcwd()
    #os.chdir('/common/projects/diagnostics/MAST/SPEXBDMS/Lightfield_output/Data_Files/')

    saveable_data = dict["saveable_data"]
    file_path = dict["file_path"]
    np.savez(file_path, [saveable_data])


    #changes the directory back
    #os.chdir(cur_dir)

def intergration_picker():
    '''Resets the picker and then sets up the canvas that takes the points for clicking. Sets the program to do intergration'''
    dict["picker data list"] = []
    dict["picker setting"] = "Intergration"
    dict["cid"] = dict["fig"].canvas.mpl_connect('button_press_event', clicking_anywhere)

def intergration_window_graph():
    """
    Creates a new window that contains a graph.
    The graph takes a selected area, then intergrates that area, and shows the plotted intergration.

    It can Save both the plotted intergration values, the x axis, and the total intergration values.


    :return:
    """


    global dict

    real_data = dict["total"][1]
    wave_data = dict["total"][0]

    x1, x2 = dict["current_x_axis"]


    count = 0
    current = wave_data[count]

    while current < x1:
        count += 1
        current = wave_data[count]

    position_min = count
    count = (len(real_data)) -1
    current = wave_data[count]
    while current > x2:
        count -= 1
        current = wave_data[count]

    position_max = count

    real_data_slice = real_data[position_min:position_max]
    wave_data_slice = wave_data[position_min:position_max]

    count = 1
    intergrated_data_slice = []
    intergrated_wave_axis = []


    dict["text_window"] = Tk.Toplevel(root)
    dict["text_window"].wm_title("Saving window")


    dict["text_box"] = Tk.Entry(dict["text_window"])
    dict["text_box"].grid(column = 0, row = 0)


    result = (np.trapz(real_data_slice, wave_data_slice))
    print(result)

    #maximum = np.max(real_data_slice) + (0.1 * np.max(real_data_slice))
    #minimum = (np.min(real_data_slice) - (0.1 * (np.max(real_data_slice))))



    btn_1 = Tk.Button(dict["text_window"], text="Store Slice", command=internally_save_data).grid(row=0, column=1)

    if True == True:
        x_axis = dict["wavelength_r"]
        spec = dict["o"]['spectra_abs']

        pixel_numbers_1 = []

        pixel_numbers_1.append(find_point_from_below(x1, x_axis[0]))
        pixel_numbers_1.append(find_point_from_below(x2, x_axis[0]))

        selection_1 = np.sum(spec[:,:,pixel_numbers_1[0]:pixel_numbers_1[1]],2)*np.median(np.diff(o['wavelength'][0,:]))
        set_of_intergration = []
        plt.xlabel('Fibre')
        plt.ylabel('Time (s)')
        axis = [1*10**17, np.max(selection_1)]
        axis = [5 * 10 ** 17, 1.5 * 10 ** 19] #Take this out when done!
        im = plt.imshow(selection_1, aspect='auto',vmin=axis[0],vmax=axis[1] , extent = [1,41, max(dict["t"]), min(dict["t"])])
        string = dict["intergration_units"]
        plt.colorbar(im, label = str(string))
        # a tk.DrawingArea
        x = [1,41, max(dict["t"]), min(dict["t"])]
        dict["data_to_be_saved"] = ["intergration", result, selection_1, x, axis, dict["intergration_units"]]

        plt.show()

        print("result")
        print(result)


def Zooming_picker():
    '''Resets the picker and then sets up the canvas that takes the points for clicking. Sets the program to do zooming in'''
    dict["picker data list"] = []
    dict["picker setting"] = "Zooming"
    dict["cid"] = dict["fig"].canvas.mpl_connect('button_press_event', clicking_anywhere)

def Zooming_in():
    """
    Allows the user to click on two points in a graph and then sets the
    x and y axis to the min and max value

    :return:
    """

    global dict

    #call the data points from the pickers

    #clicking_point = dict["fig"].ginput(n=2, timeout=0, show_clicks=True)
    #point_1 = (clicking_point[0])
    #point_2 = (clicking_point[1])
    #y = [point_1[1], point_2[1]]
    #x = [point_1[0], point_2[0]]

    x = dict["picker data list"][0], dict["picker data list"][1]

    print(x)

    x_min = min(x)
    x_max = max(x)

    real_data = dict["total"][1]
    wave_data = dict["total"][0]

    reference_point_lower = find_point_from_below(x_min, wave_data)
    reference_point_upper = find_point_from_below(x_max, wave_data)
    wave_data = dict["total"][0]
    segment =  real_data[reference_point_lower:reference_point_upper+1]

    y_max = max(segment) + (0.1 * max(segment))
    y_min = min(segment) - (0.1 * max(segment))
    #ax.set_ylim(y_min, y_max)
    dict["ax"].set_xlim(x_min, x_max)
    dict["ax"].set_ylim(y_min, y_max)
    dict["current_x_axis"] = [x_min, x_max]
    #setting to check if we're zoomed in, so we can keep the zoom while changing time and fibre
    dict["are_zoomed"] = True

    dict["fig"].canvas.draw_idle()
def UnZooming():
    '''
    resets the x and y axis to include all of the data on the graph.

    :return:
    '''
    global dict

    minimum, maximum, min_wavelength_r, max_wavelength_r = dict["original_limits"]
    dict["ax"].set_ylim(minimum, maximum)
    dict["ax"].set_xlim(min_wavelength_r, max_wavelength_r)
    dict["current_x_axis"] = [min_wavelength_r, max_wavelength_r]
    #setting that we are no longer zoomed in
    dict["are_zoomed"] = False

    dict["fig"].canvas.draw_idle()

def comparing_ratios_picker():
    '''Resets the picker and then sets up the canvas that takes the points for clicking. Sets the program to do zooming in'''
    dict["picker data list"] = []
    dict["picker data sub list1"] = []
    dict["picker data sub list2"] = []
    dict["picker setting"] = "Comparing Ratios"
    dict["cid"] = dict["fig"].canvas.mpl_connect('button_press_event', clicking_anywhere)

def comparing_ratios():
    """
    Allows the user to select two areas along the x axis.
    It then compaires the intensity between the two ratios (area 1/area 2)
    It then plots a colour coded graph of all the different ratios across all the LOS and times.

    :return:
    """

    global dict

    x_axis = output['wavelength']

    spec = dict["o"]['spectra_abs']
    #clicking_point_1 = dict["fig"].ginput(n=2, timeout=0, show_clicks=True)
    #clicking_point_2 = dict["fig"].ginput(n=2, timeout=0, show_clicks=True)

    #clicking_point_1_x = clicking_point_1[0][0] , clicking_point_1[1][0]
    #clicking_point_2_x = clicking_point_2[0][0] , clicking_point_2[1][0]

    clicking_point_1_x = dict["picker data list"][0]


    clicking_point_2_x = dict["picker data list"][1]

    #dict["ax"].set_xlim(dict["current_x_axis"][0], dict["current_x_axis"][1])
    #dict["fig"].canvas.draw_idle()

    pixel_numbers_1 = []
    pixel_numbers_2 = []

    pixel_numbers_1.append(find_point_from_below((min(clicking_point_1_x)), x_axis[0]))
    pixel_numbers_1.append(find_point_from_below((max(clicking_point_1_x)), x_axis[0]))
    pixel_numbers_2.append(find_point_from_below((min(clicking_point_2_x)), x_axis[0]))
    pixel_numbers_2.append(find_point_from_below((max(clicking_point_2_x)), x_axis[0]))


    selection_1 = np.sum(spec[:,:,pixel_numbers_1[0]:pixel_numbers_1[1]],2)*np.median(np.diff(o['wavelength'][0,:]))
    selection_2 = np.sum(spec[:,:,pixel_numbers_2[0]:pixel_numbers_2[1]],2)*np.median(np.diff(o['wavelength'][0,:]))



    dict["data_to_be_saved"] = ["ratios", [1,40, max(dict["t"]), min(dict["t"])] ,selection_1, selection_2]

    create_naming_window_internal()

    plt.xlabel('Fibre')
    plt.ylabel('Time (s)')
    im = plt.imshow(selection_1/selection_2, aspect='auto',vmin=0.15,vmax=0.55 , extent = [1,40, max(dict["t"]), min(dict["t"])])
    plt.colorbar(im, label="Ratio")
    # a tk.DrawingArea
    plt.show()


def find_point_from_below(input, reference):
    count = 0

    while reference[count] < input:
        count += 1

    return count


def find_point_from_above(input, reference):
    count = -1

    while reference[count] < input:
        count -= 1
    count += 1
    return count

def retrieve_data_from_file():
    """
    Retrieves the data from the files

    :return: wavelength(x data), t(timings), spectra count(y data), settings (settings for calibrations)
    """
    # load
    spe = sls.load()
    wavelength = spe.wavelength
    spectra = np.squeeze(spe.data)
    wavelength_r = matlib.repmat(wavelength,np.shape(spectra)[1],1)
    # calculate time
    t0 = -2.5
    freq = float(spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.Acquisition.FrameRate.cdata)
    nthrown =int(spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.Experiment.Acquisition.FramesToInitiallyDiscard.cdata)
    t = t0 + (nthrown + np.arange(0,np.shape(spe.data)[0],1))/freq
    spectra = np.array(spectra)

    if len(np.shape(spectra)) == 2:
        spectra = np.reshape(spectra, [np.shape(spectra)[0],1,np.shape(spectra)[1]])

    bg = np.mean(spectra[t<-0.05,:,:],0)
    spectra = spectra - bg

    exp_time = float(
        spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.ShutterTiming.ExposureTime.cdata) / 1e3

    full_dir = spe.file.filepath
    dum = full_dir.rfind('/')
    dumdum = full_dir[0:dum].rfind('/')
    endd = full_dir.rfind('.spe')

    settings = {'exposure_time' : exp_time, 'fname' : full_dir[dumdum:endd], 'cwl' : float(spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Spectrometers.Spectrometer.Grating.CenterWavelength.cdata), 'grating_str' : spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Spectrometers.Spectrometer.Grating.Selected.cdata}

    #apply absolute calibration

    if spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.System.Spectrometers.Spectrometer.__dict__['_attributes']['serialNumber']=='32010485':
        eff = get_abs_calib(settings)

        if spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Spectrometers.Spectrometer.FilterWheel.Filter.Name.cdata=='2':
            eff=eff*(1/(10**(-0.5)))

        if spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Spectrometers.Spectrometer.FilterWheel.Filter.Name.cdata=='3':
            eff=eff*(1/(10**(-1.0)))

        if spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Spectrometers.Spectrometer.FilterWheel.Filter.Name.cdata=='4':
            eff=eff*(1/(10**(-1.5)))

        if spe.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Spectrometers.Spectrometer.FilterWheel.Filter.Name.cdata=='5':
            eff=eff*(1/(10**(-2.5)))


        spectra_cal = eff[None,:,:]*spectra/exp_time

        settings['abs_cal_type'] = 'ph/m2/sr/s/nm'

        dict['efficiency calibration'] = eff
    else:
        spectra_cal = np.array(np.empty( shape=(0, 0) ))
        settings['abs_cal_type'] = 'Counts'

    data_output = {'wavelength' : wavelength_r, 'spectra_counts' : spectra, 'time' : t, 'settings' : settings, 'spectra_abs' : spectra_cal}

    return data_output

def get_abs_calib(settings):

    calibr_str = calibr_settings()

    #get absolyte calibration

    cal = np.load(calibr_str['abs_sys_cal'],allow_pickle=True)

    abs_cal = cal['abs_cal']

    #find appropriate calibration

    found_index = int()

    for i in range(0,len(abs_cal)):
        if abs_cal[i]['cwl']==settings['cwl'] and abs_cal[i]['grating_str']==settings['grating_str']:
            found_index = i
            eff = abs_cal[i]['eff']


    if not found_index:
        cwl_list = []
        indx_list = []
        for i in range(0, len(abs_cal)):
            if abs_cal[i]['grating_str']==settings['grating_str']:
                cwl_list.append(abs_cal[i]['cwl'])
                indx_list.append(i)

        #make calibration matrix
        abs_cal_mat = np.zeros([np.shape(abs_cal[indx_list[0]]['eff'])[0],np.shape(abs_cal[indx_list[0]]['eff'])[1],len(indx_list)])
        indx_sort = np.argsort(indx_list)

        for i in range(0,len(indx_list)):
            abs_cal_mat[:,:,indx_sort[i]] = abs_cal[indx_sort[i]]['eff']

        cwl_list = np.array(cwl_list)
        eff_i = interp.interp1d(cwl_list[indx_sort],abs_cal_mat,kind='cubic')

        eff = eff_i(settings['cwl'])

    return eff

def calibr_settings():

    return {'abs_sys_cal' : '/common/projects/diagnostics/MAST/SPEXBDMS/analysed_calbration_files/current/abs_cal_calib.npz', 'spatial_instrumental_cal' : '/common/projects/diagnostics/MAST/SPEXBDMS/analysed_calbration_files/current/spatial_instrum_calib.npz'}

def load_new_data():
    # load
    """
    Reopens the original loading bar and allows for selection of new data to load.
    Then deletes and replots the graph with the new graph.

    :return:
    """

    global dict

    #changes current directory to the directory where the data files are
    cur_dir = os.getcwd()
    os.chdir('/common/projects/diagnostics/MAST/SPEXBDMS/Lightfield_output/Data_Files/')
    #loads the data
    output = retrieve_data_from_file()
    o = output
    dict["o"] = o
    dict["wavelength_r"] = output['wavelength']
    dict["t"] = output['time']
    (dict["settings"]) = output['settings']
    if len(output['spectra_abs'])>0:
        dict["data_spectra"] = output['spectra_abs']
    else:
        dict["data_spectra"] = output['spectra_counts']
    #changes the directory back
    os.chdir(cur_dir)

    dict["saveable_data"] = {}

    dict["data_spectra"] = np.einsum('kli->lki', dict["data_spectra"]) #Converts from Time, Fibre, Pixel to Fibre, Time, Pixel.
    dict["reference"] = dict["data_spectra"]

    A = dict["data_spectra"].tolist()
    dict["A"] = dict["data_spectra"].tolist()


    for widget in subframe.winfo_children():
        widget.destroy()
    dict["ax_time"].remove()
    dict["ax_fibre"].remove()
    dict["ax"].remove()
    plot_graph()

    wavelength_r = dict["wavelength_r"]
    t = dict["t"]
    data_spectra = dict["data_spectra"]
    return wavelength_r, data_spectra, t


def main(slider_fibre, slider_time):
    """
    fibre: int
    the value for fibre from slider
    time: int
    the value for time from slider

    is processor that takes any selection of fibre or time and returns the appropriate data selected from the A data.
    It also currently adjusts the time selection as I'm still figuring out how to adjust the steps of the sliders.
    :return:
    """


    global dict

    time_number = (slider_time - dict["shift_offset"]) / dict["shift_multiplier"]


    modifier = dict["desired_sample_rate"] / dict["current_sample_rate"]
    time_modified = int(time_number * modifier)

    data_lst = A[slider_fibre][time_modified]
    data_lst = (dict["A"])[slider_fibre][time_modified]
    data_lst = df.create_single_sublist(data_lst)
    dict["total"] = process(data_lst)
    total = dict["total"]
    return total


def process(real_data):
    """
    real_data: List
    A list of the values for the pixels to be processed

    processes the data. creates and applies exposure time, moniters saturation, also makes the wave data that goes along
    the x axis.

    :return: total: dataframe
    A dataframe of the processed pixels, the values, (and also the time which is redundent now but hey) and the x axis
    wave data
    """

    global dict

    # Note:
    # The wavelength range of the XSA data is probably around 386-404 nm
    max_waveln = np.max(dict["wavelength_r"])
    min_waveln = np.min(dict["wavelength_r"])
    # I belive the exposure time is 8000 seconds, so converting to seconds


    # selecting the prefered fibre and time, later to be placed into a GUI
    fibre = 2
    # This selects from a time onwards to beging collecting data as a lot of the earlier data is unhelpful
    min_time = 18
    max_time = 28
    N = 56

    # setting a maximum possible and minimum possible value
    yaxis_min = -1 * 10 ** 9
    yaxis_max = 2 * (10 ** 10)

    # Setting the values for the minimum point for linearity and
    A_min = 0.1 * 10 ** 8
    B_max = 1 * 10 ** 20

    current_sample_rate = 10
    desired_sample_rate = 2

    # using functions to create lists for the time and pixel positions relative to the values
    time_lst = df.create_time(real_data)
    pixel_lst = df.create_pixel(real_data)

    # taking them all from super lists to singular lists
    time_lst = df.merge_sublists(time_lst)
    pixel_lst = df.merge_sublists(pixel_lst)
    real_data = df.merge_sublists(real_data)


    # forging the standard dataframe for input to means and stds
    final_df = pd.DataFrame({
        'time': time_lst,
        'pixel': pixel_lst,
        'value': real_data
    })

    # final_df = df.means_and_stds(final_df)

    # converting the output from means and stds to lists for plotting
    means = final_df["value"].values.tolist()
    pixel_data = final_df["pixel"].values.tolist()
    # stds = final_df["Standard Deviations"].values.tolist()

    means_check = np.array(means)
    # counting the number of oversaturated values
    saturation = np.count_nonzero(means_check > B_max)
    # sets up a flag system for future use in general
    warning_flag = 0
    if saturation > 350:
        warning_flag = 2
    elif saturation > 10:
        warning_flag = 1
    else:
        warning_flag = 0

    if warning_flag == 1:
        print("minor saturation occuring")
    elif warning_flag == 2:
        print("Major saturation occuring")

    # std_error = []
    # if min_time == max_time:
    #    for i in stds:
    #        i = 0
    #        std_error.append(i)
    # else:
    #    for i in stds:
    #        i = (i / (math.sqrt(max_time - min_time)))
    #        std_error.append(i)

    nm_per_pixel = (max_waveln - min_waveln) / len(pixel_data)
    wave_data = []

    # a way to take the max and min wavelength and convert it into a per pixel measurement for plotting
    wave_data = np.linspace(min_waveln,max_waveln,np.shape(dict["wavelength_r"])[1])

    # plotting the new nm postion and the mean values
    # plt.plot(wave_data, means)

    dict["total"] = []
    dict["total"].append(wave_data)
    dict["total"].append(means)
    total = dict["total"]
    return total

def open_spectra_window():
    """
    Opens a new window for selecting the spectra
    also detects the x limits and only shows the spectra within those x limits
    (raises and error if you try to zoom in on an area that doesn't show a currently visible line, but this doesn't
    appear to actually break the program)
    :return:
    """

    global dict

    top = Tk.Toplevel()
    top.title("Spectra Selection Window")
    top.geometry("200x500")
    btn2 = Tk.Button(top, text="Process", command=spectra_proccess).grid(row=0, column=0)

    # creates a global listbox so that it can be read

    # creates a listbox that allows for multiple selection
    dict["spec_listbox"] = Tk.Listbox(top, selectmode="extended", height = 30, width = 27)
    count = 0
    limits = dict["current_x_axis"]
    while int(known_spectra_lines[count][1]) < limits[0]:
        count += 1
    dict["minimum_spectra_line"] = count
    count = -1
    while int(known_spectra_lines[count][1]) > limits[1]:
        count -= 1
    maximum_spectra_line = count


    #selects which spectra lines to show
    sliced_known_spectra_lines = known_spectra_lines[dict["minimum_spectra_line"]:maximum_spectra_line+1]
    sliced_known_spectra_lines = reversed(sliced_known_spectra_lines)
    for i in sliced_known_spectra_lines:
        dict["spec_listbox"].insert(count, (str(i[0][0]) + ' ' + str(i[1])))
        count += 1

    dict["spec_listbox"].grid(row=1, column=0)

def open_sample_rate_window():
    """
    Creates a seperate window that will have an entry box for the user to input their desired sample rate
    should also tell them if they input an incorrect input.

    The process button should then remake the graph with the new sample rate

    :return:
    """

    global dict

    dict["top_sample"] = Tk.Toplevel()
    dict["top_sample"].geometry("300x100")
    dict["top_sample"].title("Sample rate Selection Window")

    dict["entry_box"] = Tk.Entry(dict["top_sample"], bg="white", fg="grey", width=22)
    dict["entry_box"].insert(0, 'Enter desired sample rate: ')
    entry_box_units = Tk.Label(dict["top_sample"], text="Hz").grid(row=0, column=1)
    update_btn = Tk.Button(dict["top_sample"], text="Update Sample rate", command=calculate_sample_rate).grid(row=2, column=0)
    # this grid pack needs to be on a seperate line otherwise the entry_box type gets set to None and doesn't have .insert
    dict["entry_box"].grid(row=0, column=0)

    # allowing for the text box to know when it needs to be clicked on
    dict["entry_box"].bind('<FocusIn>', on_entry_click)
    dict["entry_box"].bind('<FocusOut>', on_focusout)


def open_max_min():
    """
    opens a tkinter window allowing the user to select if they want the max min lines to be shown

    :return:
    """
    global dict

    top_max_min = Tk.Toplevel()
    top_max_min.title("Select max and min")

    btn2 = Tk.Button(top_max_min, text="Process", command=min_max_proccess).grid(row=0, column=0)

    # creates a listbox that allows for multiple selection
    dict["horiz_listbox"] = Tk.Listbox(top_max_min, selectmode="multiple")
    count = 0
    for i in horizontal:
        dict["horiz_listbox"].insert(count, i[0])
        count += 1

    dict["horiz_listbox"].grid(row=1, column=0)


def on_entry_click(event):
    """
    Whenever entry is clicked it gets rid of the inital text in the box.

    """
    if dict["entry_box"].get() == 'Enter desired sample rate: ':
        dict["entry_box"].delete(0, "end")  # delete all the text in the entry
        dict["entry_box"].insert(0, '')  # Insert blank for user input
        dict["entry_box"].config(fg='black')


def on_focusout(event):
    """
    Should re-insert the standard text when the box is clicked off, but I'm not really sure how the focusout
    and focusin tags work so may be janky.

    :param event:
    :return:
    """
    if dict["entry_box"].get() == '':
        dict["entry_box"].insert(0, 'Enter desired sample rate: ')
        dict["entry_box"].config(fg='grey')


def spectra_proccess():
    """
    plots the selected spectra upon the button being clicked,

    """
    global dict

    values = [dict["spec_listbox"].get(idx) for idx in dict["spec_listbox"].curselection()]
    true_or_false = [False] * (len(known_spectra_lines))
    dict["total_spec"] = dict["spec_listbox"].get(0, Tk.END)
    count = dict["minimum_spectra_line"]


    # creating a true false list for if I want a spectra line to be visible or not
    for i in values:
        for x in dict["total_spec"]:
            if i == x:
                true_or_false[count] = True
            count += 1
        count = dict["minimum_spectra_line"]

    count_2 = 0
    for i in true_or_false:
        dict["spectra_index"][count_2].set_visible(i)
        dict["text_index"][count_2].set_visible(i)
        count_2 += 1

    dict["fig"].canvas.draw_idle()

    count_2 = 0


def min_max_proccess():
    """
    is the process that sets the horizontal (max and min) lines to either be plotted or not on the graph,
    is called by the spectra tkinter window to be initiated.

    :return:
    """

    global dict


    values = [dict["horiz_listbox"].get(idx) for idx in dict["horiz_listbox"].curselection()]
    true_or_false = [False] * (len(horizontal))
    dict["total_spec"] = dict["horiz_listbox"].get(0, Tk.END)
    count = 0

    # creating a true false list for if I want a spectra line to be visible or not
    for i in values:
        for x in dict["total_spec"]:
            if i == x:
                true_or_false[count] = True
            count += 1
        count = 0

    count_2 = 0
    for i in true_or_false:
        dict["horizontal_index"][count_2].set_visible(i)
        count_2 += 1

    dict["fig"].canvas.draw_idle()


# Update values
def update_slider(val):
    """
    val: does nothing
    s_fibre.val: (gets turned into interger)
    s_time.val: (gets turned into interger)
    They are both slider values in long float format, both are drawn each time on update.

    Update is a whole function that completely replots the data with a new set upon the slider being changed.


    doesn't return anything but it does autoset the x and y axis limits and updates the plot
    """
    global dict

    B_max = 1 * 10 ** 16
    slider_fibre = (int(dict["s_fibre"].val)) - 1
    slider_time = (dict["s_time"].val)
    dict["total"] = main(slider_fibre, slider_time)
    real_data = dict["total"][1]
    wave_data = dict["total"][0]
    dict["f_d"].set_data(wave_data, real_data)
    dict["fig"].canvas.draw_idle()


    Unzoomed_x_min = np.min(dict["wavelength_r"])
    Unzoomed_x_max = np.max(dict["wavelength_r"])
    Unzoomed_y_max = max(real_data) + (0.1 * max(real_data))
    Unzoomed_y_min = (min(real_data) - (0.1 * max(real_data)))

    if dict["are_zoomed"] == True:
        zoomed_x_min, zoomed_x_max = dict["current_x_axis"]

        reference_point_lower = find_point_from_below(zoomed_x_min, wave_data)
        reference_point_upper = find_point_from_below(zoomed_x_max, wave_data)
        segment = real_data[reference_point_lower:reference_point_upper + 1]
        zoomed_y_max = max(segment) + (0.1 * max(segment))
        zoomed_y_min = min(segment) - (0.1 * max(segment))
        dict["ax"].set_ylim(zoomed_y_min, zoomed_y_max)
    elif dict["are_zoomed"] == False:
        dict["ax"].set_ylim(Unzoomed_y_min, Unzoomed_y_max)
        dict["ax"].set_xlim(Unzoomed_x_min, Unzoomed_x_max)
        dict["current_x_axis"] = [Unzoomed_x_min, Unzoomed_x_max]


    dict["original_limits"] = Unzoomed_y_min, Unzoomed_y_max, Unzoomed_x_min, Unzoomed_x_max


def calculate_sample_rate():
    """
    This is the part that will take the inputted value and use that to resample the data.
    It will also produce an error that will appear in the window if a non-integer value is inputted.
    Currently has a problem in that introcuding the label changes up the layout of the window.
    Trying to find a way to make the label invisible and then become visible so this is a placeholder, still works, just ugly

    :return:
    """
    global dict

    dict["desired_sample_rate"] = dict["entry_box"].get()
    # using a try function to see if the correct entry has been made
    try:
        dict["desired_sample_rate"] = int(dict["desired_sample_rate"])
    except ValueError:
        dict["error_label"] = Tk.Label(dict["top_sample"], text="Error: Unrecognised input, please use integer values only")
        dict["error_label"].grid(row=3, column=0, columnspan=2)
    except NameError:
        dict["error_label"] = Tk.Label(dict["top_sample"], text="Error: Please enter a value")
        dict["error_label"].grid(row=3, column=0)

    # timeing to see if multiprocessing is needed
    start = time.perf_counter()
    raw_data_using = dict["data_spectra"].tolist()
    print(raw_data_using)
    desired_sample_rate = dict["desired_sample_rate"]
    current_sample_rate = dict["current_sample_rate"]
    resampled_data = threeD_resampling(raw_data_using, current_sample_rate, desired_sample_rate)
    stop = time.perf_counter()
    print(f"time take {stop - start:0.4f} seconds")
    dict["A"] = resampled_data


def threeD_resampling(data, current_sample_rate, desired_sample_rate):
    """
    :param data: Superlist
    a Superlist that contains values for every fibre, and every time within each fibre
    :param current_sample_rate: Is the desired sample rate that will need to be converted towards
    :param desired_sample_rate: Is the current sample rate  that it is being compared to
    :return:
    """

    fibre_count = 0
    final_data = []
    while fibre_count < len(data):
        # placeholder = df.resample(data[fibre_count],current_sample_rate,desired_sample_rate)
        placeholder = df.test_resample(data[fibre_count], current_sample_rate, desired_sample_rate)
        final_data.append(placeholder)
        fibre_count += 1
    return final_data


def plot_graph():
    """
    Plots the graph in the frame. also adds in sliders that allow for real time changes to the data displayed

    :return:
    """

    # Having to set a lot of these internal variables as globals in order for them to be useable in other functions.
    # I don't think this is the best way to do it so if you have an improvement feel free to suggest it.
    global dict


    dict["are_zoomed"] = False

    # esentially does what plt.show() does but in tkninter
    canvas = FigureCanvasTkAgg(dict["fig"], subframe)
    canvas.get_tk_widget().grid(row=1, column=2)

    dict["ax"] = dict["fig"].add_subplot(111)
    dict["fig"].subplots_adjust(bottom=0.25)
    fibre_min = 1
    fibre_max = ((np.shape(dict["reference"]))[0])
    reference_time = dict["t"]
    reference_time = reference_time
    dict["shift_multiplier"] = reference_time[1] - reference_time[0]
    time_min = reference_time[0]
    time_max = reference_time[-1]
    dict["shift_offset"] = time_min

    dict["ax"].axis([0, 9, 20, 40])
    # creting all the sliders
    dict["ax_time"] = dict["fig"].add_axes([0.12, 0.05, 0.78, 0.03])
    dict["s_time"] = Slider(dict["ax_time"], 'Time', time_min, time_max, valinit=0, facecolor='#cc7000', valstep=dict["shift_multiplier"])
    dict["ax_fibre"] = dict["fig"].add_axes([0.12, 0.1, 0.78, 0.03])
    dict["s_fibre"] = Slider(dict["ax_fibre"], 'Fibre', fibre_min, fibre_max, valinit=0, valfmt=' %1.f ', facecolor='#cc7000')

    infinite = [-1 * 10 ** 100, 1 * 10 ** 100]

    dict["horizontal_index"] = []
    colour_index = ["b", "r"]
    horizontal_count = 0
    for i in horizontal:
        # creating a plot vertically upwards for all the spectra in the spectra list
        blank = 0
        dict["horizontal_index"].append(blank)
        # The labeling allows it to be selected
        dict["horizontal_index"][horizontal_count], = dict["ax"].plot(infinite, [horizontal[horizontal_count][1],
                                                                 horizontal[horizontal_count][1]],
                                                      color=colour_index[horizontal_count], visible=False,
                                                      label=horizontal[horizontal_count][1])
        horizontal_count += 1

    dict["spectra_index"] = []
    dict["text_index"] = []
    graph_text_index = []
    spectra_count = 0
    for i in known_spectra_lines:
        # creating a plot vertically upwards for all the spectra in the spectra list
        blank = 0
        dict["spectra_index"].append(blank)
        dict["text_index"].append(blank)
        graph_text_index.append(blank)
        text = (str(known_spectra_lines[spectra_count][0][0]))
        dict["spectra_index"][spectra_count], = dict["ax"].plot([known_spectra_lines[spectra_count][1], known_spectra_lines[spectra_count][1]], infinite,
                                                color="red", visible=False, label=known_spectra_lines[spectra_count][1],
                                                ls=('dotted'))
        # gives a text labeling each spectra line next to it
        dict["text_index"][spectra_count] = dict["ax"].text(known_spectra_lines[spectra_count][1], 0.5 * 10 ** 9, str(text), fontsize=12,
                                            rotation=90, verticalalignment='center', visible=False)
        spectra_count += 1


    # checkbuton widget
    # activated = [True, True]
    # axCheckButton = fig.add_axes([0.03, 0.4, 0.15, 0.15])
    # chxbox = CheckButtons(axCheckButton, activated)
    # chxbox.on_clicked(func)
    # fig, axs = plt.subplots()

    dict["f_d"], = dict["ax"].plot([], [], linewidth=2.5, color="limegreen", picker = True)

    (dict["ax"]).set_title((dict["settings"])['fname'])
    (dict["ax"]).set_ylabel((dict["settings"])['abs_cal_type'])
    (dict["ax"]).set_xlabel('Wavelength (nm)')

    dict["intergration_units"] = dict["settings"]['abs_cal_type'][:10]


    #dict["fig"].canvas.mpl_connect('pick_event', onpick2) notcurrently used

    #dict["fig"].canvas.mpl_connect('pick_event', onpick1) #not currently needed

    # when the sliders are changed it activates the update function
    dict["s_time"].on_changed(update_slider)
    dict["s_fibre"].on_changed(update_slider)



if __name__ == "__main__":


    global dict
    dict = {}
    savable_data = {}
    dict["picker data list"] = []
    dict["saveable_data"] = savable_data

    example_spectra_lines = (np.load('/home/gwill/PycharmProjects/scheduler-routines/MAST-U_datafiles/wavelength_database.npz', allow_pickle=True))
    description = example_spectra_lines['description']
    example_spectra_wavelength = example_spectra_lines['wavelength']

    arr = np.stack((description, example_spectra_wavelength), axis=1)
    #print(arr)
    # Stores the data into the A variable to be drawn from later
    #changes current directory to the directory where the data files are
    cur_dir = os.getcwd()
    os.chdir('/common/projects/diagnostics/MAST/SPEXBDMS/Lightfield_output/Data_Files/')
    #loads the data
    # loads the data
    output = retrieve_data_from_file()
    o = output
    dict["o"] = output
    dict["wavelength_r"] = output['wavelength']
    dict["t"] = output['time']
    dict["settings"] = output['settings']

    #if a.size == 0:
    if len(output['spectra_abs'])>0:
        dict["data_spectra"] = output['spectra_abs']
    else:
        dict["data_spectra"] = output['spectra_counts']
    #changes the directory back
    os.chdir(cur_dir)

    #data needs to be in the shape of - Fibre, Time, Pixel
    dict["data_spectra"] = np.einsum('kli->lki', dict["data_spectra"]) #Converts from Time, Fibre, Pixel to Fibre, Time, Pixel.
    dict["reference"] = dict["data_spectra"]
    A = dict["data_spectra"].tolist()
    dict["A"] = dict["data_spectra"].tolist()
    sample_rate = int(np.round(1 / ((dict["t"])[1] - (dict["t"])[0])))
    dict["current_sample_rate"] = sample_rate
    dict["desired_sample_rate"] = dict["current_sample_rate"]
    A_min = 0.1 * 10 ** 19
    B_max = 1 * 10 ** 19
    horizontal = [["A_min",A_min], ["B_max", B_max]]
    known_spectra_lines = arr

    # makes the main window called root
    root = Tk.Tk()
    root.wm_title("GUI for data viewing")
    root.geometry("1500x750")
    # creating a frame to contain the graph

    subframe = Tk.LabelFrame(root, padx=100, pady=75)
    subframe.grid(row=0, column=3, padx=0, pady=0, rowspan=10, columnspan = 6)

    dict["fig"] = plt.Figure(figsize = (10,5))

    btn_1 = Tk.Button(root, text="Change sample rate", command=open_sample_rate_window).grid(row=0, column=0)

    btn_2 = Tk.Button(root, text="Display Lines", command=open_spectra_window).grid(row=1, column=0)

    btn_3 = Tk.Button(root, text="Display maximum and minimum", command=open_max_min).grid(row=2, column=0)

    btn_4 = Tk.Button(root, text="Load Data", command= load_new_data).grid(row=3, column=0)

    btn_6 = Tk.Button(root, text="Zoom", command= Zooming_picker).grid(row=10, column=3)

    btn_7 = Tk.Button(root, text="UnZoom", command= UnZooming).grid(row=10, column=4)

    btn_8 = Tk.Button(root, text="Intergrate selection", command= intergration_window_graph).grid(row=10 , column=6)

    btn_9 = Tk.Button(root, text="Comparing ratios", command=comparing_ratios_picker).grid(row=10, column=5)

    btn_10 = Tk.Button(root, text="Export saved data", command=create_naming_window_external).grid(row=4, column=0)



    plot_graph()


    # don't remove unless you like errors in your code
    Tk.mainloop()


'''
“possible improvments: 


Want to be able to display multiple intergrals. Boxes to switch.Allowing for ratios (so save the data)

saving the shot number to individual data points

Having some documentation on how to work the GUI, what it's capable of, a guide how to use it.
'''