import monthly_totals
import monthly_details
import streamlit as st

mons = ['Mar', 'Apr'] # <--- input

PAGES = {
    "Monthly Totals": monthly_totals,
    "Monthly Details": monthly_details,
}

# set_page_config() can only be called once per app, and must be called as the 
# first Streamlit command in your script.
st.set_page_config(page_title='Consorcio Activities',  
    layout='wide', page_icon=':hospital:')

# set header
st.header("Consorcio Activities Summary")

# st.sidebar.title('Navigation')
# selection = st.sidebar.radio("Go to", list(PAGES.keys()))

selection = st.radio("Go to", list(PAGES.keys()))
# st.markdown("""---""")
page = PAGES[selection]
page.app(mons)

# refs
# https://share.streamlit.io/pablocfonseca/streamlit-aggrid/main/examples/example.py?example=Two%20grids%20in%20page
# https://github.com/PablocFonseca/streamlit-aggrid/blob/main/examples/main_example.py
# https://streamlit.io/components
# https://html-color.codes/green