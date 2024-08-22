import json
import traceback

from PIL import Image

from server import PromptServer
from aiohttp import web

from PIL import ImageFile, Image, ImageOps
from PIL.PngImagePlugin import PngInfo, PngImageFile

@PromptServer.instance.routes.post("/shinich39/parse-image/load-metadata")
async def load_metadata(request):
  try:
    req = await request.json()
    file_path = req["path"]
    with Image.open(file_path) as image:
      if isinstance(image, PngImageFile):
        return web.json_response({
          "width": image.width,
          "height": image.height,
          "info": image.info,
          "format": image.format,
        })
    return web.Response(status=400)
  except Exception:
    print(traceback.format_exc())
    return web.Response(status=400)

@PromptServer.instance.routes.post("/shinich39/parse-image/save-metadata")
async def save_metadata(request):
  try:
    req = await request.json()
    file_path = req["path"]
    info = req["info"]

    prompt = info["prompt"]
    extra_pnginfo = info["extra_data"]["extra_pnginfo"]

    metadata = PngInfo()
    if prompt is not None:
      metadata.add_text("prompt", json.dumps(prompt))
    if extra_pnginfo is not None:
      for x in extra_pnginfo:
        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

    image = Image.open(file_path)
    image.save(file_path, pnginfo=metadata)

    return web.Response(status=200)
  except Exception:
    print(traceback.format_exc())
    return web.Response(status=400)