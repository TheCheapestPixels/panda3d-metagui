from panda3d.core import TextNode

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectScrolledFrame


class SizeSpec:
    def __init__(self,
                 w_min=0.0, w_weight=1.0,
                 h_min=0.0, h_weight=1.0,
                 ):
        self.w_min = w_min
        self.w_weight = w_weight
        self.h_min = h_min
        self.h_weight = h_weight


class SimplexFrame:
    def __init__(self, child):
        self.child = child

    def create(self, parent, parent_np):
        self.parent = parent
        self.np = parent_np
        self.child.create(self, self.np)

    def destroy(self):
        self.child.destroy()
        self.np.destroy_node()
        self.np = None

    def get_size(self):
        return self.child.get_size()

    def resize(self, size_x, size_y):
        self.child.resize(size_x, size_y)


class MultiFrame(SimplexFrame):
    def __init__(self, *children, weight=1.0):
        self.children = list(children)
        self.weight = weight

    def create(self, parent, parent_np):
        self.parent = parent
        self.parent_np = parent_np
        self.nps = [
            parent_np.attach_new_node(repr(self))
            for c in self.children
        ]
        for child, np in zip(self.children, self.nps):
            child.create(self, np)

    def destroy(self):
        for child in self.children:
            child.destroy()
        self.children = []

        for np in self.nps:
            np.destroy_node()
        self.nps = []

    def get_size(self):
        raise NotImplemented

    def resize(self, size_x, size_y):
        raise NotImplemented

    def add(self, idx, child):
        assert 0 <= idx <= len(self.children)
        self.children.insert(idx, child)
        np = self.parent_np.attach_new_node(repr(self))
        self.nps.insert(idx, np)
        child.create(self, np)
        self.mark_dirty()

    def remove(self, idx):
        assert 0 <= idx <= len(self.children) - 1
        child = self.children.pop(idx)
        child.destroy()
        np = self.nps.pop(idx)
        np.remove_node()
        self.mark_dirty()


class PushUpDirty:
    def mark_dirty(self):
        self.parent.mark_dirty()


class RedrawOnDirty:
    def mark_dirty(self):
        self.resize()


"""
123456789012345678901234567890123456789012345678901234567890123456789012
"""


class WholeScreen(SimplexFrame, RedrawOnDirty):
    """
    This class represents the root of a tree of frames. It offers 
    several ways to automate resizing the window tree.

    Initializing may only prepare frames for actual setup; It may
    not create graphical elements yet. This is so that sub-trees can
    be set up separately (and stored in variables for later 
    manipulation), and only assembled into the full tree later. As
    in these sub-trees their parents are not yet known, it is 
    impossible to determine where to place them.

    To actually create the GUI elements, `create()` has to be 
    called. 
    """
    def __init__(self, child, name="whole screen",
                 on_event=True, on_dirty=True, task_args=None,
                 delay_create=False):
        """
        :child:        The tree in this frame.
        :name:         The name of the GUI's `NodePath`.
        :on_event:     An `aspectRatioChanged` event will trigger a
                       resize. True by default.
        :on_dirty:     The child can report that a change has occurred
                       within it that necessitates a resize. If
                       :on_dirty: is `True` (default), that resize will
                       be done immediately.
        :task_args:    To create a task that triggers a resize every 
                       frame, pass an `(args, kwargs)` tuple with
                       arguments to pass to `base.task_mgr.add`. By
                       default, no such task is created.
        """
        SimplexFrame.__init__(self, child)

        self.name = name
        self.on_event = on_event
        self.on_dirty = on_dirty
        if task_args is None:
            self.by_task = False
        else:
            self.by_task = True
            self.task_args = task_args

        self.dirty = True
        if not delay_create:
            self.create()

    def create(self):
        """
        Create the widget, call `create` on the child (recursively
        triggering the creation of all widgets), and perform the initial
        resize. Also perform all the administrative work necessitated by
        the parameters to `__init__`.
        """
        self.np = base.a2dTopLeft.attach_new_node(self.name)
        self.child.create(self, self.np)
        self.resize()

        if self.on_event:
            base.accept('aspectRatioChanged', self.resize)
        if self.by_task:
            args, kwargs = self.task_args
            base.task_mgr.add(*args, **kwargs)

    def destroy(self):
        """
        """
        self.child.destroy()
        self.np.destroy()
        self.np = None

        if self.on_event:
            # FIXME: Unregister event listener
            pass
        if self.by_task:
            # FIXME: Remove task
            pass

    def get_size(self):
        SimplexFrame.get_size(self)

    def resize(self):
        size = base.a2dTopRight.get_pos() - base.a2dBottomLeft.get_pos()
        width = size.x
        height = size.z

        min_size = self.child.get_size()
        if min_size.w_min > width or min_size.w_weight == 0.0:
            width = min_size.w_min
        if min_size.h_min > height or min_size.h_weight == 0.0:
            height = min_size.h_min

        SimplexFrame.resize(self, width, height)
        self.dirty = False

    def mark_dirty(self):
        self.dirty = True
        if self.on_dirty:
            RedrawOnDirty.mark_dirty(self)


