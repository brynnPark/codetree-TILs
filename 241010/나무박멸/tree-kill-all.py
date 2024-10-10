n,m,k,c = map(int, input().split())
# 범위 밖은 -2로 감싸서 같이 처리
board = [[-2]*(n+2)]+[[-2] +list(map(int, input().split()))+[-2] for _ in range(n)] + [[-2]*(n+2)]
d = [(-1,1),(1,1),(1,-1),(-1,-1)]     # clockwise
gq=[]   #grow queue
add_q = []
q =[]
ans=0

def grow():
    for y in range(1,n+1):
        for x in range(1,n+1):
            if board[y][x] >0:  #나무인 경우만 성장( !=0 하면 벽도 성장해버려서 안됨)
                cnt = 0
                for ddy, ddx in [(-1,0),(1,0),(0,1),(0,-1)]:
                    if board[y+ddy][x+ddx] >0: cnt+=1
                gq.append((y,x,cnt))    #동시추가하기 위해 큐에 담아둠
    while gq:   # 동시성장
        cy,cx,ccnt=gq.pop()
        board[cy][cx] += ccnt

def thrive():
    for y in range(1,n+1):
        for x in range(1,n+1):
            if board[y][x]>0:   #나무인 경우, 주변 번식
                cnt = 0
                for ddy, ddx in [(-1,0),(1,0),(0,1),(0,-1)]:
                    if board[y+ddy][x+ddx]==0: cnt+=1   #빈칸수로 나눔
                if cnt:
                    will_add = board[y][x]//cnt
                    add_q.append((y,x,will_add))    #y,x 좌표 주변은 add만큼 번식

    # 동시추가를 위해서 현재 빈칸인 곳들 담아두기
    while add_q:
        cy,cx,add = add_q.pop()
        for ddy, ddx in [(-1, 0), (1, 0), (0, 1), (0,-1)]:
            if board[cy + ddy][cx + ddx] == 0:  #현재 빈칸이 아닌 곳은 추가하지 않음
                q.append((cy+ddy,cx+ddx,add))

    while q:
        ccy,ccx,add=q.pop()
        board[ccy][ccx] += add


def remove(k,c):
    global ans
    rq = []
    #수명 다 된 제초제 제거 작업
    for rry in range(1,n+1):
        for rrx in range(1,n+1):
            if board[rry][rrx] < -1000:
                board[rry][rrx]+=1
                if board[rry][rrx] == -1000:
                    board[rry][rrx]=0

    for y in range(1,n+1):
        for x in range(1,n+1):
            trees = 0
            if board[y][x]>0:   #나무인 경우
                trees += board[y][x]
                for dy, dx in d:
                    ny, nx = y, x
                    for i in range(k):
                        ny += dy
                        nx += dx
                        if board[ny][nx]>0:
                            trees+=board[ny][nx]
                        else:  # 빈칸이나 벽인 경우 중단
                            break
                rq.append((trees,y,x))
    rq.sort(key=lambda x: (x[0], -x[1], -x[2]))
    if not rq:
        return
    rtree,ry,rx = rq.pop()
    ans += rtree
    board[ry][rx] = -1000-c
    for dy, dx in d:
        ny, nx = ry, rx
        for i in range(k):
            ny += dy
            nx += dx
            if board[ny][nx] > 0:
                board[ny][nx] = -1000-c
            else:
                if board[ny][nx] != -2:
                    board[ny][nx] = -1000 - c
                break

for _ in range(m):
    grow()
    thrive()
    remove(k,c)
print(ans)