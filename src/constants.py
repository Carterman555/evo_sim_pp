import os

PROJECT_PATH = os.path.abspath(os.path.join(__file__, '../..'))
IMAGE_PATH = os.path.join(PROJECT_PATH, 'images')

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BOOSTER_ENERGY_USAGE = 0.1
BASE_ENERGY_DRAIN = 0.1

INVINCIBILITY_TIME = 60 # frames

BANANA_ENERGY_GAIN = 20

BANANA_SPAWN_COOLDOWN = 90 # frames

# mutations
MOVE_JOINT_PROB = 0.10
AVG_JOINT_MOVE_AMOUNT = 5

ADD_JOINT_PROB = 0.03
NEW_JOINT_DIST = 15

ADD_BONE_PROB = 0.03
REMOVE_BONE_PROB = 0.03

MOVE_PART_PROB = 0.05
AVG_PART_MOVE_AMOUNT = 5

RESIZE_PART_PROB = 0.05
AVG_PART_RESIZE_AMOUNT = 3

ADD_PART_PROB = 0.01
REMOVE_PART_PROB = 0.01 # note for implementation: chance to remove one part, don't loop through parts and have a 0.01 probably to remove each because then parts are more likely to be removed than added