import json
import os

def parse_markdown_to_ipynb(md_path, ipynb_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cells = []
    current_cell_lines = []
    in_python_code_block = False
    
    for line in lines:
        # Clean trailing newlines
        clean_line = line.rstrip('\r\n')
        
        # Check for start/end of python code block
        if clean_line.strip() == '```python':
            # End current markdown cell if it has content
            if current_cell_lines:
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": current_cell_lines
                })
                current_cell_lines = []
            in_python_code_block = True
            continue
        elif in_python_code_block and clean_line.strip() == '```':
            # End current code cell
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": current_cell_lines
            })
            current_cell_lines = []
            in_python_code_block = False
            continue
            
        current_cell_lines.append(clean_line)
        
    # Append any remaining lines
    if current_cell_lines:
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": current_cell_lines
        })
        
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    with open(ipynb_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    print(f"Successfully converted {md_path} to {ipynb_path}")

if __name__ == '__main__':
    md = r"c:\Users\roman\Documents\proyectos\tripleten\bootcamp_ds_da\v7\07-herramientas-desarrollo\01-entorno-python.md"
    ipynb = r"c:\Users\roman\Documents\proyectos\tripleten\bootcamp_ds_da\v7\07-herramientas-desarrollo\01-entorno-python.ipynb"
    parse_markdown_to_ipynb(md, ipynb)
