import pandas as pd 

from prompts import TRIP_PLANNER_PROMPT_TEMPLATE_MISTRAL_MODEL, TRIP_PLANNER_PROMPT_TEMPLATE
from time import perf_counter

from langchain_community.llms import GPT4All
from langchain_core.prompts import PromptTemplate


# MODEL_PATH = r'D:\Programs\GPT4ALL DOWNLOAD\mistral-7b-instruct-v0.2.Q4_K_M.gguf'
MODEL_PATH = r'D:\Programs\GPT4ALL DOWNLOAD\qwen2-1_5b-instruct-q4_0.gguf'

t1 = perf_counter()
model = GPT4All(model=MODEL_PATH, 
                device='kompute', 
                verbose=True) # cuda - kompute - nvidia - gpu
t2 = perf_counter() 

places_df = pd.read_excel('places.xlsx')

trip_prompt = PromptTemplate.from_template(template = TRIP_PLANNER_PROMPT_TEMPLATE)

def select_places_from_trip_data(user_data):
    chosen_activity = user_data["activities"]
    chosen_places = places_df[places_df['Activity'].isin(chosen_activity)]
    user_data["places"] = list(chosen_places.itertuples(index=False, name=None))
    return user_data

def model_invocation(trip_data):
    chain = trip_prompt | model
    
    t3 = perf_counter() 
    response = chain.invoke(trip_data)
    t4 = perf_counter() 
    
    return {"response": response,
            "execute_time": f'{t4-t3}s'}

def csv_parser(response, max_split=3, n_columns=4):
    # try split by new line.
    table = []
    try:
        lines = response.split('\n')
        # check each line is empty or not.
        for line in lines:
            if len(line) == 0:
                continue
            try:
                row = line.split(',', maxsplit=max_split)
                # add validator 
                if len(row) == n_columns:
                    table.append(row)
            except Exception as e:
                print(f'[ERROR] can not split each line by , --- {e}')
    except Exception as e:
        print(f'[ERROR] can not split response by \n --- {e}')

    return table

def get_AI_trip_plan(data_from_user):
    trip_data = select_places_from_trip_data(data_from_user)
    model_out = model_invocation(trip_data) 
    table = csv_parser(model_out['response'], max_split=2, n_columns=3)
    model_out['table'] = table
    return model_out

if __name__ == "__main__":
    data_from_user = {"destination": "Saudi Arabia",
                        "start_date": "August-15-2024",
                        "end_date": "August-20-2024",
                        "activities": ["Shopping", "Photography", "Unique Experiences", "Museums"],
                        "person_status": "Single",
                        "budget": "Low"}
    
    print( get_AI_trip_plan(data_from_user) )