import math

palette = [
    (0.0, 0.0, 1.0),
    (0.0, 0.5, 0.5),
    (0.0, 1.0, 0.0),
    (0.5, 0.5, 0.0),
    (1.0, 0.0, 0.0),
]

def get_color(t: float) -> tuple[float, float, float]:
    assert len(palette) > 1
    assert t >= 0.0 and t <= 1.0

    # Find the fractional index position across the color segments
    max_idx = len(palette) - 1
    scaled_t = t * max_idx
    
    # Determine the lower and upper bounding color indices
    idx_low = int(scaled_t)
    idx_high = min(idx_low + 1, max_idx)
    
    # Extract the precise interpolation factor between these two specific colors
    local_t = scaled_t - idx_low
    
    # Get the bounding color channels
    r1, g1, b1 = palette[idx_low]
    r2, g2, b2 = palette[idx_high]
    
    # Perform standard linear interpolation (lerp) per channel
    r = r1 + (r2 - r1) * local_t
    g = g1 + (g2 - g1) * local_t
    b = b1 + (b2 - b1) * local_t
    
    # Return as integers if dealing with 0-255 ranges, or floats for 0-1 ranges
    return (r, g, b)


def create_materials(filename: str, num_steps: list[dict]):
    with open(filename, 'w') as f:
        for idx in range(num_steps):
            t = idx / (num_steps - 1)
            color = get_color(t)
            f.write('\n\n')
            f.write(f'newmtl mat-{idx}\n')
            f.write(f'Ka 0.0 0.0 0.0\n')
            f.write(f'Kd {color[0]} {color[1]} {color[2]}\n')
            f.write(f'Ks 0.0 0.0 0.0\n')
            f.write(f'd 1.0\n')
    print('Saved to', filename)


def get_material_name(t: float, num_steps: int) -> str:
    curved = math.atan(t * 20) * 0.65
    idx = round(curved * (num_steps - 1))
    return f'mat-{idx}'


if __name__ == "__main__":
    print(get_color(0.1))
    print(get_color(0.5))
    print(get_color(0.9))