import sys

def add_polyfill():
    with open('board.html', 'r', encoding='utf-8') as f:
        content = f.read()

    polyfill = """
    <!-- Mobile Touch Polyfill -->
    <script>
        (function() {
            function touchHandler(event) {
                var touch = event.changedTouches[0];
                var simulatedEvent = document.createEvent("MouseEvent");
                
                var type = "";
                switch(event.type) {
                    case "touchstart": type = "mousedown"; break;
                    case "touchmove":  type = "mousemove"; break;
                    case "touchend":   type = "mouseup";   break;
                    case "touchcancel":type = "mouseup";   break;
                    default: return;
                }

                // If touching an input or editable area, allow native behavior
                if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA' || event.target.isContentEditable || event.target.closest('.editable')) {
                    if (type === 'mousedown') return; // let native focus happen
                }

                simulatedEvent.initMouseEvent(type, true, true, window, 1,
                    touch.screenX, touch.screenY,
                    touch.clientX, touch.clientY, false,
                    false, false, false, 0, null);

                touch.target.dispatchEvent(simulatedEvent);
                
                // Prevent default to avoid scrolling/zooming while dragging, 
                // UNLESS it's an editable element or button where we want native clicks.
                if (!event.target.closest('button') && !event.target.closest('.editable') && !event.target.closest('input')) {
                    if (event.cancelable) event.preventDefault();
                }
            }

            document.addEventListener("touchstart", touchHandler, {passive: false});
            document.addEventListener("touchmove", touchHandler, {passive: false});
            document.addEventListener("touchend", touchHandler, {passive: false});
            document.addEventListener("touchcancel", touchHandler, {passive: false});
            
            // Apply touch-action none to body to prevent native scrolling interference
            document.body.style.touchAction = "none";
        })();
    </script>
    """

    content = content.replace("</body>", polyfill + "\n</body>")

    with open('board.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Polyfill added to board.html")

if __name__ == '__main__':
    add_polyfill()
