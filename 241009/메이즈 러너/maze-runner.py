N, M, K = map(int,input().split())
maze = [list(map(int,input().split())) for _ in range(N)]
# 참가자들이 이동할 것이기 때문에 tuple이 아닌 list로 좌표 설정
participants = [list(map(int, input().split())) for _ in range(M)]   # y,x 순서
for p in participants:  # 좌표 시작 1부터라서 -1 해서 0으로 맞춤
    p[0] -= 1
    p[1] -= 1
exit_y, exit_x = map(int, input().split())  #좌표
exit_x -=1
exit_y -=1

here = [[False]*N for _ in range(N)]
for y,x in participants:
    here[y][x]=True
cal_list = [0 for _ in range(len(participants))]

dx = [0, 0, 1, -1] # 남 북 동 서
dy = [1, -1, 0, 0]
move_dist = 0
done = 0
done_list = [False for _ in range(len(participants))]

#bfs
def move():
    global move_dist, done
    for j in range(len(participants)):
        if not done_list[j]:
            for i in range(4):
            # 벽이 아닌 경우에만 거리 계산 실행
                cy, cx = participants[j][0]+dy[i], participants[j][1]+dx[i]
                #print("cy", cy, "cx", cx)
                if cy == exit_y and cx == exit_x:
                    #print("move 1")
                    done += 1
                    here[participants[j][0]][participants[j][1]] = False
                    move_dist += 1
                    done_list[j]=True
                    break
                    #del participants[j]
                    #del cal_list[j]
                    
                if in_range(cy, cx) and not maze[cy][cx] and not here[cy][cx]:
                    #print("move 2")
                    cur_dist = cal_list[j] # x, y 좌표
                    temp = cal_dist(cx,cy)
                    #print(f"cal list[{j}]: ", temp)
                    if temp < cur_dist:
                        #print("j",j, "i", i)
                        #print("temp", temp, "cur", cur_dist)
                        here[participants[j][0]][participants[j][1]] = False
                        here[cy][cx] = True
                        participants[j][0] = cy
                        participants[j][1] = cx
                        move_dist += 1
                        break                    

def cal_dist(cx, cy):
    return abs(cx-exit_x)+abs(cy-exit_y)

def in_range(cx, cy):
    return 0<=cx<N and 0<=cy<N

def rotate(sx, sy, length):   # 90도 회전
    global exit_x, exit_y
    narr = [x[sx:sx+length] for x in maze[sy:sy+length]] #회전할 배열 복사
    #exit하고 참가자 좌표 회전 부분 다시 보기 ㅠㅠ
    if sy <= exit_y < sy+length and sx<= exit_x < sx+length:
        exit_x, exit_y = length - (exit_y - sy) - 1, exit_x - sx
        exit_x += sx
        exit_y += sy
        #print("exit rot", exit_y, exit_x)
    for person in participants:
        px, py = person[1], person[0]
        if sy <= py < sy + length and sx <= px < sx + length:
            new_x = sx + (length - (py - sy) - 1)
            new_y = sy + (px - sx)
            person[1], person[0] = new_x, new_y
    # 이거는 회전만 한 것
    for y in range(length):
        for x in range(length):
            narr[x][length-y-1] = maze[sy+y][sx+x]
    # 회전된 배열을 원래 배열에 반영해야함
    for y in range(length):
        for x in range(length):
            maze[sy+y][sx+x] = narr[y][x]
    #벽의 내구도 -1 적용
    for y in range(sy, sy+length):
        for x in range(sx, sx+length):
            if maze[y][x]!=0:
                maze[y][x] -= 1
                

def find_box():
    mins = float('inf')
    length = 0
    sy, sx = 0, 0  # Top-left corner of the box
    for i in range(len(cal_list)):
        if not done_list[i]:
            dist = cal_list[i]
            #print("dist", dist)
            if dist < mins:
                mins = dist
                h= abs(participants[i][0]-exit_y)
                w = abs(participants[i][1]-exit_x)
                length = max(h,w)+1
                #print("len", length)
            #여기 코드는 다시 보기 ㅠㅠ
                sy = max(participants[i][0], exit_y)
                sx = min(participants[i][1], exit_x)
                sy = max(0, sy - (length - 1))
                sx = max(0, sx - (length - 1))

                if sy + length > N:
                    sy = N - length
                if sx + length > N:
                    sx = N - length
    return sy, sx, length

for k in range(K):
    if done == len(participants):
        break
    for person_idx in range(len(participants)):
        cy, cx = participants[person_idx][0],participants[person_idx][1]
        cal_list[person_idx] = cal_dist(cx, cy)
    #print("cal list: ", cal_list)
    #print("1 : ", participants)
    move()
    for person_idx in range(len(participants)):
        cy, cx = participants[person_idx][0],participants[person_idx][1]
        cal_list[person_idx] = cal_dist(cx, cy)
    sy, sx, length = find_box()
    #print("2 : ", participants)
    #print("ssl", sy,sx,length)
    rotate(sx, sy, length)
    #print("after",participants)
    #print('K:', k)
    #print(f'move_dist:{move_dist}, done:{done}')

print(move_dist)
print(exit_x, exit_y)