"""
ComfyUI Prompt Translator Node
A custom node for translating prompts to different languages
"""

import os
import folder_paths
from .nodes.prompt_translator_node import PromptTranslatorNode, GGUFLoader
from .nodes.show_text_node import ShowTextNode

# Add gguf model folder path
model_path = os.path.join(folder_paths.models_dir, 'gguf')
folder_paths.add_model_folder_path('gguf', model_path)

# Create models/gguf directory if it doesn't exist
if not os.path.exists(model_path):
    os.makedirs(model_path, exist_ok=True)
    print(f"[PromptTranslatorNode] Created directory: {model_path}")
else:
    print(f"[PromptTranslatorNode] Found directory: {model_path}")

NODE_CLASS_MAPPINGS = {
    "GGUFLoader": GGUFLoader,
    "PromptTranslatorNode": PromptTranslatorNode,
    "ShowTextNode": ShowTextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GGUFLoader": "GGUFLoader",
    "PromptTranslatorNode": "Prompt Translator (GGUF)",
    "ShowTextNode": "Show Text",
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
