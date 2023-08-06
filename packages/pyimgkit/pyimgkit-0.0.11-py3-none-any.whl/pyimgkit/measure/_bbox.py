import numpy as np
from scipy.spatial import ConvexHull

def obb(in_points, with_axes=False):
	'''object-oriented bounding box'''
	
	# convex hull
	_ch = ConvexHull(in_points)
	in_points = _ch.points[_ch.vertices]
	
	# eigenvalues and eigenvectors
	val, vec = np.linalg.eig(np.cov(in_points, y=None, rowvar=0, bias=1))
	vec = np.transpose(vec)

	# use the inverse of the eigenvectors as a rotation matrix and rorate the points 
	# so they align with the x,y,z(in case of 3D) axes
	points_rotated = np.dot(in_points, np.linalg.inv(vec))
	# get the minimum and maxmum values of each axis
	vmin = np.min(points_rotated, axis=0)
	vmax = np.max(points_rotated, axis=0)
	diff = (vmax - vmin) * .5
	# center could be got half way b/w min and max of each axis
	center = vmin + diff

	# get the corners
	n_dim = len(center)
	if n_dim == 2: signs = [[-1, -1], [1 , -1], [1, 1], [-1, 1]]
	elif n_dim == 3: signs = [[-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1], [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]]
	corners = []
	for _sign in signs:
		corners.append(center + _sign * diff)
	corners = np.array(corners)
	
	# get the long and short axes
	if with_axes:
		longaxis, shortaxis = np.argmax(diff), np.argmin(diff)
		
		diffs = np.zeros(n_dim)
		diffs[longaxis] = diff[longaxis]
		longaxis = [center - diffs, center + diffs]

		diffs = np.zeros(n_dim)
		diffs[shortaxis] = diff[shortaxis]
		shortaxis = [center - diffs, center + diffs]
		
		return np.dot(center, vec), np.dot(corners, vec), np.dot(longaxis, vec), np.dot(shortaxis, vec)
	return np.dot(center, vec), np.dot(corners, vec)
