N,M,P,C,D = map(int, input().split())
# 루돌프=-100 / 산타=본인 숫자 / 빈칸=0 / 범위 밖(벽)=-1
#이거 외우기 !!!!!!!!!!!1
#요소들 다 리스트로 감싸져있어야함 []이든 list(map())이든
arr = [[-1]*(N+2)]+[[-1]+[0 for _ in range(N)] + [-1] for _ in range(N)]+[[-1]*(N+2)]
ruy,rux = map(int, input().split())   #루돌프 초기 위치 / 계속 글로벌로 사용
arr[ruy][rux]=-100
santa = {}  #sy,sx,score 리스트로 담음
status = [1 for _ in range(P+1)] #산타상태 > 살아있음=1/기절=0/죽음=-1    #[[]] 인지 체크 식 맞는지
d8 = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]    #루돌프 이동
clock= [0 for _ in range(P+1)]

for _ in range(1,P+1):
    idx,sy,sx=map(int, input().split())
    santa[idx] = ([sy,sx,0])    #현재 위치, score
    arr[sy][sx]=idx

def get_d(y,x):
    return abs(y-ruy)**2 + abs(x-rux)**2

# 루돌프가 이동해서 충돌날 경우 1,i,dir 리턴 (산타인덱스 i) > ru_crush로 이동
# 충돌 없을 경우 0,-1,dir 리턴 > santa move로 이동
def ru_move():
    global ruy, rux
    r_dist=[]
    for s in range(1,P+1):
        #죽지않은 산타만 계산하기
        if status[s] != -1:
            y,x=santa[s][0],santa[s][1]
            dist = get_d(y,x)
            r_dist.append((dist,y,x))
    r_dist.sort(key=lambda x: (-x[0], x[1], x[2]))
    _,ny,nx=r_dist.pop()
    # # 죽지 않은 산타인지 체크 (기절해도 충돌 가능)
    # while status[ny][nx] ==-1:
    #     _, ny, nx = r_dist.pop()
    # 범위 체크 안함 (어차피 산타쪽으로 가기 때문에)
    # 8방향 중 루돌프 한 칸 이동
    nruy=nrux =1
    dir = -1    #산타 충돌 시, 방향 전달해서 그 방향으로 날라가야함
    if nx == rux and ny<ruy:    #위로 이동
        arr[ruy][rux]=0
        nruy,nrux = ruy+d8[0][0],rux+d8[0][1]
        arr[nruy][nrux] = -100
        dir = 0
    elif nx == rux and ny>ruy:  #아래로 이동
        arr[ruy][rux] = 0
        nruy, nrux = ruy + d8[4][0], rux + d8[4][1]
        arr[nruy][nrux] = -100
        dir = 4
    elif ny == ruy and nx>rux:  #오른쪽 이동
        arr[ruy][rux] = 0
        nruy, nrux = ruy + d8[2][0], rux + d8[2][1]
        arr[nruy][nrux] = -100
        dir = 2
    elif ny == ruy and nx<rux:  #왼쪽 이동
        arr[ruy][rux] = 0
        nruy, nrux = ruy + d8[6][0], rux + d8[6][1]
        arr[nruy][nrux] = -100
        dir = 6
    elif ny < ruy and nx<rux: #왼쪽 위로 이동
        arr[ruy][rux] = 0
        nruy, nrux = ruy + d8[7][0], rux + d8[7][1]
        arr[nruy][nrux] = -100
        dir = 7
    elif ny<ruy and nx>rux: #오른쪽 위로 이동
        arr[ruy][rux] = 0
        nruy, nrux = ruy + d8[1][0], rux + d8[1][1]
        arr[nruy][nrux] = -100
        dir = 1
    elif ny>ruy and nx<rux: #왼쪽 아래 이동
        arr[ruy][rux] = 0
        nruy, nrux = ruy + d8[5][0], rux + d8[5][1]
        arr[nruy][nrux] = -100
        dir = 5
    elif ny>ruy and nx>rux: #오른쪽 아래 이동
        arr[ruy][rux] = 0
        nruy, nrux = ruy + d8[3][0], rux + d8[3][1]
        arr[nruy][nrux] = -100
        dir = 3
    ruy, rux = nruy, nrux
    for i in range(1,P+1):
        if ruy==santa[i][0] and rux==santa[i][1]:
            # ru_crush()
            return 1, i, dir #산타 인덱스 같이 반환
    return 0,-1, dir

