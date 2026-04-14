# ComfyUI-PromptTranslator

[English](README.md) | 中文

一个基于本地 GGUF 模型的 ComfyUI 自定义节点，用于翻译文生图提示词。使用 llama-cpp-python 驱动，支持任何语言翻译成中文或者英文，无需联网或 API Key。

## 功能特性

- **本地翻译**：使用 GGUF 模型通过 llama-cpp-python 运行，无需联网
- **中英双语支持**：支持翻译成英文或中文（简体）
- **显存优化**：翻译完成后自动卸载模型，不占用显存
- **文本显示节点**：内置 ShowTextNode 用于调试和展示翻译结果

## 1. 安装方法

### 要求

- Python 3.10+
- 已安装 ComfyUI

### 安装节点

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/er1cw00/ComfyUI-PromptTranslator.git
cd ComfyUI-PromptTranslator
pip install -r requirements.txt
```
重启 ComfyUI


## 2. 模型目录

### GGUF 模型存放位置

请手动下载 `.gguf` 模型文件放在models/gguf目录下：

```
ComfyUI/
├── models/
│   └── gguf/           
│       ├── Qwen2.5-7B-Instruct-Q4_K_M.gguf
│       ├── Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf
│       └── ...
```

节点会自动：
1. 扫描并列出`models/gguf/` 目录下所有 `.gguf` 文件到下拉菜单
2. 如果 `models/gguf/` 目录不存在，启动时将会自动创建

### 推荐模型

| 模型 | 大小 | 下载链接 |
|------|------|----------|
| Qwen2.5-7B-Instruct-Q4_K_M.gguf | ~4.7GB | [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF) |
| Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf | ~4.7GB | [HuggingFace](https://huggingface.co/QuantFactory/Qwen2.5-7B-Instruct-Uncensored-GGUF/resolve/main/Qwen2.5-7B-Instruct-Uncensored.Q4_K_M.gguf) |

**注意**：模型越大翻译质量越好，但需要更多显存/内存。


## 3. 使用指南

### Prompt Translator 节点

- **prompt**: 输入需要翻译的提示词
- **model**: 选择 GGUF 模型
- **device**: 选择推理设备 (cpu/cuda/mps)
- **n_gpu_layers**: GPU 层数（仅 device=cuda 时生效，-1 表示全部层使用 GPU）
- **target_language**: 目标语言（English 或 Chinese (Simplified)）

### Show Text 节点

用于显示和调试文本内容，可将 PromptTranslatorNode 的翻译结果可视化。

- **text**: 输入文本（支持连接到其他节点的 STRING 输出）
- 节点上会实时显示输入的文本内容

![节点截图](docs/screenshot.png)


## 许可证

MIT License

