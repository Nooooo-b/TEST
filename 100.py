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

    # 都市の座標を取る
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(',')
        city_name.append(line[0])
        city_condition.append([int(line[1]), int(line[2])])
city_condition = np.array(city_condition)


#パラメータ設定
butterfly_count = 200
p_max = 0.9
p_min = 0.1
peri = 1.2
MaxGen = 200
iter = 1
BAR = 5/12
p = 0

#ランダムにリストを生成しる
city_count = len(city_name)
butterfly = []
for ko in range(butterfly_count):
    city = random.sample(range(1, city_count+1), city_count)
    butterfly.append(city)

#都市の間の距離を計算
distance = np.zeros((city_count, city_count))
for i in range(city_count):
    for j in range(city_count):
        if i != j:
            distance[i][j] = math.sqrt((city_condition[i][0] - city_condition[j][0]) ** 2 + (city_condition[i][1] - city_condition[j][1]) ** 2)
        else:
            distance[i][j] = 100000

list_answer_distance = []
list_answer_butterfly = []
while iter <= MaxGen:

    a = (p_min * MaxGen - p_max) / (MaxGen - 1)
    b = (p_max - p_min) / (MaxGen - 1)
    p = a + b * iter


    list_distance = []

    #すべての距離を計算
    for a in range(butterfly_count):
        sum_distance = 0
        for row in range(city_count-1):
            sum_distance += distance[butterfly[a][row]-1][butterfly[a][row+1]-1]
        sum_distance += distance[butterfly[a][-1]-1][butterfly[a][0]-1]
        list_distance.append(sum_distance)




    #排列する
    sequence_distance = sorted(list_distance)



    new_butterfly = []
    for x in sequence_distance:
        y = butterfly[list_distance.index(x)]
        new_butterfly.append(y)


    butterfly = copy.deepcopy(new_butterfly)
    best = 0    #sequence_distance.index(min(sequence_distance))
    best_butterfly = new_butterfly[best]

    #チョウの群れに二つ分ける
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

        list_substring_distance = []
        if r <= p:
            Le = random.randint(1, city_count)
            R1 = random.randint(0, len(Land1)-1)
            for two in range(1, city_count+1):
                two_distance = distance[Le-1][two-1]
                list_substring_distance.append(two_distance)
            change_Land1 = new_Land1[i]
            if Le != change_Land1[-1]:
                change_Land1[change_Land1.index(Le)+1], change_Land1[change_Land1.index(list_substring_distance.index(min(list_substring_distance))+1)] = change_Land1[change_Land1.index(list_substring_distance.index(min(list_substring_distance))+1)],change_Land1[change_Land1.index(Le)+1]
            else:
                change_Land1[0], change_Land1[change_Land1.index(list_substring_distance.index(min(list_substring_distance))+1)] = change_Land1[change_Land1.index(list_substring_distance.index(min(list_substring_distance))+1)], change_Land1[0]
            i_distance = 0
            change_distance = 0
            for rw in range(city_count-1):
                i_distance += distance[new_Land1[i][rw]-1][new_Land1[i][rw+1]-1]
            i_distance += distance[new_Land1[i][-1]-1][new_Land1[i][0]-1]
            for rq in range(city_count-1):
                change_distance += distance[change_Land1[rq]-1][change_Land1[rq+1]-1]
            change_distance += distance[change_Land1[-1]-1][change_Land1[0]-1]

            if change_distance < i_distance:
                new_Land1[i] = change_Land1

            #else:
                #new_Land1[i] = Land1_c[R1]


        else:
            R2 = random.randint(0, len(Land2)-1)
            new_Land1[i] = Land2_c[R2]





    for j in range(0, len(Land2)):


        beta = 1
        alpha_u = math.pow((gamma(1 + beta) * math.sin(math.pi * beta / 2) / (gamma(((1 + beta) / 2) * beta * math.pow(2, (beta - 1) / 2)))), (1 / beta))
        alpha_v = 1
        u = np.random.normal(0, alpha_u, 1)
        v = np.random.normal(0, alpha_v, 1)
        step = int(abs(u / math.pow(abs(v), (1 / beta))))
        new_step = step
        if new_step < 1:
            new_step = 1
        elif new_step > city_count-2*new_step:
            new_step = city_count-2*new_step
        m = new_step
        k = random.randint(0, city_count-2*new_step)



        rand = random.random()

        if rand <= p:
            new_Land2[j] = best_butterfly

        else:
            R3 = random.randint(0, len(Land2)-1)
            new_Land2[j] = Land2_c[R3]


            #ley flight

            if rand > BAR:
                for x in range(m):
                    new_Land2[j][k+x], new_Land2[j][k+x+new_step] = new_Land2[j][k+x+new_step], new_Land2[j][k+x]


    #最后把新的land1和land2重新合并成一个新的蝴蝶种群

    butterfly = new_Land1 + new_Land2


    #ベストのチョウを計算
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






