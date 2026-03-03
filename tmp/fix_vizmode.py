import sys

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_str = "let vizMode = 'solid';"
new_str = "let vizMode = 'both';"

if old_str in text:
    text = text.replace(old_str, new_str)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully changed default render mode to 'both'.")
else:
    print("Could not find the target string to replace.")

