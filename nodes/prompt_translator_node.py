"""
Prompt Translator Node Implementation
Uses GGUF models via llama-cpp for translation.
"""

import os
import folder_paths
from langdetect import detect


def get_gguf_models():
    """Get list of .gguf model files from models/gguf directory."""
    model_path = os.path.join(folder_paths.models_dir, 'gguf')
    if not os.path.exists(model_path):
        return []

    models = []
    for filename in os.listdir(model_path):
        if filename.endswith('.gguf'):
            models.append(filename)

    return sorted(models) if models else []


class PromptTranslatorNode:
    """
    A ComfyUI node that translates prompts using GGUF models.
    Supports translation to English or Chinese.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        gguf_models = get_gguf_models()

        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Enter your prompt here..."
                }),
                "model": (gguf_models if gguf_models else ["none"], {
                    "default": gguf_models[0] if gguf_models else "none"
                }),
                "device": (["cpu", "cuda", "mps"], {
                    "default": "cpu"
                }),
                "n_gpu_layers": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 100,
                    "step": 1,
                    "tooltip": "Number of GPU layers (-1 for all, 0 for CPU). Only used when device=cuda"
                }),
                "target_language": ([
                    "English",
                    "Chinese"
                ], {
                    "default": "English"
                }),
            },
            "optional": {
                "auto_release": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Release model memory after translation"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("translated", "origin",)
    FUNCTION = "translate_prompt"
    CATEGORY = "utils/prompt"
    OUTPUT_NODE = False

    # Mapping from langdetect codes to target language codes
    LANGUAGE_CODES = {
        'en': 'en',
        'zh-cn': 'zh-CN',
        'zh-tw': 'zh-TW',
        'ja': 'ja',
        'ko': 'ko',
        'fr': 'fr',
        'de': 'de',
        'es': 'es',
        'it': 'it',
        'pt': 'pt',
        'ru': 'ru',
        'ar': 'ar',
        'hi': 'hi',
        'th': 'th',
        'vi': 'vi',
        'id': 'id',
        'tr': 'tr',
        'pl': 'pl',
        'nl': 'nl',
        'sv': 'sv',
        'el': 'el',
        'cs': 'cs',
        'ro': 'ro',
        'hu': 'hu',
        'he': 'he',
        'da': 'da',
        'fi': 'fi',
        'no': 'no',
        'uk': 'uk',
        'ms': 'ms',
        'zh': 'zh-CN',
    }

    TARGET_LANGUAGE_CODES = {
        "English": "en",
        "Chinese": "zh-CN",
    }

    @staticmethod
    def _get_model_path(model):
        """Get the full path of the selected model."""
        if not model or model == "none":
            return ""
        model_path = os.path.join(folder_paths.models_dir, 'gguf', model)
        return model_path if os.path.exists(model_path) else ""

    def _detect_language(self, text):
        """Detect the language of the input text using langdetect."""
        try:
            detected = detect(text)
            return self.LANGUAGE_CODES.get(detected, 'auto')
        except Exception as e:
            print(f"[PromptTranslator] Language detection failed: {e}")
            return 'auto'

    def translate_prompt(self, prompt, model, target_language, device="cpu", n_gpu_layers=-1, auto_release=True):
        """
        Translate the prompt using GGUF model.

        Args:
            prompt: The input text to translate
            model: The selected GGUF model file
            target_language: The target language name
            device: The device to use for inference (cpu, cuda, mps)
            n_gpu_layers: Number of GPU layers (-1 for all), only used when device=cuda

        Returns:
            Tuple of (translated_text, original_text)
        """
        if not prompt or not prompt.strip():
            return ("", "")

        # Auto-detect source language
        source_code = self._detect_language(prompt)
        target_code = self.TARGET_LANGUAGE_CODES.get(target_language, "en")

        # Get model full path
        full_model_path = self._get_model_path(model)

        if not full_model_path:
            raise ValueError(f"Model file not found: {model}")

        # Skip translation if source and target are the same
        if source_code == target_code and source_code != 'auto':
            return (prompt, prompt)

        try:
            # Import here to avoid loading if not needed
            from .gguf_translator import GGUFTranslator

            translator = GGUFTranslator(full_model_path, target_language, device, n_gpu_layers)
            translated = translator.translate(prompt)

            # Release model only if auto_release is True
            if auto_release:
                translator.unload()

            return (translated, prompt)

        except Exception as e:
            print(f"[PromptTranslator] Translation error: {e}")
            # Return original prompt if translation fails
            return (prompt, prompt)

