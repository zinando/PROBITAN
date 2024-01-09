"""This is the graph class module"""
from myapp.helpers import myfunc as func
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string
import matplotlib.pyplot as plt
import numpy as np


class MYGRAPH(object):
    """Class used to generate different graph for the machine/equipment data"""

    def __init__(self):
        """Initialize the MYGRAPH class. No argument required"""
        super(MYGRAPH, self).__init__()
        pass

    def generate_uptime_and_downtime_graph(self, data, title=""):
        """Genearates the graph of uptime and downtime events from processed data"""

        data = data[:6]
        width = 0.25
        x = [x['month'] for x in data]

        uptime = [x['total_uptime'] for x in data]

        downtime = [x['total_downtime'] for x in data]
        upt_percent = ['{}%'.format(round(x['total_uptime'] / (x['total_uptime'] + x['total_downtime']) * 100)) for x in
                       data]
        dwnt_percent = ['{}%'.format(round(x['total_downtime'] / (x['total_uptime'] + x['total_downtime']) * 100)) for x
                        in data]

        x_axis = np.arange(len(x))

        A = plt.bar(x_axis - width, uptime, width, label='Uptime', color=['brown'])
        B = plt.bar(x_axis, downtime, width, label='Downtime', color=['blue'])

        def annotations(bars, text, index=0):
            count = 0
            for bar in bars:
                height = bar.get_height()
                plt.annotate('{}'.format(text[count]),
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 1),  # 1 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom',
                             )
                count += 1

        annotations(A, upt_percent)
        annotations(B, dwnt_percent)
        plt.xticks(x_axis - width / 2, x, rotation='vertical')
        plt.xlabel("Months")
        plt.ylabel("Time in mins")
        plt.title(title)
        plt.legend()
        plt.show()

        return

    def generate_planned_and_unplanned_dt_graph(self, data, title=""):
        """Genearates the graph of planned and unplanned downtime events from processed data"""

        data = data[:6]
        width = 0.4
        x = [x['month'] for x in data]

        uptime = [x['planned_downtime'] for x in data]
        downtime = [x['unplanned_downtime'] for x in data]
        upt_percent = [
            '{}%'.format(round(x['planned_downtime'] / (x['planned_downtime'] + x['unplanned_downtime']) * 100)) for x
            in data]
        dwnt_percent = [
            '{}%'.format(round(x['unplanned_downtime'] / (x['planned_downtime'] + x['unplanned_downtime']) * 100)) for x
            in data]

        x_axis = np.arange(len(x))

        A = plt.bar(x_axis - width, uptime, width, label='Planned DT', color=['brown'])
        B = plt.bar(x_axis, downtime, width, label='Unplanned DT', color=['grey'])

        def annotations(bars, text, index=0):
            count = 0
            for bar in bars:
                height = bar.get_height()
                plt.annotate('{}'.format(text[count]),
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 1),  # 1 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom',
                             )
                count += 1

        annotations(A, upt_percent)
        annotations(B, dwnt_percent)
        plt.xticks(x_axis - width / 2, x, rotation='vertical')
        plt.xlabel("Months")
        plt.ylabel("Time in mins")
        plt.title(title)
        plt.legend()
        plt.show()
        return

    def get_bar_colors(self, number_of_colors):

        from matplotlib import colors as mcolors
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

        # Sort colors by hue, saturation, value and name.
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name) for name, color in colors.items())

        sorted_names = [name for hsv, name in by_hsv]

        if number_of_colors > len(sorted_names):
            return None

        random.shuffle(sorted_names)

        return sorted_names[:number_of_colors]

    def generate_average_monthly_dt_graphyyy(self, processed_data, title=""):
        """generates a graph of monthly PR"""
        data = processed_data[:6]
        width = 0.4
        x = [x['month'] for x in data]
        color = self.get_bar_colors(len(x))

        pr = self.calculate_PR(data)
        uptime = pr

        x_axis = np.arange(len(x))

        A = plt.bar(x_axis, uptime, width, label=x, color=color)

        def annotations(bars, text):
            count = 0
            for bar in bars:
                height = bar.get_height()
                plt.annotate('{}'.format(text[count]),
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 1),  # 1 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom',
                             )
                count += 1

        annotations(A, uptime)

        # plt.xticks(x_axis, x, rotation='vertical')
        plt.xticks(x_axis, [], rotation='vertical')
        plt.xlabel("Work Points")
        plt.ylabel("Time in mins")
        plt.title(title)
        plt.legend()
        plt.show()
        return

    def generate_average_monthly_dt_graph(self, data, event_types, title=""):
        """generates average planned downtime graphs for all the event types"""
        bar_width = 0.4
        event_types = sorted(event_types)
        color = self.get_bar_colors(len(event_types))
        # create numbers to represent each event at the graph bottom
        bottom_labels = [str(x) for x in list(range(1, 201))[:len(event_types)]]
        # Generate sample data
        info = self.compute_average_time(data, event_types)
        uptime = [info[func.enslave_strings(i)] for i in event_types]
        # uptime = np.random.randint(50, 300, len(event_types))

        # Create the graph
        fig, ax = plt.subplots(figsize=(18, 8))
        bars = ax.bar(bottom_labels, uptime, bar_width, color=color)
        ax.set_xlabel("DownTime Events")
        ax.set_ylabel("Time in mins")
        ax.set_title(title)

        # Create legend for event types
        legends = self.combine_lists(bottom_labels, event_types, uptime)
        ax.legend(bars, legends)

        # Configure the graph's appearance
        ax.set_facecolor('white')  # Set white background
        fig.set_facecolor('white')

        return fig, plt

    def generate_monthly_pr_graph(self, processed_data, title=""):
        """generates monthly pr graph"""
        bar_width = 0.4
        months = [x['month'] for x in processed_data]
        color = self.get_bar_colors(len(months))
        random.shuffle(color)

        # Generate sample data
        uptime = self.calculate_PR(processed_data)

        # Create the graph
        fig, ax = plt.subplots(figsize=(18, 8))
        bars = ax.bar(months, uptime, bar_width, color=random.choice(color))
        ax.set_xlabel("Months of the Year")
        ax.set_ylabel("Process Reliability in %")
        ax.set_title(title)

        # Configure the graph's appearance
        ax.set_facecolor('white')  # Set white background
        fig.set_facecolor('white')

        # Annotate each bar with its volume
        for bar, pr in zip(bars, uptime):
            ax.annotate(f'{pr:.2f} %', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom')

        return fig, plt

    def generate_monthly_volume_graph(self, processed_data, title="", vpm=5.525):
        """generates monthly volume graph. vpm means volume per minute. volume is in kg.
        5.525 is 65bags of 85g in kg per minute"""
        bar_width = 0.4
        months = [x['month'] for x in processed_data]
        color = self.get_bar_colors(len(months))
        random.shuffle(color)

        # Generate sample data
        uptime = self.calculate_volume_per_month(processed_data, vpm)
        uptime = [round(y / 1000, 2) for y in uptime]

        # Create the graph
        fig, ax = plt.subplots(figsize=(18, 8))
        bars = ax.bar(months, uptime, bar_width, color=random.choice(color))
        ax.set_xlabel("Months of the Year")
        ax.set_ylabel("Volume in Kg (x 1000)")
        ax.set_title(title)

        # Configure the graph's appearance
        ax.set_facecolor('white')  # Set white background
        fig.set_facecolor('white')

        # Annotate each bar with its volume
        for bar, vol in zip(bars, uptime):
            ax.annotate(f'{vol:.2f} kg', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom')

        return fig, plt

    def compare_graphs(self, y1, x1, y2, x2, title='', x_label='', y_label='', legend=None):
        """plots before and after data of the given graph description"""
        x_data = x1

        y_data1 = y1
        y_data2 = y2

        bar_width = 0.4
        index = np.arange(len(x_data))

        fig, ax = plt.subplots(figsize=(18, 8))

        bar1 = ax.bar(index - bar_width / 2, y_data1, bar_width, label='Before', color='skyblue')
        bar2 = ax.bar(index + bar_width / 2, y_data2, bar_width, label='After', color='salmon')

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(index)
        ax.set_xticklabels(x_data)
        if legend is None:
            ax.legend()
        else:
            ax.legend(bar1, legend)

        # Adding annotations above each bar
        for i, v in enumerate(y_data1):
            ax.text(i - bar_width / 2, v + 10, str(v), color='black', ha='center')

        for i, v in enumerate(y_data2):
            ax.text(i + bar_width / 2, v + 10, str(v), color='black', ha='center')

        return fig, plt

    def generate_top_losses_graph(self, y_data, x_data, title="", x_label='', y_label=''):
        """generates monthly volume graph. vpm means volume per minute. volume is in kg.
        5.525 is 65bags of 85g in kg per minute"""
        bar_width = 0.4
        months = x_data
        color = self.get_bar_colors(len(months))
        random.shuffle(color)

        # Generate sample data
        uptime = y_data

        # Create the graph
        fig, ax = plt.subplots(figsize=(18, 8))
        bars = ax.bar(months, uptime, bar_width, color=color)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

        # Configure the graph's appearance
        ax.set_facecolor('white')  # Set white background
        fig.set_facecolor('white')

        # Annotate each bar with its volume
        for bar, vol in zip(bars, uptime):
            ax.annotate(f'{vol}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom')

        return fig, plt

    def generate_monthly_event_graph(self, data: list, option: str, title=""):
        """Genearates monthly downtime graph for a chosen option"""

        data = data[:6]
        width = 0.4
        x = [x['month'] for x in data]

        uptime = [x[func.enslave_strings(option)] for x in data]

        x_axis = np.arange(len(x))

        A = plt.bar(x_axis - width, uptime, width, label=option.title(), color=['brown'])

        def annotations(bars, text, index=0):
            count = 0
            for bar in bars:
                height = bar.get_height()
                plt.annotate('{}'.format(text[count]),
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 1),  # 1 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom',
                             )
                count += 1

        annotations(A, uptime)
        plt.xticks(x_axis - width / 2, x, rotation='vertical')
        plt.xlabel("Months")
        plt.ylabel("Time in mins")
        plt.title(title)
        plt.legend()
        plt.show()
        return

    def combine_lists(self, alphas, names, numbers=None):
        combined_list = []

        if numbers is None:
            # Check if all lists have the same length
            if len(alphas) != len(names):
                return alphas

            # Zip the lists together and combine items
            for alpha, name in zip(alphas, names):
                combined_item = f"{alpha}. {name}"
                combined_list.append(combined_item)
        else:
            # Zip the lists together and combine items
            # Check if all lists have the same length
            if len(alphas) != len(names) or len(alphas) != len(numbers):
                return alphas

            for alpha, name, num in zip(alphas, names, numbers):
                combined_item = f"{alpha}. {name} - {num}"
                combined_list.append(combined_item)

        return combined_list

    def compute_average_time(self, data, event_types):

        mr = {}
        for pts in event_types:
            pt = func.enslave_strings(pts)
            total_time = sum(x.get(pt, 0) for x in data)
            average_time = total_time // len(data) if len(data) > 0 else 0
            mr[pt] = round(average_time, 2)  # Rounding to 2 decimal places

        return mr

    def calculate_PR(self, data):
        """
        Calculate the Percentage Ratio (PR) for each month based on total uptime and total downtime.

        Args:
        - data (list): A list of dictionaries containing monthly data.

        Returns:
        - list: A list of PR values (rounded whole numbers) for each month.
        """
        PR_list = []

        for month_data in data:
            total_uptime = month_data['total_uptime']
            total_downtime = month_data['total_downtime']

            PR = (total_uptime / (total_uptime + total_downtime)) * 100
            PR_list.append(round(PR))

        return PR_list

    def calculate_volume_per_month(self, data, volume_per_minute):
        """
        Calculate the volume per month based on total uptime and volume per minute.

        Args:
        - data (list): A list of dictionaries containing monthly data.
        - volume_per_minute (float): Volume produced per minute.

        Returns:
        - list: A list of calculated volumes for each month based on total uptime and volume per minute.
        """
        volume_list = []

        for month_data in data:
            total_uptime = month_data['total_uptime']
            volume = total_uptime * volume_per_minute
            volume_list.append(volume)

        return volume_list


