from panda3d.core import TextNode

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectFrame


class SizeSpec:
    def __init__(self,
                 w_min=0.0, h_min=0.0,
                 w_weight=1.0, h_weight=1.0,
                 ):
        self.w_min = w_min
        self.h_min = h_min
        self.w_weight = w_weight
        self.h_weight = h_weight


class BaseFrame:
    def create(self, parent):
        raise NotImplemented

    def resize(self, size_x, size_y):
        pass

    def destroy(self):
        self.np.destroy()


class WholeScreen:
    def __init__(self, child, name="whole screen", auto_resize=True):
        self.child = child
        self.np = base.a2dTopLeft.attach_new_node(name)
        self.auto_resize = auto_resize

    def create(self):
        self.child.create(self.np)
        if self.auto_resize:
            base.accept('aspectRatioChanged', self.resize)
        self.resize()

    def destroy(self):
        self.child.destroy()
        self.child = None
        self.np.destroy()
        self.np = None

    def resize(self):
        size = base.a2dTopRight.get_pos() - base.a2dBottomLeft.get_pos()
        width = size.x
        height = size.z

        min_size = self.child.get_size()
        if min_size.w_min > width or min_size.w_weight == 0.0:
            width = min_size.w_min
        if min_size.h_min > height or min_size.h_weight == 0.0:
            height = min_size.h_min

        self.child.resize(width, height)

    def get_size(self):
        return self.child.get_size()


class MultiFrame:
    def __init__(self, *children, weight=1.0):
        self.children = children
        self.weight = weight

    def create(self, parent):
        self.nps = [
            parent.attach_new_node(repr(self))
            for c in self.children
        ]
        for child, np in zip(self.children, self.nps):
            child.create(np)

    def destroy(self):
        for child in self.children:
            child.destroy()
        self.children = []

        for np in self.nps:
            np.destroy()
        self.nps = []
            

class HorizontalFrame(MultiFrame):
    def get_size(self):
        child_sizes = [c.get_size() for c in self.children]
        w_min = sum(c.w_min for c in child_sizes)
        h_min = max(c.h_min for c in child_sizes)
        w_weight = sum(c.w_weight for c in child_sizes)
        h_weight = self.weight
        return SizeSpec(
            w_min=w_min,
            h_min=h_min,
            w_weight=w_weight,
            h_weight=h_weight,
        )

    def resize(self, width, height):
        child_sizes = [c.get_size() for c in self.children]
        min_size = self.get_size()
        if min_size.w_weight == 0.0:
            flex_width_unit = 0.0
        else:
            flex_width_unit = (width - min_size.w_min) / min_size.w_weight
        left = 0.0
        for np, c, cs in zip(self.nps, self.children, child_sizes):
            c_width = cs.w_min + flex_width_unit * cs.w_weight
            c_height = height  # FIXME
            np.set_pos(left, 0, 0)
            c.resize(c_width, c_height)
            left += c_width
            

class VerticalFrame(MultiFrame):
    def get_size(self):
        child_sizes = [c.get_size() for c in self.children]
        w_min = max(c.w_min for c in child_sizes)
        h_min = sum(c.h_min for c in child_sizes)
        w_weight = self.weight
        h_weight = sum(c.h_weight for c in child_sizes)
        return SizeSpec(
            w_min=w_min,
            h_min=h_min,
            w_weight=w_weight,
            h_weight=h_weight,
        )

    def resize(self, width, height):
        child_sizes = [c.get_size() for c in self.children]
        min_size = self.get_size()
        if min_size.h_weight == 0.0:
            flex_height_unit = 0.0
        else:
            flex_height_unit = (height - min_size.h_min) / min_size.h_weight
        top = 0.0
        for np, c, cs in zip(self.nps, self.children, child_sizes):
            c_width = width  # FIXME
            c_height = cs.h_min + flex_height_unit * cs.h_weight
            np.set_pos(0, 0, top)
            c.resize(c_width, c_height)
            top -= c_height


class Element:
    def __init__(self, element_cls, kwargs=None, size_spec=None):
        self.element_cls = element_cls
        self.kwargs = kwargs
        self.size_spec = size_spec
        # FIXME: The text_pos has to be set to align the text with the label's boundaries. This solution is brittle AF.
        if 'text_align' not in self.kwargs:
            self.kwargs['text_align'] = TextNode.ALeft

    def create(self, parent):
        self.np = self.element_cls(
            parent=parent,
            **self.kwargs,
        )

    def destroy(self):
        self.np.destroy()

    def resize(self, width, height):
        self.np.set_pos(width / 2.0, 0, -height / 2.0)
        self.np['frameSize'] = (-width / 2.0, width / 2.0, -height / 2.0, height / 2.0)
        if self.np['text'] is not None:
            if self.kwargs['text_align'] == TextNode.ALeft:
                self.np['text_pos'] = (-width / 2.0 + self.kwargs['text_pos'][0], self.kwargs['text_pos'][1])
            elif self.kwargs['text_align'] == TextNode.ARight:
                self.np['text_pos'] = (width / 2.0 - self.kwargs['text_pos'][0], self.kwargs['text_pos'][1])
            else:
                self.np['text_pos'] = (0, self.np['text_pos'][1])

    def get_size(self):
        return self.size_spec


def spacer(spacer_spec, style=None):
    if style is None:
        style = dict()
    return Element(
        DirectFrame,
        kwargs=style,
        size_spec=SizeSpec(**spacer_spec),
    )


def spacer_factory(spacer_spec, style=None):
    def inner():
        return spacer(spacer_spec, style=style)
    return inner


def filler(style=None):
    if style is None:
        style = dict()
    return Element(
        DirectLabel,
        kwargs=style,
        size_spec=SizeSpec(
            w_min=0.0,
            w_weight=1.0,
            h_min=0.0,
            h_weight=1.0,
        ),
    )
