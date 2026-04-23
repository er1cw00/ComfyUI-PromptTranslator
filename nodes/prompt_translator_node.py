"""
Prompt Translator Node Implementation
Uses GGUF models via llama-cpp for translation.
"""

import os
import folder_paths
import comfy.utils
import comfy.model_management as mm
from llama_cpp import Llama


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

class GGUFLoader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        gguf_models = get_gguf_models()
        return {
            "required": {
                "model": (gguf_models if gguf_models else ["none"], {
                    "default": gguf_models[0] if gguf_models else "none"
                }),
                "device": (["cpu", "cuda", "mps"], {
                    "default": "cpu"
                }),
                "n_gpu_layers": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 4096,
                    "step": 1,
                    "tooltip": "Number of GPU layers (-1 for all, 0 for CPU). Only used when device=cuda"
                }),
            }
        }

    RETURN_TYPES = ("LLAMACPPMODEL",)
    RETURN_NAMES = ("llama_model",)
    FUNCTION = "load_model"
    CATEGORY = "utils/prompt"
    
    @staticmethod
    def _get_model_path(model):
        """Get the full path of the selected model."""
        if not model or model == "none":
            return ""
        model_path = os.path.join(folder_paths.models_dir, 'gguf', model)
        return model_path if os.path.exists(model_path) else ""
    
    def load_model(self, model, device, n_gpu_layers):
        mm.soft_empty_cache()
        
        custom_config = {
            "model": model,
        }
        if not hasattr(self, "model") or custom_config != self.current_config:
            self.current_config = custom_config

            full_model_path = self._get_model_path(model)

            if not full_model_path:
                raise ValueError(f"Model file not found: {model}")
            
            print(f"Loading gguf model from {full_model_path}")

            llm = Llama(
                model_path=full_model_path,
                n_gpu_layers=n_gpu_layers,
                n_ctx=4096,
                n_threads=4,
                verbose=False,
            )
        return (llm,)

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
                "llama_model": ("LLAMACPPMODEL",),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Enter your prompt here..."
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
    FUNCTION = "translate"
    CATEGORY = "utils/prompt"
    OUTPUT_NODE = False

    TARGET_LANGUAGE_CODES = {
        "English": "en",
        "Chinese": "zh-CN",
    }
    SYSTEM_PROMPTS = {
        "English": (
            "You are a professional prompt engineer. "
            "Your task is to translate prompts and enhance prompts for image generation tools "
            "like ComfyUI or Stable Diffusion. "
            "Translate the user's prompt into fluent, expressive English. "
            "Rules:\n"
            "- Keep all style tags, weights, parentheses, and comma-separated structure.\n"
            "- Preserve artistic keywords and rendering parameters.\n"
            "- Do not remove NSFW tags if present.\n"
            "- Translate it into a clear action-oriented phrase in English.\n"
            "- Make the translation sound natural and expressive.\n"
            "- Output only the English translation.\n"
            "No explanation. No extra text."
        ),
        "Chinese": (
            "您是专业的图像编辑提示词工程师，你的任务是将用户的提示翻译成中文。\n"
            "规则：\n"
            "- 保留所有样式标签、括号和逗号分隔的结构。\n"
            "- 保留艺术关键词和渲染参数。\n"
            "- 如果存在 NSFW 标签，请勿移除。\n"
            "- 翻译主体描述时，避免死板直译，使其听起来像自然的中文口语，画面感更强。\n"
            "- 仅输出中文翻译。\n"
            "无需解释，无需额外文本。"
        ),
    }

    def translate(self, llama_model, prompt, target_language, device="cpu", n_gpu_layers=-1, auto_release=True):
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
        
        sys_prompt = self.SYSTEM_PROMPTS.get(
            target_language,
            self.SYSTEM_PROMPTS["English"]
        )

        messages = [
            {
                "role": "system",
                "content": sys_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
        try:
            # Import here to avoid loading if not needed
            output = llama_model.create_chat_completion(
                        messages=messages,
                        temperature=0.7,
                        top_p=0.9,
                        repeat_penalty=1.05,
                        max_tokens=4096
                    )

            result = output["choices"][0]["message"]["content"]
            translated = result.strip()

            # # Release model only if auto_release is True
            # if auto_release:
            #     translator.unload()

            return (translated, prompt)

        except Exception as e:
            print(f"[PromptTranslator] Translation error: {e}")
            # Return original prompt if translation fails
            return (prompt, prompt)

