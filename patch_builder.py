import sys

def modify_builder():
    with open('builder.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add move functions to script
    move_functions = """
        function moveLogUp(id) {
            const index = appData.logs.findIndex(l => l.id === id);
            if (index > 0) {
                const temp = appData.logs[index];
                appData.logs[index] = appData.logs[index - 1];
                appData.logs[index - 1] = temp;
                renderLogs();
            }
        }
        function moveLogDown(id) {
            const index = appData.logs.findIndex(l => l.id === id);
            if (index < appData.logs.length - 1 && index !== -1) {
                const temp = appData.logs[index];
                appData.logs[index] = appData.logs[index + 1];
                appData.logs[index + 1] = temp;
                renderLogs();
            }
        }
    """
    
    # inject before renderLogs
    if 'function renderLogs()' in content and 'function moveLogUp' not in content:
        content = content.replace('function renderLogs() {', move_functions + '\n        function renderLogs() {')

    # 2. Add buttons to log item UI
    # Currently it has a drag-handle div:
    # <div class="cursor-grab active:cursor-grabbing text-zinc-500 hover:text-green-500 transition-colors p-1"
    #      onmousedown="this.closest('.log-item').setAttribute('draggable', 'true')" ... > <svg>...
    
    # Let's find the header of the log div where this happens:
    drag_handle_html = """<div class="cursor-grab active:cursor-grabbing text-zinc-500 hover:text-green-500 transition-colors p-1 hidden md:block" """
    
    # Actually just string replace the block that has the svg for drag handle
    target_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="12" r="1"></circle><circle cx="9" cy="5" r="1"></circle><circle cx="9" cy="19" r="1"></circle><circle cx="15" cy="12" r="1"></circle><circle cx="15" cy="5" r="1"></circle><circle cx="15" cy="19" r="1"></circle></svg>"""
    
    buttons_html = f"""
        <div class="flex flex-col gap-1 md:hidden">
            <button onclick="moveLogUp('${{log.id}}')" class="text-zinc-500 hover:text-green-500 bg-zinc-800 rounded p-1"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg></button>
            <button onclick="moveLogDown('${{log.id}}')" class="text-zinc-500 hover:text-green-500 bg-zinc-800 rounded p-1"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
        </div>
        {target_svg}
    """
    
    content = content.replace(target_svg, buttons_html)
    
    # Hide the drag handle div on mobile by adding hidden md:block, wait the div itself has classes:
    # `div class="cursor-grab active:cursor-grabbing text-zinc-500 hover:text-green-500 transition-colors p-1" ...`
    # It's better to just let the drag handle be there, but the mobile buttons appear next to it.

    with open('builder.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Modified builder.html")

if __name__ == '__main__':
    modify_builder()
