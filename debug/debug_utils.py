python << 'EOF'
import sys
import os
import traceback

print("=== DEBUG VALIDATION SCRIPT ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Check file existence
files_to_check = [
    'utils/docx_parser.py',
    'utils/__init__.py',
    'docx_parser.py'
]

print("\n--- File Existence Check ---")
for file_path in files_to_check:
    exists = os.path.exists(file_path)
    print(f"{file_path}: {'✅ EXISTS' if exists else '❌ NOT FOUND'}")
    if exists:
        try:
            with open(file_path, 'r') as f:
                lines = len(f.readlines())
            print(f"  - {lines} lines")
        except Exception as e:
            print(f"  - Error reading: {e}")

# Check utils directory
print("\n--- Utils Directory Contents ---")
if os.path.exists('utils'):
    utils_contents = os.listdir('utils')
    print(f"utils/ contents: {utils_contents}")
else:
    print("utils/ directory does not exist")

# Check current directory contents  
print("\n--- Current Directory Contents ---")
current_contents = [f for f in os.listdir('.') if f.endswith('.py') or os.path.isdir(f)]
print(f"Python files and directories: {current_contents}")

# Add paths
sys.path.append('.')
sys.path.append('utils')
print(f"\n--- Updated Python Path ---")
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")

# Try different import methods
print("\n--- Import Testing ---")

# Method 1: Direct import
print("1. Testing direct import:")
try:
    import utils.docx_parser as parser
    print("✅ utils.docx_parser imported successfully")
    
    # Check attributes
    attrs = ['main', '__main__', 'campaign_main', 'load_campaign_content']
    found_attrs = []
    for attr in attrs:
        if hasattr(parser, attr):
            found_attrs.append(attr)
    
    if found_attrs:
        print(f"  - Found functions: {found_attrs}")
    else:
        print("  - No main functions found")
        
except Exception as e:
    print(f"❌ Direct import failed: {e}")
    print("  Traceback:")
    traceback.print_exc(limit=3)

# Method 2: Import from utils directory
print("\n2. Testing utils directory import:")
try:
    if os.path.exists('utils/docx_parser.py'):
        import importlib.util
        spec = importlib.util.spec_from_file_location("docx_parser", "utils/docx_parser.py")
        parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser)
        print("✅ Module loaded via importlib")
        
        if hasattr(parser, 'campaign_main'):
            print("  - campaign_main function found")
        if hasattr(parser, '__name__'):
            print(f"  - Module name: {parser.__name__}")
            
    else:
        print("❌ utils/docx_parser.py not found")
        
except Exception as e:
    print(f"❌ Importlib method failed: {e}")
    print("  Traceback:")
    traceback.print_exc(limit=3)

# Method 3: Check for missing dependencies
print("\n3. Testing dependencies:")
dependencies = [
    ('os', 'built-in'),
    ('sys', 'built-in'), 
    ('json', 'built-in'),
    ('argparse', 'built-in'),
    ('pathlib', 'built-in'),
    ('datetime', 'built-in'),
    ('docx', 'python-docx package'),
    ('email_sender', 'custom module'),
    ('data_loader', 'custom module')
]

for dep, desc in dependencies:
    try:
        __import__(dep)
        print(f"✅ {dep} ({desc})")
    except ImportError as e:
        if dep in ['docx', 'email_sender', 'data_loader']:
            print(f"⚠️ {dep} ({desc}) - optional dependency missing")
        else:
            print(f"❌ {dep} ({desc}) - REQUIRED dependency missing: {e}")

print("\n=== VALIDATION COMPLETE ===")
EOF
