# comfyui-parse-image

Extract metadata from image.  

## Nodes  
Add node > loaders > ...  

Load Boolean From Image  
Load Int From Image  
Load Float From Image  
Load String From Image  
Load Combo From Image  

## Supported image node types  
LoadImage  
LoadImage //Inspire  
Load image with metadata \[Crystools\]  
Image Load  
PutImage  

## Usage  
The node must be connected to a flow started by supported image node.  

Query format:  \<TITLE|TYPE|ID\>.\<WIDGET_NAME\>  

Load Checkpoint.ckpt_name  
CheckpointLoaderSimple.ckpt_name  
1.ckpt_name  
KSampler.seed  
KSampler\[1\].seed  
...  

Special format:  
width  
height  

## References

- [ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)