# %%
import pandas as pd
import streamlit as st
import plotly.express as px 
import altair as alt
import matplotlib.pyplot as plt
import numpy as np

# %%
file_path = "/Users/kevin/Documents/projects/project_4/vehicles_us.csv"

vehicles = pd.read_csv(file_path)

vehicles[['make', 'model']] = vehicles['model'].str.split(n=1, expand=True)

print(vehicles.head(10))

# %%
columns = list(vehicles.columns)

columns.remove('make')

model_index = columns.index('model')

columns.insert(model_index, 'make')

vehicles = vehicles[columns]

print(vehicles.head(10))

# %%
unique_makes_sorted = sorted(vehicles['make'].unique())

print(unique_makes_sorted)


# %%
vehicles_cleaned = vehicles.dropna(subset=['price'])

average_price_per_make = vehicles_cleaned.groupby('make')['price'].mean().reset_index()

average_price_per_make.columns = ['make', 'Average Price']

average_price_per_make = average_price_per_make.sort_values(by='Average Price', ascending=False)

print(average_price_per_make)

# %%
value_counts = vehicles['is_4wd'].value_counts()
print(value_counts)

vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)
print('\n')

value_counts = vehicles['is_4wd'].value_counts()
print(value_counts)

# %%

vehicles_4wd_cleaned = vehicles.dropna(subset=['is_4wd'])

percentage_4wd = vehicles_4wd_cleaned.groupby('make')['is_4wd'].mean().reset_index()

percentage_4wd['Percentage 4WD'] = percentage_4wd['is_4wd'] * 100

percentage_4wd = percentage_4wd[['make', 'Percentage 4WD']]

percentage_4wd = percentage_4wd.sort_values(by='Percentage 4WD', ascending=False)

print(percentage_4wd)
print('\n')

merged_df = pd.merge(average_price_per_make, percentage_4wd, on='make', how='inner')

print(merged_df)

plt.figure(figsize=(10, 6))
plt.scatter(merged_df['Percentage 4WD'], merged_df['Average Price'], alpha=0.7)

plt.xlabel('Percentage of 4WD Vehicles (%)')
plt.ylabel('Average Price ($)')
plt.title('Correlation Between 4WD Percentage and Average Price')
plt.grid(True)

plt.show()


unique_makes = merged_df['make'].unique()

colors = plt.cm.tab20(np.linspace(0, 1, len(unique_makes)))

color_map = dict(zip(unique_makes, colors))

plt.figure(figsize=(10, 6))
for make in unique_makes:
    make_data = merged_df[merged_df['make'] == make]
    plt.scatter(
        make_data['Percentage 4WD'], 
        make_data['Average Price'], 
        color=color_map[make],
        label=make,
        alpha=0.8
    )

plt.xlabel('Percentage of 4WD Vehicles (%)')
plt.ylabel('Average Price ($)')
plt.title('Correlation Between 4WD and Average Price')
plt.legend(title='Make', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside the plot
plt.grid(True)

plt.show()


# %%
fig = px.scatter(
    merged_df, 
    x='Percentage 4WD', 
    y='Average Price', 
    color='make',  
    hover_data=['make'], 
    title='Correlation Between 4WD Percentage and Average Price',
    labels={'Percentage 4WD': 'Percentage of 4WD Vehicles (%)', 'Average Price': 'Average Price ($)'}
)

st.plotly_chart(fig)

# %%
st.header("Car Price Distribution")

fig = px.histogram(
    merged_df, 
    x="Average Price", 
    nbins=16, 
    title="Distribution of Average Car Prices", 
    labels={"Average Price": "Car Price ($)"}
)

st.plotly_chart(fig)


