import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Mengatur gaya tampilan seaborn
sns.set(style='whitegrid')

# Fungsi bantu untuk menghasilkan berbagai dataframe
def generate_casual_register_df(dataframe):
    casual_year_df = dataframe.groupby("yr")["casual"].sum().reset_index()
    casual_year_df.columns = ["yr", "total_casual"]
    
    registered_year_df = dataframe.groupby("yr")["registered"].sum().reset_index()
    registered_year_df.columns =["yr", "total_registered"]
    
    casual_register_df = casual_year_df.merge(registered_year_df, on="yr")
    return casual_register_df

def generate_season_df(dataframe):
    season_df = dataframe.groupby(by=['season', 'weekday']).agg({
        "cnt":"sum"
    }).reset_index()
    return season_df

def generate_fall_season_df(dataframe):
    fall_season_df = dataframe[dataframe["season"]== "Fall"].groupby(by=["workingday", "yr"]).agg({
        "windspeed":"sum",
        "cnt":"sum"
    }).reset_index()
    return fall_season_df

main_dataframe = pd.read_csv("main_data.csv")


# Analisis Peminjaman Sepeda berdasarkan Musim dan Hari
st.subheader("Total Peminjaman Sepeda berdasarkan Musim")
figure, axes = plt.subplots(figsize=(12, 9))
sns.barplot(data=generate_season_df(main_dataframe), x="season", y="cnt", hue="weekday", palette="muted")
plt.ylabel("Total")
plt.title("Total Peminjaman Sepeda berdasarkan Musim")
plt.legend(title="Hari", loc="upper right")
for container in axes.containers:
    axes.bar_label(container, fontsize=8, color='black', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(figure)

# Analisis Peminjaman Sepeda berdasarkan Tahun pada Musim Gugur (Pengaruh Kecepatan Angin terhadap Peminjaman Sepeda)
st.subheader("Total Peminjaman Sepeda berdasarkan Tahun untuk Musim Gugur dengan parameter Hari Kerja dan Kecepatan Angin")
figure, axes = plt.subplots(figsize=(12, 9))
sns.barplot(data=generate_fall_season_df(main_dataframe), x="workingday", y="windspeed", hue="yr", palette="muted")
plt.ylabel("Kecepatan Angin")
plt.title("Total Peminjaman Sepeda berdasarkan Tahun untuk Musim Gugur")
plt.legend(title="Tahun", loc="upper right")
for container in axes.containers:
    axes.bar_label(container, fontsize=8, color='black', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(figure)
