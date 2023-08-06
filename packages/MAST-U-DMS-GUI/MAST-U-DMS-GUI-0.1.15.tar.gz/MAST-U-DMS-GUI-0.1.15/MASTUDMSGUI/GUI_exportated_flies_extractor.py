import numpy as np
import matplotlib.pyplot as plt
import tkinter as Tk
from tkinter import filedialog
import os
import click

global listbox
global dictionary

def ratios(data):
    selection_1 = data[2]
    selection_2 = data[3]
    x = data[1]
    plt.xlabel('Fibre')
    plt.ylabel('Time (s)')
    im = plt.imshow(selection_1 / selection_2, aspect='auto', vmin=0.15, vmax=0.55,extent=x)
    plt.colorbar(im, label="Ratio")
    plt.show()

def intergration(data):
    fig, axis = plt.subplots()
    print(data[1])
    selection_1 = data[2]
    widths = data[3]
    axis = data[4]
    intergration_units = data[5]


    plt.xlabel('Fibre')
    plt.ylabel('Time (s)')
    im = plt.imshow(selection_1, aspect='auto', vmin=axis[0], vmax=axis[1],
               extent=widths)
    plt.colorbar(im, label=str(intergration_units))
    plt.show()
    if True == False:
        wavelength = 0
        intergration_data = 0
        plt.plot(wavelength, intergration_data)
        maximum = np.max(intergration_data) + (0.1 * np.max(intergration_data))
        minimum = (np.min(intergration_data) - (0.1 * (np.max(intergration_data))))
        axis.set_ylim(minimum, maximum)
        axis.set_xlim(np.min(wavelength), np.max(wavelength))
        plt.show()

def sort_data(data):
    if data[0] == "ratios":
        ratios(data)
    elif data[0] == "intergration":
        intergration(data)

def process():
    global listbox
    global dictionary
    values = [listbox.get(idx) for idx in listbox.curselection()]
    for i in values:
        value = str(i)
        data = dictionary[value]
        sort_data(data)
@click.command()
def main():
    global listbox
    global dictionary
    file_window = Tk.Tk()
    file_window.withdraw()

    cur_dir = os.getcwd()
    os.chdir('/common/projects/diagnostics/MAST/SPEXBDMS/GUI_Exported_Data')
    file_path = filedialog.askopenfilename()
    os.chdir(cur_dir)
    test = np.load(file_path, allow_pickle = True)
    file_window.destroy()

    root = Tk.Tk()
    root.geometry("300x200")
    root.wm_title("GUI for data viewing")

    names = []

    dictionary = test["arr_0"][0]

    for i,j in test["arr_0"][0].items():
        names.append(i)

    listbox = Tk.Listbox(root, selectmode="multiple")

    count = 0
    for i in names:
        listbox.insert(count, i)
        count += 1

    listbox.grid(column = 0, row = 0)

    btn = Tk.Button(root, text = "Process selected data", command = process)
    btn.grid(column = 0, row = 1)

    root.mainloop()

main()