This project's aim was to create an animated plot of Portugal COVID-19 new daily cases.

It does so by first obtaining the most recent data available at [Our World in Data](https://ourworldindata.org/).

This was my first attempt at making an animated plot and was heavily inspired by [this animation](https://www.reddit.com/r/dataisbeautiful/comments/s2vni6/oc_us_covid_patients_in_hospital/).


### Animated Plot
Below is the result (with data of 12/03/2022):

https://user-images.githubusercontent.com/57732731/158072303-433d3f75-cbdc-4a2f-9467-320edc135492.mp4


### Usage
To create the animation simply run `py Code\Portugal_covid19_cases_plot.py`.

### Requirements
The only requirement is the Matplotlib library (the version used was the 3.5.1).

To install the exact dependencies through the `requirements.txt` in a virtual environment, simply run the lines below (the file to activate the environment is different for those not on Windows running through Command Prompt, see more on [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)):
```
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```
