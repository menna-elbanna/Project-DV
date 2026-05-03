# =========================
# Interactive Stacked Column
# =========================
import pandas as pd
import plotly.express as px
df = pd.read_csv('clean_players.csv')

df = df[['club_name', 'player_positions']].dropna()
df['main_position'] = df['player_positions'].apply(lambda x: x.split(',')[0])

grouped = df.groupby(['club_name', 'main_position']).size().reset_index(name='count')

top_clubs = df['club_name'].value_counts().head(10).index
grouped = grouped[grouped['club_name'].isin(top_clubs)]

fig = px.bar(
    grouped,
    x='club_name',
    y='count',
    color='main_position',
    title='Number of Players per Club by Position'
)

fig.show()

# =========================
# Interactive Cluster Column
# =========================
import pandas as pd
import plotly.express as px

df = pd.read_csv('clean_players.csv')

df = df[['overall', 'player_positions']].dropna()
df['main_position'] = df['player_positions'].apply(lambda x: x.split(',')[0])

bins = [40, 60, 70, 80, 90, 100]
labels = ['40-60', '60-70', '70-80', '80-90', '90+']

df['rating_group'] = pd.cut(df['overall'], bins=bins, labels=labels, right=False)

grouped = df.groupby(['main_position', 'rating_group']).size().reset_index(name='count')

fig = px.bar(
    grouped,
    x='main_position',
    y='count',
    color='rating_group',
    barmode='group', 
    title='Players by Rating and Position'
)

fig.show()