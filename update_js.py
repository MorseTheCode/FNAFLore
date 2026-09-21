import sys

def modify_js():
    with open('assets/js/archive.js', 'r', encoding='utf-8') as f:
        content = f.read()

    new_init = """async function init() {
    const jsonUrl = window.jsonSourceUrl || "classic.json";
    const absoluteUrl = new URL(jsonUrl, window.location.href).href;
    const cacheKey = 'mcm_archive_cache_' + absoluteUrl.replace(/[^a-zA-Z0-9]/g, '_');
    const cached = localStorage.getItem(cacheKey);
    
    if (cached) {
        try {
            appData = JSON.parse(cached);
            populateUI();
            render();
            setTimeout(() => { updateArrows('filterBar'); }, 100);
        } catch(e) {}
    }

    try {
        const response = await fetch(jsonUrl + '?t=' + Date.now(), { cache: 'no-store' });
        if(!response.ok) throw new Error("Network response was not ok");
        const serverData = await response.json();
        
        appData = serverData;
        localStorage.setItem(cacheKey, JSON.stringify(appData));
        populateUI();
        render();
        setTimeout(() => { updateArrows('filterBar'); }, 100);
    } catch (error) {
        console.error("Failed to load archive data:", error);
        if (!cached) {
            document.getElementById('page-title').textContent = "CONNECTION ERROR";
            document.getElementById('page-subtitle').textContent = "Failed to retrieve databank. Make sure content json is accessible.";
        }
    }
}"""

    # find the start and end of init()
    start = content.find('async function init() {')
    end = content.find('\n}\n\nfunction populateUI()') + 2 # include closing brace

    if start != -1 and end != -1:
        content = content[:start] + new_init + content[end:]
        with open('assets/js/archive.js', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated archive.js")
    else:
        print("Could not find init() in archive.js")

if __name__ == '__main__':
    modify_js()
