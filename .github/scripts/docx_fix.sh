#!/bin/bash
# Automated DOCX File Checker & Fixer
# Usage: ./docx_fix.sh campaign-templates/

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        DOCX File Integrity Checker & Fixer              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if directory provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No directory specified${NC}"
    echo "Usage: $0 <directory>"
    echo "Example: $0 campaign-templates/"
    exit 1
fi

SEARCH_DIR="$1"

if [ ! -d "$SEARCH_DIR" ]; then
    echo -e "${RED}Error: Directory does not exist: $SEARCH_DIR${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 Scanning directory: $SEARCH_DIR${NC}"
echo ""

# Find all DOCX files
DOCX_FILES=$(find "$SEARCH_DIR" -name "*.docx" -type f)
TOTAL_FILES=$(echo "$DOCX_FILES" | grep -c ".")
VALID_FILES=0
INVALID_FILES=0
FIXED_FILES=0

if [ -z "$DOCX_FILES" ]; then
    echo -e "${YELLOW}⚠️  No DOCX files found in $SEARCH_DIR${NC}"
    exit 0
fi

echo -e "${BLUE}📁 Found $TOTAL_FILES DOCX file(s)${NC}"
echo ""

# Array to store invalid files
declare -a INVALID_FILE_LIST
declare -a INVALID_FILE_REASONS

# Check each file
for file in $DOCX_FILES; do
    FILENAME=$(basename "$file")
    RELATIVE_PATH=$(realpath --relative-to="$SEARCH_DIR" "$file")
    
    echo -e "${BLUE}───────────────────────────────────────────────────${NC}"
    echo -e "${BLUE}📄 Checking: $RELATIVE_PATH${NC}"
    
    # Test 1: File not empty
    if [ ! -s "$file" ]; then
        echo -e "${RED}  ❌ FAILED: File is empty (0 bytes)${NC}"
        INVALID_FILE_LIST+=("$file")
        INVALID_FILE_REASONS+=("Empty file")
        ((INVALID_FILES++))
        
        echo -e "${YELLOW}  🔧 Attempting to fix...${NC}"
        
        # Try to create a minimal valid DOCX
        if command -v python3 &> /dev/null; then
            python3 -c "
from docx import Document
doc = Document()
doc.add_paragraph('Template content - please update')
doc.save('$file')
print('  ✅ Created minimal valid DOCX')
" 2>/dev/null && {
                echo -e "${GREEN}  ✅ Fixed: Created minimal valid DOCX${NC}"
                ((FIXED_FILES++))
                continue
            } || {
                echo -e "${RED}  ❌ Could not auto-fix (python-docx not available)${NC}"
            }
        fi
        continue
    fi
    
    FILE_SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    FILE_SIZE_KB=$(echo "scale=2; $FILE_SIZE / 1024" | bc)
    echo -e "  📊 Size: ${FILE_SIZE_KB} KB"
    
    # Test 2: Valid ZIP structure
    if ! unzip -tq "$file" > /dev/null 2>&1; then
        echo -e "${RED}  ❌ FAILED: Not a valid ZIP archive${NC}"
        INVALID_FILE_LIST+=("$file")
        INVALID_FILE_REASONS+=("Invalid ZIP structure")
        ((INVALID_FILES++))
        
        # Check file type
        FILE_TYPE=$(file -b "$file")
        echo -e "${YELLOW}  📋 Detected type: $FILE_TYPE${NC}"
        
        # Try to determine if it's actually a text file that was renamed
        if file "$file" | grep -q "text"; then
            echo -e "${YELLOW}  🔧 File appears to be text - attempting conversion...${NC}"
            
            if command -v pandoc &> /dev/null; then
                TEMP_FILE="${file}.temp"
                mv "$file" "$TEMP_FILE"
                
                pandoc "$TEMP_FILE" -o "$file" 2>/dev/null && {
                    echo -e "${GREEN}  ✅ Fixed: Converted text to DOCX${NC}"
                    rm "$TEMP_FILE"
                    ((FIXED_FILES++))
                    ((VALID_FILES++))
                    continue
                } || {
                    mv "$TEMP_FILE" "$file"
                    echo -e "${RED}  ❌ Conversion failed${NC}"
                }
            else
                echo -e "${YELLOW}  💡 Install pandoc to auto-convert: apt install pandoc${NC}"
            fi
        fi
        
        continue
    fi
    
    # Test 3: Required DOCX structure
    HAS_DOCUMENT_XML=$(unzip -l "$file" 2>/dev/null | grep -c "word/document.xml" || echo "0")
    HAS_CONTENT_TYPES=$(unzip -l "$file" 2>/dev/null | grep -c "\[Content_Types\].xml" || echo "0")
    
    if [ "$HAS_DOCUMENT_XML" -eq 0 ] || [ "$HAS_CONTENT_TYPES" -eq 0 ]; then
        echo -e "${RED}  ❌ FAILED: Missing required DOCX files${NC}"
        
        if [ "$HAS_DOCUMENT_XML" -eq 0 ]; then
            echo -e "${RED}     Missing: word/document.xml${NC}"
        fi
        if [ "$HAS_CONTENT_TYPES" -eq 0 ]; then
            echo -e "${RED}     Missing: [Content_Types].xml${NC}"
        fi
        
        INVALID_FILE_LIST+=("$file")
        INVALID_FILE_REASONS+=("Corrupted DOCX structure")
        ((INVALID_FILES++))
        continue
    fi
    
    # Test 4: python-docx can open it
    if command -v python3 &> /dev/null; then
        if python3 -c "
