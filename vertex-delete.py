import re

with open(file_location, 'r') as f:
    data = f.read()

target_x = 88.305
target_y = 58.12
max_dist = 3.5
retraction = 0.4
de_retraction_ratio = 1.25
z_lift = .4

layer_list = [x.split("\n") for x in data.split('AFTER_LAYER_CHANGE')]
for layer_num, layer in enumerate(layer_list):
    if layer_num < 4 or layer_num >= 14:
        continue
    for i, cmd in enumerate(layer):
        if type(cmd) is not str:
            continue
        match = re.match(r'G1 X(.*) Y(.*) E.*', cmd)
        if match is None:
            continue
        x, y = [float(x_) for x_ in match.groups()]
        if abs(x - target_x) < max_dist and abs(y - target_y) < max_dist:
            backstep = re.match(r'G1 X(.*) Y(.*) E.*', layer_list[layer_num][i-2])
            if backstep is None:
                continue
            back_x, back_y = [float(x__) for x__ in backstep.groups()]
            layer_list[layer_num][i] = ';MOD_START'
            
            insertion = [
                f'G1 X{back_x} Y{back_y} E-{retraction};reverse move and retract',
                'G91;relative positioning',
                f'G1 Z{z_lift};lift z',
                'G90;absolute positioning',
                f'G1 X{x} Y{y};next move',
                'G91;relative positioning',
                f'G1 Z-{z_lift} E{retraction * de_retraction_ratio};resume z and de-retract',
                'G90;absolute positioning',
                'G4 P50;dwell 50ms',
                ';MOD_END',
                ]

            for item in insertion[::-1]:
                layer_list[layer_num].insert(i + 1 ,item)
            
out_data = ';AFTER_LAYER_CHANGE'.join(["\n".join(x) for x in layer_list])

with open("output1.gcode", "w") as f:
    f.write(out_data)