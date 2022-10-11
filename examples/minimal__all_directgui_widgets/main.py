import sys

from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectCheckButton
from direct.gui.DirectGui import DirectRadioButton
from direct.gui.DirectGui import DirectEntry
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.DirectGui import DirectSlider
from direct.gui.DirectGuiGlobals import RAISED
from direct.gui.DirectGuiGlobals import RIDGE

from metagui.gui import SizeSpec
from metagui.gui import SimplexFrame
from metagui.gui import WholeScreen
from metagui.gui import HorizontalFrame
from metagui.gui import VerticalFrame
from metagui.gui import Element
from metagui.gui import Empty
from metagui.gui import spacer_factory
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

        if spacer_factory is not None:
            all_subframes = intersperse(
                self.radio_buttons,
                spacer_factory,
                first=True,
                last=True,
            )
        else:
            all_subframes = list(self.radio_buttons)

        self.child = multiframe_cls(*all_subframes)

    def create(self, parent, parent_np):
        SimplexFrame.create(self, parent, parent_np)

        nps = [button.np for button in self.radio_buttons]
        for np in nps:
            np.setOthers(nps)

    def click(self):
        print(f"DirectRadioButton state: {self.variable}")


class WrappedEntry(Element):
    def __init__(self, kwargs=None, size_spec=None):
        Element.__init__(self, DirectEntry, kwargs=kwargs, size_spec=size_spec)

    def create(self, *args):
        Element.create(self, *args)
        self.np['command'] = self.enter

    def enter(self, text):
        print(f"DirectEntry: {text}")
            

class WrappedProgressBar(Element):
    def __init__(self, kwargs=None, size_spec=None):
        Element.__init__(self, DirectWaitBar, kwargs=kwargs, size_spec=size_spec)
        self.created = False

    def create(self, *args):
        Element.create(self, *args)
        self.created = True

    def set_value(self, value):
        if self.created:
            self.np['value'] = value
            

class WrappedSlider(Element):
    def __init__(self, kwargs=None, size_spec=None):
        Element.__init__(self, DirectSlider, kwargs=kwargs, size_spec=size_spec)
        self.created = False
            
    def create(self, *args):
        Element.create(self, *args)
        self.np['command'] = self.click

    def click(self):
        print(f"Slider state: {self.np['value']}")


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
    color_red = dict(
        frameColor=(1.0, 0.0, 0.0, 1),
    )
    color_green = dict(
        frameColor=(0.0, 1.0, 0.0, 1),
    )
    color_blue = dict(
        frameColor=(0.0, 0.0, 1.0, 1),
    )

    # Text attributes
    small_text = dict(text_scale=0.07)
    text_standard_centered = dict(
        text_pos=(0, -0.02),
        text_align=TextNode.ACenter,
        **small_text,
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

    # Relief
    relief_thin = dict(
        relief=RAISED,
        borderWidth=(0.03, 0.03),
    )

    # The actual GUI
    progress_bar = WrappedProgressBar(
        kwargs=dict(
            barColor=(0, 0, 0.75, 1),
            barRelief=RAISED,
            barBorderWidth=(0.03, 0.03),
            **relief_thin,
            **small_text,
        ),
    )
    def set_value(task):
        progress_bar.set_value((task.time % 10) * 10.0)
        return task.cont
    base.task_mgr.add(set_value)

    gui = WholeScreen(
        VerticalFrame(
            VerticalFrame(
                WrappedButton(
                    kwargs=dict(
                        text='DirectButton',
                        **text_standard_centered,
                        **relief_thin,
                    ),
                ),
                #WrappedCheckButton(
                #    kwargs=dict(
                #        text='DirectCheckButton',
                #        **text_standard_centered,
                #        **relief_thin,
                #    ),
                #),
                #RadioButtonFrame(
                #    VerticalFrame,
                #    values=[[0], [1]],
                #    spacer_factory=spacer_factory(dict(h_min=0.1, h_weight=0.0), style=color_blue),
                #    initial_value=[1],
                #    kwargs_each=[
                #        dict(text="DirectRadioButton 0", indicatorValue=False),
                #        dict(text="DirectRadioButton 1", indicatorValue=False),
                #    ],
                #    kwargs_all=dict(
                #        scale=0.95,
                #        #boxBorder=0.03,
                #        **text_standard_centered,
                #        #**relief_thin,
                #    ),
                #),
                WrappedEntry(
                    kwargs=dict(
                        **small_text,
                        #**relief_thin,
                        relief=RIDGE,
                        borderWidth=(0.03, 0.03),
                    ),
                ),
                progress_bar,
                WrappedSlider(kwargs=relief_thin),
                #Empty(),
            ),
        ),
    )
    base.run()
