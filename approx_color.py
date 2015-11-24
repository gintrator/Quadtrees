from PIL import Image
import random
import math
import sys


class QuadTree:

	def __init__(self, depth, size, x, y, tl=None, tr=None, br=None, bl=None, color=(0, 0, 0)):
		self.depth = depth
		self.size = size
		self.x = x
		self.y = y
		self.tl = tl
		self.tr = tr
		self.br = br
		self.bl = bl
		self.is_leaf = (tl == tr == br == bl == None)
		if self.is_leaf:
			self.color = color
		else:
			self.color = ((tl.color[0] + tr.color[0] + br.color[0] + bl.color[0]) / 4,
						  (tl.color[1] + tr.color[1] + br.color[1] + bl.color[1]) / 4,
						  (tl.color[2] + tr.color[2] + br.color[2] + bl.color[2]) / 4)


def create_qtree(arr, width, depth, size, x=0, y=0, level=0):
	if depth == 0:
		return QuadTree(depth, size, x, y, color=arr[y * width + x])
	else:
		offset = size / 2
		return QuadTree(depth, size, x, y,
						create_qtree(arr, width, depth - 1, offset, x + offset, y + offset),
						create_qtree(arr, width, depth - 1, offset, x + offset, y),
						create_qtree(arr, width, depth - 1, offset, x, y + offset),
						create_qtree(arr, width, depth - 1, offset, x, y))


def fill_arr(arr, width, qtree, depth):
	if depth == 0:
		for y in range(qtree.y, qtree.y + qtree.size):
			for x in range(qtree.x, qtree.x + qtree.size):
				arr[y * width + x] = qtree.color
	else:
		fill_arr(arr, width, qtree.tl, depth - 1)
		fill_arr(arr, width, qtree.tr, depth - 1)
		fill_arr(arr, width, qtree.br, depth - 1)
		fill_arr(arr, width, qtree.bl, depth - 1)

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
	depth = int(sys.argv[2])
	img = Image.open(image_name)
	size = img.size[0]
	arr = list(img.getdata())
	#depth = 8
	width = size
	qtree = create_qtree(arr, width, depth, size)
	out = [(255, 255, 255) for _ in range(size**2)]
	fill_arr(out, width, qtree, depth)
	outimage_name = "{0}_out.tiff".format(image_name.split(".")[0])
	writeimage(outimage_name, out, size)
	

main()
