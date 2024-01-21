"""
    This contains functions for specific tasks
"""
import tkinter as tk
import customtkinter as ctk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.filedialog import askopenfile as aof
import shutil
from myapp.appclasses.fileclass import FILEHANDLER
import re
import os
from datetime import datetime


def display_msg(msg=None):
    """ Pops a message when there is need to. Message to be displayed can be given as an arg """
    if msg is None:
        showinfo("Alert!", f"I am a message button.")
    else:
        showinfo("Alert!", "{}".format(msg))


def show_widget(my_widget, x, y):
    """ displays a widget in the given positions"""
    my_widget.place(x=x, y=y)


def upload_file(folder_id, projectname=None):
    """ Uploads new project file 
        Calls FILEHANDLER class to save and process file
        Returns a tuple containing the project name and the file name 
    """
    if folder_id == 1:
        path = "/"
        f_types = [("Excel file", "*.xlsx"), ("Excel file", "*.xls"), ("Excel file", "*.csv")]
        filename = tk.filedialog.askopenfilename(initialdir=path, filetypes=f_types)
        fh = FILEHANDLER(folder_id)
        result = fh.save_file(filename)
    elif folder_id == 2:
        path = "myapp/documents/after/"
        check = check_that_file_exists(projectname, path)
        if not check or projectname == None:
            f_types = [("Excel file", "*.xlsx"), ("Excel file", "*.xls"), ("Excel file", "*.csv")]
            filename = tk.filedialog.askopenfilename(initialdir="/", filetypes=f_types)
        else:
            f_types = [("Excel file", "*.xlsx"), ("Excel file", "*.xls"), ("Excel file", "*.csv")]
            filename = tk.filedialog.askopenfilename(initialdir=path, filetypes=f_types)

        fh = FILEHANDLER(folder_id)
        result = fh.save_file(filename, projectname)

    return result


def select_file(path, folder_id):
    """ Opens the path of existing project for user to select file 
        Calls FILEHANDLER class to process file
        Returns a tuple containing the project name and the file name 
    """
    f_types = [("Excel file", "*.xlsx"), ("Excel file", "*.xls"), ("Excel file", "*.csv")]
    filename = tk.filedialog.askopenfilename(initialdir=path, filetypes=f_types)
    fh = FILEHANDLER(folder_id)
    result = fh.use_saved_file(filename)
    return result  # tuple


def create_image_obj(imagepath, size):
    """ This creates a CTkImage object that could be used on any of the app widgets
            It takes two args: imagepath (string)  to image and size (tuple) representing the width and height of image (w,h)
            Returns the image obj
        """
    image = Image.open(imagepath)
    # img = ImageTk.PhotoImage(image)
    img = ctk.CTkImage(image, size=size)

    return img


def upload_result_file(projectname):
    """ This will allow user to select the appropriate file from within or outside the app using the projectname.
        It first checks if the file already exists within the project for the user to select it; 
        if not, it opens the users device file explorer for them to select the appropriate file from their system.
        Returns the result of the processed file
    """
    path = "myapp/documents/after/"
    check = check_that_file_exists(projectname, path)
    if not check or projectname == None:
        f_types = [("Excel file", "*.xlsx"), ("Excel file", "*.xls"), ("Excel file", "*.csv")]
        filename = tk.filedialog.askopenfilename(filetypes=f_types)
    else:
        f_types = [("Excel file", "*.xlsx"), ("Excel file", "*.xls"), ("Excel file", "*.csv")]
        filename = tk.filedialog.askopenfilename(initialdir=path, filetypes=f_types)

    return None


def check_that_file_exists(projectname, directory):
    """ Uses filename to match any file in the given directory.
        Returns True if there is a match, else False
    """
    files = os.listdir(directory)
    if len(files) > 0:
        for file in files:
            if re.match(projectname, file.split("_")[0]):
                return True
    return False


def unique_list(mylist):
    """Returns unique values of a list"""
    new_list = []
    for x in mylist:
        if x not in new_list:
            new_list.append(x)
    return new_list


def enslave_strings(mystrings):
    """Accepts multiword strings and returns a single string in which the words are chained with underscore"""
    if len(str(mystrings).split()) > 1:
        return "_".join(str(mystrings).lower().split())
    elif len(str(mystrings).split()) == 1:
        return str(mystrings).lower()
    else:
        return "untitled"


def get_date_format(data: list):
    """Decodes the format of a date/datetime literal from a list of datetimes of unknown formats and converts it to a
    datetime object"""

    for x in data:
        if find_prime_date(x):
            datetyme = x
            # check if input is datetime or just date
            check = datetyme.split(" ")
            if len(check) > 1:
                # it is a datetime

                # check that it has microseconds or not
                if len(datetyme.split(".")) > 1:
                    # it has microseconds
                    possible_formats = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%d-%m %H:%M:%S.%f", "%d-%m-%Y %H:%M:%S.%f",
                                        "%m-%d-%Y %H:%M:%S.%f", "%Y/%m/%d %H:%M:%S.%f", "%Y/%d/%m %H:%M:%S.%f",
                                        "%d/%m/%Y %H:%M:%S.%f", "%m/%d/%Y %H:%M:%S.%f"]
                else:
                    # no microseconds %H:%M:%S.%f
                    possible_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%d-%m %H:%M:%S", "%d-%m-%Y %H:%M:%S",
                                        "%m-%d-%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y/%d/%m %H:%M:%S",
                                        "%d/%m/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S"]
            else:
                # it is just a date
                possible_formats = ["%Y-%m-%d", "%Y-%d-%m", "%d-%m-%Y", "%m-%d-%Y", "%Y/%m/%d", "%Y/%d/%m", "%d/%m/%Y",
                                    "%m/%d/%Y"]

            for x in possible_formats:
                if check_datetime_format(datetyme, x):
                    return x
    return None


