import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import MaxNLocator

def top_points():
        top_p = np.argmax(df['total_points'])
        first = df['first_name'][top_p]
        second = df['second_name'][top_p]
        return f'{first} {second}'

def wrap_labels(labels, max_characters=10):
    return ['\n'.join([label[i:i+max_characters] for i in range(0, len(label), max_characters)]) for label in labels]

plt.style.use("dark_background")

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
response = requests.get(url)

data = json.loads(response.text)
df = pd.DataFrame.from_dict(data['elements'])

### Points Analysis ###
threshold = 85
filtered_df = df[df['total_points'] > threshold]

filtered_names = filtered_df['second_name']
filtered_points = filtered_df['total_points']
filtered_mins = filtered_df['minutes']
filtered_cost = filtered_df['now_cost'] / 10

filtered_VFM = filtered_df['total_points'] / filtered_df['now_cost']
filtered_form_fix_score = filtered_df['form'].astype(float) * 0.7 + filtered_VFM * 0.3

diffrentials = filtered_df[filtered_df['selected_by_percent'].astype(float) < 5 & (filtered_form_fix_score > 4.5)]
diffrential_names = diffrentials['second_name']

print(diffrential_names)

points_per_min = filtered_points / filtered_mins
points_per_game = filtered_df['points_per_game']

wrapped_labels = wrap_labels(filtered_names, max_characters=10)

### xG Analysis ###
xGA = ( ( 2 * filtered_df['goals_scored'] ) + (1 * filtered_df['assists']) ) / (filtered_df['minutes'] /  2)
df['xGA'] = xGA

filtered_df2 = df[df['xGA'] > 0.001]
# filtered_df2 = filtered_df2.sort_values(by='xGA')

filtered_xGA = filtered_df2['xGA']
filtered_names2 = filtered_df2['second_name']

wrapped_labels2 = wrap_labels(filtered_names2, max_characters=10)

### Plotting ###
fig = plt.figure(figsize=[10,9])
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

ax1 = fig.add_subplot(gs[0, 0])  # First row, spanning both columns
ax2 = fig.add_subplot(gs[0, 1])  # Second row, first column
ax3 = fig.add_subplot(gs[1, 0])  # Second row, second column
ax4 = fig.add_subplot(gs[1, 1])  # Second row, second column
ax5 = fig.add_subplot(gs[2, :])  # Third row, spanning both columns

sns.kdeplot(df['total_points'], ax=ax1, fill=True, color='#FFABAB')
ax1.set_xlabel('Total Points')
ax1.set_title('Density Plot of Total Points', color='#FFABAB')

ax2.bar(filtered_names, filtered_points, color='#85E3FF')
ax2.set_xlabel("Player Name")
ax2.set_ylabel("Total Points")
ax2.set_title(f'Total Points of Players Above Threshold ({threshold})', color='#85E3FF')
ax2.text(0.3, 0.9, f'Top = {top_points()}', 
             fontsize=8, 
             ha='center', 
             color='white', 
             bbox=dict(facecolor='none', 
                       edgecolor='white'), 
             transform=ax2.transAxes)
ax2.set_xticks(filtered_names)
ax2.set_xticklabels(wrapped_labels, rotation=90, fontsize=6)

ax3.bar(filtered_names, points_per_min, color='#FF9CEE')
ax3.set_xlabel("Player Name")
ax3.set_ylabel("Points per Minute")
ax3.set_title(f'Points per Minute for Players Above Threshold ({threshold})', color='#FF9CEE')
ax3.set_xticks(filtered_names)
ax3.set_xticklabels(wrapped_labels, rotation=90, fontsize=6)

ax4.bar(filtered_names, points_per_game, color='#FFF5BA')
ax4.set_xlabel("Player Name")
ax4.set_ylabel("Points per Game")
ax4.set_title(f'Points per Game for Players Above Threshold ({threshold})', color='#FFF5BA')
ax4.set_xticks(filtered_names)
ax4.set_xticklabels(wrapped_labels, rotation=90, fontsize=6)
ax4.yaxis.set_major_locator(MaxNLocator(nbins='auto'))
ax4.tick_params(axis='y', which='major', pad=10)  # Optional, increases spacing

# ax4.scatter(filtered_cost, filtered_points, lw=2, color='#FFABAB')
ax4.set_xlabel("Price (millions)")
ax4.set_ylabel("Total Points")

ax5.plot(filtered_names2, filtered_xGA, lw=2, color='#CCFFCC')
ax5.fill_between(filtered_names2, filtered_xGA, color='#CCFFCC', alpha=0.2)
ax5.set_xlabel("Player Name")
ax5.set_ylabel("xGA")
ax5.set_xlim([0, len(filtered_names2)-1])
ax5.set_xticks(filtered_names2)
ax5.set_xticklabels(wrapped_labels2, rotation=90, fontsize=8)

plt.tight_layout()
plt.savefig('Player_analysis/plots/fpl_data.png')
plt.close()
