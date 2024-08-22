from .libs import workflow
from .nodes.parsers import LoadBoolean, LoadInt, LoadFloat, LoadString, LoadCombo

NODE_CLASS_MAPPINGS = {
  "LoadBooleanFromImage": LoadBoolean, 
  "LoadIntFromImage": LoadInt, 
  "LoadFloatFromImage": LoadFloat, 
  "LoadStringFromImage": LoadString, 
  "LoadComboFromImage": LoadCombo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "LoadBooleanFromImage": "Load Boolean From Image", 
  "LoadIntFromImage": "Load Int From Image", 
  "LoadFloatFromImage": "Load Float From Image", 
  "LoadStringFromImage": "Load String From Image", 
  "LoadComboFromImage": "Load Combo From Image",
}
