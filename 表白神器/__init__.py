import turtle
import math
import random

# 设置整体变换速度
speed = 5

# 设置窗体
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")


# 随机生成七彩颜色
def random_color():
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    return random.choice(colors)


# 定义心形函数
def heart_curve(t):
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, y


# 绘制心形
def draw_heart():
    turtle.color("red")
    turtle.begin_fill()
    turtle.penup()
    for t in range(0, 628, speed):
        x, y = heart_curve(t / 100)
        turtle.goto(x * 10, y * 10)  # 放大10倍以适应窗口大小
        turtle.pendown()
    turtle.end_fill()
    turtle.hideturtle()


# 写文字
def write_text(text):
    turtle.penup()
    turtle.color("white")
    turtle.goto(0, -200)
    turtle.write(text, align="center", font=("Arial", 24, "bold"))


# 发散粒子效果
def scatter_particles():
    for _ in range(50):
        x = random.randint(-400, 400)
        y = random.randint(-300, 300)
        turtle.penup()
        turtle.goto(x, y)
        turtle.dot(5, random_color())


# 主函数
def main():
    turtle.speed(0)
    while True:
        draw_heart()
        write_text("我爱Python")
        scatter_particles()
        turtle.clearstamps()
        turtle.clear()
    turtle.done()


if __name__ == "__main__":
    main()
