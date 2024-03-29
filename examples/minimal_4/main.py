import sys

from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectLabel

from metagui.gui import SizeSpec
from metagui.gui import WholeScreen
from metagui.gui import HorizontalFrame
from metagui.gui import VerticalFrame
from metagui.gui import Element
from metagui.gui import Empty


class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Basics
        base.disable_mouse()

        # Escape for Quit
        base.accept('escape', sys.exit)

        # F10 for frame rate meter
        base.frame_rame_meter_visible = False
        base.set_frame_rate_meter(base.frame_rame_meter_visible)
        def toggle_frame_rate_meter():
            base.frame_rame_meter_visible = not base.frame_rame_meter_visible
            base.set_frame_rate_meter(base.frame_rame_meter_visible)
        base.accept('f10', toggle_frame_rate_meter)

        # F11 for debug
        def debug():
            import pdb; pdb.set_trace()
        base.accept('f11', debug)


class SelfDescribingTextBox(Element):
    def __init__(self, kwargs=None, size_spec=None):
        Element.__init__(self, DirectLabel, kwargs=kwargs, size_spec=size_spec)

    def resize(self, width, height):
        self.np['text'] = f'w {width}\nh {height}'
        Element.resize(self, width, height)


if __name__ == '__main__':
    Application()

    color_white = dict(
        frameColor=(1.0, 1.0, 1.0, 1),
    )
    color_light_grey = dict(
        frameColor=(0.75, 0.75, 0.75, 1),
    )
    color_medium_grey = dict(
        frameColor=(0.5, 0.5, 0.5, 1),
    )
    color_dark_grey = dict(
        frameColor=(0.25, 0.25, 0.25, 1),
    )
    color_black = dict(
        frameColor=(0.0, 0.0, 0.0, 1),
    )

    unit_box = dict(
        w_min=1.0, w_max = 1.0, w_weight=0.,
        h_min=1.0, h_max = 1.0, h_weight=0.0,
    )
    vanishing_height = dict(
        w_min=0.0, w_weight=1.0,
        h_min=0.0, h_weight=0.0,
    )

    uninspired_text_box = dict(
        text="Foo",
        text_pos=(0, -0.02),
        text_align=TextNode.ACenter,
        text_scale=0.07,
    )

    gui = WholeScreen(
        VerticalFrame(
            HorizontalFrame(
                SelfDescribingTextBox(
                    kwargs=dict(
                        **uninspired_text_box,
                        **color_light_grey,
                    ),
                    size_spec=SizeSpec(**unit_box),
                ),
                SelfDescribingTextBox(
                    kwargs=dict(
                        **uninspired_text_box,
                        **color_medium_grey,
                    ),
                    size_spec=SizeSpec(**vanishing_height),
                ),
                weight=0.0,
            ),
            SelfDescribingTextBox(
                kwargs=dict(
                    **uninspired_text_box,
                    **color_dark_grey,
                ),
                #size_spec=SizeSpec(**vanishing),
            ),
        ),
    )
    base.run()
