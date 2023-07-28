import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter

def draw_scatter(props):
    """Props = {
        title : str,
        x : list,
        y : list,
        xlabel : str,
        ylabel : str,
        save_path: str,
        xlim: float,
        ylim: float,
        isLog : boolean,
    }"""

    if (props['isLog']):
        props['y'] = np.log10(props['y'])
        props['x'] = np.log10(props['x'])
        plt.gca().xaxis.set_major_formatter(FuncFormatter(__format_func))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(__format_func))

    plt.rcParams['font.family'] = 'Hiragino Sans'
    plt.scatter(props["x"], props["y"], color="darkorange", s=1)
    plt.xlabel(props["xlabel"])
    plt.ylabel(props["ylabel"])

    if(props['xlim']):
        plt.xlim(0, props['xlim'])
    if(props['ylim']):
        plt.ylim(0, props['ylim'])

    plt.title(props["title"])
    plt.grid(True)
    plt.savefig(props["save_path"])
    plt.show()

def draw_hexbin(props):
    """Props = {
        title : str,
        x : list,
        y : list,
        xlabel : str,
        ylabel : str,
        save_path: str,
        xlim: float,
        ylim: float,
        isLog : boolean,
    }"""

    plt.rcParams['font.family'] = 'Hiragino Sans'

    if (props['isLog']):
        props['y'] = np.log10(props['y'])
        props['x'] = np.log10(props['x'])
        plt.gca().xaxis.set_major_formatter(FuncFormatter(__format_func))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(__format_func)) 

    # hexbinプロット
    plt.hexbin(props['x'], props['y'], gridsize=25, cmap='Wistia')

    # カラーバーを表示
    plt.colorbar(label='Count')

    # グラフを表示
    plt.xlabel(props['xlabel'])
    plt.ylabel(props['ylabel'])

    if(props['xlim']):
        plt.xlim(0, props['xlim'])
    if(props['ylim']):
        plt.ylim(0, props['ylim'])

    plt.title(props["title"])
    plt.grid(True)
    plt.savefig(props["save_path"])
    plt.show()


def draw_lines(props):
    """Props = {
        title : str,
        x : array,
        y1 : array,
        y2 : array,
        xlabel : str,
        ylabel : str,
        save_path: str,
        xlim: float,
        ylim: float,
    }"""

    plt.rcParams['font.family'] = 'Hiragino Sans'

    plt.plot(props["x"], props["y1"], linestyle='-', color='b', label='X')
    plt.plot(props["x"], props["y2"], linestyle='-', color='darkorange', label='Y')

    # グラフのタイトルとラベルを設定
    plt.xlabel(props['xlabel'], fontsize=16)
    plt.ylabel(props['ylabel'], fontsize=16)

    # 凡例を表示
    plt.legend()

    plt.title(props["title"])
    plt.grid(True)

    # グラフを表示
    plt.savefig(props["save_path"])
    plt.show()

def __format_func(value):
    return r'$10^{{{:.0f}}}$'.format(value)

def __formatx_func(value):
    return "{:.2f}".format(10 ** value)
