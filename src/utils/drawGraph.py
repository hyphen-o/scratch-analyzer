import matplotlib.pyplot as plt

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