class HorizontalFrame(MultiFrame, PushUpDirty):
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
            

class VerticalFrame(MultiFrame, PushUpDirty):
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


class Empty(SimplexFrame):
    def __init__(self, size_spec=None):
        if size_spec is None:
            size_spec = SizeSpec()
        self.size_spec = size_spec

    def create(self, parent, parent_np):
        pass

    def destroy(self):
        pass

    def get_size(self):
        return self.size_spec

    def resize(sef, size_, size_y):
        pass


class Element(SimplexFrame):
    def __init__(self, element_cls, kwargs=None, size_spec=None):
        self.element_cls = element_cls
        self.kwargs = kwargs
        if size_spec is None:
            size_spec = SizeSpec()
        self.size_spec = size_spec
        # FIXME: The text_pos has to be set to align the text with the
        # label's boundaries. This solution is brittle AF.
        if 'text_align' not in self.kwargs:
            self.kwargs['text_align'] = TextNode.ALeft

    def create(self, parent, parent_np):
        self.parent = parent
        self.np = self.element_cls(
            parent=parent_np,
            **self.kwargs,
        )

    def destroy(self):
        self.np.destroy()
        self.np = None

    def get_size(self):
        return self.size_spec

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


class ScrollableFrame(SimplexFrame):
    def __init__(self, child, size_spec=None):
        self.child = child
        if size_spec is None:
            size_spec = SizeSpec()
        self.size_spec = size_spec

    def create(self, parent, parent_np):
        self.parent = parent
        self.np = DirectScrolledFrame(
            parent=parent_np,
            frameColor=(1,0,0,1),
        )
        self.child.create(self, self.np.getCanvas())

    def destroy(self):
        self.np.destroy()

    def get_size(self):
        return self.size_spec

    def resize(self, width, height):
        self.np['frameSize'] = (0, width, -height, 0)

        min_size = self.child.get_size()
        actual_width = max(width, min_size.w_min)
        actual_height = max(height, min_size.h_min)
        # Is the up-and-down scrollbar active?
        if actual_height > height:
            # Can we trim its width from the canvas' width?
            left, right, _, _ = self.np['verticalScroll_frameSize']
            bar_width = right - left
            actual_width = max(width - bar_width, min_size.w_min)
        # Is the left-and-right scrollbar active?
        if actual_width > width:
            # Can we trim its height from the canvas' height?
            _, _, bottom, top = self.np['horizontalScroll_frameSize']
            bar_height = top - bottom
            actual_height = max(height - bar_height, min_size.h_min)
        self.np['canvasSize'] = (
            0,
            actual_width,
            -actual_height,
            0,
        )
        self.child.resize(actual_width, actual_height)


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
