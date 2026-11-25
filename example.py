import argparse
import csv
from pathlib import Path

HEADERS = ('位置', '容量', '已摆')
DEFAULT_RECORDS = (
    ('东架绘本', 18, 13),
    ('中架散文', 22, 17),
    ('西架画册', 12, 7),
    ('窗边矮筐', 14, 7),
)
UNIT = '册'


def read_records(file_path):
    with file_path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != list(HEADERS):
            raise ValueError("表头应为 " + "、".join(HEADERS))
        records = []
        for row in reader:
            try:
                label = (row[HEADERS[0]] or "").strip()
                capacity = int(row[HEADERS[1]])
                occupied = int(row[HEADERS[2]])
            except (TypeError, ValueError) as error:
                raise ValueError(f"第{reader.line_num}行数量应为整数") from error
            if not label or not 0 <= occupied <= capacity:
                raise ValueError(f"第{reader.line_num}行名称或数量有误")
            records.append((label, capacity, occupied))
        return records


def main():
    parser = argparse.ArgumentParser(description='换书架余位速查')
    parser.add_argument("file", nargs="?", type=Path, help="UTF-8 CSV 文件")
    args = parser.parse_args()
    try:
        records = read_records(args.file) if args.file else DEFAULT_RECORDS
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")

    for label, capacity, occupied in records:
        print(f"{label}  剩余 {capacity - occupied} {UNIT}")
    total = sum(capacity - occupied for _, capacity, occupied in records)
    print(f"合计剩余 {total} {UNIT}")


if __name__ == "__main__":
    main()
