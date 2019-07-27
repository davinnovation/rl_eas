import numpy as numpy
import tensorflow as tf

state_size = []

class Model():
    def __init__(self):
        self.input = tf.placeholder(shape=[None, state_size[0]], dtype=tf.float32)
        
        self.fc1 = tf.layers.dense(self.input, 512, activation=tf.nn.relu)
        self.