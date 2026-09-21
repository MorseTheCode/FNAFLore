import os

def remove_from_html(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start = content.find('<script id="archive-data"')
    if start == -1:
        print(f"No archive-data script found in {filepath}")
        return

    end = content.find('</script>', start)
    if end != -1:
        end += len('</script>\n')
        new_content = content[:start] + content[end:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed archive-data from {filepath}")
    else:
        print(f"Could not find closing script tag in {filepath}")

def remove_from_builder():
    filepath = 'builder.html'
    if not os.path.exists(filepath):
        print("builder.html not found.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = '    <script id="archive-data" type="application/json">${safeJsonData}${scriptEnd}\n'
    if target in content:
        content = content.replace(target, '')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Removed archive-data from builder.html")
    else:
        print("Could not find exact template string in builder.html")

if __name__ == '__main__':
    remove_from_html('classic.html')
    remove_from_html('sotm.html')
    remove_from_builder()