from docx import Document
try:
    doc = Document('$file')
    print('  ✅ python-docx: OK')
except Exception as e:
    print('  ❌ python-docx: Failed -', str(e))
    exit(1)
" 2>/dev/null; then
            echo -e "${GREEN}  ✅ PASSED: All validation tests${NC}"
            ((VALID_FILES++))
        else
            echo -e "${RED}  ❌ FAILED: Cannot be opened by python-docx${NC}"
            INVALID_FILE_LIST+=("$file")
            INVALID_FILE_REASONS+=("python-docx compatibility issue")
            ((INVALID_FILES++))
        fi
    else
        echo -e "${YELLOW}  ⚠️  SKIPPED: python-docx validation (not installed)${NC}"
        echo -e "${GREEN}  ✅ PASSED: Basic validation tests${NC}"
        ((VALID_FILES++))
    fi
done

# Summary Report
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   VALIDATION SUMMARY                     ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  📄 Total files scanned: ${TOTAL_FILES}"
echo -e "  ${GREEN}✅ Valid files: ${VALID_FILES}${NC}"
echo -e "  ${RED}❌ Invalid files: ${INVALID_FILES}${NC}"

if [ $FIXED_FILES -gt 0 ]; then
    echo -e "  ${YELLOW}🔧 Auto-fixed files: ${FIXED_FILES}${NC}"
fi

echo ""

if [ $INVALID_FILES -gt 0 ]; then
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║                   INVALID FILES REPORT                   ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    for i in "${!INVALID_FILE_LIST[@]}"; do
        file="${INVALID_FILE_LIST[$i]}"
        reason="${INVALID_FILE_REASONS[$i]}"
        relative_path=$(realpath --relative-to="$SEARCH_DIR" "$file")
        
        echo -e "${RED}❌ $relative_path${NC}"
        echo -e "   Reason: $reason"
        echo -e "   Path: $file"
        echo ""
    done
    
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║               RECOMMENDED ACTIONS                        ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "1. For empty files:"
    echo "   - Delete and recreate in Word/LibreOffice"
    echo "   - Or run: python3 -c \"from docx import Document; doc = Document(); doc.add_paragraph('Content'); doc.save('file.docx')\""
    echo ""
    echo "2. For invalid ZIP files:"
    echo "   - Open in Microsoft Word or LibreOffice"
    echo "   - Save again (may auto-repair)"
    echo "   - Or regenerate from source"
    echo ""
    echo "3. For corrupted structure:"
    echo "   - Recreate file from scratch"
    echo "   - Restore from backup"
    echo ""
    echo "4. Run diagnostic on specific file:"
    echo "   python3 utils/docx_diagnostic.py <file-path>"
    echo ""
    
    exit 1
else
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              🎉 ALL FILES VALIDATED! 🎉                  ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "✅ All DOCX files are valid and ready for campaign processing"
    echo ""
    
    exit 0
fi
