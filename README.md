# Simple DLP

This Python script scans text files for potential **sensitive information** such as **email**, **API keys** and **IP addresses**.  
It is intended to assist with **Data Loss Prevention (DLP)** by detecting sensitive data patterns.

---

## Features

- Detects common types of sensitive information:
  - Emails
  - API Keys
  - IPv4 addresses

- Supports **multiple input files**
- Outputs a **JSON report** with all detections
- Reports include **file name**, **line number**, and **value detected**
- **Customizable regex patterns** through an external configuration file

---

## File Structure

The project is organized as follows:

```bash
/
├── dlp.py              # Main script
├── regex_config.json   # Custom regex definitions (user-editable)
└── README.md           # Documentation
```

---

## How It Works

1. The script loads regular expressions from `regex_config.json`.  
2. Each file provided via command-line arguments is scanned line by line.  
3. When a pattern match is found, the result is added to a JSON report.  
4. The final report lists all detections with file name, line number, and value.

---

## Usage

Run the script with the `-i` flag followed by the files to scan.  
Optionally, use `-o` to specify a custom output file name for the JSON report.

### Example (basic)

```bash
python dlp.py -i file1.txt file2.txt
```

This generates a report named **report_dlp.json** in the current directory.

---

### Example (custom output file)

```bash
python dlp.py -i logs.log emails.csv -o result.json
```

---

## Output Structure

The JSON report contains a list of detections.  
Each detection entry includes:

- **file:** file name analyzed  
- **line:** line number where the match was found  
- **type:** type of information detected  
- **value:** matched value

### Example Output (`report_dlp.json`)

```json
[
    {
        "file": "logs.txt",
        "line": 12,
        "type": "email",
        "value": "user@example.com"
    },
    {
        "file": "test.txt",
        "line": 18,
        "type": "ip",
        "value": "10.10.10.1"
    }
]
```

---

## Regex Customization

Regular expressions are defined in a separate configuration file called **`regex_config.json`**.  
You can easily modify or add new patterns without editing the main script.

### Example (`regex_config.json`)

```json
{
    "email": "\\b[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,63}\\b",
    "apikey": "(?i)\\b(?:api[_-]?\\s*key|apikey|key)\\b[\\s:=\\\"']+([A-Za-z0-9\\-_./+=]{16,128})",
    "ip": "\\b(?:(?:25[0-5]|2[0-4]\\d|1?\\d{1,2})\\.){3}(?:25[0-5]|2[0-4]\\d|1?\\d{1,2})\\b"
}
```

### Adding new patterns

To detect new data types (for example, credit card numbers), simply add a new entry:

```json
{
    "credit_card": "\\b(?:\\d[ -]*?){13,16}\\b"
}
```

The script will automatically include it in future scans.

---

## Example

Given a text file `data.txt` with the following content:

```text
Name: John Doe
Email: john@example.com
Server: 192.168.0.10
API_KEY: A1B2C3D4E5F6G7H8I9J0
```

Run the script:

```bash
python dlp.py -i data.txt
```

Output (`report_dlp.json`):

```json
[
    {"file": "data.txt", "line": 2, "type": "email", "value": "john@example.com"},
    {"file": "data.txt", "line": 3, "type": "ip", "value": "192.168.0.10"},
    {"file": "data.txt", "line": 4, "type": "apikey", "value": "A1B2C3D4E5F6G7H8I9J0"}
]
```

---

## Error Handling

If run with incorrect parameters, the script prints the correct usage format:

```bash
Use: python dlp.py -i <file1> <file2> ... <fileN> [-o output_file]
```

---

## Notes

- The script is dependency-free and uses only Python standard libraries.  
- The regex configuration is external and editable (`regex_config.json`).  
- Each line is scanned individually, so large files may take longer to process.  
- The default output file name is **`report_dlp.json`**, but can be changed with `-o`.
