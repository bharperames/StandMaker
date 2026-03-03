file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
idx = -1
for i, line in enumerate(lines):
    if '<div id="photo-specific-controls"' in line:
        idx = i
        break

if idx != -1:
    # Insert closing div for setting-row before photo-specific-controls
    lines.insert(idx, '                        </div>')
    
    # Find Base Style to locate the extraneous closing div later
    idx2 = -1
    for i in range(idx, min(idx + 50, len(lines))):
        if 'Base Style' in lines[i]:
            idx2 = i
            break
            
    if idx2 != -1:
        # The line before "Base Style" should be `<div class="setting-row">`
        # The line before that should be the extraneous `</div>`
        removed = lines.pop(idx2 - 2)
        print("Removed extraneous line:", removed)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Fixed nesting logic successfully.")
else:
    print("Could not find photo-specific-controls")
