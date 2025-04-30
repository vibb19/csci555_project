import numpy as np
import matplotlib.pyplot as plt

def create_plot():
    labels = ['Cache Type']
    values = [0, 11.3, 54.5, 79.7]
    #std = [62.63, 72.02, 71.72, 49.41]
    bar_labels = ['No Cache', 'Redis 2MB', 'Redis 10MB', 'Nginx & Redis']

    # Bar settings
    x = np.arange(len(labels))  # [0]
    width = 0.2  # Width of each bar

    # Create the plot
    fig, ax = plt.subplots()
    #ax.bar(x - 2*width, values[0], width, yerr=std[0],label=bar_labels[0])
    #ax.bar(x - width,   values[1], width, yerr=std[1],label=bar_labels[1])
    #ax.bar(x,         values[2], width, yerr=std[2],label=bar_labels[1])
    #ax.bar(x + width, values[3], width, yerr=std[3],label=bar_labels[2])
    
    ax.bar(x - 2*width, values[0], width, label=bar_labels[0])
    ax.bar(x - width,   values[1], width, label=bar_labels[1])
    ax.bar(x,         values[2], width, label=bar_labels[2])
    ax.bar(x + width, values[3], width, label=bar_labels[3])
    #ax.bar(x, values, width=0.2)

    # Customization
    ax.set_xlabel('Cache Configuration')
    ax.set_ylabel('Cache Hit Rate (%)')
    ax.set_title('Cache Hit Rate')
    #ax.set_xticks([x - 2*width, x - width, x, x+width])
    #ax.set_xticklabels(bar_labels)
    ax.legend()

    plt.tick_params(axis='x', bottom=False)
    plt.xticks([])
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    create_plot()