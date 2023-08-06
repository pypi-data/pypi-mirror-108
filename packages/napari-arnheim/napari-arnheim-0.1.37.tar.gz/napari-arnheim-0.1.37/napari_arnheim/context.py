import sys

import qasync
from napari_arnheim.widgets.arnheim import ArnheimWidget
import napari
import os

if os.name() == "nt":
    from qasync import QSelectorEventLoop
    EventLoop = QSelectorEventLoop
else:
    from qasync import QEventLoop
    EventLoop = QEventLoop

    
import asyncio

class gui_qt:
    
    def __init__(self, *args, bergen_params= {}):
        self.args = args
        self.bergen_params = bergen_params

   
    def __enter__(self): 
        self.napari_context = napari.gui_qt()
        self.app = self.napari_context.__enter__()
        self.viewer = napari.Viewer()
        self.widget = ArnheimWidget(bergen_params=self.bergen_params)
        self.viewer.window.add_dock_widget(self.widget, area="right")

        self.loop = QSelectorEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        self.loop.__enter__()
        self.loop.run_until_complete(self.widget.connectBergen())
        self.client = self.widget.bergen

        self.helper = self.widget.helper
        return self
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(exc_type, exc_value, exc_traceback)
        task = self.loop.create_task(self.client.provide_async())
        self.napari_context.__exit__(exc_type, exc_value, exc_traceback)
        task.cancel()
        self.loop.__exit__(exc_type, exc_value, exc_traceback)
        sys.exit()
        