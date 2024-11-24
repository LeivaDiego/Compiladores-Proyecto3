import os

def generate_name(path, base_name=None):
    """
    Generates the output file name based on the input file name.

    Args:
        - path: The path to the input file.
        - base_name: The base name for the output file.

    Returns:
        - The output file name.
    """
    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(path))[0]

    # Append the file name to the output file name
    output_file_name = f"{base_name}{file_name}"

    return output_file_name