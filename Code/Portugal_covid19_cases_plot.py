import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator

from datetime import datetime
from os import mkdir
import os.path

from Get_OWID_Data import format_owid_data



# Support Function
def check_dir(dir):
    """ Checks if directory exists, if it doesn't then creates it """

    # Checking if path exists
    path_exists = os.path.exists(dir)

    if not path_exists:
        mkdir(dir)
        print("The following directory was created", dir)
#--------------------



def axes_adjustment_to_data(ax, data_coord, axes_adjust):
    """ Adjusts coordinates in data (coordinate system) by adding values in the axes coordinate system """
    """
    ax ----- ax object of the plot
    data_coord ----- original tuple in the default data coordinates
    axes_adjust ----- adjustment (that is added to data_coord) written in the axes coordinate system
    """

    # data -> display
    data_to_display = ax.transData.transform(data_coord)

    # display -> axes
    display_to_axes = ax.transAxes.inverted().transform(data_to_display)

    # axes + adjustment -> display
    axes_to_display = ax.transAxes.transform((display_to_axes[0] + axes_adjust[0], display_to_axes[1] + axes_adjust[1]))

    # display -> data
    display_to_data = ax.transData.inverted().transform(axes_to_display)
    
    return display_to_data



def plot_animation(dates, cases):

    
    # The Figure
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    fig.set_size_inches(9, 7, forward=True) # Defining the figure/window size
    # fig.set_size_inches(7, 7*7/9, forward=True) # Defining the figure/window size
    ax.spines[['top', 'right']].set_visible(False) # Hides right and top axis


    plt.subplots_adjust(bottom = 0.16)
    plt.subplots_adjust(top = 0.80)

    xmin = 0
    xmax = len(cases) - 1

    ydata = cases[0]

    xdata_line = [0]
    ydata_line = [cases[0]]


    line, = ax.plot(ydata_line, color = "#FF7000") # #48DFEB
    point, = ax.plot(ydata, "o", color = "#FF7000", markersize = 8.5) # point should be created after line

    # ----- Text ----- #
    # Label new cases
    new_cases_text_pos = (0.05, 0.84) # Position of the Text with the label of New Daily Cases
    new_cases_legend = ax.text(new_cases_text_pos[0], new_cases_text_pos[1], "Daily new cases", transform = fig.transFigure) # The transform specifies the coordinates to be relative to the Figure (fig).  1,1 is the top right corner and 0,0 the bot left

    # Data
    date_text_pos = (0.85, 0.85) # Position of the Text with the Date
    date_text = ax.text(date_text_pos[0], date_text_pos[1], "0", transform = fig.transFigure) # The transform specifies the coordinates to be relative to the Figure (fig).  1,1 is the top right corner and 0,0 the bot left

    # Current number of cases
    cases_text = ax.text(0, cases[0], "0") #, transform = fig.transFigure) # The transform specifies the coordinates to be relative to the Figure (fig).  1,1 is the top right corner and 0,0 the bot left

    # Title
    title_text_pos = (0.31, 0.93) # Position of the Text with the Title
    title_text = ax.text(title_text_pos[0], title_text_pos[1], "Portugal COVID-19 Daily New Cases", transform = fig.transFigure, fontsize = 15)

    # Source
    date_today = datetime.today().strftime('%d/%m/%Y')
    date_formatted = "12 Jan 2022"
    source_text_pos = (0.03, 0.04) # Position of the Text with the Source
    source_text = ax.text(source_text_pos[0], source_text_pos[1], "Source: Our World in Data, " + date_today, transform = fig.transFigure, fontsize = 8.5)
    # ----- Text ed ----- #

    # Ticks
    xticks_nums = []
    xticks_dates = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i in range(len(cases)):
        if dates[i][-2:] == "01":
            xticks_nums.append(i)
            
            # xticks_dates.append(dates[i])
            month = months[int(dates[i][-5:-3]) -1]
            year = dates[i][-8:-6]
            xticks_dates.append(month + "\n" + year)

    # X Ticks
    # ax.set_xticks(xticks_nums, labels = xticks_dates)
    ax.set_xticks(xticks_nums)
    ax.set_xticklabels(xticks_dates)

    # Y Ticks
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) # Allow only integer values for the yticks
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].set_visible(False) # Make first ytick invisible (both the tick itself and the label)



    def update_plot(n, point, line):

        if n < len(cases):
            print("Day", dates[n])

            ########## Axis X and Y limits ##########
            if n == 0: # For the first frame
                ax.set_ylim([0,1])
                ax.set_xlim([0,1])
            else:
                # Y-Axis
                ymin = 0
                ymax = max(cases[:n+1])

                ymargin = (cases[n] - ymin)/75 # Adding a margin to the top for better visibility (and to avoid having the dot 'cropped')
                ymax += ymargin

                ax.set_ylim([ymin,ymax])

                # X-Axis
                margin = (n-xmin)/75
                ax.set_xlim([xmin, n + margin])

            ########## Date and Cases Texts ##########
            new_cases_legend.set_position(new_cases_text_pos)

            # Date Text
            date_text.set_text(dates[n])
            date_text.set_position(date_text_pos)

            # Cases Text
            cases_text.set_text(int(cases[n]))
            cases_text_pos = axes_adjustment_to_data(ax, (n, cases[n]), (0.03, -0.01)) # The adjustment is being written in the axes coordinate system
            cases_text.set_position(cases_text_pos)

            # Title Text
            title_text.set_position(title_text_pos)

            ########## Point and Line data ##########

            # Point
            ydata = cases[n]
            point.set_data(n, ydata)

            # Line
            xdata_line.append(n)
            ydata_line.append(cases[n])
            line.set_data(xdata_line, ydata_line)

            return point, line
        else:
            # Counter for the command line (Finishing saving the video, "pause" time after all the dates have been plotted)
            # This doesn't really count in seconds as it's faster saving than showing, but a signifier made sense so that it shows that it's finishing creating the file
            frames_left = pause_at_end + len(cases) - n
            seconds_left = frames_left * 80 / 1000

            frames_left_next = pause_at_end + len(cases) - (n + 1)
            seconds_left_next = frames_left_next * 80 / 1000

            if int(seconds_left) != int(seconds_left_next):
                print(int(seconds_left))

            return point, line


    animation_interval = 80 # Milliseconds delay between each frame
    pause_at_end_seconds = 30 # Seconds to be added at the end of the animation (only relevant when exporting)
    pause_at_end = int((1000/animation_interval) * pause_at_end_seconds) # Number of frames to be added, to increase. This rounds up to the integer, so the duration isn't exactly that many seconds but shouldn't be perceivable

    ani = animation.FuncAnimation(fig, update_plot, len(cases) + pause_at_end, fargs=(point, line), interval = animation_interval, repeat = False)
    # the frames = len(points_x), is the first argument of the function, so in this case "n"

    # ani.save("Plot_animations\\Portugal_daily_new_cases.mp4") # Make sure to create the folder before running
    ani.save("Plot_animations\\Portugal_daily_new_cases_" + str(dates[-1]) + ".mp4") # Make sure to create the folder before running
    # plt.show()


if __name__ == "__main__":
    # Add this bit to Obsidian, "Python - Create directory"
    file_dir = os.path.dirname(__file__) # Script Directory
    main_dir = os.path.split(file_dir)[0] # Main Directory (parent folder of script)

    # Creating two directories (if they don't alreay exist) - "_Data" and "Plot_animations"
    check_dir(main_dir + "\\Plot_animations")
    check_dir(main_dir + "\\Code\\_Data")


    dates, new_cases = format_owid_data()
    plot_animation(dates, new_cases)