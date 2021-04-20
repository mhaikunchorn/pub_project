## bar chart
import pandas as pd
import plotly.express as pt
df = pd.read_csv('every_pub_in_london.csv')
print(df)
# colours = ['#e84e1b', '#2f3e58', '#ffdd00', '#ebe3dd', '#a9d9d9', '#5b2b3e', '#e7326d']
fig = pt.bar(df, x='Local Authority', y='Number of Pubs', title='Number of Pubs in London')
fig.show()