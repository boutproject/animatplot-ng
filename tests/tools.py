import os
from os.path import join, split
import functools
import pytest

import matplotlib.pyplot as plt
from matplotlib.animation import FileMovieWriter
from matplotlib.testing.compare import compare_images
from matplotlib.testing.decorators import remove_ticks_and_titles
from matplotlib.testing.exceptions import ImageComparisonFailure


class BunchOFiles(FileMovieWriter):
    """
    Exports an animation to a series of images.

    called like:
    ``anim.save('name.format', writer=BunchOFiles())``
    which produces a series of files named ``name{num}.format``
    """

    supported_formats = ["png", "jpeg", "bmp", "svg", "pdf"]

    def __init__(self, *args, extra_args=None, **kwargs):
        # extra_args aren't used but we need to stop None from being passed
        super().__init__(*args, extra_args=(), **kwargs)

    def setup(self, fig, dpi, frame_prefix):
        super().setup(fig, dpi, frame_prefix)
        self.fname_format_str = "%s%%d.%s"
        self.temp_prefix, self.frame_format = self.outfile.split(".")

    def finish(self):
        pass


def _compare_animation(anim, expected, format_, nframes, tol):
    # generate images from the animation
    base_dir, filename = split(join("tests", "baseline_images", expected))
    out_dir = split(join("tests", "output_images", expected))[0]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    anim.save(os.path.join(out_dir, (filename + format_)), writer=BunchOFiles())

    for i in range(nframes):
        image_name = "%s%d%s" % (filename, i, format_)
        expected_name = os.path.join(base_dir, image_name)
        actual_name = os.path.join(out_dir, image_name)

        err = compare_images(expected_name, actual_name, tol, in_decorator=True)

        if not os.path.exists(expected_name):
            raise ImageComparisonFailure("image does not exist: %s" % expected_name)

        if err:
            for key in ["actual", "expected"]:
                err[key] = os.path.relpath(err[key])
            raise ImageComparisonFailure(
                "images not close (RMS %(rms).3f):\n\t%(actual)s\n\t%(expected)s " % err
            )


def animation_compare(baseline_images, nframes, fmt=".png", tol=1e-3, remove_text=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # First close anything from previous tests
            plt.close("all")

            anim = func(*args, **kwargs)
            if remove_text:
                fignum = plt.get_fignums()[0]
                fig = plt.figure(fignum)
                remove_ticks_and_titles(fig)
            try:
                _compare_animation(anim, baseline_images, fmt, nframes, tol)
            finally:
                plt.close("all")

        return wrapper

    return decorator
