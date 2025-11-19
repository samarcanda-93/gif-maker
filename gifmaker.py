from PIL import Image, ImageOps
import os

# === CONFIGURATION ===
folder = "images"  # Folder containing input images
output_path = os.path.join(folder, "output.gif")  # Output file
default_duration = 500  # Default duration (ms) per frame
durations = []  # Optional: per-frame durations (in ms)
# durations = [300, 500, 800]    # Uncomment to test per-frame durations

# === FILE COLLECTION ===
allowed_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff")
image_files = sorted(
    [f for f in os.listdir(folder) if f.lower().endswith(allowed_exts)]
)

if not image_files:
    raise FileNotFoundError(f"No image files found in folder: {folder}")

num_images = len(image_files)

# === DURATION CHECK ===
if not durations or any(d == 0 for d in durations):
    print(
        f"ℹ️  No valid durations provided. Using default of {default_duration} ms for all {num_images} frames."
    )
    durations = [default_duration] * num_images
elif len(durations) != num_images:
    raise ValueError(
        f"⚠️  {num_images} images found, but {len(durations)} durations provided."
    )

# === LOAD & PROCESS IMAGES ===
images = []

# Use first image to determine reference size
first_path = os.path.join(folder, image_files[0])
first_img = Image.open(first_path)
first_img = ImageOps.exif_transpose(first_img)
ref_size = first_img.size

for f in image_files:
    path = os.path.join(folder, f)
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)  # Fix orientation
    img = ImageOps.pad(img, ref_size)  #  Pad to uniform size
    if img.mode != "RGB":
        img = img.convert("RGB")  # Convert for GIF
    images.append(img)

# === SAVE GIF ===
images[0].save(
    output_path,
    save_all=True,
    append_images=images[1:],
    duration=durations,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"GIF created at: {output_path}")
