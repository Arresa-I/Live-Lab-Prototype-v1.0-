from Information import *
from Search import *
from Combination import *

# -------------VARIABLES-------------

index = []

# ---------AUXILIARY FUNCTION---------
### List clearing

def delete_lists(lst):
    """Clears all provided lists."""
    if lst is not None and isinstance(lst, list):  # Check that lst is a valid list
        lst.clear()
    else:
        print("Error: The variable is not a valid list.")

# -------------FUNCTION 1: Musical Search-------------
### Search results based on the "Central Element" from the "Show Results" button

def search_musical_results(parameter):
    index.clear()

    # Find the index of main_element in Categories (1 to 4)
    for key, subcategories in categories.items():
        try:    
            if parameter in subcategories:
                index.append(key)  # Store the category name
                index.append(subcategories.index(parameter))  # Store the index within the list
                break  # Exit loop when element is found
        except ValueError:
            continue  # If Parameter is not found, continue

    # Call the category options function
    show_category_options(index)

    # Call the function for lesson and goal search
    call_lessons_goals(parameter, True)

    # Access dictionary keys directly
    matching_results = {key: lst for key, lst in matched_lists.items()}
    
    return matching_results

# -------------FUNCTION 2: Lesson Search-------------
### Search results based on the "Central Lesson" from the "Show Results" button
##### 1. Find lessons and goals with the selected parameter
##### 2. Review each lesson to check contained elements

def search_lesson_results(parameter):
    [delete_lists(matched_lists[key]) for key in ["Skill", "Musical Dimensions", "Musical SubDimensions", "Techniques", "Modes"]]

    # Call the function for lesson and goal search
    call_lessons_goals(parameter, True)

    # Analyze lesson features to collect element lists
    for key in ["Warmup", "Fundamentals", "Development", "Improvisation"]:
        for file in matched_lists[key]:
            analyze_lessons(file)


# -------------FUNCTION 3: Combination (Musical and Lesson)-------------
# Main combination and processing function
def combine(selection):
    # Clean lists
    clear_lists(*matches.values(), *originals.values())

    # Transfer to "originals" the previous result list before selection
    for key, new_list in zip(originals.keys(), matched_lists.values()):
        originals[key].extend(new_list)   

    # Identify category and process -> Determines if the selected item is musical or non-musical
    for cat, items in categories.items():
        if selection in items:
            category1, category2 = cat, items.index(selection)
            show_category_options([category1, category2])
            break
    else:
        clear_lists(*matched_lists.values())
        if selection.startswith("  - "):
            selection = selection.removeprefix("  - ")

        analyze_lessons(selection)

        # Process each element in relevant lists
        relevant_keys = {"Skill", "Musical Dimensions", "Musical SubDimensions", "Techniques", "Modes"}

        #for key in relevant_keys:
        #   if key in matched_lists:
        #       for item in matched_lists[key]:
        #           call_lessons_goals(item, False)

    # Call function for lesson and goal search
    call_lessons_goals(selection, False)

    # Remove duplicates in each list
    for key, values in matched_lists.items():
        matched_lists[key] = list(set(values))

    # Compare original lists with parameter matches across all categories
    match_lists(originals, matched_lists, matches)
    
    # Clean match lists to include coincidences
    clear_lists(*matched_lists.values())
                   
    # Pass matches to main list
    for new_key, match_list in zip(matched_lists.keys(), matches.values()):
        matched_lists[new_key].extend(match_list)

    return matched_lists

            