#루돌프가 이동해서 충돌
def ru_crush(i,dir):    #충돌할 산타 인덱스, 날라갈 방향
    sy,sx,sco=santa[i]
    santa[i][2]+=C  # 산타 점수 얻음
    status[i]=0     #산타 기절로 상태 변경
    clock[i]=2
    dy,dx= d8[dir]
    ny = sy + dy*C
    nx = sx + dx*C
    if ny <1 or ny > N or nx <1 or nx>N:
        status[i]=-1
        #arr[sy][sx]=0   #산타 죽었으니까 있던 자리 빈칸으로 변경안해도 됨 어차피 루돌프가 오버라이트함
        return      #범위 밖으로 나갔으니까 연쇄충돌없음
    else:   #충돌해서 날라간 산타 위치로 갱신
        if arr[ny][nx] >0: #날아갈 위치(루돌프 없음)에 산타가 있어서 연쇄 충돌인 경우
            chain_effect(i, dir,ny,nx) # ny, nx 충돌 시작될 위치
        else:
            #arr[sy][sx]=0 > 이미 루돌프 있음
            arr[ny][nx]=i
            santa[i][0], santa[i][1] = ny, nx

#산타끼리 충돌 연쇄 작용
def chain_effect(s,dir,y,x):    #s는 시작 산타 인덱스/ dir는 연쇄작용방향/ y,x는 충돌 시작 위치
    #santa[s][0], santa[s][1] = y,x #충돌 시작 위치에 시작 산타 두기
    #sy,sx,sc=santa[s]   #충돌 시작한 산타
    dy,dx=d8[dir]
    ny,nx=y,x
    q=[]
    while 0<ny<=N and 0<nx<=N:
        for i in range(1,P+1):
            if i!=s and status[i]!=-1 and ny==santa[i][0] and nx==santa[i][1]:
                q.append(i)
                break
        ny+=dy
        nx+=dx

    while q:
        idx = q.pop()
        cy,cx=santa[idx][0],santa[idx][1]
        nny,nnx=cy+dy, cx+dx
        if 0 < nny <= N and 0 < nnx <= N:
            santa[idx][0],santa[idx][1]=nny,nnx
            arr[nny][nnx]=idx
            arr[cy][cx]=0
        else:
            status[idx]=-1  #죽음 표시
    arr[y][x]=s

# 기절하지 않고 살이있는 산타만 움직이게 본문에서 처리 미리 해둠
def san_move(idx):
    global ruy, rux
    y, x = santa[idx][0], santa[idx][1]

    def move_step(i,dir,cy,cx):
        ny,nx= cy+d8[dir][0],cx+d8[dir][1]
        if 0<ny<=N and 0<nx<=N:   #범위 내에서만 움직임
            if arr[ny][nx] > 0:  # 산타있는경우 움직이지 않음
                return
            elif arr[ny][nx] == -100:  # 루돌프있는경우
                s_crush(i,dir,ny,nx)
            else:   #빈칸인 경우
                arr[cy][cx]=0
                arr[ny][nx]=i
                santa[i][0], santa[i][1] = ny, nx

    def move_step_2(i,dir1,dir2,cy,cx):
        redo=False
        ny,nx= cy+d8[dir1][0],cx+d8[dir1][1]
        if 0<ny<=N and 0<nx<=N:   #범위 내에서만 움직임
            if arr[ny][nx] > 0:  # 산타있는경우 움직이지 않음
                redo=True
            elif arr[ny][nx] == -100:  # 루돌프있는경우
                s_crush(i,dir,cy,cx)
            else:   #빈칸인 경우
                arr[cy][cx]=0
                arr[ny][nx]=i
                santa[i][0], santa[i][1] = ny, nx
        if redo:
            ny, nx = cy + d8[dir2][0], cx + d8[dir2][1]
            if 0 < ny <= N and 0 < nx <= N:  # 범위 내에서만 움직임
                if arr[ny][nx] > 0:  # 산타있는경우 움직이지 않음
                    return
                elif arr[ny][nx] == -100:  # 루돌프있는경우
                    s_crush(i, dir, ny, nx)
                else:  # 빈칸인 경우
                    arr[cy][cx] = 0
                    arr[ny][nx] = i
                    santa[i][0], santa[i][1] = ny, nx

    # 범위 체크 안함 (어차피 루돌프쪽으로 가기 때문에)
    # 4방향 중 산타 한 칸 이동
    dir = -1
    if x == rux and y>ruy:    #위로 이동
        dir = 0
        move_step(idx, dir, y, x)
    elif x == rux and y<ruy:  #아래로 이동
        dir = 4
        move_step(idx, dir, y, x)
    elif y == ruy and x<rux:  #오른쪽 이동
        dir = 2
        move_step(idx, dir, y, x)
    elif y == ruy and x>rux:  #왼쪽 이동
        dir = 6
        move_step(idx, dir, y, x)
    elif y > ruy and x>rux:  #왼쪽 위로 이동
        ny1,nx1=y+d8[6][0],x+d8[6][1] #왼쪽
        temp1 = get_d(ny1,nx1)
        ny2, nx2 = y + d8[0][0], x + d8[0][1] #위쪽
        temp2 = get_d(ny2, nx2)
        if temp1<temp2:
            dir1, dir2=6,0
        else:   #상하 우선
            dir1, dir2=0,6
        move_step_2(idx, dir1, dir2, y, x)
    elif y>ruy and x<rux: #오른쪽 위로 이동
        ny1,nx1=y+d8[2][0],x+d8[2][1] #오른쪽
        temp1 = get_d(ny1,nx1)
        ny2, nx2 = y + d8[0][0], x + d8[0][1] #위쪽
        temp2 = get_d(ny2, nx2)
        if temp1<temp2:
            dir1,dir2=2,0
        else:   #상하 우선
            dir1,dir2=0,2
        move_step_2(idx, dir1, dir2, y, x)
    elif y<ruy and x>rux:  #왼쪽 아래 이동
        ny1, nx1 = y + d8[6][0], x + d8[6][1]  # 왼쪽
        temp1 = get_d(ny1, nx1)
        ny2, nx2 = y + d8[4][0],x+d8[4][1]  # 아래
        temp2 = get_d(ny2, nx2)
        if temp1 < temp2:
            dir1,dir2 = 6,4
        else:  # 상하 우선
            dir1,dir2 = 4,6
        move_step_2(idx, dir1, dir2, y, x)
    elif y<ruy and x<rux:  #오른쪽 아래 이동
        ny1, nx1 = y+d8[2][0],x+d8[2][1]  # 오른쪽
        temp1 = get_d(ny1, nx1)
        ny2, nx2 = y+d8[4][0],x+d8[4][1]  # 아래
        temp2 = get_d(ny2, nx2)
        if temp1 < temp2:
            dir1,dir2 = 2,4
        else:  # 상하 우선
            dir1,dir2 = 4,2
        move_step_2(idx, dir1, dir2, y, x)


