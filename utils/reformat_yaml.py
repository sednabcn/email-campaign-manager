import yaml
import sys

def reformat_yaml(input_file, output_file=None, indent=2):
    try:
        # Read the YAML content
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)

        # Write it back with correct indentation
        formatted_yaml = yaml.dump(data, indent=indent, default_flow_style=False, sort_keys=False)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(formatted_yaml)
            print(f"Reformatted YAML written to: {output_file}")
        else:
            print(formatted_yaml)

    except yaml.YAMLError as e:
        print(f"YAML Error: {e}")
    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reformat_yaml.py <input_file> [output_file]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        reformat_yaml(input_file, output_file)
