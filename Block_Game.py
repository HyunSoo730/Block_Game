import turtle as t  #turtle 그래픽 모듈 사용할꺼야
import random as r
import sys
import time

dy=[-1, 0, 1, 0]
dx=[0, 1, 0, -1]   #방향벡터 초기화

class Brick():  #블럭 객체
    def __init__(self):  #생성자.
        self.y = 0  #첫 생성은 0행
        self.x = 6  #1~12사이인 6번에 위치
        self.color = r.randint(1,6)  

    def move_left(self, grid):
        if grid[self.y][self.x-1]==0 and grid[self.y+1][self.x-1]==0:
            grid[self.y][self.x]=0
            self.x-=1
    
    def move_right(self, grid):
        if grid[self.y][self.x+1]==0 and grid[self.y+1][self.x+1]==0:
            grid[self.y][self.x]=0
            self.x+=1


def draw_grid(block, grid):    #보드판(그리드) 그리기
    block.clear()
    top = 250
    left = -150
    colors = ["black", "red", "blue", "orange", "yellow", "green", "purple", "white"]
    for y in range(len(grid)):  #행 개수만큼(25)
        for x in range(len(grid[0])):   #열 개수 만큼(14)
            sc_x = left + (x * 22) #박스 하나에 20px여서   #스크린의 x좌표
            sc_y = top - (y * 22)  #스크린의 y좌표
            #스크린 상에서는 좌표대로 위로갈수록 y좌표 증가 아래로 갈수록 y좌표 감소 이런 식이야!

            block.goto(sc_x, sc_y)
            if y == 15 and grid[y][x] == 7:   
                block.color("red")
            else:
                block.color(colors[grid[y][x]])
            block.stamp()


def DFS(y, x, grid, color):
    global ch, blank
    ch[y][x]=1
    blank.append((y, x))
    for i in range(4):
        yy=y+dy[i]
        xx=x+dx[i]
        if 0<yy<24 and 0<xx<13:
            if grid[yy][xx]==color and ch[yy][xx]==0:
                DFS(yy, xx, grid, color)

def max_height(grid):
    for y in range(1, 24):
        for x in range(1, 13):
            if grid[y][x]!=0:
                return y              


def grid_update(grid, blank):
    for y, x in blank:
        grid[y][x]=0
    height=max_height(grid)
    for y in range(23, height, -1):
        for x in range(1, 13):
            if grid[y][x]==0:
                tmp_y=y
                while grid[tmp_y-1][x]==0 and tmp_y-1>0:
                    tmp_y-=1
                grid[y][x]=grid[tmp_y-1][x]
                grid[tmp_y-1][x]=0

def continual_remove():
    global blank, ch
    while True:
        flag=1
        for y in range(23, 15, -1):
            for x in range(1, 13):
                if grid[y][x]!=0:
                    ch=[[0]*14 for _ in range(25)]
                    blank=[]
                    DFS(y, x, grid, grid[y][x])
                    if len(blank)>=4:
                        grid_update(grid, blank)
                        flag=0
        draw_grid(block, grid)
        if flag==1:
            break

def game_over():
    pen.up()
    pen.goto(-120, 100)
    pen.write("Game Over", font=("courier", 30))

def you_win():
    pen.up()
    pen.goto(-100, 100)
    pen.write("You Win", font=("courier", 30))


if __name__ == "__main__":
    sc = t.Screen()   #스크린 객체 만들어
    sc.tracer(False)  #추적 기능을 꺼! --> 한방에 확 그려줌.
    sc.bgcolor("black")  #배경을 검은색으로
    sc.setup(width = 600, height=700)   #창의 크기 지정

    #격자판 2차원 리스트로 만들자
    grid = [[0] * 12 for _ in range(24)]  #행이 24 열이 12개
    for i in range(24):    #벽을 칠해야지
        grid[i].insert(0,7)
        grid[i].append(7)   #벽을 7로 표현
    grid.append([7] * 14)  #맨 마지막 줄 역시 벽으로
    for y in range(23,20,-1):   #밑에 3줄만 랜덤으로 색깔 채우자
        for x in range(1, 13):
            grid[y][x] = r.randint(1,6)   #1~6까지 랜덤으로 부여
    #7을 읽으면 흰색 블럭, 0을 만나면 검은색 블럭(빈공간처럼 보이도록)
    #블럭의 한 변의 길이 20px인거 기억하고 진행하자
    #여기까지가 기본 설정


    block = t.Turtle()   #그래픽 객체 만들어서 창에다가 그리디 정보를 표현하자
    block.penup()   
    block.speed(0)   
    block.shape("square")
    block.color("red")
    block.setundobuffer(None)  #버퍼 누적 x
    #창의 좌표는 정중앙이 0,0이고 좌표의 개념 그대로 적용하면 돼


    brick = Brick()
    grid[brick.y][brick.x] = brick.color  #블럭 생성위치 그리디에 그려주자
    draw_grid(block, grid)   #격자정보를 블럭이라는 객체를 이용해서 그래픽 처리하자
    #좌표공간처럼 사용할 것이기에 행을 y로 열을 x로 표현하자
    
    pen=t.Turtle()
    pen.ht()
    pen.goto(-80, 290)
    pen.color("white")
    pen.write("Block Game", font=('courier', 20, 'normal'))
  
    sc.onkeypress(lambda: brick.move_left(grid), "Left")
    sc.onkeypress(lambda: brick.move_right(grid), "Right")
    sc.listen()
    
    
    #블럭의 움직임 구현
    while True:
        sc.update()  #스크린을 계속 업데이트 해줘야함. 
        if grid[brick.y+1][brick.x]==0:  #블럭 앞에서 멈춰주기.
            grid[brick.y][brick.x]=0  #먼저 현재 좌표를 지우고 내려가야지
            brick.y+=1
            grid[brick.y][brick.x]=brick.color
        else:
            ch=[[0]*14 for _ in range(25)]
            blank=[]
            DFS(brick.y, brick.x, grid, brick.color)
            if len(blank)>=4:
                grid_update(grid, blank)
                continual_remove()

            height=max_height(grid)
            if height<=15:
                game_over()
                break
            elif height>=22:
                draw_grid(block, grid)
                you_win()
                break

            brick=Brick()

        draw_grid(block, grid)
        time.sleep(0.05)
    
    


    sc.mainloop()   #창을 유지하기 위해