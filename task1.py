import argparse
import shutil
import sys
from pathlib import Path


def extension_folder(file_path: Path) -> str:
    return file_path.suffix.lower().lstrip(".") or "no_extension"


def unique_destination(directory: Path, file_name: str) -> Path:
    destination = directory / file_name
    if not destination.exists():
        return destination

    source_file = Path(file_name)
    counter = 1
    while True:
        candidate = directory / f"{source_file.stem}_{counter}{source_file.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def copy_file(source_file: Path, destination_root: Path) -> None:
    folder = destination_root / extension_folder(source_file)
    folder.mkdir(parents=True, exist_ok=True)
    destination_file = unique_destination(folder, source_file.name)
    shutil.copy2(source_file, destination_file)
    print(f"Скопійовано: {source_file} -> {destination_file}")


def sort_directory(
    source_dir: Path,
    destination_root: Path,
    skipped_dir: Path,
) -> tuple[int, int]:
    copied = 0
    errors = 0

    try:
        entries = sorted(source_dir.iterdir(), key=lambda entry: entry.name.lower())
    except OSError as error:
        print(f"Не вдалося прочитати {source_dir}: {error}", file=sys.stderr)
        return copied, errors + 1

    for entry in entries:
        try:
            resolved_entry = entry.resolve()
            if resolved_entry == skipped_dir or skipped_dir in resolved_entry.parents:
                continue
            if entry.is_symlink():
                print(f"Символічне посилання пропущено: {entry}", file=sys.stderr)
                continue
            if entry.is_dir():
                child_copied, child_errors = sort_directory(
                    entry, destination_root, skipped_dir
                )
                copied += child_copied
                errors += child_errors
            elif entry.is_file():
                copy_file(entry, destination_root)
                copied += 1
        except OSError as error:
            print(f"Не вдалося обробити {entry}: {error}", file=sys.stderr)
            errors += 1

    return copied, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли та групує їх за розширенням."
    )
    parser.add_argument("source", type=Path, help="вихідна директорія")
    parser.add_argument(
        "destination",
        nargs="?",
        type=Path,
        default=Path("dist"),
        help="директорія призначення (за замовчуванням: dist)",
    )
    args = parser.parse_args()

    source_dir = args.source.resolve()
    destination_root = args.destination.resolve()
    if not source_dir.is_dir():
        parser.error(f"вихідна директорія не існує або недоступна: {source_dir}")
    if source_dir == destination_root:
        parser.error("директорії джерела та призначення мають бути різними")

    try:
        destination_root.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        parser.error(f"не вдалося створити директорію призначення: {error}")

    copied, errors = sort_directory(source_dir, destination_root, destination_root)
    print(f"Готово. Скопійовано файлів: {copied}; помилок: {errors}.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())