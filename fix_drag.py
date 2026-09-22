import sys

def modify_board():
    with open('board.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add isPrimary check to startItemDrag
    content = content.replace("function startItemDrag(e, id) {", "function startItemDrag(e, id) {\n            if (e.pointerId !== undefined && !e.isPrimary) return;")

    with open('board.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed startItemDrag")

if __name__ == '__main__':
    modify_board()
