from tkinter import *
from tkinter import ttk
import tkinter as tk
from collections import defaultdict
import re

# Separate module imports
import Information
from Main_Functions import *


# -------------------MAIN WINDOW--------------------

main = Tk()
main.title("Live Lab")
main.geometry("1450x850")

# -------------------IMPORTING VARIABLES-------------------

categories = Information.categories

# -------------------AUXILIARY FUNCTIONS-------------------

# Auxiliary function to create labels at a specific location within a frame
def create_label(text, row, column, frame):
    label = Label(frame, text=text)
    label.grid(row=row, column=column, padx=5, pady=5, sticky="w")
    return label

# Auxiliary function to create list boxes in a specific location
def create_listbox(row, column, frame, width=30, height=12):
    listbox = Listbox(frame, width=width, height=height)
    listbox.grid(row=row, column=column, padx=5, pady=5)
    return listbox

def delete_result(List):
    for item in List:
        item.delete(0, END)

def rearrange_matching(lesson_coincidence_lists):
    """
    Rearranges the elements of 'Warmup', 'Fundamentals', and 'Development' in matched_lists
    by adding the grouping category to each item according to the elements in Lessons.
    """

    # Dictionary to group keys by unique values
    grouped = defaultdict(list)
    grouped.clear()

    for key, values in lessons.items():
        # Convert the list of values to a tuple to make it hashable
        if len(values) == 1:
            value = next(iter(values))  # Extract the single value from the set/list
            grouped[value].append(key)
        else:
            grouped[tuple(values)].append(key)

    # Step 1: Sort by the number of elements in the tuple
    sorted_by_elements = sorted(
        grouped.items(),
        key=lambda x: len(x[0]),
    )

    # Convert to an ordered dictionary
    grouped_ordered = dict(sorted_by_elements)

    # Iterate over the specific keys of matched_lists
    for group, values in grouped_ordered.items():
        for key in ["Warmup", "Fundamentals", "Development"]:
            for item in matched_lists.get(key, []):  # Ensure the key exists in matched_lists
                # Search for the group (key) in grouped_ordered where the item appears
                if item in values:
                    # If the group does not exist in lesson_coincidence_lists[key], create it
                    if group not in lesson_coincidence_lists[key]:
                        lesson_coincidence_lists[key][group] = []
                    # Add the item to the corresponding group within lesson_coincidence_lists
                    lesson_coincidence_lists[key][group].append(item)

    return lesson_coincidence_lists


