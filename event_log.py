import copy

my_list = [
    {'error': 'Photoeye Fault', 'r1': 'Planned Stop', 'r2': 'Pack Material', 'r3': 'Manufacturer Splice', 'r4': None,
     'comment': '', 'event_type': 'daily', 'freq': [4, 6, 3, 2], 'uptime': [75, 288, 125, 312, 277, 103, 81],
     'mins': [3, 2, 5, 7]},
    {'error': 'Coder Fault', 'r1': 'Planned Stop', 'r2': 'Changeover', 'r3': 'Ribbon Changeover', 'r4': None,
     'comment': '', 'event_type': 'monthly', 'freq': [1, 0, 1], 'uptime': 366, 'mins': 7},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Vertical sealing CIL',
     'r4': None, 'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 32},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Spillage hopper CIL', 'r4': None,
     'comment': '', 'event_type': 'weekly', 'freq': [1], 'mins': 23},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'S-conveyor CIL', 'r4': None,
     'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 125},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Rear web system CIL', 'r4': None,
     'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 42},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Packing conveyor CIL',
     'r4': None, 'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 55},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Outfeed conveyor CIL',
     'r4': None, 'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 86},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Markem unit CIL', 'r4': None,
     'comment': '', 'event_type': 'weekly', 'freq': [1], 'mins': 33},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Main drive CIL', 'r4': None,
     'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 30},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Machine frame CIL', 'r4': None,
     'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 40},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Main conveyor CIL', 'r4': None,
     'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 80},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Inclined conveyor CIL',
     'r4': None, 'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 75},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'TBM', 'r3': 'Imaje 9040 Maintenance',
     'r4': None, 'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 65},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Horizontal sealing CIL',
     'r4': None, 'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 80},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Front web system CIL',
     'r4': None, 'comment': '', 'event_type': 'weekly', 'freq': [1], 'mins': 66},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Forming set CIL', 'r4': None,
     'comment': '', 'event_type': 'weekly', 'freq': [1], 'mins': 60},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'TBM', 'r3': 'Fischbein Maintenance',
     'r4': None, 'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 75},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Dosing unit CIL', 'r4': None,
     'comment': '', 'event_type': 'weekly', 'freq': [1], 'mins': 85},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Triverter CIL', 'r4': None,
     'comment': '', 'event_type': 'weekly', 'freq': [1], 'mins': 17},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'CIL', 'r3': 'Triverter CIL', 'r4': None,
     'comment': '', 'event_type': 'monthly', 'freq': [1], 'mins': 54},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'RLS', 'r3': 'Shiftly RLS', 'r4': None,
     'comment': '', 'event_type': 'daily', 'uptime': [726, 840, 923, 887], 'freq': [2], 'mins': [41, 45, 47, 38]},
    {'error': 'End Of Film', 'r1': 'Planned Stop', 'r2': 'Changeover', 'r3': 'Reel Changeover', 'r4': None,
     'comment': '', 'event_type': 'daily', 'freq': [6, 4, 5, 5], 'uptime': [188, 215, 432, 294, 187, 313, 174],
     'mins': [5, 7, 10, 6]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'Changeover', 'r3': 'Size Changeover',
     'r4': 'State SKU in comment', 'comment': '', 'event_type': 'bi-weekly', 'freq': [1, 0, 2, 0],
     'mins': [15, 17, 13, 11]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Planned Stop', 'r2': 'Changeover', 'r3': 'Brand Changeover',
     'r4': 'State SKU in comment', 'comment': '', 'event_type': 'monthly', 'freq': [0, 1, 2, 0], 'mins': 33},
    {'error': 'Air Pressure Fault', 'r1': 'Planned stop', 'r2': 'IBEDC', 'r3': 'Power changeover',
     'r4': 'Changeover from IBEDC to generator', 'comment': '', 'event_type': 'weekly', 'freq': [1, 0, 1, 1, 0, 1],
     'mins': 17},
    {'error': 'Air Pressure Fault', 'r1': 'Planned stop', 'r2': 'Generator', 'r3': 'Power changeover',
     'r4': 'Changeover from generator to IBEDC', 'comment': '', 'event_type': 'weekly', 'freq': [1, 0, 1, 1, 0, 1],
     'mins': 17},
    {'error': 'End Product', 'r1': 'Unplanned stop', 'r2': 'No Powder Supply', 'r3': 'Starvation from MSG',
     'r4': 'MSG not producing (issue on MSG line)', 'comment': '', 'event_type': 'moderate', 'freq': [2, 0, 3, 0, 1],
     'mins': [60, 125, 45, 86, 246, 184]},
    {'error': 'Power Fault', 'r1': 'Unplanned stop', 'r2': 'Generator', 'r3': 'generator fault', 'r4': None,
     'comment': '', 'event_type': 'moderate', 'freq': [1], 'mins': [30, 40, 25, 28]},
    {'error': 'End Product', 'r1': 'Unplanned stop', 'r2': 'No Powder Supply', 'r3': 'Buggy not opened on time',
     'r4': 'Contractor indiscipline', 'comment': '', 'event_type': 'minor', 'freq': [5, 3, 4], 'mins': [10, 5, 7, 12]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Unplanned stop', 'r2': 'Polyfilm OOS',
     'r3': 'Ink stain on polyfilm', 'r4': 'Specify in comment', 'comment': '', 'event_type': 'major', 'freq': [1, 2, 4],
     'mins': [28, 35, 42]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Unplanned stop', 'r2': 'Contractor inefficiency',
     'r3': 'Contractor inefficiency', 'r4': 'Specify in comment', 'comment': '', 'event_type': 'major',
     'freq': [1, 3, 2], 'mins': [25, 38, 45]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Unplanned stop', 'r2': 'Secondary Coding- Domino',
     'r3': 'Domino Print head system fault', 'r4': 'Blockage in printhead', 'comment': '', 'event_type': 'major',
     'freq': [1, 3, 2], 'mins': [25, 38, 45]},
    {'error': 'Horizontal Jaw electric current limit.', 'r1': 'Unplanned stop', 'r2': 'Control System',
     'r3': 'communication loss from plc', 'r4': 'Communication loss',
     'comment': 'Communication loss between PLC and extraction belt', 'event_type': 'major', 'freq': [4, 0, 3, 0],
     'mins': [125, 86, 73, 144]},
    {'error': 'Photoeye Fault', 'r1': 'Unplanned stop', 'r2': 'Low Suction', 'r3': 'Partial blockage on DCS line',
     'r4': '', 'comment': '', 'event_type': 'major', 'freq': [1, 0], 'mins': [25, 38, 45]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Unplanned stop', 'r2': 'Main Conveyor',
     'r3': 'product trapped between  conveyors', 'r4': 'Specify in comment',
     'comment': 'Product trapped between main and inclined conveyors', 'event_type': 'moderate', 'freq': [1, 3, 0, 2],
     'mins': [12, 25, 30]},
    {'error': '2D No Read', 'r1': 'Unplanned stop', 'r2': 'Barcode reader', 'r3': '2D Camera fault',
     'r4': '2D NO READ (specify in comment)', 'comment': '', 'event_type': 'major', 'freq': [1, 0, 0, 1, 1],
     'mins': [25, 38, 45]},
    {'error': 'Temperature out of range', 'r1': 'Unplanned stop', 'r2': 'Horizontal Sealing',
     'r3': 'Defective front horizontal heating element', 'r4': 'Broken heating element cable', 'comment': '',
     'event_type': 'major', 'freq': [1, 0, 0, 0], 'mins': [166, 105, 118, 76, 92, 147]},
    {'error': 'Temperature out of range', 'r1': 'Unplanned stop', 'r2': 'Horizontal Sealing',
     'r3': 'Defective rear horizontal heating element', 'r4': 'Broken heating element cable', 'comment': '',
     'event_type': 'major', 'freq': [1, 0, 0, 0], 'mins': [125, 78, 145]},
    {'error': 'Temperature out of range', 'r1': 'Unplanned stop', 'r2': 'Horizontal Sealing',
     'r3': 'Defective front horizontal thermocouple', 'r4': 'Broken thermocouple cable',
     'comment': 'defective themocouple', 'event_type': 'major', 'freq': [1, 0, 0, 0], 'mins': [35, 48, 55, 84]},
    {'error': 'Temperature out of range', 'r1': 'Unplanned stop', 'r2': 'Horizontal Sealing',
     'r3': 'Defective rear horizontal thermocouple', 'r4': 'Broken thermocouple cable',
     'comment': 'defective themocouple', 'event_type': 'major', 'freq': [1, 0, 0, 0], 'mins': [37, 41, 58, 76]},
    {'error': 'Temperature out of range', 'r1': 'Unplanned stop', 'r2': 'Vertical Sealing',
     'r3': 'Defective vertical heating element', 'r4': 'Broken heating element cable', 'comment': '',
     'event_type': 'major', 'freq': [1, 0, 0, 0], 'mins': [35, 122, 90, 84]},
    {'error': 'Temperature out of range', 'r1': 'Unplanned stop', 'r2': 'Vertical Sealing',
     'r3': 'Defective vertical thermocouple', 'r4': 'Broken thermocouple cable', 'comment': 'defective themocouple',
     'event_type': 'major', 'freq': [1, 0, 1, 0], 'mins': [145, 148, 120, 84]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Unplanned stop', 'r2': 'Cutting and Perforation',
     'r3': 'Damaged knife Cylinder', 'r4': 'Damaged cylinder seal', 'comment': '', 'event_type': 'major',
     'freq': [1, 0, 1, 0, 0], 'mins': [65, 84, 155, 94]},
    {'error': 'Machine Stopped by Operator', 'r1': 'Unplanned stop', 'r2': 'Primary Coding',
     'r3': 'Markem Printhead system fault', 'r4': 'Worn printhead', 'comment': '', 'event_type': 'major',
     'freq': [1, 0, 1, 0], 'mins': [125, 164, 108, 84]},
    {'error': 'Photoeye Fault', 'r1': 'Unplanned stop', 'r2': 'Bag Forming', 'r3': 'Contamination on Forming set',
     'r4': 'Contamination on formingset wall', 'comment': 'film jam on forming set', 'event_type': 'minor',
     'freq': [1, 0, 2, 0, 3, 0], 'mins': [35, 25, 42, 69]},
    {'error': 'Photoeye Fault', 'r1': 'Unplanned stop', 'r2': 'Pulling', 'r3': 'Photocell lost calibration',
     'r4': 'Photocell lost calibration', 'comment': '', 'event_type': 'moderate', 'freq': [1, 0, 1, 0, 0, 0],
     'mins': [15, 23, 18, 29]},
    {'error': 'Power Fault', 'r1': 'Unplanned stop', 'r2': 'Compressor', 'r3': 'compressor fault', 'r4': None,
     'comment': '', 'event_type': 'moderate', 'freq': [1], 'mins': [30, 40, 25, 28]}
]

