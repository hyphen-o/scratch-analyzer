import matplotlib.pyplot as plt

def drawScatter(props):
    """Props = {
        title : str,
        x : list,
        y : list,
        xlabel : str,
        ylabel : str,
        save_path: str,
    }"""
    plt.rcParams['font.family'] = 'Hiragino Sans'
    plt.scatter(props["x"], props["y"], color="darkorange")
    plt.xlabel(props["xlabel"])
    plt.ylabel(props["ylabel"])
    plt.title(props["title"])
    plt.grid(True)
    plt.savefig(props["save_path"])
    plt.show()

drawScatter()