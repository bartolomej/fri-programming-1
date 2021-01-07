import numpy as np
import math
import json
from random import uniform
from matplotlib import pyplot as plt


class Cannon:
    def __init__(self):
        self.pig_dist = None
        self.pig_height = None
        self.target_dist = None
        self.dist_threshold = 0.3
        self.dt = 0.1
        self.pos_history = np.array([])

    def get_x_data(self):
        a = np.array([])
        for p in self.pos_history:
            a = np.append(a, p[0])
        return a

    def get_y_data(self):
        a = np.array([])
        for p in self.pos_history:
            a = np.append(a, p[1])
        return a

    def set_pig_distance(self, x):
        self.pig_dist = x

    def set_pig_height(self, h):
        self.pig_height = h

    def set_target_dist(self, x):
        self.target_dist = x

    def set_dist_threshold(self, x):
        self.dist_threshold = x

    def set_delta_time(self, dt):
        self.dt = dt

    def plot_data(self):
        plt.scatter(x=self.get_x_data(), y=self.get_y_data(), c="g", alpha=0.5, label="Ball path")
        plt.scatter(x=self.pig_dist, y=self.pig_height, c="b", alpha=0.5, label="Pig")
        plt.scatter(x=self.target_dist, y=0, c="r", alpha=0.5, label="Target")
        plt.xlabel("Distance")
        plt.ylabel("Height")
        plt.legend(loc='upper left')
        plt.show()

    def propagate_ball(self, phi0, v0):
        t = 0
        # current time
        pig_is_hit = False
        target_is_hit = False
        # initial velocity
        v = np.array([
            math.cos(phi0) * v0,
            math.sin(phi0) * v0
        ])
        print(v)
        # change in velocity (g)
        g = np.array([0, -9.82])
        # current position
        p = np.array([0, 0])
        # pig position
        pig = np.array([self.pig_dist, self.pig_height])
        # target position
        target = np.array([self.target_dist, 0])
        self.pos_history = np.array([p])
        while True:
            t += self.dt
            p = np.add(p, v * self.dt)
            v = np.add(v, g * self.dt)
            # add current position to pos history
            self.pos_history = np.vstack((self.pos_history, np.array([p])))
            # is current position close enough to pig's position
            if np.linalg.norm(np.subtract(p, pig)) < self.dist_threshold:
                pig_is_hit = True
            # is current position close enough to target's position
            if np.linalg.norm(np.subtract(p, target)) < self.dist_threshold:
                target_is_hit = True
                break
            # is current y position close enough to the ground
            if v[1] < 0 and (math.fabs(p[1]) < self.dist_threshold):
                break
        return pig_is_hit, target_is_hit

    # pretty much unusable :)
    def random_descent(self, plot_data=False):
        targets_are_hit = False
        while not targets_are_hit:
            phi = uniform(math.pi / 2, 0)
            v = uniform(1, 20)
            pig_is_hit, target_is_hit = self.propagate_ball(phi, v)
            targets_are_hit = pig_is_hit and targets_are_hit
            self.plot_data()

    # i wanted to make a gradient descent algorithm but didn't have the time to finish it
    # the algorithm would support multiple points
    # (obviously overengineered solution but seemed fun to develop)


def main():
    cannon = Cannon()
    test_cases_path = 'strelske-vaje/test-cases.json'
    with open(test_cases_path) as json_file:
        data = json.load(json_file)
        for p in data:
            # set some parameters
            cannon.set_pig_distance(p['pig_distance'])
            cannon.set_pig_height(p['pig_height'])
            cannon.set_target_dist(p['target_distance'])
            cannon.set_dist_threshold(0.4)
            cannon.set_delta_time(0.02)
            # fire the cannon
            # pig_is_hit, target_is_hit = cannon.propagate_ball(math.pi / 4, 10)
            cannon.random_descent()
            # print(pig_is_hit, target_is_hit)
            # cannon.plot_data()


if __name__ == '__main__':
    main()
