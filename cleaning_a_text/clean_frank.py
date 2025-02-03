import re

# Load the text file
with open("frank.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Remove the Project Gutenberg header and footer
start_match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text)
end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text)

if start_match and end_match:
    clean_text = text[start_match.end():end_match.start()].strip()
else:
    clean_text = text  # Fallback in case markers aren't found

# Save the cleaned text
with open("frankenstein_cleaned.txt", "w", encoding="utf-8") as file:
    file.write(clean_text)

print("Cleaned text saved as 'frankenstein_cleaned.txt'")
