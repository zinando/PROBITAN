"""This is the main application file. We import all modules/functions necessary to execute commands into this file and then make them to perform the required tasks.
   First we create the application window (Tikinter).
"""
import tkinter as tk
from tkinter.messagebox import showinfo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from myapp.helpers import myfunc as func
from PIL import Image, ImageTk
from myapp.appclasses.views import WinView, TopLevel
from myapp.appclasses.fileclass import FILEHANDLER
from myapp.appclasses.graphclass import MYGRAPH
from myapp.appclasses.projectclass import PROJECT
from functools import partial


class Probitan(WinView):
    """ Class for managing app button click actions. This class inherits from the app window view class (WinView) """
    processed_data = None
    event_types = None
    cil_locations = None
    planned_events = []
    unplanned_events = []
    date_format = None
    current_display = None
    location_processed_data = None  # computes downtime based on cil location
    monthly_events = None
    current_plot = None

    def __init__(self):
        """ initializes the Probitan class, and calls on the base_view method which creates the project entry point """
        super(Probitan, self).__init__()
        self.saved_objects = {}  # stores objects that could be used on other parts of the app
        self.base_view()

    def toggle_file_mode(self, projectclass):
        """Toggles class instance attributes between before or after file"""
        if self.active_class != projectclass:
            self.active_class = projectclass
            self.initialize_project_variables("activate project")

    def create_new_project(self):
        """ Calls the upload_file function to upload a new project file and to process it
		    Calls the create_work_view to create the main work_view
		"""
        self.initialize_project_variables()
        self.projectname, self.projectfile = func.upload_file(1)
        if self.top_level_window is not None:
            self.top_level_window.destroy()
        self.process_project_file(1)

    def select_project(self):
        """ Calls the upload_file function to upload a new project file and to process it
			Calls the create_work_view to create the main work_view
		"""
        # self.start_animation()
        self.initialize_project_variables()
        self.projectname, self.projectfile = func.select_file("myapp/documents/before/", 1)
        # self.stop_animation()

        if self.top_level_window is not None:
            self.top_level_window.destroy()

        self.process_project_file(1)

    def process_project_file(self, folder_id, file_to_process=None):
        """Processes project file after upload/selection"""

        if self.projectname is not None:
            # process the file data and display time span of events
            info = FILEHANDLER(folder_id)
            if file_to_process is not None:
                full_file_path = "{}{}".format(info.file_path, file_to_process)
            else:
                full_file_path = "{}{}".format(info.file_path, self.projectfile)

            # read the file content
            result1 = info.read_file(full_file_path)
            event_types, planned_events, unplanned_events, cil_locations = info.get_list_of_event_types(result1)

            # get the date format from the content
            datelist = [x["start_date"] for x in result1]
            date_format = func.get_date_format(datelist)

            # group events into the months in which they occurred
            result2 = info.get_event_duration_in_months(result1, date_format)
            result3 = info.group_events_by_month(result1, result2, date_format)
            monthly_events = result3

            # get the time for each event by month
            result4 = info.compute_time_for_monthly_events(result3)
            processed_data = result4

            # get processed data based on cil location
            result5 = info.process_cil_location_data(result3, cil_locations)
            location_processed_data = result5

            list_items = list(result2.items())
            first_key, first_value = list_items[0]
            last_key, last_value = list_items[-1]

            text = "Analysing data from {} to {}.".format(first_value, last_value)
            self.instantiate_project(folder_id, self.projectname, self.projectfile, processed_data, event_types,
                                     planned_events, unplanned_events, cil_locations, date_format,
                                     location_processed_data, monthly_events, list_items)
            self.create_work_view(text)

    def instantiate_project(self, folder_id, name, file, processed_data, event_types, planned_events, unplanned_events,
                            cil_locations, date_format, location_processed_data, monthly_events, month_list):
        """Creates instance of the PROJECT class"""
        if folder_id == 1:
            self.project_class_before = PROJECT(name, file, processed_data, event_types, planned_events,
                                                unplanned_events, cil_locations, date_format, location_processed_data,
                                                monthly_events, month_list)
            self.active_class = self.project_class_before
            self.initialize_project_variables("activate project")
        elif folder_id == 2:
            self.project_class_after = PROJECT(name, file, processed_data, event_types, planned_events,
                                               unplanned_events, cil_locations, date_format, location_processed_data,
                                               monthly_events, month_list)
            self.active_class = self.project_class_after
            self.initialize_project_variables("activate project")

    def create_work_view(self, text=""):
        """ This creates the working window where analytical graphs are being generated	"""

        # background image objects
        view_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG', (self.w, self.h))
        menu_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG', (self.w, 40))
        menu_title_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG', ((self.w / 2) - 80, 20 + 40))
        divi_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG', (3, 115 + 40))
        bg_1 = func.create_image_obj('myapp/appfiles/images/btn/1.PNG', (40, 20))

        # labels
        bg_lab2 = self.create_label(text="", image=view_bg, height=self.h, width=self.w)
        footer = self.create_label(
            text="This project is submitted to the department of Mechanical Engineering, Obafemi Awolowo University, Ile Ife, Nigeria.",
            height=40, width=self.w, y=self.h - 40, fg_color="#495068", text_color="#fffada", bg_color="#495068",
            font_size=14, font_weight="bold")
        menu_bar = self.create_label(height=40, width=self.w, image=menu_bg)
        sub_menu_bar = self.create_label(height=115 + 40, y=40, width=self.w, bg_color="#D9D9D9", fg_color="#495068")
        self.saved_objects['sub_menu_bar'] = sub_menu_bar

        sub_menu_bar_before_menu_bar = self.create_label(height=20 + 40, y=43, x=40, width=(self.w / 2) - 80,
                                                         image=menu_title_bg)
        self.saved_objects['sub_menu_bar_before_menu_bar'] = sub_menu_bar_before_menu_bar

        sub_menu_bar_before_menu_bar_title = self.create_label(text="BEFORE", height=20, y=43, x=40,
                                                               width=(self.w / 2) - 80, bg_color='transparent',
                                                               text_color="#495068")

        sub_menu_bar_after_menu_bar = self.create_label(height=20 + 40, y=43, x=(self.w / 2) + 40,
                                                        width=(self.w / 2) - 80, image=menu_title_bg)
        self.saved_objects['sub_menu_bar_after_menu_bar'] = sub_menu_bar_after_menu_bar

        sub_menu_bar_after_menu_bar_title = self.create_label(text="AFTER", height=20, y=43, x=(self.w / 2) + 40,
                                                              width=(self.w / 2) - 80, bg_color='transparent',
                                                              text_color="#495068")

        title_divider = self.create_label(height=115 + 40, y=40, x=(self.w / 2) - 1.5, width=3, image=divi_bg)
        display = self.create_label(font_size=11, height=30, y=5, x=300, width=150,
                                    text="Processing: {}\n{}".format(self.projectname, text), text_color="#fffada",
                                    fg_color="#495068", bg_color="#495068")

        #  each submenu button displays some action buttons/fields below the submenu bar
        #  these buttons/fields will be contained in a label widget called action_container

        #  before action container
        w = int(sub_menu_bar_before_menu_bar.cget("width"))
        x = sub_menu_bar_before_menu_bar.position_x
        y = sub_menu_bar_before_menu_bar.position_y + int(sub_menu_bar_before_menu_bar.cget("height")) + 5
        h = int(sub_menu_bar.cget("height")) - int(sub_menu_bar_before_menu_bar.cget("height")) - 13
        a_container_img = func.create_image_obj('myapp/appfiles/images/bg/12.PNG', (w, h))
        before_action_container = self.create_label(height=h, y=y, x=x, width=w, bg_color="#D9D9D9",
                                                    fg_color="white", image=a_container_img)

        #  before action container
        w = int(sub_menu_bar_after_menu_bar.cget("width"))
        x = sub_menu_bar_after_menu_bar.position_x
        y = sub_menu_bar_after_menu_bar.position_y + int(sub_menu_bar_after_menu_bar.cget("height")) + 5
        h = int(sub_menu_bar.cget("height")) - int(sub_menu_bar_after_menu_bar.cget("height")) - 13
        a_container_img = func.create_image_obj('myapp/appfiles/images/bg/12.PNG', (w, h))
        after_action_container = self.create_label(height=h, y=y, x=x, width=w, bg_color="#D9D9D9",
                                                   fg_color="white", image=a_container_img)

        # Buttons: Top Bar menu
        result_file = self.create_button(text="Load Result File", bg_color="#E5E5E5",
                                         command=self.create_form_window_after,
                                         height=20, width=40, y=5, x=5, fg_color="#495068", text_color="#fffada")
        new_project_file = self.create_button(text="New Project", bg_color="#E5E5E5", command=self.create_form_window,
                                              height=20, width=40, y=5, x=130, fg_color="#495068", text_color="#fffada")

        ##Buttons: Sub-menu

        #  Before Submenu buttons
        #  the View Button
        w = (int(sub_menu_bar_before_menu_bar.cget("width")) - 40) // 3
        x = sub_menu_bar_before_menu_bar.position_x + 10
        y = sub_menu_bar_before_menu_bar.position_y + int(sub_menu_bar_before_menu_bar_title.cget('height')) + 6
        _w = int(before_action_container.cget('width'))
        _h = int(before_action_container.cget('height'))
        view = self.create_button(height=28, width=w, y=y, x=x, bg_color="#e3e7f0", fg_color="#495068",
                                  text_color="#FFFADA", text="View",
                                  command=lambda: self.create_view_widgets_view(before_action_container, _w - 10,
                                                                                _h - 10)
                                  )
        self.saved_objects['view'] = view

        #  the Analyze Button
        w = int(view.cget("width"))
        x = view.position_x + w + 10
        y = view.position_y
        h = int(view.cget("height"))
        _w = int(before_action_container.cget('width'))
        _h = int(before_action_container.cget('height'))
        analyze = self.create_button(
            command=lambda: self.create_analyze_widgets_view(before_action_container, _w - 10, _h - 10),
            height=h, width=w, y=y, x=x, bg_color="#e3e7f0", fg_color="#495068",
            text_color="#FFFADA", text="Analyze")
        self.saved_objects['analyze'] = analyze

        #  the Predict Button
        w = int(analyze.cget("width"))
        x = analyze.position_x + w + 10
        y = analyze.position_y
        h = int(view.cget("height"))
        _w = int(before_action_container.cget('width'))
        _h = int(before_action_container.cget('height'))
        predict = self.create_button(height=h, width=w, y=y, x=x, bg_color="#e3e7f0", fg_color="#495068",
                                     text_color="#FFFADA", text="Predict",
                                     command=lambda: self.create_predict_widgets_view(before_action_container, _w - 10,
                                                                                      _h - 10)
                                     )
        self.saved_objects['predict'] = predict

        #  After Submenu buttons
        #  the View Button
        w = (int(sub_menu_bar_after_menu_bar.cget("width")) - 40) // 3
        x = sub_menu_bar_after_menu_bar.position_x + 10
        y = sub_menu_bar_before_menu_bar.position_y + int(sub_menu_bar_before_menu_bar_title.cget('height')) + 6
        _w = int(before_action_container.cget('width'))
        _h = int(before_action_container.cget('height'))
        view2 = self.create_button(command=lambda: self.create_view_widgets_view(after_action_container,
                                                                                 _w - 10, _h - 10, 'after'),
                                   height=28, width=w, y=y, x=x, bg_color="#e3e7f0", fg_color="#495068",
                                   text_color="#FFFADA", text="View")
        self.saved_objects['view2'] = view2

        #  the Analyze Button
        w = int(view.cget("width"))
        x = view2.position_x + w + 10
        y = view2.position_y
        h = int(view.cget("height"))
        _w = int(before_action_container.cget('width'))
        _h = int(before_action_container.cget('height'))
        analyze2 = self.create_button(command=lambda: self.create_analyze_widgets_view(after_action_container,
                                                                                       _w - 10, _h - 10, 'after'),
                                      height=h, width=w, y=y, x=x, bg_color="#e3e7f0", fg_color="#495068",
                                      text_color="#FFFADA", text="Analyze")
        self.saved_objects['analyze2'] = analyze2

        #  the Predict Button
        w = int(analyze.cget("width"))
        x = analyze2.position_x + w + 10
        y = analyze2.position_y
        h = int(view.cget("height"))
        _w = int(before_action_container.cget('width'))
        _h = int(before_action_container.cget('height'))
        predict2 = self.create_button(command=lambda: self.create_predict_widgets_view(after_action_container,
                                                                                       _w - 10, _h - 10, 'after'),
                                      height=h, width=w, y=y, x=x, bg_color="#e3e7f0", fg_color="#495068",
                                      text_color="#FFFADA", text="Predict")
        self.saved_objects['predict2'] = predict2

        # uptime and dt
        # uptm_dwntm1 = self.create_button(command=self.plot_uptime_and_downtime,
        # height=20, width=70, y=80 + 40, x=10, text="Uptime & DT")
        # uptm_dwntm2 = self.create_button(command=self.plot_uptime_and_downtime_after,
        # height=20, width=70, y=80 + 40, x=(self.w / 2) + 10, text="Uptime & DT")
        # average planned downtime
        # pl_dwntm1 = self.create_button(command=self.plot_average_planned_downtime_events,
        # height=20, width=70, y=80 + 40, x=100, text="Planned DT")
        # pl_dwntm2 = self.create_button(command=self.plot_average_planned_downtime_events_after,
        # height=20, width=70, y=80 + 40, x=(self.w / 2) + 100, text="Planned DT")
        # average cil
        # cil1 = self.create_button(command=self.plot_average_cil_planned_downtime_events,
        # height=20, width=70, y=80 + 40, x=185, text="Av. CIL")
        # cil2 = self.create_button(command=self.plot_average_cil_planned_downtime_events_after,
        # height=20, width=70, y=80 + 40, x=(self.w / 2) + 185,
        # text="Av. CIL")  # each char is 8 by width

        # planned and unplanned dt
        # pl_updt1 = self.create_button(command=self.plot_planned_and_unplanned_downtime,
        # height=20, width=70, y=80 + 20 + 10 + 5 + 40, x=10, text="Planned & UPDT")
        # pl_updt2 = self.create_button(command=self.plot_planned_and_unplanned_downtime_after,
        # height=20, width=70, y=80 + 20 + 10 + 5 + 40, x=(self.w / 2) + 10,
        # text="Planned & UPDT")
        # cil per month
        # cilpm1 = self.create_button(command=self.plot_cil_per_month,
        # height=20, width=70, y=80 + 20 + 10 + 5 + 40, x=127, text="CIL/month")
        # cilpm2 = self.create_button(command=self.plot_cil_per_month_after,
        # height=20, width=70, y=80 + 20 + 10 + 5 + 40, x=(self.w / 2) + 127,
        # text="CIL/month")

        # list event
        # eventlist1 = self.create_button(command=self.create_events_list,
        # height=20, width=70, y=115 + 40, x=127 + 90, text="List events")
        # eventlist2 = self.create_button(command=self.create_events_list_after,
        # height=20, width=70, y=115 + 40, x=(self.w / 2) + 127 + 90, text="List events")

        # list event locations
        # locationlist1 = self.create_button(command=self.create_cil_location,
        # height=20, width=70, y=115 + 40, x=217 + 98, text="CIL Locations")
        # locationlist2 = self.create_button(command=self.create_cil_location_after,
        # height=20, width=70, y=115 + 40, x=(self.w / 2) + 217 + 98,
        # text="CIL Locations")

    def initialize_project_variables(self, status=""):
        """ This function initializes the following variables to default values when the user decides to start a new
            project after working on a previous one without reopening the app
        """
        if status == "activate project":
            instance = self.active_class

            self.processed_data = instance.processed_data
            self.event_types = instance.event_types
            self.cil_locations = instance.cil_locations
            self.date_format = instance.date_format
            self.location_processed_data = instance.location_processed_data
            self.monthly_events = instance.monthly_events
            self.projectname = instance.name
            self.projectfile = instance.file
            self.unplanned_events = instance.unplanned_events
            self.planned_events = instance.planned_events
        else:
            self.projectname = None
            self.projectfile_before = None
            self.active_class = None
            self.project_class_after = None
            self.project_class_before = None
            self.unplanned_events = []
            self.planned_events = []

    def create_form_window(self):
        """Creates a new toplevel window for user to choose where to upload project file from"""

        if self.top_level_window is None or not self.top_level_window.winfo_exists():
            title = "Choose Result File Destination"
            self.top_level_window = obj = TopLevel(self, title)
            self.create_button(window=self.top_level_window, command=self.create_new_project, text="New File",
                               bg_color="#E5E5E5", height=30, width=80, fg_color="#495068", text_color="#fffada",
                               x=(obj.w / 2) - 85, y=180)
            self.create_button(window=self.top_level_window, command=self.select_project, text="Existing File",
                               bg_color="#E5E5E5", fg_color="#495068", text_color="#fffada", height=30, width=80,
                               x=(obj.w / 2) + 5, y=180)

        else:
            self.top_level_window.focus()

        return

    def create_events_list(self):
        """Displays a list of all downtime event types in the project being analyzed"""
        self.toggle_file_mode(self.project_class_before)
        text = ""
        if self.event_types is not None:
            count = 0

            for x in self.event_types:
                count += 1
                text += "{}. {}\n".format(count, x.title())

        # close the current display
        if self.current_display:
            self.current_display.destroy()

        # create display label
        title = "PLANNED DOWNTIME EVENTS"
        event_display = self.create_display(font_size=16, text=text, text_color="black", title=title)

        self.current_display = event_display

    def create_cil_location(self):
        """Displays a list of all locations the downtime events occurred"""
        self.toggle_file_mode(self.project_class_before)
        text = ""
        if self.cil_locations is not None:
            count = 0

            for x in sorted(self.cil_locations):
                count += 1
                text += "{}. {}\n".format(count, x.title())

        # close the current display
        if self.current_display:
            self.current_display.destroy()

        # create display label
        title = "CIL WORKPOINTS"
        location_display = self.create_display(font_size=16, text=text, text_color="black", title=title)
        self.current_display = location_display

    def plot_uptime_and_downtime(self):
        """Plots the graph of uptime and downtime events"""

        self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        title = "Monthly Uptime And Downtime Graphs"
        plot.generate_uptime_and_downtime_graph(self.processed_data, title)

    def plot_planned_and_unplanned_downtime(self):
        """Plots the graph of planned and unplanned downtime events"""

        self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        title = "Monthly Planned And Unplanned Downtme Graphs"
        plot.generate_planned_and_unplanned_dt_graph(self.processed_data, title)

    def plot_average_planned_downtime_events(self, project):
        """Plots the graph of average planned downtime for all the event types"""
        if project != 'before':
            if not self.project_class_after:
                func.display_msg("You have not loaded result file!")
                return
            else:
                self.toggle_file_mode(self.project_class_after)
        else:
            self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        title = "Average Planned Downtime Per Month"
        self.close_plot()
        fig, self.current_plot, legend_obj = plot.generate_average_monthly_dt_graph(self.processed_data, self.planned_events, title)
        self.display_graph(fig, compare_command=lambda: self.compare_before_and_after_graphs('planned_events'),
                           legend_obj=legend_obj)

    def plot_average_unplanned_downtime_events(self, project):
        """Plots the graph of average planned downtime for all the event types"""
        if project != 'before':
            if not self.project_class_after:
                func.display_msg("You have not loaded result file!")
                return
            else:
                self.toggle_file_mode(self.project_class_after)
        else:
            self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        title = "Average Unplanned Downtime Per Month"
        self.close_plot()
        fig, self.current_plot, legend_obj = plot.generate_average_monthly_dt_graph(self.processed_data, self.unplanned_events, title)
        self.display_graph(fig, compare_command=lambda: self.compare_before_and_after_graphs('unplanned_events'),
                           legend_obj=legend_obj)

    def plot_monthly_pr_graph(self, project):
        """Plots monthly pr graph"""
        if project != 'before':
            if not self.project_class_after:
                func.display_msg("You have not loaded result file!")
                return
            else:
                self.toggle_file_mode(self.project_class_after)
        else:
            self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        title = "Process Reliability Per Month"
        self.close_plot()
        fig, self.current_plot = plot.generate_monthly_pr_graph(self.processed_data, title)
        self.display_graph(fig, compare_command=lambda: self.compare_before_and_after_graphs('pr'))

    def plot_monthly_volume_graph(self, project):
        """Plots monthly pr graph"""
        if project != 'before':
            if not self.project_class_after:
                func.display_msg("You have not loaded result file!")
                return
            else:
                self.toggle_file_mode(self.project_class_after)
        else:
            self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        title = "Volume of Products Produced Per Month"
        self.close_plot()
        fig, self.current_plot = plot.generate_monthly_volume_graph(self.processed_data, title)
        self.display_graph(fig, compare_command=lambda: self.compare_before_and_after_graphs('volume'))

    def plot_average_cil_planned_downtime_events(self):
        """Plots the graph of average cil downtime """

        self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        title = "Average CIL Downtime Per Workpoint"
        plot.generate_average_dt_graph(self.location_processed_data, self.cil_locations, title)

    def plot_cil_per_month(self):
        """Plots the graph monthly cil downtime"""

        self.toggle_file_mode(self.project_class_before)

        # process the data to be used
        info = FILEHANDLER()
        processed_data = info.process_monthly_event_data(self.monthly_events, "type", "cil")

        plot = MYGRAPH()
        title = "Monthly CIL Downtime Graph"
        plot.generate_monthly_event_graph(processed_data, "cil", title)

    def create_events_list_after(self):
        """Displays a list of all downtime event types in the project being analyzed"""

        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
        else:
            self.toggle_file_mode(self.project_class_after)

            text = ""
            if self.event_types is not None:
                count = 0

                for x in self.event_types:
                    count += 1
                    text += "{}. {}\n".format(count, x.title())

            # close the current display
            if self.current_display:
                self.current_display.destroy()

            # create display label
            title = "PLANNED DOWNTIME EVENTS"
            event_display = self.create_display(font_size=16, text=text, text_color="black", title=title)

            self.current_display = event_display

    def create_cil_location_after(self):
        """Displays a list of all locations the downtime events occurred"""

        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
        else:
            self.toggle_file_mode(self.project_class_after)

            text = ""
            if self.cil_locations is not None:
                count = 0

                for x in sorted(self.cil_locations):
                    count += 1
                    text += "{}. {}\n".format(count, x.title())

            # close the current display
            if self.current_display:
                self.current_display.destroy()

            # create display label
            title = "CIL WORKPOINTS"
            location_display = self.create_display(font_size=16, text=text, text_color="black", title=title)
            self.current_display = location_display

    def plot_uptime_and_downtime_after(self):
        """Plots the graph of uptime and downtime events"""

        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
        else:
            self.toggle_file_mode(self.project_class_after)

            plot = MYGRAPH()
            title = "Monthly Uptime And Downtime Graphs"
            plot.generate_uptime_and_downtime_graph(self.processed_data, title)

    def plot_planned_and_unplanned_downtime_after(self):
        """Plots the graph of planned and unplanned downtime events"""

        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
        else:
            self.toggle_file_mode(self.project_class_after)

            plot = MYGRAPH()
            title = "Monthly Planned And Unplanned Downtime Graphs"
            plot.generate_planned_and_unplanned_dt_graph(self.processed_data, title)

    def plot_average_planned_downtime_events_after(self):
        """Plots the graph of average planned downtime for all the event_types"""

        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
        else:
            self.toggle_file_mode(self.project_class_after)

            plot = MYGRAPH()
            title = "Average Planned Downtime Per Event"
            plot.generate_average_dt_graph(self.processed_data, self.event_types, title)

    def plot_average_cil_planned_downtime_events_after(self):
        """Plots the graph of average cil downtime """

        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
        else:
            self.toggle_file_mode(self.project_class_after)

            plot = MYGRAPH()
            title = "Average CIL Downtime Per Workpoint"
            plot.generate_average_dt_graph(self.location_processed_data, self.cil_locations, title)

    def plot_cil_per_month_after(self):
        """Plots the graph monthly cil downtime"""

        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
        else:
            self.toggle_file_mode(self.project_class_after)

            # process the data to be used
            info = FILEHANDLER()
            processed_data = info.process_monthly_event_data(self.monthly_events, "type", "cil")

            plot = MYGRAPH()
            title = "Monthly CIL Downtime Graph"
            plot.generate_monthly_event_graph(processed_data, "cil", title)

    def create_view_widgets_view(self, window, w, h, view_type='before'):
        """ creates the button menus for the submenu views """

        if view_type == "before":
            #  menu label
            inner_container = self.create_label(window=window, height=h, y=5, x=5,
                                                width=w, bg_color="#D9D9D9", fg_color="#495068")
            self.saved_objects.get('view').configure(fg_color='#E3E7F0', text_color="#495068")
            self.saved_objects.get('analyze').configure(fg_color="#495068", text_color="#fffada")
            self.saved_objects.get('predict').configure(fg_color="#495068", text_color="#fffada")

            #  view all button: button to display all events
            x, y = 2, 2
            h = (int(inner_container.cget('height')) - 6) // 2
            w = (int(inner_container.cget('width')) - 10) // 4
            btn1 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Pl Events",
                                      font_size=12)
            btn1.configure(command=lambda: self.display_events(self.planned_events, "LIST OF PLANNED EVENTS"))

            x = btn1.position_x + int(btn1.cget('width')) + 2
            btn2 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Unp Events",
                                      font_size=12)
            btn2.configure(command=lambda: self.display_events(self.unplanned_events, "LIST OF UNPLANNED EVENTS"))

            x = btn2.position_x + int(btn2.cget('width')) + 2
            btn3 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Pl DT M")
            btn3.configure(command=lambda: self.plot_average_planned_downtime_events('before'))

            x = btn3.position_x + int(btn3.cget('width')) + 2
            btn4 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Unpl DT M")
            btn4.configure(command=lambda: self.plot_average_unplanned_downtime_events('before'))

            y = btn1.position_y + h + 2
            x = btn1.position_x
            btn5 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="PR M")
            btn5.configure(command=lambda: self.plot_monthly_pr_graph('before'))

            x = btn2.position_x
            btn6 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Volume M")
            btn6.configure(command=lambda: self.plot_monthly_volume_graph('before'))

            x = btn3.position_x
            # btn7 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="BUTTON")

            x = btn4.position_x
            # btn8 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="BUTTON")
        else:
            #  menu label
            inner_container = self.create_label(window=window, height=h, y=5, x=5,
                                                width=w, bg_color="#D9D9D9", fg_color="#495068")
            self.saved_objects.get('view2').configure(fg_color='#E3E7F0', text_color="#495068")
            self.saved_objects.get('analyze2').configure(fg_color="#495068", text_color="#fffada")
            self.saved_objects.get('predict2').configure(fg_color="#495068", text_color="#fffada")

            #  view all button: button to display all events
            x, y = 2, 2
            h = (int(inner_container.cget('height')) - 6) // 2
            w = (int(inner_container.cget('width')) - 10) // 4
            btn1 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Pl Events",
                                      font_size=12)
            btn1.configure(command=lambda: self.display_events(self.planned_events, "LIST OF PLANNED EVENTS",
                                                               'after'))

            x = btn1.position_x + int(btn1.cget('width')) + 2
            btn2 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Unp Events",
                                      font_size=12)
            btn2.configure(command=lambda: self.display_events(self.unplanned_events, "LIST OF UNPLANNED EVENTS",
                                                               'after'))

            x = btn2.position_x + int(btn2.cget('width')) + 2
            btn3 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Pl DT M")
            btn3.configure(command=lambda: self.plot_average_planned_downtime_events('after'))

            x = btn3.position_x + int(btn3.cget('width')) + 2
            btn4 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Unpl DT M")
            btn4.configure(command=lambda: self.plot_average_unplanned_downtime_events('after'))

            y = btn1.position_y + h + 2
            x = btn1.position_x
            btn5 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="PR M")
            btn5.configure(command=lambda: self.plot_monthly_pr_graph('after'))

            x = btn2.position_x
            btn6 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="Volume M")
            btn6.configure(command=lambda: self.plot_monthly_volume_graph('after'))

            x = btn3.position_x
            # btn7 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="BUTTON")

            x = btn4.position_x
            # btn8 = self.create_button(window=inner_container, height=h, width=w, y=y, x=x, text="BUTTON")

    def create_analyze_widgets_view(self, window, w, h, view_type='before'):
        """ creates the button menus for the submenu views """

        def toggle_event_dropdown_items(choice, target, side: str = 'before') -> None:
            """creates dropdown items for event dropdown combobox"""
            my_list = []
            if side == "before":
                planned = self.planned_events
                unplanned = self.unplanned_events
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


        if view_type == "before":
            #  menu label
            inner_container = self.create_label(window=window, height=h, y=5, x=5,
                                                width=w, bg_color="#495068", fg_color="#495068")
            self.saved_objects.get('analyze').configure(fg_color='#E3E7F0', text_color="#495068")
            self.saved_objects.get('view').configure(fg_color="#495068", text_color="#fffada")
            self.saved_objects.get('predict').configure(fg_color="#495068", text_color="#fffada")

            # top losses label
            h = int(inner_container.cget('height')) // 2
            w = int(inner_container.cget('width'))
            x, y = 0, 0
            top_loss_label = self.create_label(window=inner_container, height=h, y=y, x=x,
                                               width=w, bg_color="#fffada", fg_color="#fffada")
            h = int(top_loss_label.cget('height'))

            top_loss_title = self.create_label(window=top_loss_label, text=" Top\n Losses", height=h, y=0, x=0,
                                               width=50, bg_color="#fffada", fg_color="#495068", text_color="#fff")

            x = int(top_loss_title.cget('width')) + top_loss_title.position_x + 7
            y = top_loss_title.position_y + 2

            # group dropdown
            top_loss_group_drop_down = ctk.CTkComboBox(top_loss_label, values=["All", "Planned", "Unplanned"],
                                                       width=120, height=30, corner_radius=5, border_width=3,
                                                       border_color="#495068", fg_color="#fffada",
                                                       button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                       dropdown_hover_color="#E3E7F0")
            top_loss_group_drop_down.place(x=x, y=y)
            top_loss_group_drop_down.set('Select')
            top_loss_group_drop_down.position_x, top_loss_group_drop_down.position_y = x, y
            selected_option = top_loss_group_drop_down.get()

            # loss event dropdown
            x = top_loss_group_drop_down.position_x + int(top_loss_group_drop_down.cget('width')) + 5
            y = top_loss_group_drop_down.position_y
            h = int(top_loss_group_drop_down.cget('height'))
            w = int(top_loss_group_drop_down.cget('width'))
            top_loss_event_drop_down = ctk.CTkComboBox(top_loss_label, width=w, height=h, corner_radius=5,
                                                       border_width=3, border_color="#495068", fg_color="#fffada",
                                                       button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                       dropdown_hover_color="#E3E7F0")
            top_loss_event_drop_down.place(x=x, y=y)
            top_loss_event_drop_down.set('Select')
            top_loss_event_drop_down.position_x, top_loss_event_drop_down.position_y = x, y

        else:
            #  menu label
            inner_container = self.create_label(window=window, height=h, y=5, x=5,
                                                width=w, bg_color="#495068", fg_color="#495068")
            self.saved_objects.get('analyze2').configure(fg_color='#E3E7F0', text_color="#495068")
            self.saved_objects.get('view2').configure(fg_color="#495068", text_color="#fffada")
            self.saved_objects.get('predict2').configure(fg_color="#495068", text_color="#fffada")

            # top losses label
            h = int(inner_container.cget('height')) // 2
            w = int(inner_container.cget('width'))
            x, y = 0, 0
            top_loss_label = self.create_label(window=inner_container, height=h, y=y, x=x,
                                               width=w, bg_color="#fffada", fg_color="#fffada")
            h = int(top_loss_label.cget('height'))

            top_loss_title = self.create_label(window=top_loss_label, text=" Top\n Losses", height=h, y=0, x=0,
                                               width=50, bg_color="#fffada", fg_color="#495068", text_color="#fff")

            x = int(top_loss_title.cget('width')) + top_loss_title.position_x + 7
            y = top_loss_title.position_y + 2

            # group dropdown
            top_loss_group_drop_down = ctk.CTkComboBox(top_loss_label, values=["All", "Planned", "Unplanned"],
                                                       width=120, height=30, corner_radius=5, border_width=3,
                                                       border_color="#495068", fg_color="#fffada",
                                                       button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                       dropdown_hover_color="#E3E7F0")
            top_loss_group_drop_down.place(x=x, y=y)
            top_loss_group_drop_down.set('Select')
            top_loss_group_drop_down.position_x, top_loss_group_drop_down.position_y = x, y
            selected_option = top_loss_group_drop_down.get()

            # loss event dropdown
            x = top_loss_group_drop_down.position_x + int(top_loss_group_drop_down.cget('width')) + 5
            y = top_loss_group_drop_down.position_y
            h = int(top_loss_group_drop_down.cget('height'))
            w = int(top_loss_group_drop_down.cget('width'))
            top_loss_event_drop_down = ctk.CTkComboBox(top_loss_label, command=None, width=w, height=h, corner_radius=5,
                                                       border_width=3, border_color="#495068", fg_color="#fffada",
                                                       button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                       dropdown_hover_color="#E3E7F0")
            top_loss_event_drop_down.place(x=x, y=y)
            top_loss_event_drop_down.set('Select')
            top_loss_event_drop_down.position_x, top_loss_event_drop_down.position_y = x, y

        def configure_event_dropdown_combobox(choice) -> None:
            """configures top_loss_event_dropdown with a list of numbers to choose from"""
            if view_type != 'before':
                if not self.project_class_after:
                    func.display_msg("You have not loaded result file!")
                    return
                else:
                    self.toggle_file_mode(self.project_class_after)
            else:
                self.toggle_file_mode(self.project_class_before)

            planned = self.planned_events
            unplanned = self.unplanned_events
            top_loss_event_drop_down.set('Select')

            if choice == 'Planned':
                top_loss_event_drop_down.configure(values=[str(i + 1) for i in range(len(planned))])
            elif choice == 'Unplanned':
                top_loss_event_drop_down.configure(values=[str(i + 1) for i in range(len(unplanned))])
            else:
                top_loss_event_drop_down.configure(
                    values=[str(i + 1) for i in range(len(unplanned) + len(planned))])

            # configure top_loss_group_drop_down with a command to control the items of
            # ...top_loss_event_drop_down
            #  combobox supplies an invisible parameter to the function call which is the selected value

        top_loss_group_drop_down.configure(command=configure_event_dropdown_combobox)

        def display_top_losses(choice):
            """calls the function that plots the  top losses graphs"""
            self.plot_top_losses(view_type, top_loss_group_drop_down.get(), choice)

        top_loss_event_drop_down.configure(command=display_top_losses)

        return

    def create_predict_widgets_view(self, window, w, h, view_type='before'):
        """ creates the button menus for the submenu views """
        if view_type == "before":
            #  menu label
            inner_container = self.create_label(window=window, height=h, y=5, x=5,
                                                width=w, bg_color="#495068", fg_color="#495068")

            self.saved_objects.get('predict').configure(fg_color='#E3E7F0', text_color="#495068")
            self.saved_objects.get('view').configure(fg_color="#495068", text_color="#fffada")
            self.saved_objects.get('analyze').configure(fg_color="#495068", text_color="#fffada")

            # Predict label
            h = int(inner_container.cget('height')) // 2
            w = int(inner_container.cget('width'))
            x, y = 0, 0
            predict_label = self.create_label(window=inner_container, height=h, y=y, x=x,
                                              width=w, bg_color="#fffada", fg_color="#fffada")
            h = int(predict_label.cget('height'))
            predict_title = self.create_label(window=predict_label, text=" Predict", height=h, y=0, x=0,
                                              width=50, bg_color="#fffada", fg_color="#495068", text_color="#fff")

            x = int(predict_title.cget('width')) + predict_title.position_x + 7
            y = predict_title.position_y + 2

            # group dropdown
            predict_group_drop_down = ctk.CTkComboBox(predict_label, values=["All", "Planned", "Unplanned"],
                                                      width=80, height=30, corner_radius=5, border_width=3,
                                                      border_color="#495068", fg_color="#fffada",
                                                      button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                      dropdown_hover_color="#E3E7F0")
            predict_group_drop_down.place(x=x, y=y)
            predict_group_drop_down.set('Select')
            predict_group_drop_down.position_x, predict_group_drop_down.position_y = x, y
            selected_option = predict_group_drop_down.get()

            # loss event dropdown
            x = predict_group_drop_down.position_x + int(predict_group_drop_down.cget('width')) + 5
            y = predict_group_drop_down.position_y
            h = int(predict_group_drop_down.cget('height'))
            w = int(predict_group_drop_down.cget('width')) + 25
            predict_event_drop_down = ctk.CTkComboBox(predict_label, command=None, width=w, height=h, corner_radius=5,
                                                      border_width=3, border_color="#495068", fg_color="#fffada",
                                                      button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                      dropdown_hover_color="#E3E7F0")
            predict_event_drop_down.place(x=x, y=y)
            predict_event_drop_down.set('Select')
            predict_event_drop_down.position_x, predict_event_drop_down.position_y = x, y

            # percentage dropdown
            x = predict_event_drop_down.position_x + int(predict_event_drop_down.cget('width')) + 5
            y = predict_event_drop_down.position_y
            h = int(predict_event_drop_down.cget('height'))
            w = int(predict_group_drop_down.cget('width'))
            options = ["{}%".format(i) for i in range(5, 201, 5)]
            predict_percentage_drop_down = ctk.CTkComboBox(predict_label, values=options, width=w, height=h,
                                                           corner_radius=5, border_width=3, border_color="#495068",
                                                           fg_color="#fffada", button_color=("#495068", "#fff"),
                                                           dropdown_fg_color="#fffada", dropdown_hover_color="#E3E7F0",
                                                           command=None)
            predict_percentage_drop_down.place(x=x, y=y)
            predict_percentage_drop_down.set('Select')
            predict_percentage_drop_down.position_x, predict_percentage_drop_down.position_y = x, y
        else:
            #  menu label
            inner_container = self.create_label(window=window, height=h, y=5, x=5,
                                                width=w, bg_color="#495068", fg_color="#495068")

            self.saved_objects.get('predict2').configure(fg_color='#E3E7F0', text_color="#495068")
            self.saved_objects.get('view2').configure(fg_color="#495068", text_color="#fffada")
            self.saved_objects.get('analyze2').configure(fg_color="#495068", text_color="#fffada")

            # Predict label
            h = int(inner_container.cget('height')) // 2
            w = int(inner_container.cget('width'))
            x, y = 0, 0
            predict_label = self.create_label(window=inner_container, height=h, y=y, x=x,
                                              width=w, bg_color="#fffada", fg_color="#fffada")
            h = int(predict_label.cget('height'))
            predict_title = self.create_label(window=predict_label, text=" Predict", height=h, y=0, x=0,
                                              width=50, bg_color="#fffada", fg_color="#495068", text_color="#fff")

            x = int(predict_title.cget('width')) + predict_title.position_x + 7
            y = predict_title.position_y + 2

            # group dropdown
            predict_group_drop_down = ctk.CTkComboBox(predict_label, values=["All", "Planned", "Unplanned"],
                                                      width=80, height=30, corner_radius=5, border_width=3,
                                                      border_color="#495068", fg_color="#fffada",
                                                      button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                      dropdown_hover_color="#E3E7F0")
            predict_group_drop_down.place(x=x, y=y)
            predict_group_drop_down.set('Select')
            predict_group_drop_down.position_x, predict_group_drop_down.position_y = x, y
            selected_option = predict_group_drop_down.get()

            # loss event dropdown
            x = predict_group_drop_down.position_x + int(predict_group_drop_down.cget('width')) + 5
            y = predict_group_drop_down.position_y
            h = int(predict_group_drop_down.cget('height'))
            w = int(predict_group_drop_down.cget('width')) + 25
            predict_event_drop_down = ctk.CTkComboBox(predict_label, command=None, width=w, height=h, corner_radius=5,
                                                      border_width=3, border_color="#495068", fg_color="#fffada",
                                                      button_color=("#495068", "#fff"), dropdown_fg_color="#fffada",
                                                      dropdown_hover_color="#E3E7F0")
            predict_event_drop_down.place(x=x, y=y)
            predict_event_drop_down.set('Select')
            predict_event_drop_down.position_x, predict_event_drop_down.position_y = x, y

            # percentage dropdown
            x = predict_event_drop_down.position_x + int(predict_event_drop_down.cget('width')) + 5
            y = predict_event_drop_down.position_y
            h = int(predict_event_drop_down.cget('height'))
            w = int(predict_group_drop_down.cget('width'))
            options = ["{}%".format(i) for i in range(5, 201, 5)]
            predict_percentage_drop_down = ctk.CTkComboBox(predict_label, values=options, width=w, height=h,
                                                           corner_radius=5, border_width=3, border_color="#495068",
                                                           fg_color="#fffada", button_color=("#495068", "#fff"),
                                                           dropdown_fg_color="#fffada", dropdown_hover_color="#E3E7F0",
                                                           command=None)
            predict_percentage_drop_down.place(x=x, y=y)
            predict_percentage_drop_down.set('Select')
            predict_percentage_drop_down.position_x, predict_percentage_drop_down.position_y = x, y

        def configure_event_dropdown_combobox(choice) -> None:
            """configures top_loss_event_dropdown with a list of numbers to choose from"""
            if view_type != 'before':
                if not self.project_class_after:
                    func.display_msg("You have not loaded result file!")
                    return
                else:
                    self.toggle_file_mode(self.project_class_after)
            else:
                self.toggle_file_mode(self.project_class_before)

            planned = self.active_class.planned_events
            unplanned = self.active_class.unplanned_events
            predict_event_drop_down.set('Select')
            predict_percentage_drop_down.set('Select')

            if choice == 'Planned':
                predict_event_drop_down.configure(values=sorted(planned))
            elif choice == 'Unplanned':
                predict_event_drop_down.configure(values=sorted(unplanned))
            else:
                predict_event_drop_down.configure(
                    values=sorted(list(set(planned + unplanned))))

        # configure top_loss_group_drop_down with a command to control the items of
        # ...top_loss_event_drop_down
        #  combobox supplies an invisible parameter to the function call which is the selected value
        predict_group_drop_down.configure(command=configure_event_dropdown_combobox)

        def reset_percent_dropdown_combobox(choice) -> None:
            """resets the percentage dropdown"""
            predict_percentage_drop_down.set('Select')

        # configure predict_event_drop_down with a command to control the
        # ...set value for predict_percentage_dropdown
        #  combobox supplies an invisible parameter to the function call which is the selected value
        predict_event_drop_down.configure(command=reset_percent_dropdown_combobox)

        def predict_outcome(choice):
            """calls the function that plots the prediction graph"""
            if predict_group_drop_down.get() != 'Select':
                if predict_event_drop_down.get() == 'Select':
                    event = predict_group_drop_down.get()
                else:
                    event = func.enslave_strings(predict_event_drop_down.get())

                self.plot_prediction_graph(view_type, event, choice[:-1])
            return

        predict_percentage_drop_down.configure(command=predict_outcome)

    def compare_before_and_after_graphs(self, description):
        """compares the data generated for before and after of the given data description"""
        # check if after result file is loaded to app
        if not self.project_class_after:
            func.display_msg("You have not loaded result file!")
            return
        plot = MYGRAPH()
        processed_data_before = self.project_class_before.processed_data
        processed_data_after = self.project_class_after.processed_data
        unplanned_events_before = self.project_class_before.unplanned_events
        unplanned_events_after = self.project_class_after.unplanned_events
        planned_events_before = self.project_class_before.planned_events
        planned_events_after = self.project_class_after.planned_events

        if description == 'volume':
            title = "Comparing Monthly Volumes Before and After Improvement"
            y1 = [round(y / 1000, 2) for y in plot.calculate_volume_per_month(processed_data_before, 5.525)]
            y2 = [round(y / 1000, 2) for y in plot.calculate_volume_per_month(processed_data_after, 5.525)]
            x1 = [x['month'] for x in processed_data_before]
            x2 = [x['month'] for x in processed_data_after]

            # ensure the two lists have the same number of elements
            # assign the volumes to their respective months in a dict
            data1 = func.convert_lists_to_dict(self.project_class_before.months_covered, y1)
            data2 = func.convert_lists_to_dict(self.project_class_after.months_covered, y2)

            # use the dict to normalize the data
            y1, y2 = func.normalize_dictionaries(data1, data2)
            x1, x2 = func.normalize_lists(x1, x2)

            x_label = 'Months of the Year'
            y_label = 'Volume in Kg (x 1000)'
            self.close_plot()
            fig, self.current_plot = plot.compare_graphs(y1, x1, y2, x2, title=title, x_label=x_label,
                                                         y_label=y_label)
            self.display_graph(fig)
        elif description == 'pr':
            title = "Comparing Monthly Process Reliability (PR) Before and After Improvement"
            y1 = plot.calculate_PR(processed_data_before)
            y2 = plot.calculate_PR(processed_data_after)
            x1 = [x['month'] for x in processed_data_before]
            x2 = [x['month'] for x in processed_data_after]

            # ensure the two lists have the same number of elements
            # assign the volumes to their respective months in a dict
            data1 = func.convert_lists_to_dict(self.project_class_before.months_covered, y1)
            data2 = func.convert_lists_to_dict(self.project_class_after.months_covered, y2)

            # use the dict to normalize the data
            y1, y2 = func.normalize_dictionaries(data1, data2)
            x1, x2 = func.normalize_lists(x1, x2)

            x_label = 'Months of the Year'
            y_label = 'PR in %'
            self.close_plot()
            fig, self.current_plot = plot.compare_graphs(y1, x1, y2, x2, title=title, x_label=x_label,
                                                         y_label=y_label)
            self.display_graph(fig)
        elif description == 'unplanned_events':
            title = "Unplanned Events' Average Downtimes Before and After Improvement"
            unplanned_events_before = sorted(unplanned_events_before)
            unplanned_events_after = sorted(unplanned_events_after)
            color = plot.get_bar_colors(len(unplanned_events_before))

            info = plot.compute_average_time(processed_data_before, unplanned_events_before)
            info2 = plot.compute_average_time(processed_data_after, unplanned_events_after)
            uptime = [info[func.enslave_strings(i)] for i in unplanned_events_before]
            x_name = [f'before' for _ in unplanned_events_before]

            y1 = [info[func.enslave_strings(i)] for i in unplanned_events_before]
            y2 = [info2[func.enslave_strings(i)] for i in unplanned_events_after]
            x1 = [str(x) for x in list(range(1, 201))[:len(unplanned_events_before)]]
            x2 = [str(x) for x in list(range(1, 201))[:len(unplanned_events_after)]]

            # ensure the two lists have the same number of elements
            # assign the volumes to their respective months in a dict
            data1 = func.convert_lists_to_dict([func.enslave_strings(i) for i in unplanned_events_before], y1)
            data2 = func.convert_lists_to_dict([func.enslave_strings(i) for i in unplanned_events_after], y2)

            # use the dict to normalize the data
            y1, y2 = func.normalize_dictionaries(data1, data2)
            x1, x2 = func.normalize_lists(x1, x2)

            x_label = 'Event Numbers - See legend for interpretation'
            y_label = 'DownTimes in mins'
            legends = plot.combine_lists(x1, unplanned_events_before, x_name)
            self.close_plot()
            fig, self.current_plot = plot.compare_graphs(y1, x1, y2, x2, title=title, x_label=x_label,
                                                         y_label=y_label, legend=legends)
            self.display_graph(fig)
        elif description == 'planned_events':
            title = "Planned Events' Average Downtimes Before and After Improvement"
            planned_events_before = sorted(planned_events_before)
            planned_events_after = sorted(planned_events_after)
            color = plot.get_bar_colors(len(planned_events_before))

            info = plot.compute_average_time(processed_data_before, planned_events_before)
            info2 = plot.compute_average_time(processed_data_after, planned_events_after)
            uptime = [info[func.enslave_strings(i)] for i in planned_events_before]
            x_name = [f'before' for _ in planned_events_before]

            y1 = [info[func.enslave_strings(i)] for i in planned_events_before]
            y2 = [info2[func.enslave_strings(i)] for i in planned_events_after]
            x1 = [str(x) for x in list(range(1, 201))[:len(planned_events_before)]]
            x2 = [str(x) for x in list(range(1, 201))[:len(planned_events_after)]]

            # ensure the two lists have the same number of elements
            # assign the volumes to their respective months in a dict
            data1 = func.convert_lists_to_dict([func.enslave_strings(i) for i in planned_events_before], y1)
            data2 = func.convert_lists_to_dict([func.enslave_strings(i) for i in planned_events_after], y2)

            # use the dict to normalize the data
            y1, y2 = func.normalize_dictionaries(data1, data2)
            x1, x2 = func.normalize_lists(x1, x2)

            x_label = 'Event Numbers - See legend for interpretation'
            y_label = 'DownTimes in mins'
            legends = plot.combine_lists(x1, planned_events_before, x_name)
            self.close_plot()
            fig, self.current_plot = plot.compare_graphs(y1, x1, y2, x2, title=title, x_label=x_label,
                                                         y_label=y_label, legend=legends)
            self.display_graph(fig)

        return

    def plot_top_losses(self, project, scope, index):
        """plots the graphs of top loss events based on given scope"""
        index = int(index)
        if project != 'before':
            if not self.project_class_after:
                func.display_msg("You have not loaded result file!")
                return
            else:
                self.toggle_file_mode(self.project_class_after)
        else:
            self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        processed_data = self.active_class.processed_data
        planned_events = self.active_class.planned_events
        unplanned_events = self.active_class.unplanned_events

        if scope == 'All':
            title = f"Top {index} Losses From All Downtime Events"
            x_label = 'Top Loss Events'
            y_label = 'Downtime in mins'
            average_downtime = plot.compute_average_time(processed_data, planned_events + unplanned_events)
            top_loss_events = func.get_highest_values(average_downtime, index)
            x_data = [x for x in top_loss_events.keys()]
            y_data = [top_loss_events.get(y, 0) for y in x_data]

            self.close_plot()
            fig, self.current_plot = plot.generate_top_losses_graph(y_data, x_data, title, x_label, y_label)
            self.display_graph(fig)

        elif scope == 'Planned':
            title = f"Top {index} Losses From Planned Downtime Events"
            x_label = 'Top Loss Events'
            y_label = 'Downtime in mins'
            average_downtime = plot.compute_average_time(processed_data, planned_events)
            top_loss_events = func.get_highest_values(average_downtime, index)
            x_data = [x for x in top_loss_events.keys()]
            y_data = [top_loss_events.get(y, 0) for y in x_data]

            self.close_plot()
            fig, self.current_plot = plot.generate_top_losses_graph(y_data, x_data, title, x_label, y_label)
            self.display_graph(fig)
        elif scope == 'Unplanned':
            title = f"Top {index} Losses From Unplanned Downtime Events"
            x_label = 'Top Loss Events'
            y_label = 'Downtime in mins'
            average_downtime = plot.compute_average_time(processed_data, unplanned_events)
            top_loss_events = func.get_highest_values(average_downtime, index)
            x_data = [x for x in top_loss_events.keys()]
            y_data = [top_loss_events.get(y, 0) for y in x_data]

            self.close_plot()
            fig, self.current_plot = plot.generate_top_losses_graph(y_data, x_data, title, x_label, y_label)
            self.display_graph(fig)

        return

    def plot_prediction_graph(self, project, event, redux_percent):
        """plots the  graph of PR for a given percentage reduction in a given downtime event"""
        redux_percent = int(redux_percent)
        if project != 'before':
            if not self.project_class_after:
                func.display_msg("You have not loaded result file!")
                return
            else:
                self.toggle_file_mode(self.project_class_after)
        else:
            self.toggle_file_mode(self.project_class_before)

        plot = MYGRAPH()
        import copy

        if project == 'before':
            processed_data_before = self.project_class_before.processed_data
            processed_data_after = copy.deepcopy(processed_data_before)
            if event == 'All':
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after, 'total_downtime', redux_percent)
            elif event == 'Planned':
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after, 'planned_downtime', redux_percent)
            elif event == 'Unplanned':
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after, 'unplanned_downtime', redux_percent)
            else:
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after, event, redux_percent)

            title = f"Predicting The PR Impact of Reducing {event} downtime by {redux_percent}%"
            y1 = plot.calculate_PR(processed_data_before)
            y2 = plot.calculate_PR(processed_data_after)
            x1 = [x['month'] for x in processed_data_before]
            x2 = [x['month'] for x in processed_data_after]
            x_label = 'Months of the Year'
            y_label = 'PR in %'
            self.close_plot()
            fig, self.current_plot = plot.compare_graphs(y1, x1, y2, x2, title=title, x_label=x_label,
                                                         y_label=y_label)
            self.display_graph(fig)
        elif project == 'after':
            processed_data_before = self.project_class_after.processed_data
            processed_data_after = copy.deepcopy(processed_data_before)
            if event == 'All':
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after, 'total_downtime',
                                                                               redux_percent)
            elif event == 'Planned':
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after, 'planned_downtime',
                                                                               redux_percent)
            elif event == 'Unplanned':
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after,
                                                                               'unplanned_downtime', redux_percent)
            else:
                processed_data_after = func.reduce_key_and_add_to_total_uptime(processed_data_after, event,
                                                                               redux_percent)

            title = f"Predicting The PR Impact of Reducing {event} downtime by {redux_percent}%"
            y1 = plot.calculate_PR(processed_data_before)
            y2 = plot.calculate_PR(processed_data_after)
            x1 = [x['month'] for x in processed_data_before]
            x2 = [x['month'] for x in processed_data_after]
            x_label = 'Months of the Year'
            y_label = 'PR in %'
            self.close_plot()
            fig, self.current_plot = plot.compare_graphs(y1, x1, y2, x2, title=title, x_label=x_label,
                                                         y_label=y_label)
            self.display_graph(fig)

        return

    def close_plot(self):
        """closes plot assigned to current_plot"""
        if self.current_plot is not None:
            self.current_plot.close()
            self.current_plot = None

        return




