"""
CSS Flattener - Combines all CSS files from OpenProps UI structure into a single flat file
"""

import os
import re
from pathlib import Path


def flatten_css(css_dir=None, output_file=None):
    """
    Combine all CSS files from OpenProps UI structure into a single flat file
    
    Args:
        css_dir (str): Path to the CSS directory (default: 'static/css')
        output_file (str): Path to the output file (default: 'static/css/flat.css')
    """
    # Set default paths if not provided
    css_dir = Path(css_dir or 'static/css')
    output_file = Path(output_file or css_dir / 'flat.css')
    
    if not css_dir.exists() or not css_dir.is_dir():
        raise ValueError(f"CSS directory not found: {css_dir}")
    
    # Read the main.css file first to determine import order
    main_css_path = css_dir / 'main.css'
    if not main_css_path.exists():
        raise ValueError(f"main.css not found in {css_dir}")
    
    main_css = main_css_path.read_text(encoding='utf-8')
    
    # Extract layer information
    layer_match = re.search(r'@layer\s+(.*?);', main_css)
    layers = []
    if layer_match:
        layers = [layer.strip() for layer in layer_match.group(1).split(',')]
        print(f"Found layers: {', '.join(layers)}")
    
    # Extract import statements
    import_pattern = re.compile(r'@import\s+["\'](.+?)["\'](?:\s+layer\((.*?)\))?;')
    imports = []
    
    for match in import_pattern.finditer(main_css):
        path = match.group(1)
        layer = match.group(2) if match.group(2) else None
        imports.append((path, layer))
    
    # Process imports
    combined_css = []
    processed_files = set()
    
    # Add layer declaration if layers were found
    if layers:
        combined_css.append(f"@layer {', '.join(layers)};")
    
    for path, layer in imports:
        # Convert relative paths
        if path.startswith('./'):
            file_path = css_dir / path[2:]
        elif path.startswith('opbeta/'):
            file_path = css_dir / path
        else:
            file_path = css_dir / path
        
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        # Avoid processing files more than once
        if str(file_path) in processed_files:
            continue
        
        # Read the file
        css_content = file_path.read_text(encoding='utf-8')
        
        # Skip import statements within the imported file
        css_content = re.sub(r'@import\s+["\'].*?["\'].*?;', '', css_content)
        
        # Add layer wrapper if specified
        if layer:
            combined_css.append(f"/* From: {path} */")
            combined_css.append(f"@layer {layer} {{")
            combined_css.append(css_content.strip())
            combined_css.append("}")
        else:
            combined_css.append(f"/* From: {path} */")
            combined_css.append(css_content.strip())
        
        combined_css.append("")  # Empty line for separation
        processed_files.add(str(file_path))
    
    # Save combined CSS to output file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(combined_css), encoding='utf-8')
    
    print(f"\nFlattened CSS created at: {output_file}")
    print(f"Combined {len(processed_files)} CSS files")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Flatten CSS files into a single file")
    parser.add_argument("--css-dir", "-d", help="Path to CSS directory (default: static/css)")
    parser.add_argument("--output", "-o", help="Output file path (default: static/css/flat.css)")
    
    args = parser.parse_args()
    
    try:
        flatten_css(args.css_dir, args.output)
    except Exception as e:
        print(f"Error: {str(e)}")
