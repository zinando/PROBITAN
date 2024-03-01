# PROBITAN
![App Logo](./myapp/appfiles/images/bg/bg.jpg)
## Description ##

**PROBITAN** is a software programme that is used to visualize equipment downtime events graphically. It accesses
statistical records of downtime events for the equipment over a period of time and uses this data to present a picture
of how each event contributes to the overall losses (PR loss) on the equipment over the period studied. 

## How **PROBITAN** works
* It accepts a project file as an input to be studied. This could be an existing file within the applications directories or a new file input
* It allows the user to create visual graphs based on the data contained in the project file 
* It allows the user to upload a second file to compare with the previous one
* When a second project file is present, user can generate comparative graphs of data between the two files

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
   - [File Upload](#file-upload)
   - [Data Extraction](#data-extraction)
   - [Analysis and Visualization](#analysis-and-visualization)
   - [Predictive Analysis](#predictive-analysis)
   - [Improvement Impact Analysis](#improvement-impact-analysis)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
4. [Usage](#usage)
   - [Uploading Files](#uploading-files)
   - [Data Analysis](#data-analysis)
   - [Visualization](#visualization)
   - [Predictive Analysis](#predictive-analysis-1)
   - [Improvement Impact Analysis](#improvement-impact-analysis-1)
5. [Output and Reports](#output-and-reports)
   - [Monthly Reports](#monthly-reports)
   - [Top Losses](#top-losses)
   - [Improvement Comparison](#improvement-comparison)
6. [FAQs](#faqs)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)


## 1. Introduction<a name="introduction"></a><br>
<p style="text-align: justify;"> <b>PROBITAN</b> is a powerful tool designed to streamline the evaluation and interpretation of downtime records for operating machines in a factory. By allowing users to effortlessly upload Excel or CSV files containing downtime data, the app automates the extraction of crucial information such as downtime events, event durations, monthly production volumes, and uptime statistics.</p>

<p style="text-align: justify;">This application goes beyond mere data representation, providing a comprehensive set of analytical features. Users can delve into planned and unplanned downtime events, visualize monthly trends, identify top losses, and assess the impact of reducing specific downtimes on overall process reliability. Additionally, the app facilitates the comparison of machine downtime records before and after the implementation of improvement measures through autonomous maintenance methodologies.</p>

<p style="text-align: justify;">With user-friendly functionalities and insightful reports, the Downtime Analysis App empowers users to make informed decisions, optimize machine performance, and enhance overall operational efficiency within a factory setting.</P>

## 2. Features<a name="features"></a>
**PROBITAN** offers a suite of features tailored to simplify and enhance the assessment of downtime records for factory operating machines.

### 2.1 File Upload<a name="file-upload"></a>
<p style="text-align: justify;">The app opens to a window with two buttons that allow user to select the project file to be analyzed. User can select 
from existing project files within the app directories, or select an entirely new file from outside the app to be a new 
project analysis.
The app sequentially numbers each new file uploaded into it. This numbering should guide the user to match selected 
pre-existing before project file with a corresponding pre-existing result file when loading the result file. The result 
file is the second file that contains the machine downtime records after improvement has been implemented.

File formats can either be Excel file (.xlxs or .xls) or csv (.csv).
Important column headings that must be present in the file include:
 - ### start_date:
    Describes the start datetime record of events. PROBITAN automatically detects regular datetime formats.
 - ### end_date:
    Describes the end datetime record of events.
 - ### uptime:
    The time difference in minutes between the start_date of one event and the end_date of the previous event.
 - ### downtime:
    The time difference in minutes between the end_date of an event  and the star_date of the same event.
 - ### class:
    The major classification of the downtime event. Recognised class names are: planned, unplanned or planned stop, unplanned stop.
 - ### type:
    This is the specific description of the event. It could be CIL event, time-based maintenance, routine events, 
    operations stop event etc.
 - ### location:
    <p style="text-align: justify;">This specifies the part of the machine responsible for the downtime event. For instance, if the downtime event is 
    for a time-based maintenance, then it is that part of the machine is where the maintenance taking place.

<p style="text-align: justify;">Downtime events are usually logged by auto-logging apps like General Electrics proficy app. Irrespective of the content,
ensure the above column headers are well represented in your file, otherwise you won't be able to get result from the app. 

### 2.2 Data Extraction<a name="data-extraction"></a>
**PROBITAN** automatically extracts crucial information such as downtime events, event durations and uptime statistics 
from the uploaded files. Volume data is being calculated based on uptime.

### 2.3 Analysis and Visualization<a name="analysis-and-visualization"></a>
<p style="text-align: justify;">Gain valuable insights by analyzing and visualizing planned and unplanned downtime events. Graphical representations
help users understand monthly trends and contribute to effective decision-making. Visualizing top loss events could help
users pay focused attention to 20% of events that contribute to 80% operational losses.

### 2.4 Predictive Analysis<a name="predictive-analysis"></a>
User can forecast the impact of reducing specific downtimes on overall process reliability, enabling proactive decision-making 
for improved operational efficiency.

### 2.5 Improvement Impact Analysis<a name="improvement-impact-analysis"></a>
Compare machine downtime records before and after implementing improvement measures, providing a clear understanding
of the impact of autonomous maintenance methodologies.

## 3. Getting Started<a name="getting-started"></a>

### 3.1 Prerequisites<a name="prerequisites"></a>
The software requires windows operating system version 8 or higher.

### 3.2 Installation<a name="installation"></a>
Download the installation file [here](installler/).
<p style="text-align: justify;">Double click on the file and allow it to install. By default, the installatiion destination is your Program Files 
directory, but you could preferably change this to Users/your-user-name/AppData/Roaming.
After installation, a shortcut desktop link of the app will appear on your device desktop.

## 4. Usage<a name="usage"></a>
Open the app by double-clicking on the app icon from your device desktop.

### 4.1 Uploading Files<a name="uploading-files"></a>
If using the app for the first time, click on the New Project button to select the project file to be analyzed 
from your device.

If you intend to open a file you have already uploaded before, click on the Select Project button to select the exact 
file within the app directories.

Once you have selected the file, click open and allow the app to  open to the work window.

### 4.2 Visualization<a name="visualization"></a>
Click the <i>view</i> button at the top of the app to reveal the buttons used to visualize the various attributes 
of the downtime record. Click each button revealed to view the corresponding information.
#### Graphs:
Graphical views can be expanded for enlarged views using the expand button beneath the view. Expanded graph views 
can be saved as images on user's desired location.

### 4.3 Data Analysis<a name="data-analysis"></a>
<p style="text-align: justify;">With <i>analyze</i> button, user can analyze top losses from the downtime events. Select the scope 
of the analysis by selecting Planned, Unplanned or All of the downtime events. Then select the number
of events to return. For instance, selecting Planned and 3 from the respective dropdowns would
display the downtime graph for the top 3 'planned events' with the highest downtimes without considering 
unplanned events.

### 4.4 Predictive Analysis<a name="predictive-analysis-1"></a>
<p style="text-align: justify;">Predict the impact of reducing downtimes by a chosen percentage on the overall 
process reliability. Select Planned, Unplanned or All from the first dropdown. Optionally select an event from the 
second dropdown, and then select percentage of reduction from the third dropdown. The graph of process reliability (PR)
for before and after the reduction will be displayed. 

<p style="text-align: justify;">The extent of change in the PR depends on the wideness of the 
scope of the prediction. Ideally, user would want to predict the impact of reducing Planned downtimes by a chosen 
percentage say 50%. So the user selects Planned in the first dropdown, leaves the second dropdown and goes to 
the third dropdown and selects 50%. This would result in a graph showing two PR trends for 
before and after a purported reduction by 50% in planned downime. Then user uses the <i>analyze</i> to get
top 20% of planned downtime events that give the highest downtime. By pareto principle, improving this 20% of the 
downtime events would yield 80% of the needed result.

### 4.5 Improvement Impact Analysis<a name="improvement-impact-analysis-1"></a>
Comparison is between events downtime for before and the after project files. So in order to compare, you must ensure 
that result file has also been loaded.
To compare, click on the <i>compare</i> button under the graph view.

## 5. Output and Reports<a name="output-and-reports"></a>
**PROBITAN** generates insightful reports that empower users with a comprehensive understanding of 
machine performance and operational efficiency.

### 5.1 Monthly Reports<a name="monthly-reports"></a>
Receive detailed monthly reports that include essential metrics such as process reliability and production volumes. 
These reports offer a holistic view of machine performance, aiding in strategic decision-making.

### 5.2 Top Losses<a name="top-losses"></a>
Identify and prioritize issues by accessing reports on top losses. This feature pinpoints events with the 
highest downtime, allowing users to focus on areas that significantly impact operational efficiency.

### 5.3 Improvement Comparison<a name="improvement-comparison"></a>
<p style="text-align: justify;">Efficiently assess the impact of improvement measures by comparing machine 
downtime records before and after the implementation of autonomous maintenance methodologies. This feature provides 
valuable insights into the effectiveness of improvement initiatives.

**PROBITAN's** output and reports are designed to empower users with actionable insights, enabling them 
to optimize processes, reduce downtime, and enhance overall factory productivity.

## 6. FAQs<a name="faqs"></a>


## 7. Troubleshooting<a name="troubleshooting"></a>


## 8. Contributing<a name="contributing"></a>


## 9. License<a name="license"></a>

## Authors ##
👤 **Engr. Adetoro, Femi Ezekiel**

- Email: [adetorofemi@gmail.com](mailto:adetorofemi@gmail.com)

👤 **Ndubumma Samuel Nnadozie**

- GitHub: [@zinando](https://github.com/zinando)
- Twitter: [@i_am_Zinando](https://twitter.com/i_am_Zinando)
- LinkedIn: [LinkedIn](https://www.linkedin.com/in/samuel-nnadozie-38349476)
- Email: [xienando4reaconcepts@gmail.com](mailto:xienando4reaconcepts@gmail.com)
