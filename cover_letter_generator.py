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

import yaml
from openai import OpenAI

def query_openai(api_key, queries, company_info, self_info, style="Make it sound professional"):
    """
    Query the OpenAI API to generate responses based on provided information and questions.

    Args:
    - api_key (str): The OpenAI API key.
    - queries (dict of str: str): A dictionary of questions to be answered.
    - company_info (str): Information about the company.
    - self_info (str): Information about the user.
    - style (str): The desired writing style for the response.

    Returns:
    - dict: A dictionary containing the responses to the queries if successful.
    - str: The raw response text if parsing fails.
    """

    # Convert the queries dictionary to a YAML string
    queries_yaml = yaml.dump(queries, default_flow_style=False)

    # Construct the messages for OpenAI chat API
    messages = [
        {"role": "system", "content": f"Here is the company info:\n\n{company_info}\n\nHere is info about me:\n\n{self_info}\n\nWriting style should be: {style}.\n\nHere are the questions I need you to answer - the values below are the questions. In the response, replace those with the actual answers:\n\n{queries_yaml}"},
        {"role": "user", "content": "Generate responses based on the provided information. Give me the response in a YAML format and say NOTHING else. For long strings, make sure you format with the '>' character"}
    ]

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Query the OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=4096
    )

    # Get the response
    response_text = completion.choices[0].message.content

    # Strip out the yaml formatting characters
    response_text = response_text.replace("```yaml", "")
    response_text = response_text.replace("```", "")

    # Try to parse the response text as YAML
    try:
        response_dict = yaml.safe_load(response_text)
        return response_dict
    except yaml.YAMLError as exc:
        # Print the response text and raise the exception
        print(f"YAML parsing failed. Response text:\n{response_text}")
        raise exc

def main():
    parser = argparse.ArgumentParser(description='Replace placeholders in a LaTeX template with values from a YAML config file and OpenAI queries.')
    parser.add_argument('--config', '-c', required=True, help='Configuration filepath (YAML) containing key-value pairs for template replacement')
    parser.add_argument('--template', '-t', required=True, help='Template file (LaTeX file) where anything in {{brackets}} will be replaced with values from the config file')
    parser.add_argument('--output', '-o', required=True, help='Output filepath')
    parser.add_argument('--company_info', '-i', required=True, help='Company info filepath (TXT) containing job description and company info')
    parser.add_argument('--self_info', '-s', required=True, help='Individual (your info) filepath (TXT) containing an overview of you, your skills, and accomplishments')

    args = parser.parse_args()

    config = read_config(args.config)
    api_key = config.get("OPENAI_API_KEY")
    keys = config.get("keys", {})
    queries = config.get("queries", {})

    if not api_key:
        raise ValueError("OpenAI API key is missing from the config file.")

    # Read the company info
    company_info = read_info(args.company_info)

    # Read the info about 
    self_info = read_info(args.self_info)

    # Fetch values from OpenAI for the queries
    openai_responses = query_openai(api_key, queries, company_info, self_info, config.get("WRITING_STYLE"))

    template = read_template(args.template)
    result = replace_placeholders(template, keys)
    result = replace_placeholders(result, openai_responses)
    write_output(args.output, result)

if __name__ == "__main__":
    main()
