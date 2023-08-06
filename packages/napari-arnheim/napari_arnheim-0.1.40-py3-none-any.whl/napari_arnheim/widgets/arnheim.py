from napari_arnheim.widgets.dialogs.upload import createDataArrayFromLayer
from napari.layers.base.base import Layer
from napari_arnheim.dialogs.upload import UploadFileDialog
from napari_arnheim.widgets.toolbar import ArnheimToolbar
from napari_arnheim.widgets.helper import Helper
import xarray as xr
from bergen.clients.provider import ProviderBergen, Bergen
from napari.viewer import Viewer
from napari_arnheim.widgets.context.context_aware import ContextAwareWidget
from napari_arnheim.widgets.lists.replist import RepresentationListWidget
from PyQt5.QtWidgets import (QLabel,  QPushButton,
                             QVBoxLayout, QWidget)
from qasync import asyncClose, asyncSlot
import asyncio
from bergen.console import console



class ArnheimWidget(QWidget):

    def __init__(self, *args, bergen_params = {}, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.status = QLabel(self)
        self.status.text = "Arnheim"


        self.default_kwargs = {
            "config_path": "bergen.yaml",
            "force_new_token": True,
        }
        self.default_kwargs.update(bergen_params)

        self.user_button = QPushButton("Logout")
        self.layout.addWidget(self.user_button)


    @property
    def helper(self) -> Helper:
        if hasattr(self.parent(), "qt_viewer"):
            return Helper(self.parent().qt_viewer.viewer)


    @property
    def viewer(self) -> Viewer:
        if hasattr(self.parent(), "qt_viewer"):
            return self.parent().qt_viewer.viewer


    @property
    def bergen(self) -> Bergen:
        if hasattr(self, "_bergen"):
            assert self._bergen is not None, "Please instatiate correctly"
            return self._bergen


    @asyncClose
    async def closeEvent(self, event):
        await self._bergen.disconnect_async()



    @asyncSlot()
    async def createRepresentationFromCurrent(self):
        return createDataArrayFromLayer(layer=self.viewer.active_layer)


    @asyncSlot()
    async def connectBergen(self):
        try:
            self._bergen = ProviderBergen(**self.default_kwargs)
            print("Here")
            await self._bergen.negotiate_async()
        except:
            console.print_exception()



