import numpy as np
import cv2

def generate_3d_print_bump_map(width=1024, height=1024, num_layers=200):
    # Create a grid of coordinates
    y = np.linspace(0, num_layers * 2 * np.pi, height)
    x = np.linspace(0, np.pi, width)
    X, Y = np.meshgrid(x, y)

    # 1. Base Layer Lines: Sine wave across the Y axis to simulate extruded filament
    layer_pattern = (np.sin(Y) + 1) / 2.0

    # 2. Plastic Grain: High-frequency noise for the micro-texture of melted plastic
    noise = np.random.normal(scale=0.08, size=(height, width))

    # 3. Mechanical Ringing: Low-frequency wobble across the X axis to simulate printer vibration
    ringing = (np.sin(X * 15) * 0.1)

    # Combine all channels
    bump_map = layer_pattern + noise + ringing

    # Normalize to 0-255 for an 8-bit grayscale image
    bump_map = np.clip(bump_map, 0, 1) * 255
    bump_map = bump_map.astype(np.uint8)

    # Soften the noise with a slight blur to mimic semi-melted plastic rather than sharp digital static
    bump_map = cv2.GaussianBlur(bump_map, (3, 3), 0)

    # Save the output file
    filename = '3d_print_bump_map.jpg'
    cv2.imwrite(filename, bump_map)
    print(f"Texture successfully generated and saved as '{filename}' at {width}x{height}.")

if __name__ == "__main__":
    generate_3d_print_bump_map()