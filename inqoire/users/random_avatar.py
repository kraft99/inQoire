import os
import random

from django.conf import settings

'''
settings.py
RANDOM_AVATAR_PATH = os.path.join(MEDIA_ROOT,'random_avatars') 

media/
folder named random_avatars/ (all random avatars are located here)

PATH_RELATIVE = "random_avatars/"

NOTE : name can be changed but must be kept consistent for all dependants.
'''

global PATH
PATH_RELATIVE = "random_avatars/"
PATH = getattr(settings,'RANDOM_AVATAR_PATH')


def user_random_avatar():
    """ Get random avatar picked from a pool of "static" avatars"""
    avatar_names = os.listdir(PATH)
    avatar_path = random.choice([avatar_image for avatar_image in avatar_names
                                if os.path.isfile(os.path.join(PATH,avatar_image))])
    return PATH_RELATIVE+avatar_path
