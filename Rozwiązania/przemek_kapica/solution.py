from PIL import Image
import os
import re
import csv
import numpy as np
import pandas as pd

data = []

for item in os.listdir('images/'):
	img = Image.open('images/{}'.format(item))

	filename = item
	description = item[12:re.search(r"\d", item).start()].replace('-', ' ')
	photo_id = item[re.search(r"\d", item).start():-4]
	width, height = img.size
	average_color = img.resize((1, 1)).getpixel((0, 0)) # scaled using nearest neighbour algorithm
	
	img_grayscale = img.convert('L')
	pixel_map = np.array(img_grayscale)
	median = np.median(pixel_map)

	x_coord = int(np.floor(np.argmax(pixel_map) / width))
	y_coord = int(np.argmax(pixel_map) - np.floor(np.argmax(pixel_map) / width) * width)

	data.append([filename, description, photo_id, width, height, average_color, median, x_coord, y_coord])


data_frame = pd.DataFrame(data, columns=['filename', 'description', 'photo_id', 'width', 'height', 'average_color', 'median', 'brightest_pixel_x_coord', 'brightest_pixel_y_coord'])
data_frame.to_csv('images.csv', index=False)

os.system('mkdir agg-images')
for i in range(5):
	os.system('mkdir agg-images/{}-images'.format(i + 1))

id_list = data_frame.sort_values(by=['median'])[['filename']]

dir_num = 1
counter = 0
for row in id_list.iterrows():
	for filename in row[1]:
		os.system('cp images/{} agg-images/{}-images/{}'.format(filename, dir_num, filename))
		counter += 1
		if counter == 4:
			counter = 0
			dir_num += 1

os.system('zip -r agg-images.zip agg-images')