from typing import Sequence, Mapping, Tuple
import numpy as np


def get_best_location(blocks: Sequence[Mapping[str, bool]], required_buildings: Sequence[str]) -> Tuple[int, int]:
    max_distances = np.zeros(len(blocks))

    for building in required_buildings:
        building_locations_iter = (location for location, block in enumerate(blocks) if block[building])

        last_building_location = -np.inf
        try:
            next_building_location = next(building_locations_iter)
        except StopIteration:
            raise ValueError(f'Could not find block that contains {building}!')

        # since these will be written to later, we can leave them uninitialized for now
        distances = np.empty(len(blocks))
        for location in range(len(blocks)):
            distances[location] = min(location - last_building_location, next_building_location - location)
            if location == next_building_location:
                last_building_location = next_building_location
                try:
                    next_building_location = next(building_locations_iter)
                except StopIteration:
                    next_building_location = np.inf

        max_distances = np.maximum(max_distances, distances)

    # noinspection PyTypeChecker
    best_location: int = np.argmin(max_distances)
    max_distance = max_distances[best_location]
    return best_location, max_distance


def find_min(nums):
    if nums[0] < nums[-1]:
        # nums was rotated 0 times
        return nums[0]

    left = 0
    right = len(nums) - 1
    while right - left > 1:
        middle = (right + left) // 2
        if nums[middle] > nums[left]:
            left = middle
        else:
            # by the nature of the rotated array, it must be true that arr[middle] < arr[right]
            right = middle

    return nums[right]


def password_checker(password):
    contains_lower = any([character.isalpha() and character.islower() for character in password])
    contains_upper = any([character.isalpha() and character.isupper() for character in password])
    contains_number = any([character.isnumeric() for character in password])

