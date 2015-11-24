from PIL import Image
import random
import math
import sys

def has_black(arr, width, blocksize, x_start, y_start):
	for y in range(y_start, y_start + blocksize):
		for x in range(x_start, x_start + blocksize):
			if arr[y * width + x] == (0, 0, 0):
				return True
	return False

def quad_black(depth, out_arr, in_arr, width, blocksize, x_start, y_start):
	if depth <= 0 or not has_black(in_arr, width, blocksize, x_start, y_start):
		for y in range(y_start, y_start + blocksize):
			for x in range(x_start, x_start + blocksize):
				if (x == x_start or x == width - 1 or y == y_start or y == width - 1):
					out_arr[y * width + x] = (0, 0, 0)
				else:
					out_arr[y * width + x] = (255, 255, 255)
	else:
		offset = blocksize / 2
		quad_black(depth - 1, out_arr, in_arr, width, offset, x_start + offset, y_start + offset)
		quad_black(depth - 1, out_arr, in_arr, width, offset, x_start + offset, y_start)
		quad_black(depth - 1, out_arr, in_arr, width, offset, x_start, y_start + offset)
		quad_black(depth - 1, out_arr, in_arr, width, offset, x_start, y_start)


def writeimage(name, pixels, size):
	outimage = Image.new("RGB", (size, size))
	outfile = file(name, mode="w")

	for y in range(size):
		for x in range(size):
			outimage.putpixel((x, y), pixels[y * size + x])
	outimage.save(outfile)

def main():
	if len(sys.argv) < 2:
		print "No input image provided."
		return
	image_name = sys.argv[1]
	img = Image.open(image_name)
	size = img.size[0]

	pixels = list(img.getdata())

	out_pixels = [(255, 255, 255) for _ in range(size**2)]

	quad_black(10, out_pixels, pixels, size, size, 0, 0)

	outimage_name = "{0}_out.tiff".format(image_name.split(".")[0])
	
	writeimage(outimage_name, out_pixels, size)
	

main()
