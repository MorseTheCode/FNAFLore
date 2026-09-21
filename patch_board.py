import sys

def modify_board():
    with open('board.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add touch-action: none to body CSS
    content = content.replace('user-select: none;', 'user-select: none;\n            touch-action: none;')

    # 2. Change mouse events to pointer events in listeners
    content = content.replace("container.addEventListener('mousedown', handleMouseDown);", "container.addEventListener('pointerdown', handleMouseDown);")
    content = content.replace("window.addEventListener('mousemove', handleMouseMove);", "window.addEventListener('pointermove', handleMouseMove);")
    content = content.replace("window.addEventListener('mouseup', handleMouseUp);", "window.addEventListener('pointerup', handleMouseUp);\n            window.addEventListener('pointercancel', handleMouseUp);")
    content = content.replace("menu.addEventListener('mousedown'", "menu.addEventListener('pointerdown'")

    # 3. Inside inline handlers
    content = content.replace('onmousedown="', 'onpointerdown="')
    content = content.replace('onmousemove="', 'onpointermove="')
    content = content.replace('onmouseup="', 'onpointerup="')

    # 4. Inject e.isPrimary check into event handlers to prevent multi-touch glitches
    content = content.replace("function handleMouseDown(e) {", "function handleMouseDown(e) {\n            if (e.pointerId !== undefined && !e.isPrimary) return;")
    content = content.replace("function handleMouseMove(e) {", "function handleMouseMove(e) {\n            if (e.pointerId !== undefined && !e.isPrimary) return;")
    content = content.replace("function handleMouseUp(e) {", "function handleMouseUp(e) {\n            if (e.pointerId !== undefined && !e.isPrimary) return;")

    # 5. Fix startItemDrag e.stopPropagation for pointer events inline if any, but replacing 'mousedown' in HTML string templates:
    content = content.replace("onmousedown='startItemDrag(event,", "onpointerdown='startItemDrag(event,")

    with open('board.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Modified board.html correctly")

if __name__ == '__main__':
    modify_board()
