import pandas as pd
import eurostat
import streamlit as st
import numpy as np

@st.cache_data(ttl=3600)
def milk_production_data_monthly():
    df = eurostat.get_data_df('apro_mk_colm')
    df = df[(df['milkitem'] == 'PRD') & (df['dairyprod'] == 'D1110D')]
    df.drop(['freq', 'milkitem', 'dairyprod', 'unit'], axis=1, inplace=True)
    df.rename(columns={'geo\TIME_PERIOD': 'geo'}, inplace=True)
    df = df.melt(id_vars='geo', var_name='date', value_name='value')
    df = df.pivot(index='date', columns='geo', values='value').reset_index()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    df.sort_values(by='date', ascending=False, inplace = True)
    df_division = df.set_index('date')
    df_division =df_division /df_division.shift(-1)
    df_division = df_division.reset_index()
    return df, df_division

def get_quantilles(df,column_to_drop, low, high):
    values = df.drop(columns=column_to_drop).stack().dropna().values
    vmin = np.percentile(values, low)
    vmax = np.percentile(values, high)
    return vmin, vmax

df, df_division = milk_production_data_monthly()

vmin_division, vmax_division = get_quantilles(df_division, 'date', 5, 95)
print((vmin_division, vmax_division))
styled_df_division = df_division.style.background_gradient(
    cmap='coolwarm',
    axis=None,
    vmin=vmin_division,
    vmax=vmax_division
)

st.title("Monthly milk production change")
st.dataframe(styled_df_division, use_container_width=True)

vmin_production, vmax_production = get_quantilles(df, 'date', 5, 95)
print((vmin_division, vmax_division))
styled_df_production = df.style.background_gradient(
    cmap='coolwarm',
    axis=None,
    vmin=vmin_production,
    vmax=vmax_production
)

st.title("Monthly milk production")
st.dataframe(styled_df_production, use_container_width=True)