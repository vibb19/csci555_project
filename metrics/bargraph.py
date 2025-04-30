import numpy as np
import matplotlib.pyplot as plt

def create_plot():
    labels = ['Cache Type']
    values = [10, 15, 7]
    std = [1, 2, 3]
    bar_labels = ['No Cache', 'Redis Cache', 'Nginx & Redis Cache']

    # Bar settings
    x = np.arange(len(labels))  # [0]
    width = 0.2  # Width of each bar

    # Create the plot
    fig, ax = plt.subplots()
    ax.bar(x - width, values[0], width, yerr=std[0],label=bar_labels[0])
    ax.bar(x,         values[1], width, yerr=std[1],label=bar_labels[1])
    ax.bar(x + width, values[2], width, yerr=std[2],label=bar_labels[2])

    # Customization
    ax.set_ylabel('Avg Latency')
    ax.set_title('Latency')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    create_plot()