from ruamel.yaml import YAML
import sys

def fix_indentation(input_file, output_file=None):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    try:
        with open(input_file, 'r') as f:
            data = yaml.load(f)

        if data is None:
            print("The file is empty or invalid.")
            return

        if output_file:
            with open(output_file, 'w') as f:
                yaml.dump(data, f)
            print(f"Corrected YAML written to: {output_file}")
        else:
            yaml.dump(data, sys.stdout)

    except Exception as e:
        print(f"\n❌ Failed to parse and fix YAML.\nError: {e}")
        print("\nTIP: Try validating the file with a linter like `yamllint` to locate exact issues.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_yaml_indentation.py <input_file> [output_file]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        fix_indentation(input_file, output_file)
