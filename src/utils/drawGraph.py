import matplotlib.pyplot as plt
import matplotlib.font_manager

plt.rcParams['font.family'] = 'Hiragino Sans'

# props = {
#     title : string,
#     x : array,
#     y : array,
#     xlabel : string,
#     ylabel : string,
#     save_path: string,
# }

def drawScatter(props):
    plt.scatter(props["x"], props["y"], color="darkorange")
    plt.xlabel(props["xlabel"])
    plt.ylabel(props["ylabel"])
    plt.title(props["title"])
    plt.grid(True)
    plt.savefig(props["save_path"])
    plt.show()