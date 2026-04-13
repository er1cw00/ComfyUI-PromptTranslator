"""
GGUF Translator using llama-cpp
Reference: demo.py
"""

import os
import gc
import torch
from llama_cpp import Llama


class GGUFTranslator:
    """
    Translator using llama-cpp to run GGUF models.
    Supports translation to English or Chinese based on target language.
    """

    # System prompts for different target languages
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
        "Chinese (Simplified)": (
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

    def __init__(self, model_path: str, target_language: str = "English", device: str = "cpu", n_gpu_layers: int = -1):
        """
        Initialize the GGUF translator.

        Args:
            model_path: Full path to the .gguf model file
            target_language: Target language (English or Chinese (Simplified))
            device: Device to use for inference (cpu, cuda, mps)
            n_gpu_layers: Number of GPU layers (-1 for all), only used when device=cuda
        """
        self.model_path = model_path
        self.target_language = target_language
        self.device = device
        self.n_gpu_layers = 0  # CPU only by default
        self.llm = None

        # GPU layer configuration based on device selection
        if device == "cuda" and torch.cuda.is_available():
            # Use user-specified n_gpu_layers, -1 means all layers
            self.n_gpu_layers = n_gpu_layers
        elif device == "mps" and torch.backends.mps.is_available():
            # MPS uses GPU layers for acceleration
            self.n_gpu_layers = -1

        # Model parameters
        self.n_ctx = 4096
        self.n_threads = 4

    def load(self):
        """Load the GGUF model if not already loaded."""
        if self.llm is None:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found: {self.model_path}")

            print(f"[GGUFTranslator] Loading model: {self.model_path}")
            print(f"[GGUFTranslator] GPU layers: {self.n_gpu_layers}")

            self.llm = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.n_gpu_layers,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                verbose=False,
            )
        return self.llm

    def translate(self, prompt_text: str) -> str:
        """
        Translate the prompt using the loaded model.

        Args:
            prompt_text: The input text to translate

        Returns:
            Translated text
        """
        if not prompt_text or not prompt_text.strip():
            return ""

        # Get system prompt for target language
        sys_prompt = self.SYSTEM_PROMPTS.get(
            self.target_language,
            self.SYSTEM_PROMPTS["English"]
        )

        messages = [
            {
                "role": "system",
                "content": sys_prompt,
            },
            {
                "role": "user",
                "content": prompt_text,
            }
        ]

        llm = self.load()

        output = llm.create_chat_completion(
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            repeat_penalty=1.05,
            max_tokens=4096
        )

        result = output["choices"][0]["message"]["content"]
        return result.strip()

    def unload(self):
        """Unload the model to free memory."""
        if self.llm is not None:
            del self.llm
            self.llm = None
            gc.collect()
            if self.device == "cuda" and torch.cuda.is_available():
                torch.cuda.empty_cache()
            elif self.device == "mps" and torch.backends.mps.is_available():
                torch.mps.empty_cache()
            print("[GGUFTranslator] Model unloaded")


# Global translator cache to avoid reloading models
_translator_cache = {}


def get_translator(model_path: str, target_language: str, device: str = "cpu", n_gpu_layers: int = -1) -> GGUFTranslator:
    """
    Get or create a cached translator instance.

    Args:
        model_path: Path to the GGUF model
        target_language: Target language
        device: Device to use for inference (cpu, cuda, mps)
        n_gpu_layers: Number of GPU layers (-1 for all), only used when device=cuda

    Returns:
        GGUFTranslator instance
    """
    cache_key = f"{model_path}:{target_language}:{device}:{n_gpu_layers}"

    if cache_key not in _translator_cache:
        _translator_cache[cache_key] = GGUFTranslator(model_path, target_language, device, n_gpu_layers)

    return _translator_cache[cache_key]


def clear_translator_cache():
    """Clear all cached translators."""
    global _translator_cache
    for translator in _translator_cache.values():
        translator.unload()
    _translator_cache.clear()
