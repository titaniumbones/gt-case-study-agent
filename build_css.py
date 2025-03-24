#!/usr/bin/env python
"""Script to compile SCSS files to CSS."""

import os
import sass
from pathlib import Path


def compile_scss(scss_dir, css_dir):
    """Compile SCSS files to CSS.

    Args:
        scss_dir: Directory containing SCSS files
        css_dir: Directory to output CSS files
    """
    # Ensure output directory exists
    Path(css_dir).mkdir(parents=True, exist_ok=True)

    # Get all SCSS files (non-partials)
    scss_files = [
        f for f in Path(scss_dir).glob("*.scss") if not f.name.startswith("_")
    ]

    for scss_file in scss_files:
        print(f"Compiling {scss_file}...")

        # Determine output path
        css_file = Path(css_dir) / f"{scss_file.stem}.css"

        # Compile SCSS to CSS
        css = sass.compile(filename=str(scss_file), output_style="compressed")

        # Write CSS to file
        with open(css_file, "w") as f:
            f.write(css)

        print(f"Generated {css_file}")


if __name__ == "__main__":
    # Define directories
    base_dir = Path(__file__).parent
    scss_dir = base_dir / "src" / "web" / "static" / "scss"
    css_dir = base_dir / "src" / "web" / "static" / "css"

    # Compile SCSS to CSS
    compile_scss(scss_dir, css_dir)
    print("SCSS compilation complete.")
