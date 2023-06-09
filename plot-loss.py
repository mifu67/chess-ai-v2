"""
FILE: plot-loss.py
Author: Michelle Fu
Plot training loss from a csv log.
"""

import pandas as pd
import plotly.express as px

def main():
    data = pd.read_csv("lightning_logs/version_5/metrics.csv")
    fig = px.line(data, x='step', y='loss', title='Training Loss: Deep Model')
    fig.write_image("images/deep-loss.png")
    
if __name__ == "__main__":
    main()