def write_results():
    ## OBTAINING lesson_coincidence_lists
    # Proper structure of lesson_coincidence_lists
    lesson_coincidence_lists = {
        "Warmup": defaultdict(list),
        "Fundamentals": defaultdict(list),
        "Development": defaultdict(list)
    }    

    # 🔹 Rearrange the items before writing them
    rearrange_matching(lesson_coincidence_lists)

    # Convert defaultdict to normal dict to avoid issues in other processes
    lesson_coincidence_lists = {k: dict(v) for k, v in lesson_coincidence_lists.items()}

    ## TRANSFER RESULTS TO matched_lists_final
    matched_lists_final = matched_lists.copy()

    # Replace the values in matched_lists_final with those from lesson_coincidence_lists
    for key in ["Warmup", "Fundamentals", "Development"]:
        if key in lesson_coincidence_lists:
            matched_lists_final[key] = []  # Reset key in final
            
            for group, items in lesson_coincidence_lists[key].items():
                # Add the group
                # Transform the tuple into a string and apply substitutions
                group_str = str(group)
                if group_str.count(',') == 1 and group_str.endswith(',)'):
                    # Special case: only a pair
                    group_clean = group_str.strip('(),')
                else:
                    group_clean = re.sub(r",\s*", " + ", group_str)  # Replace "," with " + "
                    
                group_clean = re.sub(r"[()']", "", group_clean)  # Remove parentheses and single quotes
                group_clean = group_clean.strip()  # Remove leading/trailing whitespace

                # Add to the dictionary with the cleaned format
                matched_lists_final[key].append(f"{group_clean}:")
      
                # Add the items with indentation
                for item in items:
                    matched_lists_final[key].append(f"  - {item}")

    ## WRITE THE RESULTS
    keys = list(matched_lists_final.keys())
    values = list(matched_lists_final.values())
    
    # Iterate over result_lists and assign the corresponding values
    for result_list, key, coinciding_list in zip(result_lists, keys, values):
        # Clear result_list before inserting new values
        result_list.delete(0, END)  # Assumes result_list is a tkinter Listbox
        # Insert the values of the corresponding coinciding list
        for item in coinciding_list:
            result_list.insert(END, item)

    # Highlight the central element directly in the Listboxes (if applicable) -> Only applies to listboxes belonging to selected items
    for listbox, selected in listboxes_selections.items():
        # Get the current elements of the listbox
        current_items = listbox.get(0, "end")

        if listbox not in result_lists[5:8]:
            new_items = list(selected) + [item for item in current_items if item not in selected]
        else:
            new_items =  [item for item in current_items]

        # Clear the listbox and refill it with the ordered elements
        listbox.delete(0, "end")
        for idx, item in enumerate(new_items):
            listbox.insert("end", item)

        # Apply colors: Main Element in orange, other selected in blue
        for i, item in enumerate(new_items):
            if item == main_element and not item.startswith("  - "):
                listbox.itemconfig(i, {'bg': 'orange'})  # Main Element in orange
            elif item in selected and listbox in result_lists[0:5]:
                listbox.itemconfig(i, {'bg': 'lightblue'})  # Other selected in blue
            elif item in selected and listbox in result_lists[5:8]:
                listbox.itemconfig(i, {'bg': 'lightgreen'})  # Other selected in green
            else:
                listbox.itemconfig(i, {'bg': 'white'})  # The rest in white

    # Highlight the central element directly in the Listboxes (if applicable) -> Only applies to lesson listboxes
    for current_listbox in result_lists[5:8]:
        current_items = current_listbox.get(0, "end")

        for i, item in enumerate(current_items):
            if main_element in item and not item.startswith("  - "):
                current_listbox.itemconfig(i, {'bg': 'orange'})  # Main Element in orange
            else:
                found = False
                for listbox_sel, selected in listboxes_selections.items():
                    if any(s in item for s in selected) and listbox_sel in result_lists[0:5]:
                        found = True
                        break

                if found and not item.startswith("  - "):
                    current_listbox.itemconfig(i, {'bg': 'lightblue'})  # Other selected in blue

    ## WRITE THE DECIDED LESSONS
    # Prepare selected lessons
    # selected_lessons.clear()

    listbox_map = {
        str(result_lists[5]): str(listboxes_3[0]),
        str(result_lists[6]): str(listboxes_3[1]),
        str(result_lists[7]): str(listboxes_3[2]),
    }

    for listbox, selected in listboxes_selections.items():
        if str(listbox) in listbox_map:
            if listbox not in selected_lessons:
                selected_lessons[listbox] = {}  # Now it will be a dict of subkeys

            for item in selected:
                # Find the subkey to which this item belongs
                found_subkey = None
                for key, lst in lesson_coincidence_lists.items():
                    for subkey, sublist in lst.items(): 
                        if item.removeprefix("  - ") in sublist:
                            found_subkey = subkey
                            break

                if found_subkey is not None:
                    # Initialize subkey if it doesn't exist
                    if found_subkey not in selected_lessons[listbox]:
                        selected_lessons[listbox][found_subkey] = set()

                    # Avoid duplicates
                    if item not in {text for text, _ in selected_lessons[listbox][found_subkey]}:
                        selected_lessons[listbox][found_subkey].add((item, False))

    for listbox, categories in selected_lessons.items():
        # Copy the keys to iterate safely
        keys = list(categories.keys())
        
        # Iterate over all combinations
        for key in keys:
            for other_key in keys:
                if key == other_key:
                    continue
                
                # Convert everything to tuples for easy comparison
                key_t = key if isinstance(key, tuple) else (key,)
                other_t = other_key if isinstance(other_key, tuple) else (other_key,)
                
                # If all elements of key are contained in other_key (key is included in other_key)
                if all(elem in other_t for elem in key_t):
                    # Merge lessons into the more complete key
                    categories[other_key].update(categories[key])
                    # Remove the simpler key
                    del categories[key]
                    break

    # Write the selected lessons in the destination listboxes
    for origin_listbox, subkeys in selected_lessons.items():
        dest_name = listbox_map.get(str(origin_listbox))
        if dest_name:
            for listbox3 in listboxes_3:
                if str(listbox3) == dest_name:
                    listbox3.delete(0, END)
                    
                    for subkey, selected in subkeys.items():
                        key_str = str(subkey)
                        if subkey.count(',') == 1:
                            clean_key = subkey
                        else:
                            clean_key = re.sub(r",\s*", " + ", key_str)  # Replace "," with " + "
                            clean_key = re.sub(r"[()']", "", clean_key)

                        listbox3.insert("end", f"{clean_key}:")  # Block header
                        for item, _ in selected:
                            listbox3.insert("end", item)

#-----------------------------------------------------
# -------------------MAIN FUNCTIONS-------------------
#-----------------------------------------------------

# Primary search function

