import pytest
from src.gui.components.set_dialog import SetDialog
import customtkinter as ctk

@pytest.fixture
def setup_dialog():
    """Fixture to create and clean up dialog"""
    try:
        root = ctk.CTk()
        dialog = SetDialog(root)
        yield dialog
        root.destroy()
    except Exception as e:
        pytest.skip(f"GUI test environment not available: {e}")

def test_mixed_stroke_selection(setup_dialog):
    dialog = setup_dialog
    
    # Select mix stroke
    dialog.stroke_var.set("mix")
    dialog.on_stroke_change("mix")
    
    # Select some strokes
    dialog.mixed_strokes["freestyle"].set(True)
    dialog.mixed_strokes["butterfly"].set(True)
    
    # Set required fields using StringVars
    dialog.distance_var.set("100")
    dialog.reps_var.set("4")
    
    result = dialog.get_result()
    assert result["stroke"] == "mix"
    assert "mixed_strokes" in result
    assert set(result["mixed_strokes"]) == {"freestyle", "butterfly"}

def test_mixed_stroke_validation(setup_dialog):
    dialog = setup_dialog
    
    # Select mix without selecting strokes
    dialog.stroke_var.set("mix")
    dialog.on_stroke_change("mix")
    
    # Set required fields using StringVars
    dialog.distance_var.set("100")
    dialog.reps_var.set("4")
    
    with pytest.raises(ValueError, match="Please select at least one stroke for mix"):
        dialog.get_result()