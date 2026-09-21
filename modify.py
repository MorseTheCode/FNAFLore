import sys

def modify():
    with open('builder.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace CSS
    css_start = content.find("    <style>\n        @import url('https://fonts.googleapis.com/css2")
    css_end = content.find("    </style>\n</head>", css_start)
    if css_start != -1 and css_end != -1:
        css_end += len("    </style>\n")
        content = content[:css_start] + '    <link rel="stylesheet" href="assets/css/archive.css">\n' + content[css_end:]
    else:
        print("CSS not found!")

    # Replace JS
    js_start = content.find("        const jsonSourceUrl = \"${jsonUrl}\";\n        let appData = {")
    js_end = content.find("        // Start execution\n        init();\n    ${scriptEnd}", js_start)
    if js_start != -1 and js_end != -1:
        js_end += len("        // Start execution\n        init();\n")
        replacement = '        window.jsonSourceUrl = "${jsonUrl}";\n    ${scriptEnd}\n    <script src="assets/js/archive.js">\n'
        content = content[:js_start] + replacement + content[js_end:]
    else:
        print("JS not found!")

    with open('builder.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    modify()
