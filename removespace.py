def remove_empty_lines(filename):
    # Read the file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    # Write the updated content back to the file
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))


# Example usage
filename = 'inappropriate_words.txt'  # Replace with your file path
remove_empty_lines(filename)
print(f"Empty lines removed from {filename}.")