import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def cr_casual_register_df(df):
    casual_yr_df = df.groupby("yr")["casual"].sum().reset_index()
    casual_yr_df.columns = ["yr", "total_casual"]
    register_yr_df = df.groupby("yr")["registered"].sum().reset_index()
    register_yr_df.columns =["yr", "total_registered"]
    casual_register_df = casual_yr_df.merge(register_yr_df, on="yr")
    return casual_register_df
def cr_season_df(df):
    season_df = df.groupby(by=['season', 'weekday']).agg({
        "cnt":"sum"
    }).reset_index()
    return season_df
def cr_season_fall_df(df):
    season_fall_df = df[df["season"]== "Fall"].groupby(by=["workingday", "yr"]).agg({
        "windspeed":"sum",
        "cnt":"sum"
    }).reset_index()
    return season_fall_df

main_df = pd.read_csv("main_data.csv")

#Filter Data
main_df["dteday"] = pd.to_datetime(main_df["dteday"])
min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label = "Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#Penyewaan sepeda berdasarkan musim dan hari
st.subheader("Total Penyewaan Sepeda Berdasarkan Musim")
fig, axe= plt.subplots(figsize=(12, 9))
sns.barplot(data=cr_season_df(main_df), x="season", y="cnt", hue="weekday", palette="rocket")
plt.ylabel("Jumlah")
plt.title("Jumlah penyewaan sepeda berdasarkan musim")
plt.legend(title="Weekday", loc="upper right")
for container in axe.containers:
    
    axe.bar_label(container, fontsize=8, color='black', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)

#Penyewaan sepeda berdasarkan tahun pada musim gugur (pengaruh angin terhadap penyewaan sepeda)
st.subheader("Total Penyewaan Sepeda Berdasarkan Tahun Untuk Musim Gugur dengan parameter Workday dan Windspeed")
fig, axe= plt.subplots(figsize=(12, 9))
sns.barplot(data=cr_season_fall_df(main_df), x="workingday", y="windspeed", hue="yr", palette="rocket")
plt.ylabel("Wind Speed")
plt.title("Jumlah penyewaan sepeda berdasarkan tahun untuk musim gugur")
plt.legend(title="Year", loc="upper right")
for container in axe.containers:
    
    axe.bar_label(container, fontsize=8, color='black', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)

