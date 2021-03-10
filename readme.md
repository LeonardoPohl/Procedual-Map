# Procedural Map Generation

In this Project we generate a random Map using Perlin Noise and Worley Noise. Random Cities, lakes and Biomes are generated.

## Execution

run

```bash
python3 main.py
```

Then you can choose between the pre configured map and configuring a map.

The Pre Configured map has the following parameters:

```json
{
  'X': 1280, 
  'Y': 720, 
  'simple_water': True, 
  'water_height': 0.3, 
  'lakes': 15, 
  'even_humidity': True, 
  'random_humidity': False, 
  'complex_humidity': False, 
  'humidity': 0.6, 
  'villages': True, 
  'village_count': 6, 
  'roads': True
}
```

Afterwards a seed can be selected. For the figures in the report seed $50$ has been selected, but any number between $1$ and $2^{32} - 1$ can be selected.

The result is then saved to ./results/{X}x{Y}_{random_string}.png