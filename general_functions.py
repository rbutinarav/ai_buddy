'''This is a collection of functions that do not interact directly with OpenAI API'''

def json_to_df (file_name):
    '''This function is used to import json text file into a pandas dataframe'''

    import pandas as pd
    import json
    
    # Opening JSON file
    json_file = open(file_name)
    json_dict = json.load(json_file)
    json_df=pd.DataFrame(json_dict)
    #for i in json_dict:
    #    print(i['prompt'])
    # Closing file
    json_file.close()
    return json_df


