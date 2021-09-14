import sys

from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectLabel

from metagui.gui import SizeSpec
from metagui.gui import WholeScreen
from metagui.gui import HorizontalFrame
from metagui.gui import VerticalFrame
from metagui.gui import Element
from metagui.gui import ScrollableFrame
from metagui.gui import spacer_factory
from metagui.gui import filler
from metagui.tools import intersperse


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

    def number_box(i):
        return Element(
            DirectLabel,
            kwargs=dict(
                text=str(i),
                text_pos=(0, -0.02),
                text_align=TextNode.ACenter,
                text_scale=0.07,
                frameColor=(0.9, 0.9, 0.9, 1),
            ),
            size_spec=SizeSpec(
                w_min=0.4, w_weight=0.0,
                h_min=0.4, h_weight=0.0,
            ),
        )

    def number_field():
        return VerticalFrame(
            *intersperse(
                [HorizontalFrame(
                    *intersperse(
                        [number_box(i_x + x_fields * i_y)
                         for i_x in range(x_fields)],
                        spacer_factory(
                            dict(w_min=0.05, w_weight=0.0),
                        ),
                    ),
                    weight=0.0,
                ) for i_y in range(y_fields)],
                spacer_factory(
                    dict(
                        w_min=0.0, w_weight=1.0,
                        h_min=0.05, h_weight=0.0,
                    ),
                ),
            ),
            weight=0.0,
        )

    filler_style = dict(
        frameColor=(1, 0, 1, 1),
    )
    x_fields = 6 # horizontal number fields
    y_fields = 5 # vertical number fields

    gui = WholeScreen(
        ScrollableFrame(
            VerticalFrame(
                HorizontalFrame(
                    number_field(),
                    filler(filler_style),
                    weight=0.0,
                ),
                filler(filler_style),
                weight=0.0,
            ),
        ),
    )
    gui.create()
    base.run()
