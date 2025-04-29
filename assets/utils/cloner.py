import flet as ft
import inspect
import time

def clone_widget(widget):
    start = time.time()
    if widget is not None:
        widget_cls = widget.__class__
        init_params = inspect.signature(widget_cls.__init__).parameters
        kwargs = {}

        # Collect init parameters (skipping 'self')
        for name, param in init_params.items():
            if name == "self":
                continue
            if hasattr(widget, name):
                kwargs[name] = getattr(widget, name)

        # Special case for text_compo class

        # Instantiate a new widget with gathered parameters
        cloned = widget_cls(**kwargs)

        # Clone 'content' attribute if it exists
        if hasattr(widget, "content") and widget.content is not None:
            if isinstance(widget.content, ft.Control):
                cloned.content = clone_widget(widget.content)
            else:
                cloned.content = widget.content

        # Clone nested child widgets from 'controls'
        if hasattr(widget, "controls") and widget.controls is not None:
            cloned.controls = []
            for child in widget.controls:
                if isinstance(child, ft.Control):
                    cloned.controls.append(clone_widget(child))
                else:
                    cloned.controls.append(child)

        #print('clone time: ', time.time() - start)
        return cloned
    else:
        print("cloner: ", None)
