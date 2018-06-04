from __future__ import print_function
import numpy as np

from .augment import Augment
from .flip import FlipRotate
from .perturb import Blur


__all__ = ['Track']


class Track(Augment):
    def __init__(self, width=120, margin=20, sigma=(10,10,3), thresh=0.503,
                 skip=0, **kwargs):
        self.width = int(width)
        self.margin = int(margin)
        self.blur = [Blur(sigma[0]), Blur(sigma[1]), Blur(sigma[2])]
        self.thresh = np.clip(thresh, 0, 1)
        self.skip = np.clip(skip, 0, 1)
        self.do_aug = False
        self.imgs = []
        self.flip_rotate = FlipRotate()

    def prepare(self, spec, imgs=[], **kwargs):
        # Biased coin toss
        if np.random.rand() < self.skip:
            self.do_aug = False
            return dict(spec)

        if self.flip_rotate is not None:
            spec = self.flip_rotate.prepare(spec, **kwargs)
        self.imgs = self._validate(spec, imgs)
        self.do_aug = True
        return dict(spec)

    def __call__(self, sample, **kwargs):
        sample = Augment.to_tensor(sample)
        if self.do_aug:
            sample = self.augment(sample, **kwargs)
            if self.flip_rotate is not None:
                sample = self.flip_rotate(sample)
        return Augment.sort(sample)

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        format_string += ')'
        return format_string

    def _validate(self, spec, imgs):
        assert len(imgs) > 0
        assert all(k in spec for k in imgs)
        return imgs

    def augment(self, sample, **kwargs):
        loc = np.random.rand() * 0.5 + 0.25

        for k in self.imgs:
            img = sample[k]
            [depth,height,width] = img.shape[-3:]
            a = int(width * loc) - (self.width // 2)
            b = a + self.width
            assert a >= 0 and b < width
            for z in range(depth):
                s0 = self.stencil(height)
                s1 = self.stencil(height)
                img[...,z,:,a:b] *= (1 - s0)
                img[...,z,:,a:b] *= (1 - s1)
                img[...,z,:,a:b] += s1

        return sample

    def stencil(self, height):
        # Gradation
        grad = np.zeros((height, self.width)).astype('float32')
        grad[:,self.margin:-self.margin] = 1
        self.blur[0](grad)

        # Stencil for track mark
        stencil = np.random.rand(height, self.width).astype('float32')
        self.blur[1](stencil)
        stencil = (stencil > self.thresh).astype(stencil.dtype)
        stencil *= grad
        self.blur[2](stencil)
        return stencil