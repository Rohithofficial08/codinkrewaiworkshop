import json

def get_answer_from_json_string(json_string):
  """
  Parses a JSON string and returns the value of the 'answer' key.

  Args:
    json_string (str): A string containing a JSON object with an 'answer' key.

  Returns:
    str: The string value of the 'answer' key, or an error message if the 
         key is not found or the JSON is invalid.
  """
  try:
    # Use json.loads() to convert the string into a Python dictionary.
    data = json.loads(json_string)
    
    # Return the value associated with the 'answer' key.
    return data['answer']
  except json.JSONDecodeError:
    return "Error: Invalid JSON format"
  except KeyError:
    return "Error: 'answer' key not found"

# --- Example Usage ---
# The input string, including the quotes and newline character.
input_string = "{\"answer\": \"We issue this Group Domestic Travel Insurance policy to the Proposer.\"}\n"

# Call the function with the input string.
extracted_answer = get_answer_from_json_string(input_string)

# Print the result, which will be just the text.
print(extracted_answer) 
# Expected Output: We issue this Group Domestic Travel Insurance policy to the Proposer.
