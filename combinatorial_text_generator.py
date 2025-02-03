import re
import random
from flask import Flask, render_template_string

# Initialize Flask app
app = Flask(__name__)

# Clean Gutenberg text to remove headers and footers
def clean_gutenberg_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    
    start_match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    
    if start_match and end_match:
        clean_text = text[start_match.end():end_match.start()].strip()
    else:
        clean_text = text
    
    return clean_text

# Replace specific words in the text
def find_and_replace(text, replacements):
    for old_word, new_word in replacements.items():
        text = re.sub(rf'\b{old_word}\b', new_word, text, flags=re.IGNORECASE)
    return text

# Erasure method: Remove all occurrences of a specific letter
def erasure_lipogram(text, letter_to_remove):
    return text.replace(letter_to_remove, '')

# Generate a combinatorial cento from multiple texts
def generate_cento(cleaned_texts, num_sentences=20):
    sentences = []
    for text in cleaned_texts:
        split_text = re.split(r'(?<=[.!?])\s+', text)
        sampled_sentences = random.sample(split_text, min(len(split_text), num_sentences // len(cleaned_texts)))
        sentences.extend(sampled_sentences)
    random.shuffle(sentences)
    return " ".join(sentences)

# Convert the text to HTML structure
def text_to_html(text):
    html_content = """
    <html>
    <head>
        <title>Combinatorial Story</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
            h1 { text-align: center; color: #333; }
            p { line-height: 1.6; color: #555; }
        </style>
    </head>
    <body>
        <h1>Combinatorial Story</h1>
        <p>A blend of the classic stories: <br>
             ♡ Dracula (published 1897) by Bram Stoker ♡<br>
             ♡ Strange Case of Dr Jekyll and Mr Hyde (published 1886) by Robert Louis Stevenson ♡<br>
             ♡ Frankenstein (published 1818) by Mary Shelley ♡<br>
             ♡ Carmilla (published 1872) by Sheridan Le Fanu ♡<br>
             ♡ Grimm's Fairy Tales (published 1812) by Jacob Grimm and Wilhelm Grimm ♡
        </p>        
        <p>{}</p>
    </body>
    </html>
    """.replace("{}", text.replace("\n", "<br>"))
    return html_content

# Flask route to render the combinatorial story page
@app.route('/')
def index():
    # File paths for the texts
    file_paths = ["frank.txt", "carmilla.txt", "drac.txt", "jekyllhyde.txt", "grimm.txt"]
    cleaned_texts = [clean_gutenberg_text(path) for path in file_paths]
    
    # Apply Find and Replace method
    replacements = {"vampire": "ghost", "monster": "shadow", "doctor": "sorcerer"}
    cleaned_texts = [find_and_replace(text, replacements) for text in cleaned_texts]
    
    # Apply Erasure/Lipogram method (remove word 'him')
    cleaned_texts = [erasure_lipogram(text, 'him') for text in cleaned_texts]
    
    # Generate Cento
    cento_story = generate_cento(cleaned_texts, num_sentences=30)
    
    # Convert the combinatorial text to HTML
    html_story = text_to_html(cento_story)
    
    # Return the HTML as a response
    return render_template_string(html_story)

if __name__ == "__main__":
    app.run(debug=True)
