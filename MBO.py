import numpy as np
import math
import random
from scipy.special import gamma
import copy
import matplotlib.pyplot as plt

city_name = []
city_condition = []
with open('30城市的坐标.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()

    # 获取30城市坐标
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(',')
        city_name.append(line[0])
        city_condition.append([int(line[1]), int(line[2])])
city_condition = np.array(city_condition)


#参数設置
butterfly_count = 200
p = 5/12
peri = 1.2
MaxGen = 200
iter = 0
BAR = 5/12


#先随机生成蝴蝶数量个列表 每个列表里是城市的号码
city_count = len(city_name)
butterfly = []
for ko in range(butterfly_count):
    city = random.sample(range(1, city_count+1), city_count)
    butterfly.append(city)

#计算城市之间的距离
distance = np.zeros((city_count, city_count))
for i in range(city_count):
    for j in range(city_count):
        if i != j:
            distance[i][j] = math.sqrt((city_condition[i][0] - city_condition[j][0]) ** 2 + (city_condition[i][1] - city_condition[j][1]) ** 2)
        else:
            distance[i][j] = 100000

list_answer_distance = []
list_answer_butterfly = []
while iter < MaxGen:

    list_distance = []

    #计算每个蝴蝶里所走路线的距离
    for a in range(butterfly_count):
        sum_distance = 0
        for row in range(city_count-1):
            sum_distance += distance[butterfly[a][row]-1][butterfly[a][row+1]-1]
        sum_distance += distance[butterfly[a][-1]-1][butterfly[a][0]-1]
        list_distance.append(sum_distance)




    #把得到的距离按照由小到大排序
    sequence_distance = sorted(list_distance)


    #把蝴蝶的顺序按照距离的大小排序，放在new butterfly里
    new_butterfly = []
    for x in sequence_distance:
        y = butterfly[list_distance.index(x)]
        new_butterfly.append(y)

    #用butterfly代替new butterfly
    butterfly = copy.deepcopy(new_butterfly)
    best = 0    #sequence_distance.index(min(sequence_distance))
    best_butterfly = new_butterfly[best]

    #把蝴蝶种群分成两部分
    Land1 = butterfly[:int(butterfly_count*p-1)]
    Land2 = butterfly[int(butterfly_count*p-1):]
    Land1_c = copy.deepcopy(Land1)
    Land2_c = copy.deepcopy(Land2)
    new_Land1 = Land1
    new_Land2 = Land2



    #在land1里的所有蝴蝶，按照r和p的关系进行操作，如果r小于等于p在land1里随机选一个，
    # 如果它的距离小于之前的用它代替之前的，如果不是则保持原来的
    for i in range(0, len(Land1)):
        rand = random.random()
        r = rand * peri
        if r <= p:
            R1 = random.randint(0, len(Land1)-1)
            new_Land1[i] = Land1_c[R1]
   #如果r大于p，在land2里随机选择一个，如果他的距离小于之前的，就用它代替，如果不是就保持原来
        else:
            R2 = random.randint(0, len(Land2)-1)
            new_Land1[i] = Land2_c[R2]




    #所有在land2里的蝴蝶进行操作
    for j in range(0, len(Land2)):
        #根据公式算出step的值，并设置成正整数,范围在2到city count
        change_list = []
        beta = 1
        alpha_u = math.pow((gamma(1 + beta) * math.sin(math.pi * beta / 2) / (gamma(((1 + beta) / 2) * beta * math.pow(2, (beta - 1) / 2)))), (1 / beta))
        alpha_v = 1
        u = np.random.normal(0, alpha_u, 1)
        v = np.random.normal(0, alpha_v, 1)
        step = int(abs(u / math.pow(abs(v), (1 / beta))))
        if step < 2:
            step = 2
        elif step > city_count:
            step = city_count
        #根据得到step的值，建立一个列表，列表里放step个 范围在1到城市总数之间的随机整数
        change_list = random.sample(range(1, city_count + 1), step)

        rand = random.random()
        #根据rand和p的关系进行操作，如果rand 小于等于p，把在land2里第j个数据换成 best butterfly这个数据
        if rand <= p:
            new_Land2[j] = best_butterfly
        #如果不是 在land2中随机选一个，用它替换掉之前的
        else:
            R3 = random.randint(0, len(Land2)-1)
            new_Land2[j] = Land2_c[R3]


            #在rand 大于p的基础上如果rand 大于bar，则 用step建立的列表 对land2里第j个数据（因为j是个列表）
            # 里进行位置交换
            if rand > BAR:

                for good in range(len(change_list)-1):
                    new_Land2[j][new_Land2[j].index(change_list[good])], new_Land2[j][new_Land2[j].index(change_list[good+1])] = new_Land2[j][new_Land2[j].index(change_list[good+1])], new_Land2[j][new_Land2[j].index(change_list[good])]



    #最后把新的land1和land2重新合并成一个新的蝴蝶种群

    butterfly = new_Land1 + new_Land2


    #计算出每次最短路径和最好的蝴蝶
    fitness_distance = []
    for b in range(butterfly_count):
        answer_distance = 0
        for f in range(city_count - 1):
            answer_distance += distance[butterfly[b][f] - 1][butterfly[b][f + 1] - 1]
        answer_distance += distance[butterfly[b][-1] - 1][butterfly[b][0] - 1]
        fitness_distance.append(answer_distance)

    answer = min(fitness_distance)
    answer_butterfly = butterfly[fitness_distance.index(answer)]


    #为了绘制图片建立一个list answer distance列表，把answer放进去
    list_answer_distance.append(answer)
    list_answer_butterfly.append(answer_butterfly)

    iter += 1
print(list_answer_butterfly[-1])

print(list_answer_distance[-1])

#绘制迭代图
fig = plt.figure()
plt.title("Distance iteration graph")
plt.plot(range(1, MaxGen+1), list_answer_distance)
plt.xlabel("Number of iterations")
plt.ylabel("Distance value")

#绘制路线图
fig1 = plt.figure()
plt.title("Best Route Map")
x = []
y = []
path = []
for i in list_answer_butterfly[-1]:
    x.append(city_condition[i-1][0])
    y.append(city_condition[i-1][1])

x.append(city_condition[list_answer_butterfly[-1][0]-1][0])
y.append(city_condition[list_answer_butterfly[-1][0]-1][1])

path = list_answer_butterfly[-1]
path.append(list_answer_butterfly[-1][0])
for i in range(len(x)):
    plt.annotate(list_answer_butterfly[-1][i], xy=(x[i], y[i]), xytext=(x[i] + 0.3, y[i] + 0.3))
plt.plot(x, y, '-o')
plt.show()
























