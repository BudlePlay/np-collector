DATA_PATH = 'data'
NAME = 'poke'

ORIGIN_DATA_PATH = 'origin/poke/poke_11.csv'
ROW_CNT = 15


import os

SAVE_PATH = os.path.join(DATA_PATH, NAME)

files = os.listdir(SAVE_PATH)

cnt = 0
for s in files:
    try:
        num = int(s.split('_')[1].split('.')[0])
        if cnt<num:
            cnt=num
    except:
        pass

print('data의 개수 : ', cnt)

cnt += 1



import matplotlib
import clipboard

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import pandas as pd

df = pd.read_csv(ORIGIN_DATA_PATH)


fig, ax = plt.subplots(figsize=(15, 8))
plt.grid(True)
plt.xlabel('time')
plt.ylabel('y')
plt.title('IMU data collector')

ax.set_aspect('auto', adjustable='box')

x = [i for i in range(len(df))]

ax.set_ylim(-400, 400)

for i in range(1, 4):
    y = df.iloc[:, i] * 100
    ax.plot(x, y, label=str(df.columns[i]), color='r')
    ax.legend()

for i in range(4, 7):
    y = df.iloc[:, i]
    ax.plot(x, y, label=str(df.columns[i]), color='g')
    ax.legend()

x_line = []
y_line = []
line, = ax.plot(x_line, y_line)


def remove_line():
    x_line.clear()
    y_line.clear()
    line.set_data(x_line, y_line)
    plt.draw()


def draw_vertical_line(x):
    x_line.append(x)
    y_line.append(500)

    x_line.append(x)
    y_line.append(-500)

    x_line.append(x + ROW_CNT - 1)
    y_line.append(-500)

    x_line.append(x + ROW_CNT - 1)
    y_line.append(500)

    line.set_data(x_line, y_line)
    plt.draw()


x = 0


def add_point(event):
    global x
    global cnt
    if event.inaxes != ax:
        return

    # mouse left click
    if event.button == 1:
        x = int(event.xdata)

        remove_line()

        draw_vertical_line(x)

    # mouse right click
    if event.button == 3:
        cut_df = df.loc[x:x + ROW_CNT - 1].set_index('time')
        csv = cut_df.to_csv()

        # print('---------------------------------------------------')
        # print(csv)
        # clipboard.copy(csv)

        filename = NAME + '_' + str(cnt) + '.csv'
        path = os.path.join(SAVE_PATH, filename)

        f = open(path,mode='wt', encoding='utf-8')

        for i in csv.split('\n'):
            print(i)
            f.write(i)
            
        print(path)
        f.close()

        cnt += 1
        

        

    # mouse mid click
    if event.button == 2:
        plt.disconnect(cid)
        plt.close()


def on_press(event):
    global x
    if event.key == 'right':
        x += 1
        remove_line()
        draw_vertical_line(x)

    if event.key == 'left':
        x -= 1
        remove_line()
        draw_vertical_line(x)


cid = plt.connect('button_press_event', add_point)
plt.connect('key_press_event', on_press)

plt.show()