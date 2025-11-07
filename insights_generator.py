# insights_generator.py


import csv
import os
from typing import List, Dict, Tuple, Optional


def load_csv(path: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k: (v if v is not None else "") for k, v in r.items()})
    return rows


def detect_numeric_columns(rows: List[Dict[str, str]]) -> List[str]:
    if not rows:
        return []
    cols = list(rows[0].keys())
    numeric = []
    for c in cols:
        ok = True
        for r in rows:
            v = r.get(c, "").strip()
            if v == "":
                continue
            try:
                float(v)
            except ValueError:
                ok = False
                break
        if ok:
            numeric.append(c)
    return numeric


def basic_stats(rows: List[Dict[str, str]], col: str) -> Optional[Dict[str, float]]:
    vals: List[float] = []
    for r in rows:
        v = r.get(col, "").strip()
        if v == "":
            continue
        try:
            vals.append(float(v))
        except ValueError:
            # skip non-numeric garbage if any slipped through
            continue
    if not vals:
        return None
    return {
        "avg": sum(vals) / len(vals),
        "min": min(vals),
        "max": max(vals),
        "count": float(len(vals)),
    }


def missing_values(rows: List[Dict[str, str]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    if not rows:
        return out
    for c in rows[0].keys():
        cnt = 0
        for r in rows:
            if r.get(c, "").strip() == "":
                cnt += 1
        if cnt > 0:
            out[c] = cnt
    return out


def first_categorical_column(rows: List[Dict[str, str]], numeric_cols: List[str]) -> Optional[str]:
    if not rows:
        return None
    for c in rows[0].keys():
        if c not in numeric_cols:
            return c
    return None


def most_frequent(rows: List[Dict[str, str]], col: str) -> Optional[Tuple[str, int]]:
    freq: Dict[str, int] = {}
    for r in rows:
        v = r.get(col, "").strip()
        if v == "":
            continue
        freq[v] = freq.get(v, 0) + 1
    if not freq:
        return None
    k = max(freq, key=freq.get)
    return k, freq[k]


def write_report(
    out_path: str,
    file_name: str,
    rows_count: int,
    numeric_cols: List[str],
    stats_map: Dict[str, Dict[str, float]],
    cat_col: Optional[str],
    cat_top: Optional[Tuple[str, int]],
    missing: Dict[str, int],
) -> None:
    lines: List[str] = []
    lines.append("DATA INSIGHTS REPORT")
    lines.append("-" * 32)
    lines.append(f"Source file: {file_name}")
    lines.append(f"Total rows: {rows_count}")
    lines.append("")

    if numeric_cols:
        lines.append("Numeric columns summary:")
        for c in numeric_cols:
            s = stats_map.get(c)
            if not s:
                continue
            lines.append(f"  {c}: avg={s['avg']:.2f}, min={s['min']}, max={s['max']} (n={int(s['count'])})")
        lines.append("")
    else:
        lines.append("No numeric columns detected.")
        lines.append("")

    if cat_col and cat_top:
        lines.append(f"Most frequent value in '{cat_col}': {cat_top[0]} ({cat_top[1]} occurrences)")
        lines.append("")
    elif cat_col:
        lines.append(f"No frequent value computed for '{cat_col}' (no non-empty values).")
        lines.append("")

    if missing:
        lines.append("Missing values:")
        for c, n in missing.items():
            lines.append(f"  {c}: {n}")
        lines.append("")

    # short, plain insights section
    lines.append("Notes:")
    if numeric_cols:
        lines.append("- Numeric spread suggests basic variation present.")
    if cat_col and cat_top:
        lines.append(f"- '{cat_col}' has a dominant category: {cat_top[0]}.")
    if not missing:
        lines.append("- No missing values detected.")
    lines.append("-" * 32)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    # Input CSV; adjust if you keep files elsewhere. Supports running from any cwd.
    csv_path = os.path.join(os.path.dirname(__file__), "data", "sales_data.csv")
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    rows = load_csv(csv_path)
    print(f"Loaded {len(rows)} rows.")

    numeric_cols = detect_numeric_columns(rows)

    # compute stats per numeric column
    stats_map: Dict[str, Dict[str, float]] = {}
    for c in numeric_cols:
        s = basic_stats(rows, c)
        if s:
            stats_map[c] = s

    # choose first categorical column and compute top value
    cat_col = first_categorical_column(rows, numeric_cols)
    cat_top = most_frequent(rows, cat_col) if cat_col else None

    # missing values per column
    missing = missing_values(rows)

    out_path = os.path.join(os.path.dirname(__file__), "sample_output.txt")
    write_report(
        out_path=out_path,
        file_name=os.path.basename(csv_path),
        rows_count=len(rows),
        numeric_cols=numeric_cols,
        stats_map=stats_map,
        cat_col=cat_col,
        cat_top=cat_top,
        missing=missing,
    )

    print(f"Report written to: {out_path}")


if __name__ == "__main__":
    main()
