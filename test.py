import streamlit as st 
from supabase import create_client

# setup connection
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# test connection
data = supabase.table("workouts").select("*").execute()

st.write("Results from Supabase:", data)