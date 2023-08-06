
def corr_matrix(df,  figsize = (10,8)):
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    n_colors = 9
    cMap = plt.cm.get_cmap("bwr",lut=n_colors ) 

    # definir el heatmap
    plt.figure( figsize=figsize)
    h_map = sns.heatmap(df.corr().values, 
                        vmin=-1., vmax=1., 
                        cmap=cMap, 
                        annot=True, 
                        xticklabels=list(df.columns[ : -1]),
                        yticklabels=list(df.columns[ : -1]))
    plt.xticks(rotation=90) 
    
    # poner ticks en la barra de colores
    cbar = h_map.collections[0].colorbar
    l_ticks = [k/10. for k in range(-8, 9, 2)]
    cbar.set_ticks(l_ticks)
    
    # arreglar cosillas
    bottom, top = h_map.get_ylim()
    h_map.set_ylim(bottom + 0.5, top - 0.5)
    
    # generar el dibujo
    plt.show()


def plot_boxplots(data, norm = True, figsize=(16, 7)):
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    
    if norm == True:
        df = (data - data.mean()) / data.std()
    else:
        df = data

    plt.figure( figsize=figsize)
    plt.title("Boxplots")
    sns.set_style("white")
    bx_plot = sns.boxplot(data=df)
    plt.xticks(rotation=90)
    plt.xlabel("variables")
    plt.ylabel("normalized values")
    plt.show()
