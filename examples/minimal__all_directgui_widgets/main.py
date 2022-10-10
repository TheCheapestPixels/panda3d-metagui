import sys

from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectCheckButton
from direct.gui.DirectGui import DirectRadioButton

from metagui.gui import SizeSpec
from metagui.gui import SimplexFrame
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


class WrappedButton(Element):
    def __init__(self, kwargs=None, size_spec=None):
        Element.__init__(self, DirectButton, kwargs=kwargs, size_spec=size_spec)

    def create(self, *args):
        Element.create(self, *args)
        self.np['command'] = self.click

    def click(self):
        print("DirectButton clicked.")
            

class WrappedCheckButton(Element):
    def __init__(self, kwargs=None, size_spec=None):
        Element.__init__(self, DirectCheckButton, kwargs=kwargs, size_spec=size_spec)

    def create(self, *args):
        Element.create(self, *args)
        self.np['command'] = self.click

    def click(self, state):
        print(f"DirectCheckButton state: {state}")
            

class RadioButtonFrame(SimplexFrame):
    def __init__(self, multiframe_cls, values, spacer_factory=None, initial_value=None,
                 kwargs_each=None, kwargs_all=None,
                 ):
        if initial_value is None:
            self.variable = []
        else:
            self.variable = initial_value

        self.radio_buttons = []
        for v, kw_each in zip(values, kwargs_each):
            self.radio_buttons.append(
                Element(
                    DirectRadioButton,
                    kwargs=dict(
                        variable=self.variable,
                        value=v,
                        command=self.click,
                        **kw_each,
                        **kwargs_all,
                    ),
                ),
            )

        self.child = multiframe_cls(*self.radio_buttons)

    def create(self, parent, parent_np):
        SimplexFrame.create(self, parent, parent_np)

        nps = [button.np for button in self.radio_buttons]
        for np in nps:
            np.setOthers(nps)

    def click(self):
        print(f"DirectRadioButton state: {self.variable}")


if __name__ == '__main__':
    Application()

    # Frame colors
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

    # Text attributes
    text_standard_centered = dict(
        text_pos=(0, -0.02),
        text_align=TextNode.ACenter,
        text_scale=0.07,
    )

    # Frame sizes
    unit_box = dict(
        w_min=1.0, w_weight=0.0,
        h_min=1.0, h_weight=0.0,
    )
    vanishing_height = dict(
        w_min=0.0, w_weight=1.0,
        h_min=0.0, h_weight=0.0,
    )

    # The actual GUI
    gui = WholeScreen(
        VerticalFrame(
            VerticalFrame(
                WrappedButton(kwargs=dict(text='DirectButton', **text_standard_centered)),
                WrappedCheckButton(kwargs=dict(text='DirectCheckButton', **text_standard_centered)),
                RadioButtonFrame(
                    VerticalFrame,
                    values=[[0], [1]],
                    spacer_factory=None,
                    initial_value=[None],
                    kwargs_each=[
                        dict(text="DirectRadioButton 0"),
                        dict(text="DirectRadioButton 1"),
                    ],
                    kwargs_all=dict(**text_standard_centered),
                ),
            ),
        ),
    )
    base.run()
