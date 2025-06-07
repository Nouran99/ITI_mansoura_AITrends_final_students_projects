import os
from pydantic import BaseModel, ValidationError


def save_content_to_file(filename: str, content: str) -> dict:
    """
    Saves the given content to a file in the current local directory.

    Args:
        filename (str): The name of the file to save (e.g., "campaign_brief.txt").
                        The file will be saved in the current working directory.
        content (str): The string content to write into the file.

    Returns:
        str: A message indicating success or failure of the file saving operation.
    """
    try:
        # Define the full path for the file.
        # For simplicity, we'll save in the current working directory.
        # In a real application, you might define a specific 'output' folder.
        file_path = os.path.join(os.getcwd(), filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Content successfully saved to: {file_path}") # Log for debugging
        return {"Status":"Success","Message":"Content successfully saved to {filename} at {file_path}"}
    except Exception as e:
        #print(f"Error saving content to file '{filename}': {e}") # Log error
        #return f"Failed to save content to file {filename}: {e}"
        return {"Status":"Error","Message":"Failed to save content to file {filename}, {e}"}
    except ValidationError as e:
        for error in e.errors():
            print(f"Error in {error['loc']}: {error['msg']} (type: {error['type']})")
        return {"Status":"Error","Message":"Failed to save content to file {filename}, validation_error"}
