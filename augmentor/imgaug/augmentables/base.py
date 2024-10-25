# Modified from https://github.com/aleju/imgaug/blob/0101108d4fed06bc5056c4a03e2bcb0216dac326/imgaug/augmentables/base.py
# Copyright (c) 2015 aleju
# See ../LICENCE for licensing information

"""Interfaces used by augmentable objects.

Added in 0.4.0.

"""
from __future__ import print_function, division, absolute_import


class IAugmentable(object):
    """Interface of augmentable objects.

    This interface is right now only used to "mark" augmentable objects.
    It does not enforce any methods yet (but will probably in the future).

    Currently, only ``*OnImage`` clases are marked as augmentable.
    Non-OnImage objects are normalized to OnImage-objects.
    Batches are not yet marked as augmentable, but might be in the future.

    Added in 0.4.0.

    """
