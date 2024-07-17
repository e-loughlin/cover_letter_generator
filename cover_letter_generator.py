import argparse
import yaml
import openai

def read_config(config_filepath):
    with open(config_filepath, 'r') as file:
        return yaml.safe_load(file)

def read_template(template_filepath):
    with open(template_filepath, 'r') as file:
        return file.read()

def read_info(info_filepath):
    with open(info_filepath, 'r') as file:
        return file.read()

def write_output(output_filepath, content):
    with open(output_filepath, 'w') as file:
        file.write(content)

def replace_placeholders(template, config):
    for key, value in config.items():
        placeholder = f"{{{{{key}}}}}"
        template = template.replace(placeholder, str(value))
    return template

def query_openai(api_key, prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    parser = argparse.ArgumentParser(description='Replace placeholders in a LaTeX template with values from a YAML config file and OpenAI queries.')
    parser.add_argument('--config', '-c', required=True, help='Configuration filepath (YAML) containing key-value pairs for template replacement')
    parser.add_argument('--template', '-t', required=True, help='Template file (LaTeX file) where anything in {{brackets}} will be replaced with values from the config file')
    parser.add_argument('--output', '-o', required=True, help='Output filepath')
    parser.add_argument('--info', '-i', required=True, help='Company info filepath (TXT) containing job description and company info')

    args = parser.parse_args()

    config = read_config(args.config)
    api_key = config.get("OPENAI_API_KEY")
    keys = config.get("keys", {})
    queries = config.get("queries", {})

    if not api_key:
        raise ValueError("OpenAI API key is missing from the config file.")

    # Read the company info
    company_info = read_info(args.info)
    keys["company_info"] = company_info

    # Fetch values from OpenAI for the queries
    for key, prompt in queries.items():
        response = query_openai(api_key, prompt)
        keys[key] = response

    template = read_template(args.template)
    result = replace_placeholders(template, keys)
    write_output(args.output, result)

if __name__ == "__main__":
    main()
