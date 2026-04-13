# ComfyUI-PromptTranslator

[English](README_EN.md) | 中文

一个基于本地 GGUF 模型的 ComfyUI 自定义节点，用于翻译文生图提示词。使用 llama-cpp-python 驱动，支持任何语言翻译成中文或者英文，无需联网或 API Key。

## 功能特性

- **本地翻译**：使用 GGUF 模型通过 llama-cpp-python 运行，无需联网
- **自动语言检测**：使用 langdetect 自动识别输入语言
- **中英双语支持**：支持翻译成英文或中文（简体）
- **GPU 加速**：自动检测并使用 GPU（CUDA）加速
- **模型缓存**：已加载的模型会被缓存，避免重复加载

## 1. 安装方法

### 要求

- Python 3.10+
- 已安装 ComfyUI

### 安装节点

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI-PromptTranslator.git
cd ComfyUI-PromptTranslator
pip install -r requirements.txt
```
重启 ComfyUI


## 2. 模型目录

### GGUF 模型存放位置

下载 `.gguf` 模型文件放在models/gguf目录下：

```
ComfyUI/
├── models/
│   └── gguf/           
│       ├── Qwen2.5-7B-Instruct-Q4_K_M.gguf
│       ├── Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf
│       └── ...
```

节点会自动：
1. 启动时创建 `models/gguf/` 目录（如果不存在）
2. 扫描并列出所有 `.gguf` 文件到下拉菜单

### 推荐模型

| 模型 | 大小 | 下载链接 |
|------|------|----------|
| Qwen2.5-7B-Instruct-Q4_K_M.gguf | ~4.7GB | [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF) |
| Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf | ~4.7GB | [HuggingFace](https://huggingface.co/QuantFactory/Qwen2.5-7B-Instruct-Uncensored-GGUF/resolve/main/Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf) |

**注意**：模型越大翻译质量越好，但需要更多显存/内存。


## 3. 使用指南

### 截图

![节点截图](docs/screenshot.png)


## 许可证

MIT License

