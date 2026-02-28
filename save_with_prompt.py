import os
import re
import numpy as np
from PIL import Image
import folder_paths


class SaveWithPrompt:
    """
    Saves a decoded image (from VAE Decode) as PNG and optionally saves
    positive/negative prompts as a matching TXT file.

    Output naming: <output_dir>/<prefix>_1.png, <prefix>_1.txt, etc.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images":          ("IMAGE",),
                "output_dir":      ("STRING", {"default": folder_paths.get_output_directory()}),
                "filename_prefix": ("STRING", {"default": "output"}),
            },
            "optional": {
                "positive_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "negative_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "save_prompt_txt": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "image/output"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _next_counter(output_dir: str, prefix: str) -> int:
        """Return the next available counter so files are never overwritten."""
        pattern = re.compile(rf"^{re.escape(prefix)}_(\d+)\.(png|txt)$", re.IGNORECASE)
        existing = set()
        if os.path.isdir(output_dir):
            for fname in os.listdir(output_dir):
                m = pattern.match(fname)
                if m:
                    existing.add(int(m.group(1)))
        counter = 1
        while counter in existing:
            counter += 1
        return counter

    @staticmethod
    def _tensor_to_pil(image_tensor) -> Image.Image:
        """Convert a ComfyUI IMAGE tensor (H,W,C float32 0-1) to a PIL Image."""
        arr = image_tensor.cpu().numpy()
        arr = (arr * 255).clip(0, 255).astype(np.uint8)
        return Image.fromarray(arr)

    # ------------------------------------------------------------------
    # Main
    # ------------------------------------------------------------------

    def save(
        self,
        images,
        output_dir: str,
        filename_prefix: str,
        positive_prompt: str = "",
        negative_prompt: str = "",
        save_prompt_txt: bool = True,
    ):
        os.makedirs(output_dir, exist_ok=True)

        saved_files = []

        for image_tensor in images:
            counter = self._next_counter(output_dir, filename_prefix)
            base_name = f"{filename_prefix}_{counter}"

            # ── Save PNG ──────────────────────────────────────────────
            png_path = os.path.join(output_dir, f"{base_name}.png")
            pil_img = self._tensor_to_pil(image_tensor)
            pil_img.save(png_path, format="PNG", optimize=False)
            saved_files.append(png_path)

            # ── Save TXT ──────────────────────────────────────────────
            if save_prompt_txt and (positive_prompt or negative_prompt):
                txt_path = os.path.join(output_dir, f"{base_name}.txt")
                lines = []
                if positive_prompt:
                    lines.append(positive_prompt.strip())
                if negative_prompt:
                    if lines:
                        lines.append("")
                    lines.append(negative_prompt.strip())
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                saved_files.append(txt_path)

        print(f"[SaveWithPrompt] Saved {len(saved_files)} file(s):")
        for p in saved_files:
            print(f"  {p}")

        return {}


# ------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------
NODE_CLASS_MAPPINGS = {
    "SaveWithPrompt": SaveWithPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWithPrompt": "Save With Prompt",
}
