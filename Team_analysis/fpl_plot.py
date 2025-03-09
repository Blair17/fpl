import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from datetime import datetime
from fpl_data_scrape import *

plt.style.use("dark_background")

date = datetime.now().strftime("%d-%m-%Y")
GW = lastGameweek

gameweek = np.arange(1, lastGameweek+1)

fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(11.69, 8.27)) #fig size A4 in inches figsize=(11.69,8.27)
fig.suptitle("Team performance : " + teamName)
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.4)

### Team points
ax1.plot(gameweek, points, label='Team FPL points')
ax1.plot(gameweek, averagePoints, label='Average FPL points')
ax1.plot(gameweek, highestPoints, label='Highest FPL points')
ax1.set_xlabel('Gameweek')
ax1.set_ylabel('FPL points')
ax1.legend(loc='best', frameon=True, prop={'size':6})

### Team rank
gameweekRank = np.array(gameweekRank)
ax2.bar(gameweek, gameweekRank, label='GW Rank', width=0.5)
ax2.plot(gameweek, overallRank, label='Overall rank')
ax2.set_ylim(ymin=0)
ax2.set_ylim(ymax=max(gameweekRank + 400000))
ax2.get_yaxis().get_major_formatter().set_scientific(False)
ax2.set_xlabel('Gameweek')
ax2.set_ylabel('Rank')
ax2.legend(loc='best', frameon=True, prop={'size':6})
rects = ax2.patches
for rect in rects:
    height = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width() / 2, height + 100000, height, ha='center', va='bottom', size=6)

### Team value
ax3.bar(gameweek, list(map(lambda x: x/10, teamValue)), width=0.5)
ax3.set_ylim(ymin=min(list(map(lambda x: x/10, teamValue)))-0.5)
ax3.set_ylim(ymax=max(list(map(lambda x: x/10, teamValue)))+0.5)
ax3.set_xlabel('Gameweek')
ax3.set_ylabel('Team Value (incl. bank)')
rects = ax3.patches
labels = [sum(x) for x in zip(list(map(lambda x: round(x/10, 1), teamValue)))]
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax3.text(rect.get_x() + rect.get_width() / 2, height + 0.1, label, ha='center', va='bottom', size=6)

### Team transfers
ax44 = ax4.twinx()
ax4.bar(gameweek, transfers, label='Number of transfers', width=0.5)
ax44.plot(gameweek, transfersCost, label='Transfers cost')
ax4.set_xlabel('Gameweek')
ax4.set_ylabel('Number of transfers')
ax44.set_ylabel('Transfers cost')
ax4.legend(loc=2, frameon=True, prop={'size':6})
ax44.legend(loc=1, frameon=True, prop={'size':6})
ax44.set_ylim(ymin=0)
ax44.set_ylim(ymax=max(transfersCost)+1)
ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax44.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

### Captain points
captainPoints = np.array(captainPoints)
captainDisplay = []
for n in range(0, lastGameweek):
    captainDisplay.append(str(n+1) + " - " + captain[n])
mask1 = captainPoints > 3
mask2 = captainPoints <= 3
ax5.bar(gameweek[mask1], list(map(lambda x: x*2, captainPoints[mask1])), width=0.5)
ax5.bar(gameweek[mask2], list(map(lambda x: x*2, captainPoints[mask2])), width=0.5)
ax5.set_ylim(ymin=0)
ax5.set_ylim(ymax=max(list(map(lambda x: x*2, captainPoints)))+5)
ax5.set_xticks(gameweek)
ax5.set_xticklabels(captainDisplay, rotation=45, ha="right", size=6)
ax5.set_ylabel('Captain FPL points')
rects = ax5.patches
for rect in rects:
    height = rect.get_height()
    ax5.text(rect.get_x() + rect.get_width() / 2, height + 0.6, height, ha='center', va='bottom', size=6)

### Points per position
positions = list(totalPointsPerLineSeason.keys())
pointsPos = list(totalPointsPerLineSeason.values())
colors = ['#f1d18a', '#73b1c1', '#588d9c', '#36626a']

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} pts)".format(pct, absolute)

wedges, texts, autotexts = ax6.pie(pointsPos, autopct=lambda pct: func(pct, pointsPos),
                                   textprops=dict(color="k"), colors=colors)

ax6.legend(wedges, positions,
           title="Positions",
           loc="center left",
           bbox_to_anchor=(0.92, 0, 0.5, 1))

ax6.set_xlabel("Points per position over the season")

now = datetime.now()
plt.savefig(f'Team_analysis/plots/{date}_GW{GW}.png')