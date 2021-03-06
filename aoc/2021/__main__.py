import click

DAYS_SOLVED = 3

@click.command()
@click.argument('day')
def run_aoc(day: str) -> None:
    day = int(day)
    if not (1 <= day and day <= 25):
        raise RuntimeError("Day must be a value between 1-25.")
    if not (day <= DAYS_SOLVED):
        raise RuntimeError(f"There are only solutions up to day {DAYS_SOLVED}. Choose a smaller number.")

    # import the right solution code to execute
    package = f"aoc.day{day}.solution"
    name = "solution"
    solution = getattr(__import__(package, fromlist=[name]), name)

    solution()


if __name__ == '__main__':
    run_aoc()
