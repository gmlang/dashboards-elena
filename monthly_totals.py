import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder

def app(mons):
    
    # read data tables
    monthly_dfs = [pd.read_csv('data/' + mon + '/monthly.csv') for mon in mons]

    # --- config --- #

    gb_monthly = GridOptionsBuilder.from_dataframe(monthly_dfs[0])

    # use custom styles based on cell's value
    cellsytle_jscode = JsCode("""
    function(params) {
        if (params.value < 2) {
            return {
                'color': 'white',
                'backgroundColor': 'green'
            }
        } else {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        }
    };
    """)
    # apply this jscode to the field Presentations
    gb_monthly.configure_column("Presentations", cellStyle=cellsytle_jscode)
    gb_monthly.configure_grid_options(domLayout='normal')
    gridOptions_monthly = gb_monthly.build()

    # set subheader
    st.subheader('2022')

    # use 2 columns, putting two tables side by side
    c1, c2 = st.columns(2)
    with c1:
        st.text(mons[0])
        grid_res1 = AgGrid(
            monthly_dfs[0],
            gridOptions=gridOptions_monthly,
            height=210, 
            allow_unsafe_jscode=True, # True to allow jsfunction to be injected
        )
        # st.table(grid_res1['data'])

    with c2:
        st.text(mons[1])
        grid_res2 = AgGrid(
            monthly_dfs[1],
            gridOptions=gridOptions_monthly,
            height=210, 
            allow_unsafe_jscode=True, # True to allow jsfunction to be injected
        )
        # st.table(grid_res2['data'])    

