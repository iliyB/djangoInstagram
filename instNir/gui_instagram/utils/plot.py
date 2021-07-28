import matplotlib.pyplot as plt



def save_plot(dict: {}, path: str, left: float):
    s = [dict[key] for key in dict.keys()]
    x = range(len(s))
    plt.close()
    ax = plt.gca()
    ax.barh(x, s, align='edge')  # align='edge' - выравнивание по границе, а не по центру
    plt.yticks(x, dict.keys())
    plt.subplots_adjust(left=left)
    plt.savefig(path)


