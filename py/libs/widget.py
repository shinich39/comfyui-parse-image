import json
import traceback

import folder_paths
import comfy

from server import PromptServer
from aiohttp import web

@PromptServer.instance.routes.get("/shinich39/parse-image/get-options")
async def get_options():
  try:
    return web.json_response({
      "samplers": comfy.samplers.KSampler.SAMPLERS,
      "schedulers": comfy.samplers.KSampler.SCHEDULERS,
      "controlnets": folder_paths.get_filename_list("controlnet"),
      "checkpoints": folder_paths.get_filename_list("checkpoints"),
      "loras": folder_paths.get_filename_list("loras"),
      "vaes": folder_paths.get_filename_list("vae"),
    })
  except Exception:
    print(traceback.format_exc())
    return web.Response(status=400)