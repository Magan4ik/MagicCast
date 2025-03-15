#version 330
in vec2 in_position;
uniform float iZoom;
out vec2 fragCoord;
void main() {
    gl_PointSize = 4.0*iZoom;
    gl_Position = vec4(in_position, 0.0, 1.0);
    fragCoord = in_position;
}