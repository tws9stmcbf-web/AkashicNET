from pathlib import Path


SOURCE = Path("website/app/living-library-map/page.tsx")


def test_touch_focus_and_compatibility_mouse_entry_cannot_consume_first_tap():
    source = SOURCE.read_text(encoding="utf-8")

    assert 'const pointerType = useRef<string | null>(null);' in source
    assert 'pointerType.current !== "touch"' in source
    assert 'onPointerEnter={(event) => {' in source
    assert 'if (event.pointerType === "mouse") setActive(node);' in source
    assert 'onMouseEnter={() => setActive(node)}' not in source
    assert 'window.matchMedia("(hover: none)")' not in source


def test_touch_activation_uses_event_modality_and_requires_selected_node():
    source = SOURCE.read_text(encoding="utf-8")

    assert 'const isKeyboard = event.detail === 0;' in source
    assert 'pointerType.current === "touch" && active?.id !== node.id' in source
    assert 'onPointerDown={(event) => { pointerType.current = event.pointerType; }}' in source
    assert 'onClick={(event) => choose(event, node)}' in source
    assert 'if (isTouchFirst)' in source
    assert 'setActive(node);' in source
    assert 'window.location.href = node.href;' in source


def test_keyboard_activation_remains_single_step():
    source = SOURCE.read_text(encoding="utf-8")

    assert 'const isKeyboard = event.detail === 0;' in source
    assert '!isKeyboard && pointerType.current === "touch"' in source
    assert 'pointerType.current = null;' in source
