"""
Show Text Node Implementation
A simple node for displaying text content in ComfyUI.
"""


class ShowTextNode:
    """
    A ComfyUI node that displays text content.
    Useful for debugging and showing translation results.

    Connect PromptTranslatorNode's "translated" output to this node's "text" input.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "forceInput": True,  # 允许从其他节点接收输入
                }),
            }
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "show_text"
    CATEGORY = "utils/prompt"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    def show_text(self, text):
        """Display the input text on the node."""
        return {"ui": {"text": text}, "result": (text,)}
