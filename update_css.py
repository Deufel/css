from pathlib import Path
import httpx
import json

def get_css(static_dir=None):
    """Sync OpenProps and OpenProps UI files to local static directory"""
    static_dir = Path(static_dir or 'static')
    css_dir = static_dir / 'css'
    op_dir = css_dir / 'opbeta'
    
    # Create directory structure
    op_dir.mkdir(parents=True, exist_ok=True)
    (op_dir / 'css').mkdir(exist_ok=True)
    
    # Define sources
    OPENPROPS_CDN = "https://unpkg.com/open-props@2.0.0-beta.5"
    OPUI_GITHUB = "https://raw.githubusercontent.com/felix-bohlin/ui/refs/heads/main/src"
    OPUI_GITHUB_API = "https://api.github.com/repos/felix-bohlin/ui/contents/src"
    
    # OpenProps files - still hardcoded as these are specific
    op_files = [
        'index.css',
        'css/media-queries.css',
        'css/sizes/media.css',
        'css/font/lineheight.css',
        'css/color/hues.oklch.css',
        'utilities.css'
    ]
    
    # Create necessary directories for OpenProps files
    for file in op_files:
        (op_dir / Path(file).parent).mkdir(parents=True, exist_ok=True)
    
    # OpenProps UI core files
    core_files = ['normalize.css', 'utils.css', 'theme.css', 'main.css']
    
    # Dynamically discover component directories
    headers = {}
    # Add GitHub token if available (to avoid rate limits)
    # headers = {"Authorization": "token YOUR_GITHUB_TOKEN"}
    
    try:
        response = httpx.get(OPUI_GITHUB_API, headers=headers)
        if response.status_code == 200:
            content_data = response.json()
            component_dirs = []
            for item in content_data:
                if item['type'] == 'dir' and item['name'] not in ['assets', 'lib', 'icons']:
                    component_dirs.append(item['name'])
            print(f"Discovered component directories: {component_dirs}")
        else:
            # Fallback to known component directories
            component_dirs = ['actions', 'data-display', 'feedback', 'inputs', 'text']
            print(f"Using known component directories due to API error: {component_dirs}")
    except Exception as e:
        # Fallback to known component directories
        component_dirs = ['actions', 'data-display', 'feedback', 'inputs', 'text']
        print(f"Exception occurred during directory discovery: {str(e)}")
        print(f"Using known component directories: {component_dirs}")
    
    # Sync OpenProps files
    print("\nSyncing OpenProps files...")
    for file in op_files:
        response = httpx.get(f"{OPENPROPS_CDN}/{file}")
        if response.status_code == 200:
            file_path = op_dir / file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(response.text)
            print(f"Synced {file}")
    
    # Sync OpenProps UI core files
    print("\nSyncing OpenProps UI core files...")
    for file in core_files:
        response = httpx.get(f"{OPUI_GITHUB}/{file}")
        if response.status_code == 200:
            (css_dir / file).write_text(response.text)
            print(f"Synced {file}")
    
    # Sync OpenProps UI component files (dynamically)
    print("\nSyncing OpenProps UI component files...")
    for dir_name in component_dirs:
        dir_path = css_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Get the list of files in this component directory
        try:
            response = httpx.get(f"{OPUI_GITHUB_API}/{dir_name}", headers=headers)
            if response.status_code == 200:
                files_data = response.json()
                for file_info in files_data:
                    if file_info['type'] == 'file' and file_info['name'].endswith('.css'):
                        file_name = file_info['name']
                        file_response = httpx.get(f"{OPUI_GITHUB}/{dir_name}/{file_name}")
                        if file_response.status_code == 200:
                            (dir_path / file_name).write_text(file_response.text)
                            print(f"Synced {dir_name}/{file_name}")
                        else:
                            print(f"Failed to download {dir_name}/{file_name}: {file_response.status_code}")
            else:
                print(f"Failed to get file list for {dir_name}: {response.status_code}")
        except Exception as e:
            print(f"Error syncing files from {dir_name} directory: {str(e)}")
    
    print("\nSync complete!")


if __name__ == "__main__":
    get_css()
