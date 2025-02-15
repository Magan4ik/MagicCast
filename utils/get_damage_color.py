from colour import Color


def get_damage_color(damage: float) -> tuple:
    if damage < 0:
        return 0, 255, 0, 255

    damage_values = [0, 25, 50, 75]
    colors = [Color("white"), Color("yellow"), Color("orange"), Color("red")]
    for dmg in range(len(damage_values)):
        if damage <= damage_values[dmg]:
            dmg = min(dmg, len(colors) - 1)
            clrs = list(colors[dmg].range_to(colors[dmg + 1], 25))
            index = int(damage - (damage // 25) * 25)
            clr = []
            for c in clrs[index].rgb:
                clr.append(int(c*255))
            clr.append(255)
            return tuple(clr)

