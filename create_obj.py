import pandas as pd
import re
from colors import get_color, create_materials, get_material_name

land_value_csv = './data/2025/land_value.csv'
height_scale = 1.0
num_color_steps = 40
x_scale = 100

df = pd.read_csv(land_value_csv)

max_land_value = df['LandValuePerSqFt'].max()
df['norm_height'] = df['LandValuePerSqFt'] / max_land_value

print(df.head())

vertices = []
groups = []

polygon_regex_pattern = re.compile(r"\(\([^\(\)]*\)\)")
vert_regex_pattern = re.compile(r"(\d+\.?\d*) (\d+\.?\d*),?")

for _, row in df.iterrows():
	taxkey = row['Taxkey']
	geometry_str = str(row['geometry'])

	geometry_type = geometry_str.split(' ')[0]

	if geometry_type not in ['POLYGON', 'MULTIPOLYGON']:
		print(f'Skipping {taxkey} because geometry is not a valid')
		print(geometry_str)
		continue

	polygon_strings = polygon_regex_pattern.findall(geometry_str)

	norm_height = row['norm_height']
	z_height = norm_height * height_scale
	color = get_color(norm_height)

	for polygon_index, polygon_str in enumerate(polygon_strings):
		matches = vert_regex_pattern.findall(polygon_str)
		local_vertices = [(float(match[0]), float(match[1])) for match in matches]
		num_verts = len(local_vertices)

		top_vertices = [(x,y,z_height) for x,y in local_vertices]
		bottom_vertices = [(x,y,0.0) for x,y in local_vertices]

		top_face = range(num_verts)
		bottom_face = range(num_verts, num_verts * 2)
		side_faces = []

		for i in range(num_verts):
			a_index = i
			b_index = (i + 1) % num_verts

			face = [a_index, b_index, b_index + num_verts, a_index + num_verts]
			side_faces.append(face)

		offset = len(vertices) + 1

		vertices += top_vertices + bottom_vertices

		group_faces = []

		group_faces.append([i + offset for i in top_face])
		group_faces.append([i + offset for i in bottom_face])

		for face in side_faces:
			group_faces.append([i + offset for i in face])

		groups.append({
			'name': f'group-{taxkey}-{polygon_index}',
			'taxkey': taxkey,
			'address': row['Address'],
			'faces': group_faces,
			'material_name': get_material_name(norm_height, num_color_steps),
		})

min_x = vertices[0][0]
min_y = vertices[0][1]
max_x = vertices[0][0]
max_y = vertices[0][1]

for x,y,z in vertices:
	min_x = min(min_x, x)
	min_y = min(min_y, y)
	max_x = max(max_x, x)
	max_y = max(max_y, y)

if max_x > max_y:
	scale_denom = max_x
else:
	scale_denom = max_y

def normalize_vertex(v: tuple[float, float, float]):
	x,y,z = v
	x = (x - min_x) / scale_denom * x_scale
	y = (y - min_y) / scale_denom * x_scale
	return (x,y,z)

vertices = [normalize_vertex(v) for v in vertices]

vertices = [(y,z,x) for x,y,z in vertices]

out_obj = land_value_csv.replace('.csv', '.obj')

with open(out_obj, 'w') as f:
	for v in vertices:
		f.write(f'v {v[0]} {v[1]} {v[2]}\n')

	for group in groups:
		f.write('\n\n')
		f.write(f'# Taxkey: {group["taxkey"]}\n')
		f.write(f'# Address: {group["address"]}\n')
		f.write(f'g {group["name"]}\n')
		f.write(f'usemtl {group["material_name"]}\n')
		for face in group["faces"]:
			face_line = ' '.join([str(i) for i in face])
			f.write(f'f {face_line}\n')

print('Saved to', out_obj)


out_mtl = land_value_csv.replace('.csv', '.mtl')
create_materials(out_mtl, num_color_steps)