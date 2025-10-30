import sys
import re
import json

def load_regex(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {k: re.compile(v, re.IGNORECASE) for k, v in data.items()}
    except FileNotFoundError:
        print(f"Regex file '{path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON format in '{path}'.")
        sys.exit(1)
    except re.error as e:
        print(f"Invalid regex pattern: {e}")
        sys.exit(1)

def detect_in_file(file_path, regex_dict):
    results = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, start=1):
                for name, pattern in regex_dict.items():
                    for match in pattern.findall(line):
                        results.append({
                            "file": file_path,
                            "line": i,
                            "type": name,
                            "value": match
                        })
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Skipping.")
    return results

if __name__ == "__main__":
    if "-i" not in sys.argv:
        print("Usage: python dlp.py -i <file1> <file2> ... [-o output.json] [--regex-file regex.json]")
        sys.exit(1)

    file_index = sys.argv.index("-i") + 1

    # Optional arguments
    regex_index = sys.argv.index("--regex-file") if "--regex-file" in sys.argv else None
    o_index = sys.argv.index("-o") if "-o" in sys.argv else None

    # Determine input files range
    next_args = [i for i in [regex_index, o_index] if i]
    stop_index = min(next_args) if next_args else len(sys.argv)
    files = sys.argv[file_index:stop_index]

    # Default values
    regex_file = "regex-config.json"
    output = "report_dlp.json"

    # Override if provided
    if regex_index:
        regex_file = sys.argv[regex_index + 1]
    if o_index:
        output = sys.argv[o_index + 1]

    regex_dict = load_regex(regex_file)

    all_results = []
    for f in files:
        all_results.extend(detect_in_file(f, regex_dict))

    with open(output, "w", encoding="utf-8") as out:
        json.dump(all_results, out, indent=4, ensure_ascii=False)

    print(f"Report saved to {output}")
