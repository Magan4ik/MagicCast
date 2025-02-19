#version 330
uniform vec2 iResolution;
uniform vec2 iCenter;
uniform float iTime;
uniform float life_time;
uniform vec3 color_mod;
uniform float brightness;
in vec2 fragCoord;
out vec4 color;
void main() {
    vec2 uv = fragCoord.xy;
    vec2 center = iCenter.xy;
    uv.x *= iResolution.x/iResolution.y;
    center.x *= iResolution.x / iResolution.y;

    float fade = 1. - min(1., iTime/life_time);
    float d = distance(center.xy, uv.xy);
    vec3 clr = color_mod;
    fade *= brightness/d;

    color = vec4(clr, fade);
}