import random
from datetime import datetime, timedelta
import calendar
from calendar import monthrange
import pickle


class DowntimeLogger:
    def __init__(self, pr, year, month, machine, events=None):
        self.pr = pr
        self.year = year
        self.month = month
        self.machine = machine
        self.total_uptime = None
        self.total_unplanned_downtime = None
        self.total_planned_downtime = None
        self.total_downtime = None
        self.monthly_downtime = None
        self.weekly_downtime = None
        self.daily_downtime = None
        self.events = events if events else []
        self.event_log = []
        self.schedule_time = None
        self.calculate_schedule_time()
        self.calculate_uptime_downtime()
        self.calculate_random_downtime_allocation()
        self.share_downtime()
        self.log_events()
        self.add_machine()
        self.calculate_event_uptime()
        # print(self.event_log)
        # print(f'total events {len(self.event_log)}')
        # print(self.get_events_by_day(1))

    @staticmethod
    def generate_event_frequency():
        # Randomly determine the frequency from 1 to 3
        frequency = random.randint(1, 3)
        return frequency

    @staticmethod
    def get_number_of_weeks(year, month):
        # Get the matrix representing the month
        month_matrix = calendar.monthcalendar(year, month)

        # Count the number of weeks with at least one day
        num_weeks = sum(1 for week in month_matrix if any(week))

        return num_weeks

    def add_machine(self):
        for event in self.event_log:
            event['machine'] = self.machine

    def log_events(self):
        self.log_monthly_events()
        # print(f'logged {len(self.event_log)}')
        self.log_weekly_events()
        # print(f'logged {len(self.event_log)}')
        self.log_daily_events()
        # print(f'logged {len(self.event_log)}')
        self.log_major_events()
        # print(f'logged {len(self.event_log)}')
        self.log_moderate_events()
        # print(f'logged {len(self.event_log)}')
        self.log_minor_events()
        # print(f'logged finally {len(self.event_log)}')

    def total_minutes_in_month(self):
        # Check if month is valid
        if 1 <= self.month <= 12:
            # Calculate the number of days in the given month and year
            _, num_days_in_month = monthrange(self.year, self.month)

            # Assuming there are 24 hours in a day
            return num_days_in_month * 24 * 60
        else:
            # Invalid month
            print("Invalid month provided. Month should be between 1 and 12.")
            return 0

    def calculate_schedule_time(self):
        if any('shutdown' in event['event_type'] for event in self.events):
            shutdown_event = next((event for event in self.events if 'shutdown' in event['event_type']), None)
            if shutdown_event:
                start_time = datetime.strptime(shutdown_event['start_time'], '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime(shutdown_event['end_time'], '%Y-%m-%d %H:%M:%S')
                downtime = (end_time - start_time).total_seconds() / 60  # Convert to minutes
                self.schedule_time = self.total_minutes_in_month() - downtime
        else:
            # No 'shutdown' event found, schedule time is equal to total_minutes
            self.schedule_time = self.total_minutes_in_month()

    def calculate_uptime_downtime(self):
        if self.pr is not None and self.schedule_time is not None:
            self.total_uptime = (self.pr / 100) * self.schedule_time
            self.total_downtime = self.schedule_time - self.total_uptime

    def calculate_random_downtime_allocation(self):
        if self.total_downtime is not None:
            # Ensure total_planned_downtime is between 67% and 83% of total_downtime
            lower_bound = 0.47  # 0.67
            upper_bound = 0.63  # 0.83
            random_ratio = random.uniform(lower_bound, upper_bound)

            self.total_planned_downtime = self.total_downtime * random_ratio
            self.total_unplanned_downtime = self.total_downtime - self.total_planned_downtime

    def share_downtime(self, downtime=None):
        if downtime is None:
            downtime = self.total_planned_downtime

        # Define the ratios for distribution
        monthly_ratio = 0.65
        weekly_ratio = 0.25
        daily_ratio = 0.10

        # Calculate the three portions
        self.monthly_downtime = int(downtime * monthly_ratio)
        self.weekly_downtime = int(downtime * weekly_ratio)
        self.daily_downtime = int(downtime * daily_ratio)

        # Return all three downtimes
        return self.monthly_downtime, self.weekly_downtime, self.daily_downtime

    def allocate_monthly_downtime(self):
        if self.monthly_downtime is not None and self.events:
            monthly_events = [event for event in self.events if event['event_type'] == 'monthly']

            if monthly_events:
                total_monthly_minutes = sum(event['mins'] for event in monthly_events)

                for event in monthly_events:
                    event_minutes = event['mins']
                    ratio = event_minutes / total_monthly_minutes
                    event_downtime = int(self.monthly_downtime * ratio)
                    event['downtime'] = event_downtime

                return monthly_events
            else:
                print("No 'monthly' events found.")
                return None
        else:
            print("Monthly downtime or events not initialized.")
            return None

    def allocate_weekly_downtime(self):
        if self.weekly_downtime is not None and self.events:
            weekly_events = [event for event in self.events if event['event_type'] == 'weekly']

            if weekly_events:
                total_weekly_minutes = sum(event['mins'] for event in weekly_events)

                for event in weekly_events:
                    event_minutes = event['mins']
                    ratio = event_minutes / total_weekly_minutes

                    # Divide the downtime portion into four portions in ratio of 9:7:6:8
                    downtime_list = [
                        int(self.weekly_downtime * ratio * 9 / 30),
                        int(self.weekly_downtime * ratio * 7 / 30),
                        int(self.weekly_downtime * ratio * 6 / 30),
                        int(self.weekly_downtime * ratio * 8 / 30)
                    ]

                    event['downtime_list'] = downtime_list

                return weekly_events
            else:
                print("No 'weekly' events found.")
                return None
        else:
            print("Weekly downtime or events not initialized.")
            return None

    def allocate_daily_downtime(self):
        if self.daily_downtime is not None and self.events:
            total_days_in_month = monthrange(self.year, self.month)[1]

            # Check for a shutdown event
            shutdown_event = next((event for event in self.events if 'shutdown' in event), None)

            if shutdown_event:
                shutdown_start = datetime.strptime(shutdown_event['start_time'], '%Y-%m-%d %H:%M:%S')
                shutdown_end = datetime.strptime(shutdown_event['end_time'], '%Y-%m-%d %H:%M:%S')

                # Calculate the number of shutdown days
                shutdown_days = (shutdown_end - shutdown_start).days + 1

                # Subtract shutdown days from the total number of days in the month
                remaining_days = total_days_in_month - shutdown_days

                # Share the daily_downtime equally for the remaining days
                daily_downtime_per_day = int(self.daily_downtime / remaining_days)

                return daily_downtime_per_day
            else:
                # If no shutdown event, share daily_downtime equally for all days in the month
                daily_downtime_per_day = int(self.daily_downtime / total_days_in_month)
                return daily_downtime_per_day
        else:
            print("Daily downtime or events not initialized.")
            return None

    def allocate_unplanned_downtime(self):
        if self.total_unplanned_downtime is not None:
            # Define the ratios for distribution
            major_ratio = 1
            moderate_ratio = 3
            minor_ratio = 5

            # Calculate the three portions
            major_downtime = int(self.total_unplanned_downtime * major_ratio / 9)
            moderate_downtime = int(self.total_unplanned_downtime * moderate_ratio / 9)
            minor_downtime = int(self.total_unplanned_downtime * minor_ratio / 9)

            return {'major_downtime': major_downtime, 'moderate_downtime': moderate_downtime,
                    'minor_downtime': minor_downtime}
        else:
            print("Total unplanned downtime not initialized.")
            return {'major_downtime': None, 'moderate_downtime': None, 'minor_downtime': None}

    def generate_random_start_time(self, start_day, end_day):
        # Randomly select a day in the specified range
        day = random.randint(start_day, end_day)

        # Generate a random start time on the selected day
        start_time = datetime(self.year, self.month, day, random.randint(0, 23), random.randint(0, 59))

        return start_time

    def check_overlap(self, new_start_time, new_end_time):
        # Check if the new event overlaps with existing events in event_log
        for event in self.event_log:
            existing_start_time = datetime.strptime(event['start_time'], '%Y-%m-%d %H:%M:%S')
            existing_end_time = datetime.strptime(event['end_time'], '%Y-%m-%d %H:%M:%S')

            # Debug print statements
            # print(f"Checking overlap for new event: {new_start_time} - {new_end_time}")
            # print(f"Existing event: {existing_start_time} - {existing_end_time}, titlle: {event['error']}")

            # Check for overlap
            if (existing_end_time <= new_start_time and existing_start_time >= new_end_time) or \
                    (new_start_time == existing_start_time and new_end_time == existing_end_time):
                # print("Overlap found!")
                return True  # Overlap found

            # check for when one downtime is within a pair
            if ((existing_start_time <= new_start_time <= existing_end_time) or
                    (existing_start_time <= new_end_time <= existing_end_time)):
                # print("Overlap found! (within a pair)")
                return True  # Overlap found

        # print("No overlap")
        return False  # No overlap

    def log_monthly_events(self):
        monthly_events = self.allocate_monthly_downtime()

        if monthly_events:
            for temp_event in monthly_events:
                event = copy.deepcopy(temp_event)
                # Generate a random start_time for the event
                start_time = self.generate_random_start_time(1, monthrange(self.year, self.month)[1])

                # Calculate the end_time by adding 'downtime' to start_time
                end_time = start_time + timedelta(minutes=event['downtime'])

                # Check for overlap with existing events
                while self.check_overlap(start_time, end_time):
                    # Adjust start_time or end_time if there is an overlap
                    start_time = self.generate_random_start_time(1, monthrange(self.year, self.month)[1])
                    end_time = start_time + timedelta(minutes=event['downtime'])

                # Update the event dictionary with start_time and end_time
                event['start_time'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
                event['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

                # Add the event to event_log
                self.event_log.append(event)

            return self.event_log
        else:
            print("No monthly events to log.")
            return None

    def log_weekly_events(self):
        weekly_events = self.allocate_weekly_downtime()

        if weekly_events:
            for event in weekly_events:
                # Randomly select a day in the first week of the month
                start_time_first_week = self.generate_random_start_time(1, 7)

                # Log the event for the first week
                self.log_weekly_event(event, start_time_first_week, 1, 7)

                # Randomly select a day in the second week of the month
                start_time_second_week = self.generate_random_start_time(8, 14)

                # Log the event for the second week
                self.log_weekly_event(event, start_time_second_week, 8, 14)

                # Randomly select a day in the third week of the month
                start_time_third_week = self.generate_random_start_time(15, 21)

                # Log the event for the third week
                self.log_weekly_event(event, start_time_third_week, 15, 21)

                # Randomly select a day in the fourth week of the month
                start_time_fourth_week = self.generate_random_start_time(22, monthrange(self.year, self.month)[1])

                # Log the event for the fourth week
                self.log_weekly_event(event, start_time_fourth_week, 22, monthrange(self.year, self.month)[1])

            return self.event_log
        else:
            print("No weekly events to log.")
            return None

    def log_weekly_event(self, temp_event, start_time, start_day, end_day):
        # Ensure downtime_list is present in the
        event = copy.deepcopy(temp_event)
        downtime_list = event.get('downtime_list', [0, 0, 0, 0])

        if downtime_list:
            # Randomly pick a downtime from the list
            random_downtime = random.choice(downtime_list)

            # Remove the picked downtime from the list to avoid repetition in the following weeks
            downtime_list.remove(random_downtime)

            # Calculate the end_time by adding the picked downtime to start_time
            end_time = start_time + timedelta(minutes=random_downtime)

            # Check for overlap with existing events
            while self.check_overlap(start_time, end_time):
                # If there is an overlap, choose a new start_time and recalculate end_time
                start_time = self.generate_random_start_time(start_day, end_day)

                # Ensure downtime_list is not empty before picking a new downtime
                # if downtime_list:
                # random_downtime = random.choice(downtime_list)
                # downtime_list.remove(random_downtime)
                # else:
                # If downtime_list is empty, break the loop
                # break

                end_time = start_time + timedelta(minutes=random_downtime)

            # Update the event dictionary with start_time and end_time
            event['start_time'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            event['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

            # Add the event to event_log
            self.event_log.append(event)
        else:
            print("No downtime available for logging.")

    def log_daily_events(self):
        daily_events = [event for event in self.events if event['event_type'] == 'daily']

        if daily_events:

            total_days_in_month = monthrange(self.year, self.month)[1]
            shutdown_event = next((event for event in self.events if 'shutdown' in event), None)

            if shutdown_event:
                shutdown_start = datetime.strptime(shutdown_event['start_time'], '%Y-%m-%d %H:%M:%S')
                shutdown_end = datetime.strptime(shutdown_event['end_time'], '%Y-%m-%d %H:%M:%S')
                shutdown_days = (shutdown_end - shutdown_start).days + 1
                total_days_in_month -= shutdown_days

            # print(f'starting: {len(self.event_log)}')

            for day in range(1, total_days_in_month + 1):
                daily_downtime_per_day = self.allocate_daily_downtime()
                # log daily events for the day til daily downtime per day is zero
                while daily_downtime_per_day:
                    # Pick a random daily event
                    temp_event = random.choice(daily_events)
                    selected_event = copy.deepcopy(temp_event)

                    # Generate a random start_time for the day
                    start_time = self.generate_random_start_time(day, day)

                    # Pick a random downtime from the event's 'mins' attribute
                    random_downtime = random.choice(selected_event.get('mins', [0]))

                    if daily_downtime_per_day < random_downtime:
                        random_downtime = daily_downtime_per_day

                    # Calculate the end_time by adding the random_downtime
                    end_time = start_time + timedelta(minutes=random_downtime)

                    # Check for overlap with existing events
                    while self.check_overlap(start_time, end_time):
                        # If there is an overlap, choose a new start_time and recalculate end_time
                        start_time = self.generate_random_start_time(day, day)
                        # random_downtime = random.choice(selected_event.get('mins', [0]))
                        end_time = start_time + timedelta(minutes=random_downtime)

                    # Update the event dictionary with start_time and end_time
                    selected_event['start_time'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    selected_event['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

                    # Add the event to event_log
                    self.event_log.append(selected_event)
                    # print(f'dwntimeperday: {daily_downtime_per_day}, randomtime: {random_downtime}, daily event for {selected_event["start_time"]}')

                    # Subtract the downtime from daily_downtime_per_day
                    daily_downtime_per_day -= random_downtime

            return self.event_log
        else:
            print("No daily events to log.")
            return None

    def log_major_events(self):
        major_events = [event for event in self.events if event['event_type'] == 'major']
        major_downtime = self.allocate_unplanned_downtime().get('major_downtime', 0)

        if major_events and major_downtime > 0:
            for temp_event in major_events:
                # Get a random frequency for the event
                frequency = self.generate_event_frequency()
                # Create a list of selectable weeks from 1 to 4
                selectable_weeks = list(range(1, 5))

                for _ in range(frequency):
                    if major_downtime == 0:
                        break

                    event = copy.deepcopy(temp_event)

                    # Select a week from the list
                    selected_week = random.choice(selectable_weeks)

                    # Remove the selected week from the list
                    selectable_weeks.remove(selected_week)

                    # Pick a random downtime from the event's 'mins' attribute
                    random_downtime = random.choice(event.get('mins', [0]))

                    # Check that the random_downtime is not greater than major_downtime
                    downtime_to_use = min(random_downtime, major_downtime)

                    # Generate a random start_time for the selected week
                    start_time = self.generate_random_start_time(selected_week, monthrange(self.year, self.month)[1])

                    # Calculate the end_time by adding the downtime_to_use
                    end_time = start_time + timedelta(minutes=downtime_to_use)

                    # Check for overlap with existing events
                    while self.check_overlap(start_time, end_time):
                        # If there is an overlap, choose a new start_time and recalculate end_time
                        start_time = self.generate_random_start_time(selected_week,
                                                                     monthrange(self.year, self.month)[1])
                        end_time = start_time + timedelta(minutes=downtime_to_use)

                    # Update the event dictionary with start_time and end_time
                    event['start_time'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    event['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

                    # Add the event to event_log
                    self.event_log.append(event)

                    # Subtract the downtime_to_use from major_downtime
                    major_downtime -= downtime_to_use

            return self.event_log
        else:
            print("No major events to log or major_downtime is zero.")
            return None

    def log_moderate_events(self):
        moderate_events = [event for event in self.events if event['event_type'] == 'moderate']
        moderate_downtime = self.allocate_unplanned_downtime().get('moderate_downtime', 0)

        # Get the number of weeks in the month
        num_weeks_in_month = self.get_number_of_weeks(self.year, self.month)

        # Calculate week_downtime as a dividend of moderate_downtime
        week_downtime = moderate_downtime // num_weeks_in_month

        if moderate_events and week_downtime > 0:

            # Iterate through each week in the month
            for week in range(1, num_weeks_in_month + 1):
                if week_downtime == 0:
                    break

                # pick event at random
                event_temp = random.choice(moderate_events)

                # Select a random event frequency
                frequency = self.generate_event_frequency()

                for _ in range(frequency):
                    if week_downtime == 0:
                        break

                    event = copy.deepcopy(event_temp)

                    # Pick a random downtime from the event's 'mins' attribute
                    random_downtime = random.choice(event.get('mins', [0]))

                    # Check that the random_downtime is not greater than the week_downtime
                    downtime_to_use = min(random_downtime, week_downtime)

                    # Generate a random start_time within the selected week
                    start_time = self.generate_random_start_time(week, monthrange(self.year, self.month)[1])

                    # Calculate the end_time by adding the downtime_to_use
                    end_time = start_time + timedelta(minutes=downtime_to_use)

                    # Check for overlap with existing events
                    while self.check_overlap(start_time, end_time):
                        # If there is an overlap, choose a new start_time and recalculate end_time
                        start_time = self.generate_random_start_time(week, monthrange(self.year, self.month)[1])
                        end_time = start_time + timedelta(minutes=downtime_to_use)

                    # Update the event dictionary with start_time and end_time
                    event['start_time'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    event['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

                    # Add the event to event_log
                    self.event_log.append(event)

                    # Subtract the downtime_to_use from week_downtime
                    week_downtime -= downtime_to_use

            return self.event_log
        else:
            print("No moderate events to log or moderate_downtime is zero.")
            return None

    def log_minor_events(self):
        minor_events = [event for event in self.events if event['event_type'] == 'minor']
        minor_downtime = self.allocate_unplanned_downtime().get('minor_downtime', 0)

        # Get the number of days in the month
        num_days_in_month = monthrange(self.year, self.month)[1]

        # Subtract shutdown days if available
        shutdown_events = [event for event in self.events if 'shutdown' in event]
        shutdown_days = sum((datetime.strptime(event['end_time'], '%Y-%m-%d %H:%M:%S') -
                             datetime.strptime(event['start_time'], '%Y-%m-%d %H:%M:%S')).days + 1
                            for event in shutdown_events)

        remaining_days = num_days_in_month - shutdown_days

        if minor_events:
            # Iterate through each day in the month
            for day in range(1, remaining_days + 1):
                # Calculate day_downtime as a dividend of minor_downtime
                day_downtime = minor_downtime / remaining_days if remaining_days > 0 else 0

                while day_downtime:
                    # Pick an event at random
                    temp_event = random.choice(minor_events)

                    # Select a random event frequency
                    frequency = self.generate_event_frequency()

                    for _ in range(frequency):
                        if day_downtime == 0:
                            break

                        event = copy.deepcopy(temp_event)
                        # Pick a random downtime from the event's 'mins' attribute
                        random_downtime = random.choice(event.get('mins', [0]))

                        # Check that the random_downtime is not greater than the day_downtime
                        downtime_to_use = min(random_downtime, day_downtime)

                        # Generate a random start_time for the day
                        start_time = self.generate_random_start_time(day, day)

                        # Calculate the end_time by adding the downtime_to_use
                        end_time = start_time + timedelta(minutes=downtime_to_use)

                        # Check for overlap with existing events
                        while self.check_overlap(start_time, end_time):
                            # If there is an overlap, choose a new start_time and recalculate end_time
                            start_time = self.generate_random_start_time(day, day)
                            end_time = start_time + timedelta(minutes=downtime_to_use)

                        # Update the event dictionary with start_time and end_time
                        event['start_time'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
                        event['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

                        # Add the event to event_log
                        self.event_log.append(event)

                        # Subtract the downtime_to_use from day_downtime
                        day_downtime -= downtime_to_use

            return self.event_log
        else:
            print("No minor events to log or minor_downtime is zero.")
            return None

    def calculate_event_uptime(self):
        import copy
        # Sort events in the event_log by start_time
        event_log = []
        events = self.convert_event_times_to_datetime()
        # sorted_events = sorted(events, key=lambda x: datetime.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S'))
        sorted_events = sorted(events, key=lambda x: x['start_time'])

        for i, event in enumerate(sorted_events):
            if i == 0:
                # For the first event, uptime is measured from the beginning of the month
                start_time = event['start_time']
                uptime = start_time - datetime.strptime(f"{self.year}-{self.month:02d}-01 00:00:00",
                                                        '%Y-%m-%d %H:%M:%S')
            else:
                # For subsequent events, uptime is the difference between start_time of event and end_time of the preceding event
                start_time = event['start_time']
                end_time_prev = sorted_events[i - 1]['end_time']
                uptime = start_time - end_time_prev

            # calculate downtime
            downtime = event['end_time'] - event['start_time']

            # Add 'uptime' attribute to the event
            event['uptime'] = uptime.total_seconds() // 60  # Convert to minutes
            event['downtime'] = downtime.total_seconds() // 60
            event_log.append(event)

        # Assign sorted events back to event_log
        self.event_log = event_log

        return self.event_log

    def convert_event_times_to_datetime(self):
        converted_events = []

        for event in self.event_log:
            converted_event = {
                'error': event['error'],
                'start_time': datetime.strptime(event['start_time'], '%Y-%m-%d %H:%M:%S'),
                'end_time': datetime.strptime(event['end_time'], '%Y-%m-%d %H:%M:%S'),
                'r1': event['r1'],
                'r2': event['r2'],
                'r3': event['r3'],
                'r4': event['r4'],
                'comment': event['comment'],
                'freq': event['freq'],
                'mins': event['mins'],
                'event_type': event['event_type'],
                'machine': event['machine']
            }

            converted_events.append(converted_event)

        return converted_events

    def get_events_by_day(self, target_day):
        try:
            events_on_day = [event for event in self.event_log if event['start_time'].day == target_day]
        except:
            events_on_day = [event for event in self.event_log if
                             datetime.strptime(event['start_time'], '%Y-%m-%d %H:%M:%S').day == target_day]
        return events_on_day

# for after events, you have to reduce the mins of the planned dt events, reduce the sharing ratio of total_planned
# downtime
logged_events = []
data = [(4, 2022, 91, 'U'), (5, 2022, 88, 'U'), (6, 2022, 90, 'U'), (7, 2022, 88, 'U'), (8, 2022, 94, 'U'),
        (9, 2022, 89, 'U'),
        (4, 2022, 85, 'V'), (5, 2022, 89, 'V'), (6, 2022, 88, 'V'), (7, 2022, 86, 'V'), (8, 2022, 92, 'V'),
        (9, 2022, 85, 'V'),
        (4, 2022, 90, 'W'), (5, 2022, 91, 'W'), (6, 2022, 89, 'W'), (7, 2022, 92, 'W'), (8, 2022, 93, 'W'),
        (9, 2022, 84, 'W')]
for x in data:
    month, year, pr, machine = x
    logger = DowntimeLogger(pr=pr, month=month, machine=machine, year=year, events=my_list)
    logged_events.extend(logger.event_log)
    print(f'logged: {len(logged_events)}')


def write_event_log_to_file(event_log, filename='event_log.pkl'):
    """
    Write the event_log to a Python file using pickle.

    Parameters:
    - event_log: List of dictionaries representing events.
    - filename: Name of the output file (default is 'event_log.pkl').
    """
    with open(filename, 'wb') as file:
        pickle.dump(event_log, file)


write_event_log_to_file(logged_events, 'output_event_log2.pkl')

# print(logger.year)
