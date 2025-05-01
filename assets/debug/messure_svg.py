import re
import math
import sys

def tokenize_path(d):
    return re.findall(r'[a-zA-Z]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d)

def measure_path(d):
    tokens = tokenize_path(d)
    i = 0
    x, y = 0.0, 0.0
    start_x, start_y = 0.0, 0.0
    points = []

    last_cmd = ''

    while i < len(tokens):
        token = tokens[i]
        if re.match(r'[a-zA-Z]', token):
            cmd = token
            i += 1
        else:
            cmd = last_cmd

        rel = cmd.islower()
        cmd = cmd.upper()
        last_cmd = cmd

        def next_floats(n):
            vals = [float(tokens[j]) for j in range(i, i+n)]
            return vals

        if cmd == 'M':
            x1, y1 = next_floats(2)
            i += 2
            x, y = (x + x1, y + y1) if rel else (x1, y1)
            start_x, start_y = x, y
            points.append((x, y))
            while i + 1 < len(tokens) and not re.match(r'[a-zA-Z]', tokens[i]):
                x1, y1 = next_floats(2)
                i += 2
                x, y = (x + x1, y + y1) if rel else (x1, y1)
                points.append((x, y))
        elif cmd == 'L':
            while i + 1 < len(tokens) and not re.match(r'[a-zA-Z]', tokens[i]):
                x1, y1 = next_floats(2)
                i += 2
                x, y = (x + x1, y + y1) if rel else (x1, y1)
                points.append((x, y))
        elif cmd == 'H':
            while i < len(tokens) and not re.match(r'[a-zA-Z]', tokens[i]):
                x1 = float(tokens[i])
                i += 1
                x = x + x1 if rel else x1
                points.append((x, y))
        elif cmd == 'V':
            while i < len(tokens) and not re.match(r'[a-zA-Z]', tokens[i]):
                y1 = float(tokens[i])
                i += 1
                y = y + y1 if rel else y1
                points.append((x, y))
        elif cmd == 'Z':
            x, y = start_x, start_y
            points.append((x, y))
        elif cmd == 'A':
            while i + 6 < len(tokens) and not re.match(r'[a-zA-Z]', tokens[i]):
                rx = float(tokens[i])
                ry = float(tokens[i+1])
                x_axis_rotation = float(tokens[i+2])
                large_arc_flag = int(tokens[i+3])
                sweep_flag = int(tokens[i+4])
                x1 = float(tokens[i])
                y1 = float(tokens[i+1])
                i += 7
                if rel:
                    x1 += x
                    y1 += y
                # Approximate arc as a straight line
                points.append((x1, y1))
                x, y = x1, y1
        else:
            print(f"Unsupported command: {cmd}")
            break

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x = min(xs, default=0)
    max_x = max(xs, default=0)
    min_y = min(ys, default=0)
    max_y = max(ys, default=0)
    width = max_x - min_x
    height = max_y - min_y

    length = sum(
        math.hypot(x1 - x0, y1 - y0)
        for (x0, y0), (x1, y1) in zip(points, points[1:])
    )

    return width, height, length


def main():
    path_data = input()
    w, h, l = measure_path(path_data)
    print(f"Width:  {w:.2f}px")
    print(f"Height: {h:.2f}px")
    print(f"Length: {l:.2f}px")

if __name__ == '__main__':
    main()
