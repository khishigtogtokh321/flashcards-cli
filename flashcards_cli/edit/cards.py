"""Compatibility stubs for the removed flashcards-core editor.

The current project is a standalone file-based CLI. Keeping these names importable
prevents old imports from pulling in the obsolete flashcards_core dependency.
"""


def _unsupported_editor(*args, **kwargs):
    raise RuntimeError("The flashcards_core editor is not available in the standalone CLI.")


edit_cards = _unsupported_editor
create_card = _unsupported_editor
update_card = _unsupported_editor
delete_card = _unsupported_editor
