# =========================
# Stacked Column
# =========================
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('clean_players.csv')

df = df[['club_name', 'player_positions']].dropna()

df['main_position'] = df['player_positions'].apply(lambda x: x.split(',')[0])

grouped = df.groupby(['club_name', 'main_position']).size().reset_index(name='count')

top_clubs = df['club_name'].value_counts().head(10).index
grouped = grouped[grouped['club_name'].isin(top_clubs)]

pivot = grouped.pivot(index='club_name', columns='main_position', values='count').fillna(0)

pivot.plot(
    kind='bar',
    stacked=True,
    figsize=(12, 7)
)

plt.title('Number of Players per Club by Position')
plt.xlabel('Club')
plt.ylabel('Number of Players')

plt.legend(title='Position', bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig('stacked_chart.png')

plt.show()

# =========================
# Stacked Bar
# =========================
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('clean_players.csv')

df = df[['club_name', 'nationality_name']].dropna()

top_clubs = df['club_name'].value_counts().head(10).index
df = df[df['club_name'].isin(top_clubs)]

top_nationalities = df['nationality_name'].value_counts().head(8).index
df['nationality_name'] = df['nationality_name'].apply(
    lambda x: x if x in top_nationalities else 'Other'
)

grouped = df.groupby(['club_name', 'nationality_name']).size().reset_index(name='count')

pivot = grouped.pivot(index='club_name', columns='nationality_name', values='count').fillna(0)

pivot.plot(
    kind='barh',
    stacked=True,
    figsize=(12, 7)
)

plt.title('Nationality Distribution per Club')
plt.xlabel('Club')
plt.ylabel('Number of Players')

plt.legend(title='Nationality', bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('nationality_stacked.png')
plt.show()

# =========================
# Cluster Column
# =========================
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('clean_players.csv')

df = df[['overall', 'player_positions']].dropna()

df['main_position'] = df['player_positions'].apply(lambda x: x.split(',')[0])

bins = [40, 60, 70, 80, 90, 100]
labels = ['40-60', '60-70', '70-80', '80-90', '90+']

df['rating_group'] = pd.cut(df['overall'], bins=bins, labels=labels, right=False)

grouped = df.groupby(['main_position', 'rating_group']).size().reset_index(name='count')

pivot = grouped.pivot(index='main_position', columns='rating_group', values='count').fillna(0)

pivot.plot(
    kind='bar',  
    figsize=(12, 7)
)

plt.title('Players Distribution by Rating and Position')
plt.xlabel('Position')
plt.ylabel('Number of Players')

plt.legend(title='Rating Range')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('Rating and Position_clustered.png')
plt.show()

