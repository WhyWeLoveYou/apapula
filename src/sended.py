import json

def write_data_to_file(data, filename='sended.json'):
    """Writes the given data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def save_sended(link, tanggal):
    """Saves a new entry with link and date to the JSON file."""
    try:
        # Try to read existing data
        with open('sended.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize data as an empty list if file not found or empty
        data = []

    # Create a new entry
    new_object = {
        "link": link,
        "tanggal": tanggal
    }
    data.append(new_object)

    # Write updated data back to the file
    write_data_to_file(data)

def get_data():
    """Retrieves data from the JSON file."""
    try:
        with open('sended.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if file not found or empty