def check_datetime_format(datetyme: str, formert: str):
    """Checks if format matches the format of the datetime supplied"""
    try:
        obj = datetime.strptime(str(datetyme), formert)
        # print(datetyme, " ", formert)
        return True
    except:
        return False


def find_prime_date(datetyme: str):
    """Checks if the input date in the given string is a distinctive date e.g 2001-6-23 vs 2001-6-9"""
    # split the string to get the date portion
    datestr = datetyme.split(" ")[0]

    if len(datestr.split("/")) > 1:
        datelist = [x for x in datestr.split("/") if len(x) == 2]
        if len(datelist) > 0:
            for x in datelist:
                if int(x) > 12:
                    return True
    elif len(datestr.split("-")) > 1:
        datelist = [x for x in datestr.split("-") if len(x) == 2]
        if len(datelist) > 0:
            for x in datelist:
                if int(x) > 12:
                    return True
    return False


def make_dynamic(widget):
    """dynamically resizes widgets wrt window size"""
    col_count, row_count = widget.grid_size()

    for i in range(row_count):
        widget.grid_rowconfigure(i, weight=1)

    for i in range(col_count):
        widget.grid_columnconfigure(i, weight=1)

    for child in widget.children.values():
        child.grid_configure(sticky="nsew")
        make_dynamic(child)


def get_highest_values(data, num_pairs):
    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    highest_pairs = {k: sorted_data[k] for k in list(sorted_data)[:num_pairs]}
    return highest_pairs


def reduce_key_and_add_to_total_uptime(data_list, key, percentage):
    for month_data in data_list:
        if key in month_data and 'total_uptime' in month_data:
            reduced_value = month_data[key] * (percentage / 100)
            month_data[key] *= (1 - percentage / 100)
            month_data['total_uptime'] += reduced_value
            if key != 'total_downtime':
                month_data['total_downtime'] -= reduced_value

    return data_list


def normalize_lists(list1, list2):
    """
    Compare two lists and fill the deficient list based on the content type.
    If the content is numeric, fill with zeros for the missing elements.
    If the content is string, fill with missing elements from the other list.

    Args:
    - list1: First list to compare.
    - list2: Second list to compare.

    Returns:
    - Tuple containing the two filled lists.
    """
    if all(isinstance(item, (int, float)) for item in list1) and all(isinstance(item, (int, float)) for item in list2):
        # Both lists contain numbers
        max_len = max(len(list1), len(list2))
        filled_list1 = list1 + [0] * (max_len - len(list1))
        filled_list2 = list2 + [0] * (max_len - len(list2))
        list1 = filled_list1
        list2 = filled_list2
    elif all(isinstance(item, str) for item in list1) and all(isinstance(item, str) for item in list2):
        # Both lists contain strings
        max_len = max(len(list1), len(list2))
        filled_list1 = list1 + list(set(list2) - set(list1))[:max_len - len(list1)]
        filled_list2 = list2 + list(set(list1) - set(list2))[:max_len - len(list2)]
        list1 = filled_list1
        list2 = filled_list2
    else:
        # Lists have different content types
        error = 'Both lists must have the same content type.'
        display_msg(error)
    return list1, list2


def convert_lists_to_dict(keys, values):
    # Check if the lengths of both lists are equal
    if len(keys) != len(values):
        display_msg('cannot convert lists to dictionary')

    result_dict = {}

    # Iterate through the lists and construct the dictionary
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]

    return result_dict


def normalize_dictionaries(dict1, dict2):
    # Check if the dictionaries have the same keys
    if not (all(element in list(dict1.keys()) for element in list(dict2.keys())) or
            all(element in list(dict2.keys()) for element in list(dict1.keys()))):
        display_msg("Dictionaries must have the same keys")

    # Determine the dictionary with the highest number of keys
    if len(dict1) >= len(dict2):
        larger_dict = dict1
        smaller_dict = dict2
    else:
        larger_dict = dict2
        smaller_dict = dict1

    # Use the keys from the dictionary with the highest number of keys
    keys_to_use = larger_dict.keys()

    # Retrieve values from each dictionary or return zero if the key is not present
    values_dict1 = [dict1.get(key, 0) for key in keys_to_use]
    values_dict2 = [dict2.get(key, 0) for key in keys_to_use]

    return values_dict1, values_dict2


def get_screen_resolution():
    # Create a hidden Tkinter window to access screen information
    root = tk.Tk()
    root.attributes('-alpha', 0)  # Hide the window

    # Get the screen width and height in pixels
    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())

    root.destroy()

    return screen_width, screen_height
