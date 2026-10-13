"""Generate Abdalla Tech site imagery with Gemini Nano Banana 2 (gemini-3.1-flash-image).

Reads GEMINI_API_KEY from ../.env. Saves PNGs into ./site-assets/.
Run:  python gen_site_images.py            # all images
      python gen_site_images.py --test     # single cheap test image only
"""
import base64, json, os, re, sys, time, urllib.request, urllib.error

MODEL = "gemini-3.1-flash-image"          # Nano Banana 2 — fast + cheap
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
OUT = os.path.join(os.path.dirname(__file__), "site-assets")

def load_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    env = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(env, encoding="utf-8") as f:
        m = re.search(r'GEMINI_API_KEY="?([^"\r\n]+)"?', f.read())
    if not m:
        sys.exit("GEMINI_API_KEY not found in .env")
    return m.group(1)

KEY = load_key()

# Shared brand DNA so every image reads as one system.
BRAND = (
    "Photographic, cinematic, ultra-detailed. Diagnostic Neon aesthetic: near-black "
    "navy background, a single disciplined cyan signal-glow plus a warm amber accent, "
    "clinical off-white key light. Moody, premium, high-end gaming-hardware repair brand. "
    "Shallow depth of field, subtle bokeh, sharp focus on subject. No text, no logos, no watermarks."
)

def portrait(desc):
    return (
        f"Realistic candid portrait photograph of {desc}. Natural friendly expression, "
        f"looking slightly off-camera, relaxed. Lit by soft cyan and amber gaming-setup glow "
        f"in a dark room. {BRAND}"
    )

IMAGES = {
    "hero": (
        "16:9",
        "Wide cinematic hero shot: a high-end gaming PC on a technician's repair bench, "
        "side panel open, RGB fans and a graphics card glowing, thin cyan light rails and "
        "warm amber highlights on the components, a hairline of tools out of focus in the "
        "foreground. Sense of precision and craftsmanship. " + BRAND,
    ),
    "technician-gpu": (
        "16:9",
        "Close cinematic shot of a focused technician's hands using a precision screwdriver "
        "on an open graphics card GPU on an anti-static mat, macro detail on the PCB and "
        "heatsink, cyan probe light and amber solder glow. " + BRAND,
    ),
    "workshop": (
        "16:9",
        "Atmospheric wide shot of a small tidy PC-repair workshop bench at night: shelves of "
        "graphics cards, an oscilloscope readout glowing cyan, tidy cable management, one "
        "gaming PC under a focused clinical light. Empty, clean, professional. " + BRAND,
    ),
    "depoimento-1": ("1:1", portrait("a young Brazilian man in his early 20s, casual gamer, short dark hair, light stubble, wearing a hoodie")),
    "depoimento-2": ("1:1", portrait("a Brazilian woman in her late 20s with curly hair, smiling warmly, wearing a casual t-shirt, esports fan")),
    "depoimento-3": ("1:1", portrait("a Black Brazilian man in his 30s with a short beard and glasses, friendly and confident, wearing a plain dark shirt")),
}

def generate(name, aspect, prompt):
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect},
        },
    }).encode()
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"  [{name}] HTTP {e.code}: {e.read().decode()[:400]}")
        return False
    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        blob = part.get("inlineData") or part.get("inline_data")
        if blob and blob.get("data"):
            os.makedirs(OUT, exist_ok=True)
            path = os.path.join(OUT, f"{name}.png")
            with open(path, "wb") as f:
                f.write(base64.b64decode(blob["data"]))
            print(f"  [{name}] saved -> {path}")
            return True
    print(f"  [{name}] no image in response: {json.dumps(data)[:400]}")
    return False

def main():
    items = list(IMAGES.items())
    if "--test" in sys.argv:
        items = [("hero", IMAGES["hero"])]
    print(f"Model: {MODEL}  |  generating {len(items)} image(s)")
    ok = 0
    for name, (aspect, prompt) in items:
        print(f"- {name} ({aspect})")
        if generate(name, aspect, prompt):
            ok += 1
        time.sleep(1)
    print(f"Done: {ok}/{len(items)} succeeded. Output dir: {OUT}")

if __name__ == "__main__":
    main()
