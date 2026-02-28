# SaveWithPrompt — ComfyUI Custom Node

Saves generated images **and** their prompts with matching filenames:

```
prefix_1.png  /  prefix_1.txt
prefix_2.png  /  prefix_2.txt
...
```

---

## Installation

1. Clone this repo into the custom_nodes folder

2. Restart ComfyUI.

3. Search for **"Save With Prompt"** in the node menu.

---
## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `images` | IMAGE | ✅ | Connect from **VAE Decode** |
| `output_dir` | STRING | ✅ | Full path to output folder |
| `filename_prefix` | STRING | ✅ | Prefix for all files (e.g. `my_run`) |
| `positive_prompt` | STRING | optional | Connect from your text encoder / prompt node |
| `negative_prompt` | STRING | optional | Connect from your negative text encoder |
| `save_prompt_txt` | BOOLEAN | optional | Toggle TXT saving on/off (default: true) |

---

## Wiring in your workflow

```
VAE Decode [IMAGE] ──────────────────────────────→ Save With Prompt [images]
CR Prompt List [prompt] → TextEncodeQwenImageE → (also pipe raw string) → [positive_prompt]
Negative prompt string ──────────────────────────→ [negative_prompt]
```

> **Tip:** To get the raw prompt string (not the conditioning), connect the
> text output of your prompt node directly. For `CR Prompt List`, use the
> `prompt` output port.

---

## Output TXT format
If the user has connected both positive and negative they will show like this:
```
hyper-realistic frontal head shot, natural soft light ...

blurry, low quality, watermark ...
```
Otherwise if one is not connected the other will be exported
