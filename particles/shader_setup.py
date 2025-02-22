import moderngl


class ShaderConfig:
    def __init__(self, ctx: moderngl.Context, prog: moderngl.Program, win_width: int, win_height: int):
        self._ctx = ctx
        self._prog = prog
        self.win_width = win_width
        self.win_height = win_height

    @property
    def ctx(self) -> moderngl.Context:
        return self._ctx

    @property
    def program(self) -> moderngl.Program:
        return self._prog


def setup(win_width: int, win_height: int) -> ShaderConfig:
    ctx = moderngl.create_context()

    vertex_source = open("shaders/spell_particles_vertex.glsl", "r", encoding="utf-8").read()
    fragment_source = open("shaders/spell_particles_fragment.glsl", "r", encoding="utf-8").read()

    program = ctx.program(vertex_shader=vertex_source, fragment_shader=fragment_source)
    program["iResolution"].value = (win_width, win_height)
    return ShaderConfig(ctx, program, win_width, win_height)
