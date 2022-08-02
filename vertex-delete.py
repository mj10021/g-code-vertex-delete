import re

with open(r'file location', 'r') as f:
    data = f.read()

target_x = 88.305
target_y = 58.12
max_dist = 3.5
retraction = 1
z_lift = .2

layer_list = [x.split("\n") for x in data.split('AFTER_LAYER_CHANGE')]
for layer_num, layer in enumerate(layer_list):
    if layer_num < 4 or layer_num >= 18:
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
            layer_list[layer_num][i] = 'G1 X%f Y%f E%f' % (back_x, back_y, retraction * -1)
            insertion = ['G91','G1 Z%f' (z_lift),'G90','G1 X%f Y%f' % (x, y),'G91','G1 Z-%f E%f' % (z_lift, retraction),'G90']
            for item in insertion[::-1]:
                layer_list[layer_num].insert(i + 1 ,item)
            
out_data = ';AFTER_LAYER_CHANGE'.join(["\n".join(x) for x in layer_list])

with open("output1.gcode", "w") as f:
    f.write(out_data)