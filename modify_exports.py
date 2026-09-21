import sys
import glob

def modify_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace CSS
    css_start = content.find("    <style>\n        @import url('https://fonts.googleapis.com/css2")
    css_end = content.find("    </style>\n</head>", css_start)
    if css_start != -1 and css_end != -1:
        css_end += len("    </style>\n")
        content = content[:css_start] + '    <link rel="stylesheet" href="assets/css/archive.css">\n' + content[css_end:]

    # Replace JS
    js_start = content.find("        const jsonSourceUrl = \"")
    if js_start != -1:
        # Get json url
        url_end = content.find("\";\n", js_start)
        json_url = content[js_start + len("        const jsonSourceUrl = \"") : url_end]
        
        js_end = content.find("        // Start execution\n        init();\n    </script>", js_start)
        if js_end != -1:
            js_end += len("        // Start execution\n        init();\n")
            replacement = f'        window.jsonSourceUrl = "{json_url}";\n    </script>\n    <script src="assets/js/archive.js">\n'
            content = content[:js_start] + replacement + content[js_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in ['classic.html', 'sotm.html']:
    print(f"Modifying {f}")
    modify_html(f)
