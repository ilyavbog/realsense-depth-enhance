import png
import numpy as np


def Middle(a, n):

    if a[0] == 0:
        s = 0
        zero = 1
        for i in range(1, n):
            if a[i] == 0:
                if zero == 2:
                    return 0
                zero += 1
            s += a[i]
        return s / (n - zero)

    if a[1] == 0:
        s = a[0]
        zero = 1
        for i in range(2, n):
            if a[i] == 0:
                if zero == 2:
                    return 0
                zero += 1
            s += a[i]
        return s / (n - zero)

    if a[0] < a[1]:
        min = a[0]
        max = a[1]
    else:
        min = a[1]
        max = a[0]

    s = 0
    for i in range(2, n):
        if a[i] == 0:
            zero = 1
            for j in range(i + 1, n):
                if a[j] == 0:
                    if zero == 2:
                        return 0
                    zero += 1
                s += a[j]
            return (s + min + max) / (n - zero)
        if a[i] < min:
            s += min
            min = a[i]
        elif max < a[i]:
            s += max
            max = a[i]
        else:
            s += a[i]
    return s / (n - 2)


################################################


def Filter(in0, in1, in2, in3, in4, out):

    ############## Reading

    f_name = [in0, in1, in2, in3, in4]
    in_f = []
    reader = []
    info = []  #w(0), h(1), pixels(2), metadata(3)
    arr = []

    for i in range(5):
        in_f.append(open(f_name[i], 'rb'))
        reader.append(png.Reader(in_f[i]))
        info.append(reader[i].read())
        arr.append(list(info[i][2]))
        in_f[i].close()

    w = info[0][0]
    h = info[0][1]

    ############## Handling

    out_arr = np.empty([h, w], dtype=np.uint16)
    for i in range(h):
        for j in range(w):
            ar = [
                arr[0][i][j], arr[1][i][j], arr[2][i][j], arr[3][i][j],
                arr[4][i][j]
            ]
            out_arr[i, j] = Middle(ar, 5)

    ############## Writing

    out_f = open(out, 'wb')
    writer = png.Writer(
        width=w,
        height=h,
        greyscale=True,
        alpha=False,
        planes=1,
        bitdepth=16,
        interlace=0,
        size=(w, h))
    writer.write(out_f, out_arr)
    out_f.close()


################################################

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("in_file_1")
parser.add_argument("in_file_2")
parser.add_argument("in_file_3")
parser.add_argument("in_file_4")
parser.add_argument("in_file_5")
parser.add_argument("out_file")
args = parser.parse_args()

error = False
for name in args.in_file_1, args.in_file_2, args.in_file_3, args.in_file_4, args.in_file_5, args.out_file:
    if name[-4:] != ".png" and name[-4:] != ".PNG":
        print("invalid file name: %s" % (name))
        error = True

if not error:
    Filter(args.in_file_1, args.in_file_2, args.in_file_3, args.in_file_4,
           args.in_file_5, args.out_file)
