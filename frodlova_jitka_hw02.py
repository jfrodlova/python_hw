import csv
import json


def process_fields(entry, keys):
    """
    Processes specified fields in a dictionary, converting empty strings to empty lists, and splitting non-empty strings into lists based on commas.

    Parameters:
    entry (dict): A dictionary containing the fields to process.
    fields (list): A list of field names (keys) to process.

    Returns:
    dict: A new dictionary with processed fields where empty strings
    are replaced with empty lists, and non-empty strings are split into lists.
    """
    for key in keys:

        # Get the value for each key, defaulting to an empty string
        value = entry.get(key, '').strip()

        if key == 'PRIMARYTITLE':
            new_dict['title'] = value
        # Create a list from the value if it exists; otherwise, set to empty list
        elif key == 'DIRECTOR':
            new_dict[key.lower() + 's'] = value.split(', ') if value else []
        elif key == 'CAST':
            new_dict[key.lower()] = value.split(', ') if value else []
        elif key == 'GENRES':
            new_dict[key.lower()] = value.split(',') if value else []

    return new_dict


def floor_year_to_decade(entry):
    """
    Gets a string or an integer, converts to integer and returns the number (int) rounded down to the nearest ten.
    """
    try:
        start_year = int(entry['STARTYEAR'])

        if isinstance(start_year, int):
            start_year = start_year - (start_year % 10)
            new_dict['decade'] = start_year
        else:
            new_dict['decade'] = "Unknown"

    except (ValueError, KeyError):
        # Handle the case where the year is not valid or 'STARTYEAR' is missing
        new_dict['decade'] = "Unknown"

    return new_dict


with open('netflix_titles.tsv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    new_dict_list = []

    for entry in reader:
        new_dict = {}
        sorted_fields = ['PRIMARYTITLE', 'DIRECTOR', 'CAST', 'GENRES']
        process_fields(entry, sorted_fields)
        floor_year_to_decade(entry)
        new_dict_list.append(new_dict)

with open('hw02_output.json', mode='w', encoding='utf-8') as file:
    json.dump(new_dict_list,
              file,
              ensure_ascii=False,
              indent=4)
