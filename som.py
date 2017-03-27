import random
import math
from Tkinter import *

class Node:
	def __init__(self, size, coords):
		self.weights = []
		for i in range(size):
			self.weights.append(random.random())
		self.coords = coords
		self.center = [coords[0]+coords[2]/2, coords[1]+coords[3]/2]
	
	def update_weights(self, target, learning_rate, influence):
		for i in range(len(self.weights)):
			self.weights[i] += learning_rate * influence * (target[i]-self.weights[i])
		
	def update_pos(self, main):
		for i in range(len(self.center)):
			self.center[i] += 0.01 * learning_rate * influence * (main.center[i]-self.center[i])

class Som:
	def __init__(self, dataset, rad, time_const, learning_rate_const, dist_func):
		self.rad = rad
		self.dataset = dataset
		self.time_const = time_const
		self.learning_rate_const = learning_rate_const
		self.dist_func = dist_func
		self.iteration = 0
		self.nodes = []
		
	def init_nodes(self, width, height):
		for x in range(width):
			for y in range(height):
				self.nodes.append(Node(size, [x,y, 1,1]))
	
	def epoch(self):
		learning_rate = exp_decay(self.learning_rate_const, self.time_const, self.iteration)
		item = random.choice(self.dataset)
		bmu = self.find_best(item)
		neighborhood = exp_decay(self.rad, self.time_const, self.iteration)
		for node in self.nodes:
			dist = self.dist_func(node.center, bmu.center)
			if dist < neighborhood:
				influence = comp_influence(self.rad, dist)
				node.update_weights(item, learning_rate, influence)
		self.iteration = self.iteration + 1
		
	def get_nodes(self):
		return self.nodes
		
	def find_best(self, item):
		best = 9999999999
		best_node = None
		for node in self.nodes:
			dist = self.dist_func(node.weights, item)
			if dist < best:
				best = dist
				best_node = node
		return best_node
	
def euc_dist(vec1, vec2):
	sum = 0
	for item in zip(vec1,vec2):
		sum += (item[0]-item[1])**2
	return math.sqrt(sum)
	
		
def exp_decay(start, const, timestep):
	return start*math.exp(-timestep/const)
	
def comp_influence(width, distance):
	return math.exp(-(distance**2)/width**2)

def manhattan(vec1, vec2):
	sum = 0
	for item in zip(vec1,vec2):
		sum += abs(item[0]-item[1])
	return abs(sum)
		
size = 3
max_iter = 1000
width, height = 25, 25
rad = max(width, height)/2
time_const = max_iter/math.log(rad)
learning_rate_const = 0.1
dist_function = euc_dist

dataset = [[0.33,0.33,0.33],[0.66,0.66,0.66],[0.99,0.,1.], [1., 1., 0.], [0.,0.,0.4]]
		
root=Tk()
canvas=Canvas(root)
canvas.place(x=0,y=0,height=512,width=512)

som = Som(dataset, rad, time_const, learning_rate_const, dist_function)
som.init_nodes(width, height)
for iteration in range(max_iter):
	#epoch(nodes, dataset, iteration, rad, time_const, learning_rate_const, dist_function)
	som.epoch()
	canvas.delete("all")
	nodes = som.get_nodes()
	for node in nodes:
		colorval = "#%02x%02x%02x" % (round(node.weights[0]*255), round(node.weights[1]*255), round(node.weights[2]*255))
		canvas.create_rectangle(node.coords[0]*4, node.coords[1]*4, node.coords[0]*4+node.coords[2]*4+1, node.coords[1]*4+node.coords[3]*4+1, fill=colorval, outline=None)
	root.update()

mainloop()
