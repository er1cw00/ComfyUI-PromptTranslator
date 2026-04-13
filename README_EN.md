# ComfyUI-PromptTranslator

English | [中文](README.md)

A ComfyUI custom node for translating text prompts using local GGUF models. Powered by llama-cpp-python, it supports translation to English or Chinese without requiring internet connection or API keys.

## Features

- **Local Translation**: Uses GGUF models via llama-cpp-python, no internet required
- **Auto Language Detection**: Automatically detects input language using langdetect
- **English & Chinese Support**: Translate to English or Chinese (Simplified)
- **GPU Acceleration**: Automatically uses GPU if available (CUDA)
- **Model Caching**: Loaded models are cached to avoid repeated loading

## 1. Installation

### Prerequisites

- Python 3.8+
- ComfyUI installed

### Install the Node

#### Method 1: Clone into ComfyUI custom nodes

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI-PromptTranslator.git
cd ComfyUI-PromptTranslator
pip install -r requirements.txt
```

#### Method 2: Manual Installation

1. Download and extract this repository to `ComfyUI/custom_nodes/ComfyUI-PromptTranslator/`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Restart ComfyUI

### Requirements

The `requirements.txt` includes:
- `langdetect` - For automatic language detection
- `llama-cpp-python` - For running GGUF models locally

## 2. Model Directory

### Where to place GGUF models

Place your `.gguf` model files in:

```
ComfyUI/
├── models/
│   └── gguf/           
│       ├── Qwen2.5-7B-Instruct-Q4_K_M.gguf
│       ├── Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf
│       └── ...
```

The node will automatically:
1. Create the `models/gguf/` directory on startup (if it doesn't exist)
2. Scan and list all `.gguf` files in the dropdown menu

### Recommended Models

| Model | Size | Download |
|-------|------|----------|
| Qwen2.5-7B-Instruct-Q4_K_M.gguf | ~4.7GB | [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF) |
| Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf | ~4.7GB | [HuggingFace](https://huggingface.co/QuantFactory/Qwen2.5-7B-Instruct-Uncensored-GGUF/resolve/main/Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf) |

**Note**: Larger models provide better translation quality but require more VRAM/RAM.


## 3. Usage Guide

### Screenshot

![Node Screenshot](assets/screenshot.png)

*Place your screenshot image at `assets/screenshot.png`*

## License

MIT License

