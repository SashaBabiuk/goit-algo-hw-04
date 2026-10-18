import argparse
import random
import timeit
from collections.abc import Callable


Sorter = Callable[[list[int]], list[int]]


def insertion_sort(values: list[int]) -> list[int]:
    for index in range(1, len(values)):
        current = values[index]
        position = index - 1
        while position >= 0 and values[position] > current:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = current
    return values


def merge_sort(values: list[int]) -> list[int]:
    if len(values) < 2:
        return values

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    merged: list[int] = []
    left_index = right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def timsort(values: list[int]) -> list[int]:
    return sorted(values)


def build_datasets(size: int) -> dict[str, list[int]]:
    generator = random.Random(2026 + size)
    random_values = [generator.randrange(size * 10 + 1) for _ in range(size)]
    sorted_values = sorted(random_values)
    nearly_sorted = sorted_values.copy()
    for _ in range(max(1, size // 100)):
        first = generator.randrange(size)
        second = generator.randrange(size)
        nearly_sorted[first], nearly_sorted[second] = (
            nearly_sorted[second],
            nearly_sorted[first],
        )

    return {
        "random": random_values,
        "sorted": sorted_values,
        "reverse": sorted_values[::-1],
        "nearly sorted": nearly_sorted,
    }


def benchmark(sorters: dict[str, Sorter], sizes: list[int], repeats: int) -> None:
    print("| Розмір | Дані | Insertion sort, с | Merge sort, с | Timsort, с |")
    print("|---:|---|---:|---:|---:|")

    for size in sizes:
        for data_name, values in build_datasets(size).items():
            timings = {}
            for sorter_name, sorter in sorters.items():
                samples = timeit.Timer(lambda sorter=sorter, values=values: sorter(values.copy())).repeat(
                    repeat=repeats, number=1
                )
                timings[sorter_name] = min(samples)
            print(
                f"| {size} | {data_name} | {timings['Insertion sort']:.6f} "
                f"| {timings['Merge sort']:.6f} | {timings['Timsort']:.6f} |"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Порівнює insertion sort, merge sort і вбудований Timsort."
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[100, 1000, 5000],
        help="розміри наборів даних",
    )
    parser.add_argument("--repeats", type=int, default=3, help="кількість повторів timeit")
    args = parser.parse_args()
    if any(size < 1 for size in args.sizes):
        parser.error("розміри наборів мають бути додатними")
    if args.repeats < 1:
        parser.error("кількість повторів має бути додатною")

    sorters: dict[str, Sorter] = {
        "Insertion sort": insertion_sort,
        "Merge sort": merge_sort,
        "Timsort": timsort,
    }
    benchmark(sorters, args.sizes, args.repeats)


if __name__ == "__main__":
    main()