import datetime
import streamlit as st
import pandas as pd 
import requests
import json 

print('[START OF SCRIPT]')

def get_trip_plan(trip_data):
    url = 'http://127.0.0.1:8000/get_trip_plan/'
    x = requests.post(url, json = trip_data)    
    return json.loads(x.text)

def init_app():
    
    with open('countries.txt', 'r') as f:
        countries = f.readlines()
    
    st.title("Streamlit Trip Planner")

    if "countries" not in st.session_state:
        st.session_state.countries = countries
      
def main():
    # where to go dropdown list of cities
    destination = st.selectbox("Where do you want to travel ?",
                               options=st.session_state.countries,
                               index=None,
                               placeholder="You will head to ...")
    
    # select dates
    trip_date = st.date_input("Travel Date.",
                              value = (datetime.datetime.now(), datetime.datetime.now()))

    # select activity
    activity = st.multiselect("Choose Activities.",
        ["Sightseeing", "Outdoor Adventures", "Cultural Experiences", "Relaxation",
        "Shopping", "Photography", "Unique Experiences", "Museums", "Entertainment",
        "Religious", "Food"])
    
    # type of persons
    n_person = st.radio("Choose Status.",
        ["Single", "Couple", "Family", "Friends"],
        horizontal=True)
    
    # budget
    budget = st.radio("Choose Budget.",
        ["Low", "Medium", "High"],
        horizontal=True)
            
    # submit button
    if st.button("Plan Trip", type="primary"):
        with st.spinner('Wait for it...'):
            out = get_trip_plan(
                    {
                        "destination": destination.strip(),
                        "start_date": trip_date[0].strftime('%b-%d-%Y'),
                        "end_date": trip_date[1].strftime('%b-%d-%Y'),
                        "activities": activity,
                        "person_status": n_person,
                        "budget": budget
                    })
        print(out["response"])
        print(f'Plan: {out["response"]}')
        st.text(f'Plan: {out["response"]}')        
        st.text(f'Execution Time: {out["execute_time"]}')
        
        # st.table(st.session_state.result_df)
        
        
        
        
if __name__ == "__main__":
    print(f'[INFO] Starting App...')
    init_app()
    main()