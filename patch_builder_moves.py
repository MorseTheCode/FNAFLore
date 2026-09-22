import sys

def patch_builder_moves():
    with open('builder.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the old moveLogUp and moveLogDown with context-aware ones
    old_funcs = """
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
    
    new_funcs = """
        function moveLogUp(id) {
            const visibleLogs = currentBuilderFilter === 'all' 
                ? appData.logs 
                : appData.logs.filter(l => l.tags.includes(currentBuilderFilter));
                
            const visibleIndex = visibleLogs.findIndex(l => l.id === id);
            if (visibleIndex > 0) {
                const globalIndexCurrent = appData.logs.findIndex(l => l.id === id);
                const globalIndexSwap = appData.logs.findIndex(l => l.id === visibleLogs[visibleIndex - 1].id);
                
                const temp = appData.logs[globalIndexCurrent];
                appData.logs[globalIndexCurrent] = appData.logs[globalIndexSwap];
                appData.logs[globalIndexSwap] = temp;
                
                renderLogs();
            }
        }
        function moveLogDown(id) {
            const visibleLogs = currentBuilderFilter === 'all' 
                ? appData.logs 
                : appData.logs.filter(l => l.tags.includes(currentBuilderFilter));
                
            const visibleIndex = visibleLogs.findIndex(l => l.id === id);
            if (visibleIndex !== -1 && visibleIndex < visibleLogs.length - 1) {
                const globalIndexCurrent = appData.logs.findIndex(l => l.id === id);
                const globalIndexSwap = appData.logs.findIndex(l => l.id === visibleLogs[visibleIndex + 1].id);
                
                const temp = appData.logs[globalIndexCurrent];
                appData.logs[globalIndexCurrent] = appData.logs[globalIndexSwap];
                appData.logs[globalIndexSwap] = temp;
                
                renderLogs();
            }
        }
    """
    
    content = content.replace(old_funcs, new_funcs)

    with open('builder.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Modified builder.html")

if __name__ == '__main__':
    patch_builder_moves()
