from PIL import ImageFile, Image, ImageOps
from PIL.PngImagePlugin import PngInfo, PngImageFile

class AnyType(str):
  def __ne__(self, __value: object) -> bool:
    return False

any = AnyType("*")

def get_metadata(file_path):
  try:
    with Image.open(file_path) as image:
      if isinstance(image, PngImageFile):
        return {
          "width": image.width,
          "height": image.height,
          "info": image.info,
          "format": image.format,
        }
    return None
  except:
    return None
  
class LoadBoolean():
  def __init__(self):
    pass

  @classmethod
  def IS_CHANGED(s):
    return float("NaN")

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "image": ("IMAGE",),
        "query": ("STRING", {"default": "",}),
        "boolean": ("BOOLEAN", {"default": False,}),
      },
    }
  
  CATEGORY = "loaders"
  FUNCTION = "exec"
  RETURN_TYPES = ("BOOLEAN",)
  RETURN_NAMES = ("BOOLEAN",)

  def exec(self, image, query, boolean):
    return (boolean,)
  
class LoadInt():
  def __init__(self):
    pass

  @classmethod
  def IS_CHANGED(s):
    return float("NaN")

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "image": ("IMAGE",),
        "query": ("STRING", {"default": "",}),
        "int": ("INT", {"default": 0,}),
      },
    }
  
  CATEGORY = "loaders"
  FUNCTION = "exec"
  RETURN_TYPES = ("INT",)
  RETURN_NAMES = ("INT",)

  def exec(self, image, query, int):
    return (int,)
  
class LoadFloat():
  def __init__(self):
    pass

  @classmethod
  def IS_CHANGED(s):
    return float("NaN")

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "image": ("IMAGE",),
        "query": ("STRING", {"default": "",}),
        "float": ("FLOAT", {"default": 0.00,}),
      },
    }
  
  CATEGORY = "loaders"
  FUNCTION = "exec"
  RETURN_TYPES = ("FLOAT",)
  RETURN_NAMES = ("FLOAT",)

  def exec(self, image, query, float):
    return (float,)
  
class LoadString():
  def __init__(self):
    pass

  @classmethod
  def IS_CHANGED(s):
    return float("NaN")

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "image": ("IMAGE",),
        "query": ("STRING", {"default": "",}),
        "string": ("STRING", {"default": "", "multiline": True}),
      },
    }
  
  CATEGORY = "loaders"
  FUNCTION = "exec"
  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("STRING",)

  def exec(self, image, query, string):
    return (string,)

class LoadCombo():
  def __init__(self):
    pass

  @classmethod
  def IS_CHANGED(s):
    return float("NaN")

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "image": ("IMAGE",),
        "query": ("STRING", {"default": "",}),
        "combo": ("STRING", {"default": "",}),
      },
    }
  
  CATEGORY = "loaders"
  FUNCTION = "exec"
  RETURN_TYPES = (any,)
  RETURN_NAMES = ("COMBO",)

  def exec(self, image, query, combo):
    return (combo,)
