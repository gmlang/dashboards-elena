import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder #, GridUpdateMode, 
import altair as alt

df_weekly = pd.read_csv('weekly.csv')
df_monthly = pd.read_csv('monthly.csv')

st.set_page_config(page_title='Consorcio Activities',  layout='wide', page_icon=':hospital:')

# # sidebar
# st.sidebar.subheader("Consorcio Activities Summary")

# # numeric input box
# sample_size = st.sidebar.number_input("rows", min_value=10, value=30)
# grid_height = st.sidebar.number_input("Grid height", min_value=200, max_value=800, value=300)

# Infer basic colDefs from dataframe types
gb_weekly = GridOptionsBuilder.from_dataframe(df_weekly)
gb_monthly = GridOptionsBuilder.from_dataframe(df_monthly)

# # customize gridOptions
# gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
# gb.configure_column("date_tz_aware", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)
# gb.configure_column("apple", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2, aggFunc='sum')
# gb.configure_column("banana", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
# gb.configure_column("chocolate", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='max')

# configures last row to use custom styles based on cell's value, injecting JsCode on components front end
cellsytle_jscode = JsCode("""
function(params) {
    if (params.value < 2) {
        return {
            'color': 'white',
            'backgroundColor': 'darkred'
        }
    } else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
};
""")
gb_monthly.configure_column("flyers_distributed", cellStyle=cellsytle_jscode)
gb_monthly.configure_grid_options(domLayout='normal')
gridOptions_monthly = gb_monthly.build()

# gb_weekly.configure_pagination(paginationAutoPageSize=True)
gb_weekly.configure_grid_options(domLayout='normal')
gridOptions_weekly = gb_weekly.build()

# Display the grid
st.header("Consorcio Activities Summary")
st.markdown("""
    
""")

st.subheader("Weekly Data")
grid_response = AgGrid(
    df_weekly, 
    gridOptions=gridOptions_weekly,
    height=500, 
    # width='100%',
    allow_unsafe_jscode=True, # True to allow jsfunction to be injected
    )

st.subheader("Monthly Data")
grid_response = AgGrid(
    df_monthly, 
    gridOptions=gridOptions_monthly,
    # height=500, 
    # width='100%',
    allow_unsafe_jscode=True, # True to allow jsfunction to be injected
    )

# bar chart
with st.spinner("Displaying results..."):
    
    chart_data = df_monthly.loc[:,['site','month', 'month_end_date', 'flyers_distributed']]

    # stacked bar chart
    chart = alt.Chart(data=chart_data).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        y="month",
        x='flyers_distributed:Q', 
        color = "site:N", 
    )

    # display stacked bar chart
    st.header("Number of Flyers Distributed for Presentation")
    st.markdown("""
    """)
    st.altair_chart(chart, use_container_width=True)


# refs
# https://github.com/PablocFonseca/streamlit-aggrid/blob/main/examples/main_example.py
# https://streamlit.io/components
# https://altair-viz.github.io/gallery/multiline_tooltip.html