def search_function(value_inside, search_type="element"):
    global main_element  # Indicate global variables if necessary
    delete_result(result_lists)
    listboxes_selections.clear()
    lessons.clear()

    # Determine the type of search to perform
    if search_type == "musical":
        main_element = value_inside.get()
        search_musical_results(main_element)

        # Find in which category the main element is located
        listbox_index = None
        for idx, (category, elements) in enumerate(categories.items(), start=1):
            if main_element in elements:
                listbox_index = idx - 1  # Correct listbox index (0 to 4)
                break

        # Add to listboxes_selections if appropriate
        if listbox_index is not None and listbox_index < len(listboxes):
            listbox = listboxes[listbox_index]
            if listbox not in listboxes_selections:
                listboxes_selections[listbox] = set()
            listboxes_selections[listbox].add(main_element)

    elif search_type == "lesson":
        main_element = value_inside.get()
        search_lesson_results(main_element)

    write_results()  # Apply changes to the Listbox

# Function that handles selection in any Listbox

def on_select(event):
    # Get the Listbox that triggered the event
    current_listbox = event.widget
    
    # If the Listbox is not in the dictionary, initialize its selection set
    if current_listbox not in listboxes_selections:
        listboxes_selections[current_listbox] = set()

    # Get the selected index in the current event
    selected_index = current_listbox.curselection()

    # Get the currently selected items
    selected_items = {current_listbox.get(i) for i in selected_index}
    #selected_items = {current_listbox.get(i).removeprefix("  - ") for i in selected_index}
    
    # Update the accumulated selections for this Listbox
    listboxes_selections[current_listbox].update(selected_items)

    # Call the processing function with the selected items
    if selected_items:
        # Process the first selected item (as an example)
        combine(next(iter(selected_items)))
        write_results()

# Functions for selected lessons

def action_1():  # Deletion of lessons
    global selected_lessons
    for listbox in listboxes_3:
        listbox.delete(0, END)

    listbox_map = {
        str(result_lists[5]): str(listboxes_3[0]),
        str(result_lists[6]): str(listboxes_3[1]),
        str(result_lists[7]): str(listboxes_3[2]),
    }

    # Clear selected items from the lesson listboxes
    for listbox, selected_items in listboxes_selections.items():
        if str(listbox) in listbox_map:
            listboxes_selections[listbox].clear()

    # Remove items from selected_lessons marked as False
    # Create a new clean dict
    new_lessons = {}

    for listbox, subdict in selected_lessons.items():
        new_subdict = {}

        for subkey, items in subdict.items():
            true_items = {(text, state) for text, state in items if state is True}
            if true_items:
                new_subdict[subkey] = true_items

        if new_subdict:
            new_lessons[listbox] = new_subdict

    # Replace the original
    selected_lessons = new_lessons

    # Write the selected lessons in the destination listboxes
    for origin_listbox, subdict in selected_lessons.items():
        dest_name = listbox_map.get(str(origin_listbox))
        if dest_name:
            for listbox3 in listboxes_3:
                if str(listbox3) == dest_name:
                    listbox3.delete(0, END)

                    for subkey, selected_items in subdict.items():
                        key_str = str(subkey)
                        if subkey.count(',') == 1:
                            clean_key = subkey
                        else:
                            clean_key = re.sub(r",\s*", " + ", key_str)  # Replace "," with " + "
                            clean_key = re.sub(r"[()']", "", clean_key)

                        listbox3.insert("end", f"{clean_key}:")  # Block header
                        for item, _ in selected_items:
                            listbox3.insert("end", item)

def action_2():  # Mark lessons as fixed/selected
    for listbox, subdict in selected_lessons.items():
        for subkey, items in subdict.items():
            new_items = {(text, True) for text, _ in items}
            selected_lessons[listbox][subkey] = new_items

def general_clear():
    delete_result(result_lists)
    delete_result(listboxes_3)
    listboxes_selections.clear()
    lessons.clear()
    selected_lessons.clear()

    
# -------------------ORGANIZATION OF FRAMES AND ELEMENTS-------------------

# Create the main frame for column organization
options_frame = Frame(main)
options_frame.grid(row=0, column=0, rowspan=3, sticky="nw")

results_frame = Frame(main)
results_frame.grid(row=0, column=1, columnspan=5, sticky="nw")

# Create the elements in the options column
Label(options_frame, text="Options").grid(row=0, column=0, sticky="w")
value_inside1 = [StringVar(main), StringVar(main), StringVar(main)]
value_inside1[0].set("Main Musical Element")

# Menubutton "Main Element"
menubutton_element = Menubutton(options_frame, textvariable=value_inside1[0], indicatoron=True,
                                borderwidth=2, relief="raised", width=20)
main_menu = Menu(menubutton_element, tearoff=False)
menubutton_element.configure(menu=main_menu)

