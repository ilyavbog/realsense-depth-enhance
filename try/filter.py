import png
import numpy as np

def Middle (a, n) :

    if a[0] == 0 :
        s = 0
        zero = 1
        for i in range(1, n) :
            if a[i] == 0 :
                if zero == 2 :
                    return 0
                zero += 1
            s += a[i]
        return s / (n - zero)

    if a[1] == 0 :
        s = a[0]
        zero = 1
        for i in range(2, n) :
            if a[i] == 0 :
                if zero == 2 :
                    return 0
                zero += 1
            s += a[i]
        return s / (n - zero)


    if a[0] < a[1] :
        min = a[0]
        max = a[1]
    else :
        min = a[1]
        max = a[0]

    s = 0
    for i in range(2, n) :
        if a[i] == 0 :
            zero = 1
            for j in range(i+1, n) :
               if a[j] == 0 :
                    if zero == 2 :
                        return 0
                    zero += 1
               s += a[j]
            return (s + min + max) / (n - zero)
        if a[i] < min :
            s += min
            min = a[i]
        elif max < a[i] :
            s += max
            max = a[i]
        else :
            s += a[i]
    return s / (n-2)

################################################


def Filter (in0, in1, in2, in3, in4, out) :

    ############## Reading

    f_name = [in0, in1, in2, in3, in4]
    in_f = []
    reader = []
    info = [] #w(0), h(1), pixels(2), metadata(3)
    arr = []

    for i in range(5) :
        in_f.append (open(f_name[i], 'rb'))
        reader.append (png.Reader(in_f[i]))
        info.append(reader[i].read ())
        arr.append (list(info[i][2]))
        in_f[i].close()

    w = info[0][0]
    h = info[0][1]

    ############## Handling

    out_arr = np.empty([h,w], dtype=np.uint16)
    for i in range(h) :
        for j in range(w) :
            ar = [arr[0][i][j], arr[1][i][j], arr[2][i][j], arr[3][i][j], arr[4][i][j]]
            out_arr[i,j] = Middle(ar, 5)

    ############## Writing

    out_f = open(out, 'wb')
    writer = png.Writer (width=w, height=h, greyscale=True, alpha=False, planes=1, bitdepth=16, interlace=0, size=(w, h))
    writer.write(out_f, out_arr)
    out_f.close()

################################################

Filter ("in_f0.png", "in_f1.png", "in_f2.png", "in_f3.png", "in_f4.png", "out_a.png")
#Filter ("14e99a1b77fceb00-00-depth.png", "14e99a1b77fceb00-01-depth.png", "14e99a1b77fceb00-02-depth.png", "14e99a1b77fceb00-03-depth.png", "14e99a1b77fceb00-04-depth.png", "out4.png")