def s_crush(i,dir,cy,cx):
    #점수 D 획득
    #한칸이동해서 일단 충돌 자리로 이동
    #D만큼 반대 방향으로 날아감
    #범위 밖이면 탈락
    #범위 내면 빈캄 혹은 연쇄 충돌
    sy,sx,sc=santa[i]
    santa[i][2]+=D
    #cy,cx= sy+d8[dir][0],sx+d8[dir][1]  #cy인지 sy인지 어차피 두 개 동일한거 같음
    # santa[i][0],santa[i][0]=ny,nx
    ndy,ndx=d8[dir][0]*(-1),d8[dir][1]*(-1)    #반대방향으로 날아감
    ndir = d8.index((ndy,ndx))
    ny=cy+ndy*D
    nx=cx+ndx*D
    status[i]=0
    clock[i]=2
    if ny < 1 or ny > N or nx < 1 or nx > N:
        status[i] = -1
        arr[sy][sx]=0   #산타 죽었으니까 있던 자리 빈칸으로 변경
        return  # 범위 밖으로 나갔으니까 연쇄충돌없음
    else:  # 충돌해서 날라간 산타 위치로 갱신
        if arr[ny][nx] > 0:  # 날아갈 위치(루돌프 없음)에 산타가 있어서 연쇄 충돌인 경우
            santa[i][0], santa[i][1]=ny,nx  #날아간 위치 저장
            arr[sy][sx]=0   #원래 있던 위치 빈칸으로 변경
            chain_effect(i, ndir, ny, nx)  # ny, nx 충돌 시작될 위치
        else:
            arr[sy][sx]=0
            arr[ny][nx] = i
            santa[i][0], santa[i][1] = ny, nx
    return

for _ in range(M):
    finish=True
    for j in range(1,P+1):
        if clock[j]>0:
            clock[j]-=1
        if clock[j]==0 and status[j]==0:
            status[j]=1
    rgo, sidx, dir = ru_move()
    if rgo:
        ru_crush(sidx, dir)
    for idx in range(1,P+1):
        if status[idx] == 1:
            san_move(idx)
    for i in range(1,P+1):
        if status[i] != -1:
            santa[i][2] +=1
            finish=False
        if finish:  #모든 산타 죽으면 끝
            break

score = [santa[i][2] for i in range(1,P+1)]
print(*score)