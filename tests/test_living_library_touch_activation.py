from pathlib import Path


SOURCE = Path("website/app/living-library-map/page.tsx")


def test_touch_focus_cannot_consume_first_tap():
    source = SOURCE.read_text(encoding="utf-8")

    assert 'const preview = (node: Node)' in source
    assert 'if (!window.matchMedia("(hover: none)").matches)' in source
    assert 'onFocus={() => preview(node)}' in source
    assert 'onFocus={() => setActive(node)}' not in source


def test_touch_activation_still_requires_selected_node():
    source = SOURCE.read_text(encoding="utf-8")

    assert 'const isTouchFirst = (node: Node)' in source
    assert 'active?.id !== node.id' in source
    assert 'if (isTouchFirst(node))' in source
    assert 'setActive(node);' in source
    assert 'window.location.href = node.href;' in source
