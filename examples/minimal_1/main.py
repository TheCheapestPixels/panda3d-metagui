import sys

from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectLabel

from metagui.gui import SizeSpec
from metagui.gui import WholeScreen
from metagui.gui import HorizontalFrame
from metagui.gui import VerticalFrame
from metagui.gui import Element


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


if __name__ == '__main__':
    Application()

    gui = WholeScreen(
        VerticalFrame(
            Element(
                DirectLabel,
                kwargs=dict(
                    text="Foo",
                    text_pos=(0, -0.02),
                    text_align=TextNode.ACenter,
                    text_scale=0.07,
                    frameColor=(1,0,0,1),
                ),
                size_spec=SizeSpec(h_min=0.1, h_weight=0.0),
            ),
            HorizontalFrame(
                Element(
                    DirectLabel,
                    kwargs=dict(
                        text="Bar",
                        text_pos=(0, -0.02),
                        text_align=TextNode.ALeft,
                        text_scale=0.07,
                        frameColor=(0,1,0,1),
                    ),
                    size_spec=SizeSpec(h_min=0.1, h_weight=0.0),
                ),
                Element(
                    DirectLabel,
                    kwargs=dict(
                        text="Baz",
                        text_pos=(0, -0.02),
                        text_align=TextNode.ARight,
                        text_scale=0.07,
                        frameColor=(0,0,1,1),
                    ),
                    size_spec=SizeSpec(h_min=0.1, h_weight=0.0),
                ),
                weight=0.0,
            ),
        ),
    )
    base.run()
