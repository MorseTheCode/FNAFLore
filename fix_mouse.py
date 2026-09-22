import sys

def modify_board():
    with open('board.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Change all remaining mousedown/move/up event listeners to pointerdown/move/up
    content = content.replace("addEventListener('mousedown'", "addEventListener('pointerdown'")
    content = content.replace("addEventListener('mousemove'", "addEventListener('pointermove'")
    content = content.replace("addEventListener('mouseup'", "addEventListener('pointerup'")

    with open('board.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed remaining mouse events to pointer events")

if __name__ == '__main__':
    modify_board()