# Create options for the menubutton using the categories from the dictionary
for category, items in categories.items():
    menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label=category, menu=menu)
    for item in items:
        menu.add_radiobutton(
            label=item,
            value=item,
            variable=value_inside1[0],
            command=lambda: search_function(value_inside1[0], search_type="musical")
        )

# Position the menubutton
menubutton_element.grid(row=0, column=0, sticky="nw", pady=(0, 10))  # Add space below

# Menubutton "Main Lesson Element"
value_inside1.append(StringVar(main))  # Add a new variable for "Main Lesson"
value_inside1[1].set("Main Lesson Element")

menubutton_lesson = Menubutton(options_frame, textvariable=value_inside1[1], indicatoron=True,
                               borderwidth=2, relief="raised", width=20)
lesson_menu = Menu(menubutton_lesson, tearoff=False)
menubutton_lesson.configure(menu=lesson_menu)

# Create options for the menubutton using categories
for item in (("Interface", *INTERFACES), ("Level", "All", "Easy", "Medium", "Hard"), 
             ("Genres", *GENRES)):
    menu = Menu(lesson_menu, tearoff=False)
    lesson_menu.add_cascade(label=item[0], menu=menu)

    if item[0] == "Level":
        # Option "All"
        menu.add_radiobutton(
            label="All",
            variable=value_inside1[1],
            value="All",
            command=lambda: search_function(value_inside1[1], search_type="lesson")
        )

        # Submenu for "Easy"
        easy_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Easy", menu=easy_menu)
        for i in range(1, 6):
            easy_menu.add_radiobutton(
                label=str(i),
                variable=value_inside1[1],
                value=str(i),
                command=lambda: search_function(value_inside1[1], search_type="lesson")
            )

        # Submenu for "Medium"
        medium_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Medium", menu=medium_menu)
        for i in range(6, 11):
            medium_menu.add_radiobutton(
                label=str(i),
                variable=value_inside1[1],
                value=str(i),
                command=lambda: search_function(value_inside1[1], search_type="lesson")
            )

        # Submenu for "Hard"
        hard_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Hard", menu=hard_menu)
        for i in range(11, 16):
            hard_menu.add_radiobutton(
                label=str(i),
                variable=value_inside1[1],
                value=str(i),
                command=lambda: search_function(value_inside1[1], search_type="lesson")
            )

    else:
        # For other categories like Interface and Style
        for value in item[1:]:
            menu.add_radiobutton(
                value=value,
                label=value,
                variable=value_inside1[1],
                command=lambda: search_function(value_inside1[1], search_type="lesson")
            )

menubutton_lesson.grid(row=1, column=0, sticky="nw", pady=(0, 10))  # Add extra space below

# Buttons for selected lessons

button1 = tk.Button(options_frame, text="Delete Lessons", command=action_1)
button1.grid(row=2, column=0, padx=10, pady=5)

button2 = tk.Button(options_frame, text="Set Lessons", command=action_2)
button2.grid(row=3, column=0, padx=10, pady=5)

# Button for general clear

button3 = tk.Button(options_frame, text="General Clear", command=general_clear)
button3.grid(row=4, column=0, padx=10, pady=5)

# Create the labels and listboxes in the results columns
headers = ["Skills", "Musical Dimensions", "Musical Sub-Dimensions", "Techniques", "Modes"]
listboxes = []

# Create the listboxes for the 1st row: Musical elements
for i, header in enumerate(headers):
    create_label(header, 0, i, results_frame)
    listbox = create_listbox(1, i, results_frame, width=40, height=12)
    listbox.bind("<<ListboxSelect>>", on_select)  # Bind the selection event
    listboxes.append(listbox)

# Second row of results
headers_2 = ["Warmup (Lessons)", "Fundamentals (Lessons)", "Development (Lessons)", "Improvisation (Lessons)", "Goals (Lessons)"]
listboxes_2 = []

# Create the listboxes for the 2nd row: Lessons and goals result
for i, header in enumerate(headers_2):
    create_label(header, 2, i, results_frame)
    listbox = create_listbox(3, i, results_frame, width=40, height=20)
    listbox.bind("<<ListboxSelect>>", on_select)  # Bind the selection event
    listboxes_2.append(listbox)

# Save listboxes in result_lists to be referenced in other functions
result_lists = listboxes + listboxes_2

# Create the labels and listboxes in the results columns
headers = ["Warmup (Routine)", "Fundamentals (Routine)", "Development (Routine)", "Improvisation (Routine)", "Goals (Routine)"]
listboxes_3 = []

# Create the listboxes for the 3rd row: Routine selection
for i, header in enumerate(headers):
    create_label(header, 4, i, results_frame)
    listbox = create_listbox(5, i, results_frame, width=40, height=12)
    listbox.bind("<<ListboxSelect>>", on_select)  # Bind the selection event
    listboxes_3.append(listbox)

# Run the window
main.mainloop()
