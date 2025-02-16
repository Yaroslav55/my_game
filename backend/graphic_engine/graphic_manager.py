from backend.tiles.common import set_singleton
from const_variables_store import RENDER_API
from openglrender import OpenGLRender


@set_singleton
class GraphicManager:

    render_cls = None
    def __init__(self, *args, **kwargs):

        if RENDER_API == "Opengl":
            self.render_cls = OpenGLRender
        self.render_cls = self.render_cls(*args, **kwargs)

    def run(self):
        self.render_cls.run()
