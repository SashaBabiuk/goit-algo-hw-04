import argparse
import math
import turtle


def draw_koch_curve(pen: turtle.Turtle, length: float, level: int) -> None:
    if level == 0:
        pen.forward(length)
        return

    segment = length / 3
    draw_koch_curve(pen, segment, level - 1)
    pen.left(60)
    draw_koch_curve(pen, segment, level - 1)
    pen.right(120)
    draw_koch_curve(pen, segment, level - 1)
    pen.left(60)
    draw_koch_curve(pen, segment, level - 1)


def draw_snowflake(pen: turtle.Turtle, level: int, side_length: float = 300) -> None:
    height = math.sqrt(3) * side_length / 2
    pen.penup()
    pen.goto(-side_length / 2, -height / 3)
    pen.setheading(0)
    pen.pendown()

    for _ in range(3):
        draw_koch_curve(pen, side_length, level)
        pen.left(120)


def main() -> None:
    parser = argparse.ArgumentParser(description="Малює сніжинку Коха.")
    parser.add_argument(
        "--level",
        type=int,
        help="рівень рекурсії від 0 до 8 (якщо не задано, буде запитано)",
    )
    args = parser.parse_args()

    try:
        level = args.level if args.level is not None else int(input("Рівень рекурсії (0-8): "))
    except ValueError:
        parser.error("рівень рекурсії має бути цілим числом")
    if not 0 <= level <= 8:
        parser.error("рівень рекурсії має бути в межах від 0 до 8")

    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха, рівень {level}")
    screen.tracer(0, 0)
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    side_length = 300 * (3 / 4) ** level
    draw_snowflake(pen, level, side_length)
    screen.update()
    turtle.done()


if __name__ == "__main__":
    main()