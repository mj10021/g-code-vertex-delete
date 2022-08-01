import re

with open(r'gcode file location', 'r') as f:
    data = f.read()

target_x = #vertex x
target_y = #vertex y
max_dist = 3.5
retraction = 0.6

layer_list = [x.split("\n") for x in data.split('AFTER_LAYER_CHANGE')]
for layer_num, layer in enumerate(layer_list):
    if layer_num < 4 or layer_num >= 18:
        continue
    for i, cmd in enumerate(layer):
        match = re.match(r'G1 X(.*) Y(.*) E.*', cmd)
        if match is None:
            continue
        x, y = [float(x_) for x_ in match.groups()]
        if abs(x - target_x) < max_dist and abs(y - target_y) < max_dist:
            layer_list[layer_num][i] = 'G1 X%f Y%f E%f' % (x, y, retraction * -1)
            temp_match = re.match(r'G1 X(.*) Y(.*) E(.*)', layer_list[layer_num][i + 1])
            if temp_match is not None:
                x, y, e = [float(x_) for x_ in temp_match.groups()]
                layer_list[layer_num][i+1] = 'G1 X%f Y%f E%f' % (x, y, e + retraction)


out_data = ';AFTER_LAYER_CHANGE'.join(["\n".join(x) for x in layer_list])

with open("output1.gcode", "w") as f:
    f.write(out_data)