import re

def datapreprocessing(dataset):
    dataset['Salary'].astype(str)

    def minsal(x):
        num = re.findall(r'\d+',x)        
        if 'hour' in x.lower() or 'hr' in x.lower():
            hourly_rate = float(num[0])
            annual_salary = hourly_rate * 40 * 52
            return int(annual_salary)
        if 'k' in x.lower():
            return int(float(num[0]) * 1000)
        return int(num[0])

    ## below is the UDF for finding max salary from the Salary column

    def maxsal(x):
        num = list(map(float,re.findall(r"\d+\.\d+|\d+",x)))
        
        if 'hour' in x.lower() or 'hr' in x.lower():
            hourly_rate = max(num)
            annual_salary = hourly_rate * 40 * 52
            return int(annual_salary)
        elif 'k' in x.lower():
            return int(max(num) * 1000)
        else:
            return "correctit"
    def EstimatedBy(x):
        text = re.findall(r'\((.*?)\)',x)
        text1 = text[0].split(" ")
        return text1[0]
    def recency(x):
        if 'hr' in x.lower() or 'h' in x.lower():
            num = re.findall(r'\d+', x)
            return int(num[0]) / 24 
        elif 'd' in x.lower():
            num = re.findall(r'\d+', x)
            return int(num[0])  
        else:
            return None
        
    def job_role(title):
        title = title.lower()

        roles = {
            "intern": "Software Intern",
            "co-op" : "Software Intern",
            "engineer": {
                "data": "Data Engineer",
                "other": "Engineer"
            },
            "scientist": "Data Scientist",
            "devops": "DevOps Engineer",
            "developer": "Developer",
            "dev": "Developer",
            "programmer": "Developer",
            "analyst": "Data Analyst"
        }

        seniority_levels = {
            "entry": "Junior",
            "junior": "Junior",
            "jr":"Junior",
            "jr." : "Junior",
            "mid": "Mid-Level",
            "senior": "Senior",
            "sr":"Senior",
            "sr.":"Senior"
        }

        for key, role in roles.items():
            if key in title:
                if key =="intern" or key =="co-op":
                    return role
                elif key == "engineer" and "data" in title:
                    base_role = roles[key]["data"]
                elif key == "engineer":
                    base_role = roles[key]["other"]
                else:
                    base_role = role
                
                # Determine seniority
                for level in seniority_levels:
                    if level in title:
                        return f"{seniority_levels[level]} {base_role}"
                
                # Default to Mid-Level if no seniority level matched
                return f"Mid-Level {base_role}"

        return title  # Return original title if no match found


    dataset['min'] = dataset['Salary'].apply(minsal) ## creating new column for storing min salary
    dataset['max'] = dataset['Salary'].apply(maxsal)## creating new column for storing max salary
    dataset['EstimatedBy'] = dataset['Salary'].apply(EstimatedBy) ## creating new column for storing estimated by
    dataset['avgSalary']= (dataset['min']+dataset['max'])/2 ##creating the new column average salary from min and max
    ## below is the UDF for finding recency in days
    dataset['recency'] = dataset['Date'].apply(recency)
    dataset.drop('Date',axis =1) ## dropping date as information is maintained using recency
    dataset['JobRole']= dataset['Job Title'].apply(job_role)
    i = dataset[dataset['JobRole']== "node js"]
    '''
    dataset.loc[i,"JobRole"]= "Mid-Level Developer"
    dataset[dataset['JobRole']== " Engineer"]
    dataset[dataset['JobRole'].str.contains("shopify webmaster")]
    i = dataset[dataset['JobRole'].str.contains("shopify webmaster")].index
    dataset.loc[i,"JobRole"]= "Mid-Level Engineer"
    dataset['JobRole'].value_counts()
    i = dataset[dataset['Location']=="Township of Hamilton"].index
    dataset.loc[i,'Location']="Township of Hamilton,NJ"
    '''
    state_abbreviations = {
    # U.S. States
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "New York State": "NY", "Washington State": "WA",
    }
    territoriesDistricts = {
        # U.S. Territories and District
        "Washington, D.C.": "DC",  # Federal District
        "Puerto Rico": "PR",  # Territory
        "Guam": "GU",  # Territory
        "American Samoa": "AS",  # Territory
        "U.S. Virgin Islands": "VI",  # Territory
        "Northern Mariana Islands": "MP",  # Territory
        "Palau": "PW",  # Freely associated state, but often included in territory lists
        "Federated States of Micronesia": "FM",  # Freely associated state
        "Marshall Islands": "MH"  # Freely associated state
    }
    def ExtractState(x):
        def remove_words(text, words_to_remove):
            words = text.split()
            filtered_words = [word for word in words if word.lower() not in words_to_remove]
            filtered_text = " ".join(filtered_words)
            return filtered_text

        def standardize_state(state):
            if state in state_abbreviations.keys(): 
                return state_abbreviations[state] 
            elif state in state_abbreviations.values():
                return state
            else:
                return "Error"
            
        x = remove_words(x,["state","State"])
        
        if len(x.split("-"))==2:
            t = x.split("-")[1].strip()
            if t in territoriesDistricts.keys():
                return territoriesDistricts[t]
            elif t in territoriesDistricts.values():
                return t
            return standardize_state(t.lstrip())
        elif len(x.split(","))==2:
            t = x.split(",")[1].strip()
            if t in territoriesDistricts.keys():
                return territoriesDistricts[t]
            elif t in territoriesDistricts.values():
                return t
            return standardize_state(t.lstrip()) 
        elif "United States" in x:
            return "Remote"
        elif "remote" in x.lower():
            return "Remote"
        elif len(x.split(","))==1:
            if x in state_abbreviations.keys() or x in state_abbreviations.values():
                return standardize_state(x)
        else:
            return "Error"
    dataset['State'] = dataset['Location'].apply(ExtractState)
    i = dataset[dataset['State']=="Error"].index
    dataset.loc[i,'State'] = "MN"
    return dataset
