from Information import *
from Search import *
import copy

# -------------------VARIABLES-------------------
# Dictionaries to store match and original lists for each category
matches = {cat: [] for cat in matched_lists.keys()}
originals = {cat: [] for cat in matched_lists.keys()}

# -------------------MAIN FUNCTIONS-------------------
# Function to clear lists
def clear_lists(*lists):
    for lst in lists:
        lst.clear()

# Function to manage matches between original and match lists for a category
def match_lists(list1, list2, matches):
    """
    Compares two dictionaries of lists, detects matching elements, and creates a dictionary of lists with the results.
    
    - If there are matches, adds them to the result list.
    - If there are no matches, adds all elements from both lists, separated by "------------".
    - For specific keys, combines the lists directly without comparison.

    Args:
        list1 (dict of lists): First dictionary of lists to compare.
        list2 (dict of lists): Second dictionary of lists to compare.
        matches (dict of lists): Dictionary where the results will be stored.

    Returns:
        dict of lists: Dictionary with the results of the comparisons.
    """

    combined_keys = {"Warmup", "Fundamentals", "Development"}

    # Iterate over both dictionaries in parallel
    for key, sublist1, sublist2 in zip(list1.keys(), list1.values(), list2.values()):
        if isinstance(sublist1, str):
            sublist1 = globals().get(sublist1, [])
        if isinstance(sublist2, str):
            sublist2 = globals().get(sublist2, [])

        if key in combined_keys:
            # For these keys, simply combine both lists without comparison
            matches[key] = list(set(sublist1) | set(sublist2))
        else:
            # Find matching elements
            matches[key] = list(set(sublist1) & set(sublist2))
            
            if not matches[key] and sublist1 and sublist2:
                # If there are no matches, add all elements with "------------" as separator
                matches[key] = sublist1 + ["------------"] + sublist2
            
            elif not matches[key] and (sublist1 or sublist2):
                # If one of the lists is empty, simply join both
                matches[key] = sublist1 + sublist2
          
    return matches
