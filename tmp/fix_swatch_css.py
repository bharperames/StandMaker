import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

css_addition_1 = """document.getElementById('tex-swatch-pattern-1').style.backgroundImage = 'url(data:image/png;base64,' + DEFAULT_SPHERE_PATTERN_B64 + ')';
        document.getElementById('tex-swatch-pattern-1').style.backgroundSize = 'cover';
        document.getElementById('tex-swatch-pattern-1').style.backgroundPosition = 'center';"""

css_addition_2 = """document.getElementById('tex-swatch-soda').style.backgroundImage = 'url(data:image/png;base64,' + DEFAULT_SODALITE_B64 + ')';
        document.getElementById('tex-swatch-soda').style.backgroundSize = 'cover';
        document.getElementById('tex-swatch-soda').style.backgroundPosition = 'center';"""

text = text.replace("document.getElementById('tex-swatch-pattern-1').style.backgroundImage = 'url(data:image/png;base64,' + DEFAULT_SPHERE_PATTERN_B64 + ')';", css_addition_1)
text = text.replace("document.getElementById('tex-swatch-soda').style.backgroundImage = 'url(data:image/png;base64,' + DEFAULT_SODALITE_B64 + ')';", css_addition_2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Swatch CSS Cover logic fixed.")
