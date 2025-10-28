import os
from Information import *

# -------------------VARIABLE DEFINITIONS-------------------
full_file = ""
filedata_lines = []
category_list = []

# -------------------AUXILIARY FUNCTIONS-------------------

def clear_lists(Lists):
    """Clears all provided lists."""
    for lst in Lists:
        lst.clear()

def call_lessons_goals(parameter, clear):
    # Call the function for lesson search

    # Folder where the script is located
    folder_script = os.path.dirname(os.path.abspath(__file__))

    # Path to a folder named 'Lessons' in the same folder
    relative_path = os.path.join(folder_script, 'Lessons')
    
    show_options_ar2(
        relative_path, 
        parameter,
        [matched_lists["Warmup"], 
         matched_lists["Fundamentals"], 
         matched_lists["Development"]],
        ["Warmup", "Fundamentals", "Development"],
        clear
    )

    # Call the function for goal search

    # Path to a folder named 'Lessons' in the same folder
    relative_path = os.path.join(folder_script, 'Goals')

    show_options_ar(
        relative_path, 
        parameter, 
        [matched_lists["Goals"]], 
        ["Live"], 
        clear
    )

# -------------------FUNCIÓN CATEGORÍAS-------------------
def show_category_options(index):
    # Clear match lists
    clear_lists(matched_lists.values())  
    
    relations = {
        "Skill": {"Skill": 1, "Musical Dimensions": 1, "Musical SubDimensions": 1, "Techniques": 1, "Modes": 1},
        "Musical Dimensions": {"Skill": -1, "Musical Dimensions": 0, "Musical SubDimensions": 1, "Techniques": 1, "Modes": 1},
        "Musical SubDimensions": {"Skill": -1, "Musical Dimensions": -1, "Musical SubDimensions": 0, "Techniques": 1, "Modes": 1},
        "Techniques": {"Skill": -1, "Musical Dimensions": -1, "Musical SubDimensions": -1, "Techniques": 0, "Modes": 0},
        "Modes": {"Skill": -1, "Musical Dimensions": -1, "Musical SubDimensions": -1, "Techniques": 0, "Modes": 0}
    }
    
    # Browse relationships according to the main category
    for destination_category, relation in relations.get(index[0], {}).items():
        for n in range(len(categories[destination_category])):  # Iterar sobre las categorías destino
            if (
                relation == 1 
                and Relationship_Matrices[index[0]][destination_category][index[1]][n]
            ):
                matched_lists[destination_category].append(categories[destination_category][n])
            elif (
                relation == -1 
                and Relationship_Matrices[index[0]][destination_category][n][index[1]]
            ):
                matched_lists[destination_category].append(categories[destination_category][n])

    # Add the main category if it is not "Skill" (the first one)
    if index[0] != "Skills":
        matched_lists[index[0]].append(categories[index[0]][index[1]])

    return matched_lists


# -------------------FILE SEARCH FUNCTION-------------------
def show_options_ar(path, main_element, included_lists, terms, clear=True):
    if clear:
        clear_lists(included_lists)

    for root, _, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".md"):  # Check if it's a markdown file
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    filedata_lines = file.readlines()
                    count, include, index_list = 0, False, []

                    for line in filedata_lines:
                        if "---" in line:
                            count += 1
                            if count == 2:
                                break

                        if main_element in line:
                            include = True
                        
                    if include:
                        for item in terms:                    
                            if terms.index(item) not in index_list:
                                index_list.append(terms.index(item))

                        for lst in index_list:
                            included_lists[lst].append(file_name.split('.')[0])

                        if file_name.split('.')[0] not in lessons:
                            lessons[file_name.split('.')[0]] = set()
                        lessons[file_name.split('.')[0]].add(main_element)
                        
    return included_lists, lessons

def show_options_ar2(path, main_element, included_lists, terms, clear=True):
    if clear:
        clear_lists(included_lists)

    for root, _, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if "data" not in data or not isinstance(data["data"], dict):
                        return

                    tags = data["data"].get("tags", [])
                    grade = data["data"].get("grade", [])
                    genres = data["data"].get("genres", [])

                    # Normalize non-list values to lists
                    tags = [tags] if not isinstance(tags, list) else tags
                    grade = [grade] if not isinstance(grade, list) else grade
                    genres = [genres] if not isinstance(genres, list) else genres

                    # Combine tags
                    combined_tags = tags + grade + genres
                    
                    include = main_element in json.dumps(combined_tags)
                    index_list = []
                    
                    if include:
                        for item in terms:
                            if item in combined_tags:
                                index_list.append(terms.index(item))

                        for lst in index_list:
                            included_lists[lst].append(file_name.split('.')[0])

                        if file_name.split('.')[0] not in lessons:
                            lessons[file_name.split('.')[0]] = set()
                        lessons[file_name.split('.')[0]].add(main_element)
                        

    return included_lists, lessons


# -------------------FUNCTION TO SEARCH MELODICS FEATURES-------------------
def analyze_lessons(file):

    full_file = ""

    # Folder where the script is located
    folder_script = os.path.dirname(os.path.abspath(__file__))

    # Path to a folder named 'Lessons' in the same folder
    path = os.path.join(folder_script, 'Lessons')

    # Build the full path and check its existence

    for root, _, files in os.walk(path):
        if f"{file}.json" in files:
            full_file = os.path.join(root, f"{file}.json")
            break  # Optional: stop when the first is found
    
    if full_file:
        # Read the file content
        with open(full_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

            tags = data.get("data", {}).get("tags", [])
            if not isinstance(tags, list):
                tags = []

            for category_name, category_list in categories.items():
                if category_name in matched_lists:
                    for category in category_list:
                        if category in tags and category not in matched_lists[category_name]:
                            matched_lists[category_name].append(category)

    # Return all the lists from the dictionary as tuples
    return {key: matched_lists[key] for key in ["Skill", "Musical Dimensions", "Musical SubDimensions", "Techniques", "Modes"]}
