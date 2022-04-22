import pandas as pd
import numpy as np
import streamlit as st
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder 
from os.path import exists

SITES = [
    # intervention_sites
    'Scarlet Mendez (San Antonio)', 
    'Gillian Peraza (Miami)',
    'Noel Leon (SF)',
    'Svetlana Santos (Boston)',

    # control_sites
    'Martin Palacio (Fort Worth)',
    'Tatiana Colunga (Irvine)',
    # 'Enzo Paredes (Houston)',
    # 'Abigail Rodriguez (New York)',
]

def app(mons):

    site = st.radio("Choose a site", SITES)
    # st.markdown("""---""")

    # configures last row to use custom styles based on cell's value, injecting JsCode on components front end
    sytle_venues = JsCode("""
    function(params) {
        if (params.value < 10) {
            return {
                'color': 'black',
                'backgroundColor': '#7fff00'
            }
        } else {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        }
    };
    """)

    style_pct_ontime = JsCode("""
    function(params) {
        if (params.value >= 90) {
            return {
                'color': 'black',
                'backgroundColor': '#008000'
            }
        } else if (params.value >= 50) {
            return {
                'color': 'black',
                'backgroundColor': '#3cb371'
            }    
        } else {
            return {
                'color': 'black',
                'backgroundColor': '#7fff00'
            }
        }
    };
    """)

    # read data tables
    dfs_referred = []
    dfs_weekly = []
    dfs_present = []
    for mon in mons:
        dir_path = 'data/' + mon + '/' + site + '/'
        dfs_referred.append(pd.read_csv(dir_path +'referred-to-ahead.csv'))
        df_weekly = pd.read_csv(dir_path +'weekly.csv')
        if df_weekly['On-Time Reporting %'].dtype == 'O':
            df_weekly['On-Time Reporting %'] = \
                df_weekly['On-Time Reporting %'].str.rstrip('%').astype(float)
        dfs_weekly.append(df_weekly)
        fpath_presentation = dir_path +'presentation.csv'
        if exists(fpath_presentation):
            df_present = pd.read_csv(fpath_presentation)
        else: 
            df_present = None
        dfs_present.append(df_present)

    # --- config --- # 

    gb_referred = GridOptionsBuilder.from_dataframe(dfs_referred[0])
    gb_referred.configure_grid_options(domLayout='normal')
    go_referred = gb_referred.build()

    gb_weekly = GridOptionsBuilder.from_dataframe(dfs_weekly[0])
    gb_weekly.configure_grid_options(domLayout='normal')
    gb_weekly.configure_column("Venues", cellStyle=sytle_venues)
    gb_weekly.configure_column('On-Time Reporting %', cellStyle=style_pct_ontime)
    go_weekly = gb_weekly.build()

    if dfs_present[0] is not None:
        gb_present = GridOptionsBuilder.from_dataframe(dfs_present[0])
        gb_present.configure_grid_options(domLayout='normal')
        gb_present.configure_column("Latino Attendees", cellStyle=sytle_venues)
        go_present = gb_present.build()

    for i in range(len(mons)):
        mon = mons[i]
        st.subheader('2022 ' + mon)

        c1, c2 = st.columns(2)
        with c1:
            st.text(site)
            grid_res1 = AgGrid(
                dfs_referred[i],
                key = np.random.uniform(0), # crucial, otherwise duplicated key error
                gridOptions=go_referred,
                height=150, 
                allow_unsafe_jscode=True, # True to allow jsfunction to be injected
            )
            # st.table(grid_res1['data'])
        with c2:
            st.text(site)
            grid_res2 = AgGrid(
                dfs_weekly[i],
                key = np.random.uniform(0), # crucial, otherwise duplicated key error
                gridOptions=go_weekly,
                height=150, 
                allow_unsafe_jscode=True, # True to allow jsfunction to be injected
            )
            # st.table(grid_res2['data'])

        if dfs_present[i] is None:
            pass
        else:
            st.text(site)
            grid_res3 = AgGrid(
                dfs_present[i],
                key = np.random.uniform(0), # crucial, otherwise duplicated key error
                gridOptions=go_present,
                height=150, 
                allow_unsafe_jscode=True, # True to allow jsfunction to be injected
            )
        