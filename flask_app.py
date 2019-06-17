from flask import Flask, render_template
from graph import build_graph
from graph import build_bargraph
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
from math import pi
 
app = Flask(__name__)
 
@app.route('/graphs')
def graphs():
    #These coordinates could be stored in DB
    x1 = [0, 1, 2, 3, 4]
    y1 = [10, 30, 40, 15, 50]
    x2 = [0, 1, 2, 3, 4]
    y2 = [50, 30, 20, 10, 50]
    x3 = [0, 1, 2, 3, 4]
    y3 = [0, 30, 10, 5, 30]
    x4 = [0, 1, 2, 3, 4]
    y4 = [0, 1, 2, 3, 4]
 
    graph1_url = build_graph(x1,y1);
    graph2_url = build_graph(x2,y2);
    graph3_url = build_graph(x3,y3);
    graph4_url = build_graph(x4,y4);
 
    #return render_template('graphs.html',
    #graph1=graph1_url,
    #graph2=graph2_url,
    #graph3=graph3_url,
    #graph4=graph4_url)
    
    df = pd.DataFrame({
    'group': ['A','B','C','D'],
    'var1': [38, 1.5, 30, 4],
    'var2': [29, 10, 9, 34],
    'var3': [8, 39, 23, 24],
    'var4': [7, 31, 33, 14],
    'var5': [28, 15, 32, 14]
    })
	# number of variable
    categories=list(df)[1:]
    N = len(categories)
 
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    values
 
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
 
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
 
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)
 
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7 )
    plt.ylim(0,40)
 
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')
 
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    
    #graph_url = base64.b64encode(img.getvalue()).decode()
    plot_url = base64.b64encode(img.getValue()).decode()
    #return 'data:image/png;base64,{}'.format(graph_url)
    return render_template('graphs.html', plot_url=plot_url)
	
if __name__ == '__main__':
    app.debug = True
    app.run()