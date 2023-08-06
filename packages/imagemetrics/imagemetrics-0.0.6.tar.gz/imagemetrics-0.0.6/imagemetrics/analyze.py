import cv2
import numpy as np


class ImageMetrics():
	def __init__(self, img, m=2, n=2, path=False):
		# if we pass in a filepath, read it in as cv2 image
		if path:
			img = cv2.imread(img)
		self.img = img
		left_img, right_img = self.split_stereo_into_l_r(img)
		self.left_grids, self.right_grids = self.create_image_grids(left_img, 
		                                                            right_img,
																	m_dim=m,
																	n_dim=n)
		unequal_grids_msg = "left and right grid sizes do not match!"
		assert len(self.left_grids) == len(self.right_grids), unequal_grids_msg
	
	def split_stereo_into_l_r(self, img):
		h, w, c = self.img.shape 
		# Cut the image in half
		width_cutoff = w // 2
		left_img = img[:, :width_cutoff] # left image
		right_img = img[:, width_cutoff:] # right image
		return left_img, right_img

	def crop_for_left_vs_right_differences(self, left_img, right_img):
		left_width, left_height, c = left_img.shape
		right_width, right_height, c = left_img.shape

		# section a middle portion of the left image
		# cut in a bit further from the left hand side
		new_x_start = int(left_width*0.15) 
		new_x_end  = int(left_width*0.95)
		new_y_start = int(left_height*0.05)
		new_y_end = int(left_height*0.95)
		left_img = left_img[new_x_start:new_x_end, new_y_start:new_y_end]

		# section a middle portion of the right image
		# cut in a bit further from the right hand side
		new_x_start = int(right_width*0.05)
		new_x_end = int(right_width*0.85)
		new_y_start = int(right_height*0.05)
		new_y_end = int(right_height*0.95)
		right_img = right_img[new_x_start:new_x_end, new_y_start:new_y_end]

		return left_img, right_img

	def create_image_grids(self, img, m_dim=2, n_dim=2):
		# section the numpy array of the image into m x n 
		tiles = []

		m_width = img.shape[0]//m_dim
		n_height = img.shape[1]//n_dim

		for i in range(0, m_dim):
			for j in range(0, n_dim):
				tile = img[i*m_width:(i+1)*m_width,j*n_height:(j+1)*n_height,:]
				tiles.append(tile)
		return tiles

	def normalize_img(self, img):
		image = img.astype(np.uint8) 
		norm_image = cv2.normalize(image, None, alpha=0, beta=1, 
								   norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
		return np.array(norm_image)
	
	def luminance(self, normalized=False):
		luminance_difference = []

		for i in range(len(self.left_grids)):
			l_grid, r_grid = self.left_grids[i], self.right_grids[i]
			if normalized:
				l_grid = self.normalize_img(l_grid)
				r_grid = self.normalize_img(r_grid)
			l_diff = abs(self.calc_lum(l_grid) - self.calc_lum(r_grid))
			luminance_difference.append(l_diff)	
		return luminance_difference

	def calc_lum(self, img, gamma=1): 
		img = np.power(img, gamma)
		# Luminance values from 
		# http://poynton.ca/notes/colour_and_gamma/GammaFAQ.html#luminance
		weighted_R = .2126*img[:,:,2]
		weighted_G = .7152*img[:,:,1]
		weighted_B = .0722*img[:,:,0]
		return np.mean(weighted_R + weighted_G + weighted_B)

	def sharpness(self, normalized=False):
		sharpness_difference = []

		for i in range(len(self.left_grids)):
			l_grid, r_grid = self.left_grids[i], self.right_grids[i]
			if normalized:
				l_grid = self.normalize_img(l_grid)
				r_grid = self.normalize_img(r_grid)
			s_diff = abs(self.calc_sharpness(l_grid) - 
			             self.calc_sharpness(r_grid))
			sharpness_difference.append(s_diff)
		return sharpness_difference

	def calc_sharpness(self, img):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		return cv2.Laplacian(gray, cv2.CV_64F).var()


	