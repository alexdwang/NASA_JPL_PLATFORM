import matplotlib.pyplot as plt


def plotfigure(X, Y):
    plt.figure(1, figsize=(8,6))
    plt.plot(X, Y, 'b*')
    plt.plot(X, Y, 'r',label="X and Y")
    plt.xlabel("V(1)")
    plt.ylabel("I(ROUT)")
    plt.legend(loc='lower right')

    plt.show()
    return


f = open('AD590_pre_rad_27C_V1.txt', 'r')
lines = f.readlines()
f.close()


XnY = []

cnt = 0

for line in lines:
    line = line.strip('\n')
    my_line = line.split(' ')
    for word in my_line:
        if word != '':
            try:
                XnY.append(float(word))
            except:
                cnt += 1
# print(lines)

X = [XnY[i] for i in range(len(XnY)) if i % 2 == 0]
Y = [XnY[i] for i in range(len(XnY)) if i % 2 != 0]

print(X)
print()
print(Y)


plotfigure(X, Y)

