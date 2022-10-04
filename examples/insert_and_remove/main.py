import sys
import random

from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectLabel

from metagui.gui import SizeSpec
from metagui.gui import WholeScreen
from metagui.gui import HorizontalFrame
from metagui.gui import VerticalFrame
from metagui.gui import Empty
from metagui.gui import Element
from metagui.gui import spacer
from metagui.gui import filler


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

    filler_style = dict(
        text="filler",
        text_pos=(0, -0.02),
        text_align=TextNode.ACenter,
        text_scale=0.07,
        frameColor=(0,0.5,0,1),
    )

    container = HorizontalFrame(
        Element(
            DirectLabel,
            kwargs=dict(
                text="0",
                text_pos=(0, -0.02),
                text_align=TextNode.ACenter,
                text_scale=0.07,
                frameColor=(1,0,0,1),
            ),
            size_spec=SizeSpec(),
        ),
    )
    gui = WholeScreen(container)

    def add_element(idx):
        element = Element(
            DirectLabel,
            kwargs=dict(
                text=str(idx),
                text_pos=(0, -0.02),
                text_align=TextNode.ACenter,
                text_scale=0.07,
                frameColor=(
                    random.random(),
                    random.random(),
                    random.random(),
                    1,
                ),
            ),
            size_spec=SizeSpec(),
        )

        container.add(idx, element)
        gui.resize()
        print(f'+{idx}')

    def remove_element(idx):
        container.remove(idx)
        gui.resize()
        print(f'-{idx}')

    base.accept('0', add_element, extraArgs=[0])
    base.accept('1', add_element, extraArgs=[1])
    base.accept('2', add_element, extraArgs=[2])
    base.accept('3', add_element, extraArgs=[3])
    base.accept('4', add_element, extraArgs=[4])
    base.accept('5', add_element, extraArgs=[5])
    base.accept('6', add_element, extraArgs=[6])
    base.accept('7', add_element, extraArgs=[7])
    base.accept('8', add_element, extraArgs=[8])
    base.accept('9', add_element, extraArgs=[9])
    base.accept('shift-0', remove_element, extraArgs=[0])
    base.accept('shift-1', remove_element, extraArgs=[1])
    base.accept('shift-2', remove_element, extraArgs=[2])
    base.accept('shift-3', remove_element, extraArgs=[3])
    base.accept('shift-4', remove_element, extraArgs=[4])
    base.accept('shift-5', remove_element, extraArgs=[5])
    base.accept('shift-6', remove_element, extraArgs=[6])
    base.accept('shift-7', remove_element, extraArgs=[7])
    base.accept('shift-8', remove_element, extraArgs=[8])
    base.accept('shift-9', remove_element, extraArgs=[9])

    base.run()
