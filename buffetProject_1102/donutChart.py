import matplotlib.pyplot as plt

# Data
labels = 'A', 'B', 'C', 'D'
sizes = [15, 30, 45, 10]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.05, 0.05, 0.05, 0.05)  # To create a gap and make it a donut

# Create a pie chart
_, texts, _ = plt.pie(sizes, 
                      explode=explode, 
                      labels=labels, 
                      colors=colors, 
                      autopct='%1.1f%%', 
                      pctdistance=0.7, 
                      radius=1.5, 
                      textprops={'color':'w','weight':'bold','size':10}, )

for text in texts:
    text.set_visible(False)

# Draw a circle in the center to make it a donut chart
circle = plt.Circle((0, 0), 0.70, fc='#eaeaea')
plt.gca().add_artist(circle)

# Add Legends
plt.legend(labels, loc="center right")

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# # Add a title
# plt.title('Donut Chart Example')

# Save the chart as an image (e.g., PNG)
plt.savefig('./static/image/donut_chart.png', bbox_inches='tight', transparent=True)

# Display the chart
plt.show()
