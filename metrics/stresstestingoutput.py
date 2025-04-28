import numpy as np
import matplotlib.pyplot as plt

def create_plot():
    # 5 x-axis labels
    labels = ['10', '100', '500', '1000', '2000']

    # Data for each group (avg latency)
    group1 = [900, 904, 78, 305, 1000]
    group2 = [900, 904, 78, 305, 1000]
    group3 = [900, 904, 78, 305, 1000]
    
    # Standard deviations for each group
    std1 = [200.5, 0.7, 0.3, 0.4, 0.6]
    std2 = [0.6, 0.9, 0.5, 0.7, 0.8]
    std3 = [0.4, 0.6, 0.2, 0.5, 0.7]

    x = np.arange(len(labels))  # [0, 1, 2, 3, 4]

    width = 0.25  # width of each bar

    # Create the figure and axes
    fig, ax = plt.subplots()

    # Plot bars
    ax.bar(x - width, group1, width, yerr=std1, label='No Cache')
    ax.bar(x,         group2, width, yerr=std2, label='Redis Cache')
    ax.bar(x + width, group3, width, yerr=std3, label='Nginx and Redis Cache')

    # Labels and title
    ax.set_xlabel('# Threads (Users)')
    ax.set_ylabel('Latency')
    ax.set_title('Stress Testing')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    # Add a legend
    ax.legend()

    # Show the plot
    plt.show()
    
if __name__ == '__main__':
    create_plot()