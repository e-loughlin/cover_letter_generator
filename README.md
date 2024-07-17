Replace LaTeX Template Placeholders with YAML Config and OpenAI Queries

## Introduction

This script reads a YAML configuration file, a LaTeX template file, and a company info file, then replaces placeholders in the LaTeX template with values from the YAML configuration and OpenAI query results. The final output is written to a specified output file.

## Requirements

- Python 3.x
- PyYAML
- OpenAI Python client

## Installation

1. Install the required Python packages:

   ```bash
   pip install pyyaml openai
   ```

````

## Files

1. config.yaml
   This file contains the configuration settings, including the OpenAI API key, key-value pairs for template replacement, and queries.

2. template.tex
   This LaTeX template file contains placeholders in the form {{key}} that will be replaced with values from the YAML configuration file.

3. company_info.txt
   This text file contains the job description and company info that will be used to replace the {{company_info}} placeholder in the LaTeX template.

4. self_info.txt
   This text file contains a summary of who you and your resume.

## Usage

Run the script with the following command:

```bash
python cover_letter_generator.py --config ./working/config.yaml --template ./working/cover_letter_base.tex --company_info ./working/company_info.txt --self_info ./working/self_info.txt -o ./working/output.tex
```

Arguments:

- `--config` or `-c`: Path to the YAML configuration file.
- `--template` or `-t`: Path to the LaTeX template file.
- `--company_info` or `-ci`: Path to the company info text file.
- `--self_info` or `-si`: Path to the self information text file.
- `--output` or `-o`: Path to the output LaTeX file.

## Example Files

1. config.yaml

```yaml
# General Configurations
OPENAI_API_KEY: "your API key"

# Key-Value Pairs that will be replaced in the Template
keys:
  name: John Doe
  company_name: Acme Corporation
  company_title: Senior Software Engineer
  company_address: 1234 Elm Street, Springfield, USA

# Queries, where the response will be replaced in the Template based on that key
queries:
  cover_letter_content: >
    Write a cover letter for a Senior Software Engineer applying to Acme Corporation.
```

2. template.tex

```latex
\documentclass{article}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

\begin{document}

\begin{center}
    \large
    \textbf{{{company_name}}} \\
    {{{company_address}}} \\
    \vspace{1em}
    \textbf{{{company_title}}} \\
\end{center}

\vspace{2em}

\noindent
\textbf{From:} \\
{{{name}}} \\
\vspace{1em}

\noindent
{{{cover_letter_content}}}

\vspace{2em}

\noindent
\textbf{Company Info:} \\
{{{company_info}}}

\end{document}
```

3. company_info.txt

```
Acme Corporation is a leading firm in the industry, known for its innovative solutions and dynamic work environment. The Senior Software Engineer position involves working on cutting-edge projects and collaborating with a talented team of professionals.
```

## Output

The script will generate an output LaTeX file (e.g., output.tex) with all placeholders replaced by the corresponding values from the YAML configuration, OpenAI query results, company info, and self info.

## License

This project is licensed under the MIT License.
````
