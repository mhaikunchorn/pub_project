## horizontal bar chart
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('every_pub_in_london.csv')
print(df)
#colours
# laColours = ['#034694','#001C58','#5CBFEB','#D00027',
#               '#EF0107','#DA020E','#274488','#ED1A3B',
#                '#000000','#091453','#60223B','#0053A0',
#                '#E03A3E','#1B458F','#000000','#53162f',
#                '#FBEE23','#EF6610','#C92520','#BA1F1A']
primaryColours = ['#e84e1b']
#plot
plt.barh(y=df['Local Authority'], width=df['Number of Pubs'], color=primaryColours)
#title and labels
plt.title('Number of Pubs in London')
plt.xlabel('Number of Pubs')
plt.ylabel('London Boroughs')
plt.savefig('bar_chart1.png')
plt.show()

##pie chart
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('every_pub_in_london.csv')
print(df.head(7))
# plt.figure(figsize=(5,5))
local_authority = df['Local Authority'].head(7)
num_of_pubs = df['Number of Pubs'].head(7)
colours = ['#e84e1b', '#2f3e58', '#ffdd00', '#ebe3dd', '#a9d9d9', '#5b2b3e', '#e7326d']
plt.pie(num_of_pubs,labels=local_authority, colors=colours)
plt.axis('equal')
plt.title('Seven Boroughs with the highest number of pubs')
plt.savefig('pie_chart1.png')
plt.show()


#--hOrizontal bars with mean
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('every_pub_in_london.csv')
# print(df)
#plot
plt.barh(y=df['Local Authority'], width=df['Number of Pubs'], color='#2f3e58')
#title and labels
plt.title('Number of Pubs in London')
plt.ylabel('London Boroughs')
plt.xlabel('Number of Pubs')
plt.axvline(df['Number of Pubs'].mean(), color='#e84e1b', linewidth=2, linestyle='--')
plt.savefig('bar_chart2.png')
plt.show()