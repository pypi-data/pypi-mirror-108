from itertools import groupby

def sorted_groupby(iter,key=None):
	return groupby(sorted(iter,key=key),key)

from operator import attrgetter
priority_sort = attrgetter("priority")

import random

def choice(choices,weights):
	return random.choices(choices,weights)[0]
