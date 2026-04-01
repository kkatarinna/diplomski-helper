import csv
import sys
import re
from collections import defaultdict

def parse_query(query):
    query = query.strip()

    if not query.lower().startswith("select"):
        raise ValueError("Upit mora poceti sa SELECT")

    # GROUP BY
    group_by_col = None
    if re.search(r"\bGROUP BY\b", query, re.IGNORECASE):
        query, group_part = re.split(r"\bGROUP BY\b", query, flags=re.IGNORECASE)
        group_by_col = group_part.strip()

    # WHERE
    where_part = None
    if re.search(r"\bWHERE\b", query, re.IGNORECASE):
        query, where_part = re.split(r"\bWHERE\b", query, flags=re.IGNORECASE)

    # SELECT
    select_part = query[6:].strip()
    select_fields = [f.strip() for f in select_part.split(",")]

    conditions = []
    operators = []

    if where_part:
        tokens = re.split(r"\b(AND|OR)\b", where_part, flags=re.IGNORECASE)
        for token in tokens:
            token = token.strip()
            if token.upper() in ("AND", "OR"):
                operators.append(token.upper())
            else:
                if re.search(r"\bLIKE\b", token, re.IGNORECASE):
                    col, val = re.split(r"\bLIKE\b", token, flags=re.IGNORECASE)
                    conditions.append(("LIKE", col.strip(), val.strip()))
                elif "=" in token:
                    col, val = token.split("=", 1)
                    conditions.append(("=", col.strip(), val.strip()))
                else:
                    raise ValueError(f"Nevalidan WHERE uslov: {token}")

    return select_fields, conditions, operators, group_by_col


def match_like(value, pattern):
    regex = "^" + re.escape(pattern).replace("%", ".*") + "$"
    return re.match(regex, value) is not None


def evaluate_conditions(row, conditions, operators):
    if not conditions:
        return True

    def eval_single(cond):
        op, col, val = cond
        cell = row.get(col, "")
        if op == "=":
            return cell == val
        if op == "LIKE":
            return match_like(cell, val)
        return False

    result = eval_single(conditions[0])

    for i, operator in enumerate(operators):
        next_result = eval_single(conditions[i + 1])
        result = result and next_result if operator == "AND" else result or next_result

    return result


def main():
    if len(sys.argv) < 3:
        print("Korišćenje:")
        print("python csvql.py <csv_path> <separator>")
        sys.exit(1)

    csv_path = sys.argv[1]
    separator = sys.argv[2]

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter=separator))

    print("CSVQL shell (sa GROUP BY)")
    print("exit / quit za izlaz")
    print("-" * 40)

    while True:
        try:
            query = input("csvql> ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit"):
                break

            select_fields, conditions, operators, group_by = parse_query(query)

            # WHERE filtriranje
            filtered = [r for r in rows if evaluate_conditions(r, conditions, operators)]

            # GROUP BY logika
            if group_by:
                groups = defaultdict(list)
                for row in filtered:
                    groups[row[group_by]].append(row)

                print(separator.join(select_fields))

                for key, items in groups.items():
                    output = []
                    for field in select_fields:
                        if field == group_by:
                            output.append(key)
                        elif field.upper().startswith("COUNT"):
                            output.append(str(len(items)))
                        else:
                            raise ValueError("Dozvoljeno je samo GROUP kolona i COUNT()")
                    print(separator.join(output))
            else:
                print(separator.join(select_fields))
                for row in filtered:
                    print(separator.join(row[f] for f in select_fields))

        except Exception as e:
            print(f"Greška: {e}")


if __name__ == "__main__":
    main()
