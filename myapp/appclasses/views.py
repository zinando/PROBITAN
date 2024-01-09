""" This module creates a view class. """
from tkinter import *
import customtkinter as ctk
from myapp.helpers import myfunc as func
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WinView(ctk.CTk):
    """ Main application window class """

    projectname = None
    projectfile = None
    active_button = None
    project_class_before = None
    project_class_after = None
    active_class = None
    timer_id = None
    animation_canvas = None
    before_events_dropdown_list = []
    after_events_dropdown_list = []

    def __init__(self):
        """ initialize the window view class """

        super(WinView, self).__init__()
        self._set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        w, h = 860, 660
        self.w, self.h = w, h
        position_x = (self.winfo_screenwidth() // 2) - (w // 2)
        position_y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry("{}x{}+{}+{}".format(w, h, position_x, position_y))
        self.title('PROBITAN - An Equipment Process Reliability Analytical Tool.')
        func.make_dynamic(self)
        self.top_level_window = None
        self.resizable(False, False)
        # func.display_msg(str(self.winfo_width()))

    def base_view(self):
        """ creates the project entry view """

        main_bg = func.create_image_obj('myapp/appfiles/images/bg/bg.JPG', (self.w, self.h))

        # Labels
        bg_lab1 = ctk.CTkLabel(self, text="", image=main_bg, bg_color="#495068", fg_color="#495068", height=self.h,
                               width=self.w).place(x=0, y=0)

        # buttons
        start_btn = ctk.CTkButton(self, text="New Project", bg_color="#495068", fg_color="#fffada",
                                  text_color="#495068", width=self.w // 11, height=self.h // 20,
                                  command=self.create_new_project)

        start_btn.place(x=self.w // 3, y=(self.h // 2) + 140)
        self.update()

        select_btn = ctk.CTkButton(self, text="Select Project", bg_color="#495068",
                                   fg_color="#fffada",
                                   text_color="#495068", width=self.w // 11, height=self.h // 20,
                                   command=self.select_project)
        select_btn.place(x=(self.w // 3) + 120, y=self.h // 2 + 140)

        # select_btn.place(x=start_btn.winfo_x() + 120, y=start_btn.winfo_y())

    def create_label(self, **kwargs):
        """ This function creates a label when given any number of key-word args """

        text = kwargs["text"] if "text" in kwargs else ""
        image = kwargs["image"] if "image" in kwargs else ""
        height = kwargs["height"] if "height" in kwargs else 0
        width = kwargs["width"] if "width" in kwargs else 0
        x = kwargs["x"] if "x" in kwargs else 0
        y = kwargs["y"] if "y" in kwargs else 0
        window = kwargs["window"] if "window" in kwargs else self
        bg_color = kwargs["bg_color"] if "bg_color" in kwargs else "blue"
        fg_color = kwargs["fg_color"] if "fg_color" in kwargs else "transparent"
        text_color = kwargs["text_color"] if "text_color" in kwargs else "white"
        font = kwargs["font"] if "font" in kwargs else "Segoe UI"
        font_size = kwargs["font_size"] if "font_size" in kwargs else 12
        font_weight = kwargs["font_weight"] if "font_weight" in kwargs else "normal"
        anchor = kwargs["anchor"] if "anchor" in kwargs else "w"

        lab = ctk.CTkLabel(window, text=text, text_color=text_color, fg_color=fg_color, image=image, bg_color=bg_color,
                           height=height, width=width)
        lab.place(x=x, y=y)
        lab.cget("font").configure(family=font, size=font_size, weight=font_weight)

        #  create attr that returns the x and y positions of the widget
        lab.position_x, lab.position_y = x, y

        return lab

    def create_button(self, **kwargs):
        """ This function creates a button when given any number of key-word args """

        text = kwargs["text"] if "text" in kwargs else ""
        image = kwargs["image"] if "image" in kwargs else None
        height = kwargs["height"] if "height" in kwargs else 0
        width = kwargs["width"] if "width" in kwargs else 0
        x = kwargs["x"] if "x" in kwargs else None
        y = kwargs["y"] if "y" in kwargs else None
        command = kwargs["command"] if "command" in kwargs else None
        window = kwargs["window"] if "window" in kwargs else self
        bg_color = kwargs["bg_color"] if "bg_color" in kwargs else "#495068"
        fg_color = kwargs["fg_color"] if "fg_color" in kwargs else "#fffada"  # "#284B63"
        text_color = kwargs["text_color"] if "text_color" in kwargs else "#495068"
        font = kwargs["font"] if "font" in kwargs else "Segoe UI"
        font_size = kwargs["font_size"] if "font_size" in kwargs else 12
        font_weight = kwargs["font_weight"] if "font_weight" in kwargs else "normal"
        corner_radius = kwargs['corner_radius'] if "corner_radius" in kwargs else None

        butt = ctk.CTkButton(window, text=text, width=width, bg_color=bg_color, height=height,
                             fg_color=fg_color, text_color=text_color, corner_radius=corner_radius,
                             border_spacing=0, command=command, font=(font, font_size))
        butt.place(x=x, y=y)

        #  create attr that returns the x and y positions of the widget
        butt.position_x, butt.position_y = x, y

        return butt

    def create_display(self, **kwargs):
        """ This function creates a display label when given any number of key-word args """

        text = kwargs["text"] if "text" in kwargs else ""
        title = kwargs["title"] if "title" in kwargs else ""
        text_position = kwargs["text_position"] if "text_position" in kwargs else "3.0"
        image = kwargs["image"] if "image" in kwargs else ""
        height = kwargs["height"] if "height" in kwargs else self.h - (210 + 40)
        width = kwargs["width"] if "width" in kwargs else self.w - 30
        x = kwargs["x"] if "x" in kwargs else 15
        y = kwargs["y"] if "y" in kwargs else (self.h / 4) + 40
        command = kwargs["command"] if "command" in kwargs else None
        window = kwargs["window"] if "window" in kwargs else self
        bg_color = kwargs["bg_color"] if "bg_color" in kwargs else "#E5E5E5"
        fg_color = kwargs["fg_color"] if "fg_color" in kwargs else "white"
        text_color = kwargs["text_color"] if "text_color" in kwargs else "white"
        font = kwargs["font"] if "font" in kwargs else "Segoe UI"
        font_size = kwargs["font_size"] if "font_size" in kwargs else 12
        font_weight = kwargs["font_weight"] if "font_weight" in kwargs else "normal"

        txt = ctk.CTkTextbox(window)
        txt.insert("0.0", title)
        txt.insert(text_position, "\n\n" + text)
        txt.configure(width=width, bg_color=bg_color, height=height, fg_color=fg_color, text_color=text_color,
                      border_spacing=5, border_color="black", wrap="word", font=(font, font_size, font_weight))
        txt.configure(state="disabled")
        txt.place(x=x, y=y)

        #  create attr that returns the x and y positions of the widget
        txt.position_x, txt.position_y = x, y

        return txt

    def create_form_window_after(self):
        """Creates a new toplevel window for user to choose where to upload result file from"""

        if self.top_level_window is None or not self.top_level_window.winfo_exists():
            title = "Choose Result File Destination"
            self.top_level_window = obj = TopLevel(self, title)
            self.create_button(window=self.top_level_window, command=self.upload_result_file, text="New File",
                               bg_color="#E5E5E5", height=30, width=80, fg_color="#495068", text_color="#fffada",
                               x=(obj.w / 2) - 85, y=180)
            self.create_button(window=self.top_level_window, command=self.select_result_file, text="Existing File",
                               bg_color="#E5E5E5", fg_color="#495068", text_color="#fffada", height=30, width=80,
                               x=(obj.w / 2) + 5, y=180)

        else:
            self.top_level_window.focus()

        return

    def select_result_file(self):
        """This will trigger file selection from program directory"""

        projectname, projectfile = func.select_file("myapp/documents/after/", 2)
        if projectname == self.projectname:
            self.process_project_file(2)
            self.top_level_window.destroy()
        else:
            func.display_msg("Selected file does not match the before project file!")
        return

    def upload_result_file(self):
        """This will trigger file upload from other direcories in the user computer device"""

        self.projectname, self.projectfile = func.upload_file(2, self.projectname)
        self.process_project_file(2)
        self.top_level_window.destroy()
        return

    def start_animation(self):
        """This method creates animation canvas"""
        imagelist = ["dog001.gif", "dog002.gif", "dog003.gif",
                     "dog004.gif", "dog005.gif", "dog006.gif", "dog007.gif"]

        # extract width and height info
        photo = PhotoImage(file=imagelist[0])
        width = photo.width()
        height = photo.height()
        canvas = Canvas(width=width, height=height)
        canvas.place(y=(self.h / 2) + 40, x=(self.w / 3) + 40)
        self.animation_canvas = canvas

        # create a list of image objects
        giflist = []
        for imagefile in imagelist:
            photo = PhotoImage(file=imagefile)
            giflist.append(photo)

        def start_loading(n=0):
            """creates image on the canvas"""
            gif = giflist[n % len(giflist)]
            canvas.create_image(width / 2.0, height / 2.0, image=gif)
            self.timer_id = self.after(200, start_loading, n + 1)  # call this function every 10second

        start_loading()

    def stop_animation(self):
        """This method stops the animation by deleting the animation canvas"""

        if self.timer_id and self.animation_canvas:
            print("we are here")
            self.after_cancel(self.timer_id)
            self.animation_canvas.delete(ALL)
            self.animation_canvas.destroy()
            self.timer_id = None

    def toggle_event_dropdown_items(self, choice, target, side='before'):
        """ creates dropdown items for event dropdown combobox """
        my_list = []
        print(str(choice))
        if side == "before":
            planned = ['Dosing CIL', 'Triverter CIL', 'Panel Maintenance', 'Main Drive Overhauling']
            unplanned = ['Horizontal Jaw Misalignment', 'Broken Heating Element', 'Worn Printhead', 'Burnt Sensor']
            if choice == 'All':
                my_list = []
                my_list.extend(unplanned)
                my_list.extend(planned)
            elif choice == 'Planned':
                my_list = []
                my_list.extend(planned)
            elif choice == 'Unplanned':
                my_list = []
                my_list.extend(unplanned)

        target.configure(values=my_list)

    def display_events(self, data, title='', project='before'):
        """Displays a list of all planned events in the given data"""
        if project != 'before':
            if not self.project_class_after:
                func.display_msg("You have not loaded result file!")
                return
            else:
                self.toggle_file_mode(self.project_class_after)
        else:
            self.toggle_file_mode(self.project_class_before)

        text = ""
        if data:
            if len(data) > 0:
                count = 0

                for x in sorted(data):
                    count += 1
                    text += "{}. {}\n".format(count, x.title())

                # close the current display
                if self.current_display:
                    self.current_display.destroy()

                # create display label
                title = title
                location_display = self.create_display(font_size=16, text=text, text_color="black", title=title)
                self.current_display = location_display
                return
        func.display_msg("No events to display.")

    def display_graph(self, fig, compare_command=None, expand_command=None):
        if self.current_display:
            self.current_display.destroy()
        if expand_command is None:
            expand_command = self.current_plot.show

        # create a bg label to hold the graph
        x = 0
        y = (self.h // 4) + 40
        h = self.h - (210 + 40)
        w = self.w
        bg_label = self.create_label(fg_color="white", bg_color='white', x=x, y=y, height=h, width=w)
        self.current_display = bg_label

        def exit_command():
            self.current_display=None
            bg_label.destroy()
            return

        # create the label to hold the graph
        x = 0
        y = 0
        h = self.h - (210 + 40 + 30)
        w = self.w
        bg_lab = self.create_label(window=bg_label, fg_color="white", bg_color='white', x=x, y=y, height=h, width=w)

        # create a label and action buttons
        y = y + int(bg_lab.cget('height'))
        h = 30
        action_label = self.create_label(window=bg_label, fg_color="#ffffff", bg_color='#ffffff', x=x, y=y, height=h, width=w)

        # create buttons inside the action label
        w = 100
        h = 24
        y = 3
        # expand btn
        x = (self.w // 2) - 200
        expand_btn = self.create_button(window=action_label, text='expand', bg_color='#ffffff', fg_color="#495068",
                                        text_color="#FFFADA", x=x, y=y, corner_radius=8, height=h, width=w,
                                        command=expand_command)
        # compare btn
        x = x + expand_btn.cget("width") + 20
        compare_btn = self.create_button(window=action_label, text='compare', bg_color='#ffffff', fg_color="#495068",
                                         text_color="#FFFADA", x=x, y=y, corner_radius=8, height=h, width=w,
                                         command=compare_command)
        # exit btn
        x = x + compare_btn.cget("width") + 20
        exit_btn = self.create_button(window=action_label, text='exit', bg_color='#ffffff', fg_color="#495068",
                                      text_color="#FFFADA", x=x, y=y, corner_radius=8, height=h, width=50,
                                      command=exit_command)

        # Convert Matplotlib figure to Tkinter-compatible format
        canvas = FigureCanvasTkAgg(fig, master=bg_lab)  # Replace 'tk.Tk()' with your existing Tkinter window

        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0)



class TopLevel(ctk.CTkToplevel):
    """This is the TopLevel class for creating windows outside the main window"""

    def __init__(self, main, title):
        super(TopLevel, self).__init__(main)
        self.title(title)
        self.w, self.h = 600, 400
        self.geometry("{}x{}".format(self.w, self.h))

        self.grab_set()
