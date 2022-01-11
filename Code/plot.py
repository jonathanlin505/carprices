import seaborn as sns
import numpy as np

def plotData(data):
    ax = sns.kdeplot(data)
    ax.set_title("Price Density of Cars")
    ax.set_xlabel("Selling Price ($)")
    if data.shape[0] > 1:
        kdeline = ax.lines[0]
        mean = data.mean()
        sdev = data.std()
        left = mean - sdev
        right = mean + sdev
        xs = kdeline.get_xdata()
        ys = kdeline.get_ydata()
        height = np.interp(mean, xs, ys)
        ax.vlines(mean, 0, height, color="tab:blue", ls=':')
        ax.fill_between(xs, 0, ys, facecolor="tab:blue", alpha=0.2)
        ax.fill_between(xs, 0, ys, where=(left <= xs) & (xs <= right), facecolor="tab:blue", alpha=0.2)
    return