import sys
import re
import json

regex = {
    "cpf": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "email": re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,63}\b", re.IGNORECASE),
    "apikey": re.compile(r"(?i)\b(?:api[_-]?\s*key|apikey|key)\b[\s:=\"']+([A-Za-z0-9\-_./+=]{16,128})"),
    "cellphone": re.compile(r"\b(?:\+?55\s?)?(?:\(?[1-9][0-9]\)?\s?)?(?:9?\d{4})-?\d{4}\b"),
    "ip": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}(?:25[0-5]|2[0-4]\d|1?\d{1,2})\b")
}

def detect_info(text):
    all_matches = {}
    for name, pattern in regex.items():
        matches = pattern.findall(text)
        if matches:
            all_matches[name] = matches
    return all_matches if all_matches else None


def read_file(file):
    results = []
    with open(file, 'r') as infile:
        lines = infile.readlines()

    for idx, line in enumerate(lines, start=1):
        detections = detect_info(line)
        if detections:
            for tipo, valores in detections.items():
                for valor in valores:
                    results.append({
                        "file": file,
                        "line": idx,
                        "type": tipo,
                        "value": valor
                    })
    return results


def report(info, output_name):
    if not info:
        print("No info found.")
        return None

    with open(output_name, "w") as outfile:
        json.dump(info, outfile, indent=4, ensure_ascii=False)

    return output_file


if __name__ == "__main__":

    all_infos = []

    if len(sys.argv) < 3 or "-i" not in sys.argv:
        print("Use: python dlp.py -i <file1> <file2> ... <fileN> [-o output_file]")
        sys.exit(1)

    file_index = sys.argv.index("-i") + 1

    if file_index >= len(sys.argv):
        print("Use: python dlp.py -i <file1> <file2> ... <fileN> [-o output_file]")
        sys.exit(1)

    if "-o" in sys.argv:
        o_index = sys.argv.index("-o")
        files = sys.argv[file_index:o_index]
        output_file = sys.argv[o_index + 1]
    else:
        files = sys.argv[file_index:]
        output_file = "report_dlp,json"
        
    for file_path in files:
        infos = read_file(file_path)
        all_infos.extend(infos)

    final = report(all_infos, output_file)
