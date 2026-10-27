import re
import argparse
import html
import random
import os
import markdown
import json
import yaml

def resolve_path(include_path, current_file_dir, root_file_dir):
    """
    Resolves the given path using a fallback strategy:
    1. Absolute path.
    2. Relative to directory of file currently being processed.
    3. Relative to directory of root input file.
    4. Relative to current working directory.
    """
    if os.path.isabs(include_path):
        return include_path

    path1 = os.path.abspath(os.path.join(current_file_dir, include_path))
    if os.path.exists(path1):
        return path1

    path2 = os.path.abspath(os.path.join(root_file_dir, include_path))
    if os.path.exists(path2):
        return path2

    path3 = os.path.abspath(include_path)
    if os.path.exists(path3):
        return path3

    return path1

def resolve_includes(content, current_file_path, root_file_dir, visited=None):
    """
    Recursively resolves @include{path="..."} markers in the content.
    """
    if visited is None:
        visited = set()

    current_abs_path = os.path.abspath(current_file_path)
    if current_abs_path in visited:
        print(f"Warning: Circular include detected for file '{current_abs_path}'")
        return ""
    visited.add(current_abs_path)

    current_file_dir = os.path.dirname(current_abs_path)

    pattern = r'@include\s*\{\s*path\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s}]+))\s*\}'
    
    def replace_match(match):
        include_path = match.group(1) or match.group(2) or match.group(3)
        resolved_path = resolve_path(include_path, current_file_dir, root_file_dir)
        
        if not os.path.exists(resolved_path):
            print(f"Error: Included file '{include_path}' (resolved to '{resolved_path}') not found.")
            return f"\n<!-- Error: Included file '{include_path}' not found -->\n"

        try:
            with open(resolved_path, 'r', encoding='utf-8') as f:
                included_content = f.read()
        except Exception as e:
            print(f"Error reading included file '{resolved_path}': {e}")
            return f"\n<!-- Error reading included file '{include_path}': {e} -->\n"

        resolved_content = resolve_includes(included_content, resolved_path, root_file_dir, visited.copy())
        
        if not resolved_content.strip().endswith('---'):
            resolved_content = resolved_content.rstrip() + "\n---\n"
            
        return resolved_content

    return re.sub(pattern, replace_match, content)

def parse_markdown(content):
    """
    Parses the entire markdown content and splits it into slide objects.
    """
    slides_content = re.split(r'(?m)^---\s*$', content.strip())
    slides = []

    for slide_content in slides_content:
        slide_content = slide_content.strip()
        if not slide_content:
            continue

        slide = {
            'type': 'unknown',
            'params': {},
            'content': '',
            'title': '',
            'subtitle': ''
        }

        tag_match = re.match(r'@(\w+(?:-\w+)?)\s*(\{.*\})?', slide_content)

        if tag_match:
            slide['type'] = tag_match.group(1)
            params_str = tag_match.group(2)

            if params_str:
                params_str = params_str.strip('{}')
                try:
                    params = {}
                    for param_match in re.finditer(r'(\w+)\s*:\s*(?:"([^"]*)"|([^,}]+))', params_str):
                        key = param_match.group(1)
                        val = param_match.group(2) if param_match.group(2) is not None else param_match.group(3).strip()
                        params[key] = val
                    slide['params'] = params
                except Exception as e:
                    print(f"Warning: Could not parse params '{params_str}': {e}")
            
            content_after_tag = slide_content[tag_match.end():].strip()
        else:
            content_after_tag = slide_content

        lines = content_after_tag.split('\n')
        
        title_found = False
        subtitle_found = False
        remaining_lines = []

        for line in lines:
            if line.startswith('# ') and not title_found:
                slide['title'] = line[2:].strip()
                title_found = True
            elif line.startswith('## ') and not subtitle_found:
                slide['subtitle'] = line[3:].strip()
                subtitle_found = True
            else:
                remaining_lines.append(line)
        
        slide['content'] = '\n'.join(remaining_lines).strip()
        slides.append(slide)

    return slides

def generate_css():
    """
    Generates the CSS for the presentation, including the Full-Screen Isometric Pixel Art Lobby
    with a dedicated Top Header Bar so the countdown never overlaps the pixel art.
    """
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&family=Playfair+Display:wght@700&display=swap');

    :root {
        --color-orange: #F2855A;
        --color-green: #66B37D;
        --color-light-gray: #F2F2F2;
        --color-dark-mode: #111111;
        --color-black: #0A0A0A;
        --color-dark-gray-1: #333333;
        --color-dark-gray-2: #5F5F5F;
        --color-white-soft: #F5F5F5;
        --font-main: 'Montserrat', sans-serif;
        --px-bg: #070c17;
        --px-gold: #f5b963;
        --px-cream: #f4e8c1;
    }

    body {
        margin: 0;
        font-family: var(--font-main);
        overflow: hidden;
    }

    .presentation {
        position: relative;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
    }

    .slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
        box-sizing: border-box;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.6s ease-in-out, visibility 0.6s ease-in-out;
    }

    .slide.active {
        opacity: 1;
        visibility: visible;
        z-index: 1;
    }

    .slide h1 { font-size: 3rem; font-weight: 700; margin: 0 0 0.5rem 0; }
    .slide h2 { font-size: 1.8rem; font-weight: 300; margin: 0; }

    /* =====================================================================
       ESTILOS DEL LOBBY PIXEL ART ISOMÉTRICO (100% PANTALLA SIN SOLAPARSE)
       ===================================================================== */
    .slide-countdown {
        background: radial-gradient(circle at 50% 55%, #162a4a 0%, #070c17 85%);
        color: var(--px-cream);
        padding: 0 !important;
        overflow: hidden;
    }

    .px-stage-wrapper {
        position: relative;
        width: 100vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    /* Barra superior dedicada (175px) para que la cuenta regresiva jamás tape el Pixel Art */
    .px-top-bar {
        height: 175px;
        min-height: 175px;
        width: 100%;
        background: linear-gradient(90deg, rgba(7, 12, 23, 0.97) 0%, rgba(15, 25, 45, 0.97) 50%, rgba(7, 12, 23, 0.97) 100%);
        border-bottom: 3px solid var(--px-gold);
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.85);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 28px;
        box-sizing: border-box;
        z-index: 80;
        position: relative;
    }

    .px-title-block {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        text-align: left;
        max-width: 44%;
    }

    .px-webinar-tag {
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--px-gold);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.2px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .px-webinar-dot {
        width: 8px;
        height: 8px;
        background: var(--px-gold);
        border-radius: 50%;
        box-shadow: 0 0 8px var(--px-gold);
        animation: pxPulse 1.4s infinite;
    }

    @keyframes pxPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    .px-title-block h1 {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 26px !important;
        color: var(--px-cream) !important;
        margin: 0 0 3px 0 !important;
        line-height: 1.15;
    }

    .px-title-block h2 {
        font-size: 13.5px !important;
        color: #9aa7b8 !important;
        font-weight: 400 !important;
        line-height: 1.25;
        margin: 0 !important;
    }

    /* Reloj circular central en la barra superior */
    .px-center-clock {
        display: flex;
        align-items: center;
        gap: 16px;
        background: rgba(5, 9, 18, 0.9);
        border: 2px solid var(--px-gold);
        border-radius: 55px;
        padding: 6px 24px 6px 12px;
        box-shadow: 0 0 22px rgba(245, 185, 99, 0.25);
    }

    .px-clock-wrapper {
        position: relative;
        width: 100px;
        height: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .px-clock-svg {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        transform: rotate(-90deg);
    }

    .px-ring-bg {
        fill: none;
        stroke: rgba(255, 255, 255, 0.12);
        stroke-width: 6;
    }

    .px-ring-fg {
        fill: none;
        stroke: var(--px-gold);
        stroke-width: 6.5;
        stroke-linecap: round;
        stroke-dasharray: 440;
        stroke-dashoffset: 0;
        filter: drop-shadow(0 0 6px rgba(245, 185, 99, 0.65));
        transition: stroke-dashoffset 0.5s linear;
    }

    .slide-countdown .timer {
        font-size: 23px !important;
        font-weight: 700 !important;
        color: var(--px-cream) !important;
        letter-spacing: 1px !important;
        margin: 0 !important;
        line-height: 1;
        z-index: 2;
        font-family: 'Montserrat', monospace;
    }

    .slide-countdown .start-message {
        font-family: 'Press Start 2P', monospace;
        font-size: 11px !important;
        color: #4ade80 !important;
        margin: 0 !important;
        display: none;
        z-index: 2;
    }

    .px-clock-meta {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        text-align: left;
    }

    .px-clock-sub {
        font-family: 'Press Start 2P', monospace;
        font-size: 9px;
        letter-spacing: 1.5px;
        color: var(--px-gold);
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .px-loop-progress-label {
        font-family: 'VT323', monospace;
        font-size: 17px;
        color: #38bdf8;
    }

    /* Controles derecha (Radio 8-bit, Todos los diálogos, Globos) */
    .px-hud-controls {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 6px;
    }

    .px-hud-card {
        background: rgba(7, 12, 23, 0.92);
        border: 2px solid var(--px-gold);
        border-radius: 6px;
        padding: 7px 11px;
        display: flex;
        align-items: center;
        gap: 7px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.6);
    }

    .px-btn {
        background: #17253b;
        color: var(--px-cream);
        border: 1px solid var(--px-gold);
        padding: 6px 9px;
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        cursor: pointer;
        border-radius: 4px;
        transition: all 0.15s;
    }

    .px-btn:hover, .px-btn.active {
        background: var(--px-gold);
        color: #070c17;
    }

    .px-eq-bars {
        display: flex;
        align-items: flex-end;
        gap: 2px;
        height: 14px;
        width: 18px;
    }

    .px-eq-bar {
        width: 3px;
        background: #4ade80;
        height: 3px;
        transition: height 0.1s;
    }

    /* Área principal del escenario Pixel Art (ocupa todo el resto de la pantalla) */
    .px-viewport-area {
        position: relative;
        flex: 1;
        width: 100%;
        height: calc(100vh - 112px);
        overflow: hidden;
    }

    .px-canvas {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        display: block;
        z-index: 2;
    }

    /* Globos de diálogo estilo cómic 100% visibles */
    .px-bubbles-layer {
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 60;
        overflow: hidden;
    }

    .px-speech-bubble {
        position: absolute;
        transform: translate(-50%, -100%);
        background: #fffef8;
        color: #0f172a;
        border: 3px solid #0f172a;
        padding: 7px 11px;
        font-family: 'VT323', monospace;
        font-size: 19px;
        line-height: 1.12;
        max-width: 245px;
        min-width: 140px;
        text-align: center;
        box-shadow: 4px 4px 0px #0f172a, 0 0 18px rgba(245, 185, 99, 0.45);
        animation: pxPopIn 0.22s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards;
    }

    .px-speech-bubble .px-speaker {
        display: block;
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        color: #b45309;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    .px-speech-bubble.alert {
        background: #fef2f2;
        border-color: #991b1b;
        color: #7f1d1d;
        box-shadow: 4px 4px 0px #991b1b, 0 0 18px rgba(239, 68, 68, 0.65);
    }

    .px-speech-bubble.success {
        background: #f0fdf4;
        border-color: #166534;
        color: #14532d;
        box-shadow: 4px 4px 0px #166534, 0 0 18px rgba(74, 222, 128, 0.55);
    }

    .px-speech-bubble::after {
        content: "";
        position: absolute;
        bottom: -9px;
        left: 50%;
        transform: translateX(-50%);
        border-width: 9px 7px 0;
        border-style: solid;
        border-color: #0f172a transparent;
    }

    @keyframes pxPopIn {
        0% { opacity: 0; transform: translate(-50%, -85%) scale(0.7); }
        100% { opacity: 1; transform: translate(-50%, -100%) scale(1); }
    }

    /* Barra inferior de línea de tiempo interactiva del bucle (60s) */
    .px-bottom-timeline {
        position: absolute;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(7, 12, 23, 0.9);
        border: 2px solid rgba(245, 185, 99, 0.6);
        border-radius: 30px;
        padding: 6px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 75;
        box-shadow: 0 4px 16px rgba(0,0,0,0.7);
    }

    .px-bottom-timeline span {
        font-family: 'Press Start 2P', monospace;
        font-size: 8.5px;
        color: var(--px-gold);
    }

    .px-timeline-slider {
        width: 240px;
        accent-color: var(--px-gold);
        cursor: pointer;
    }

    .bouncing-logo-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; z-index: 1; pointer-events: none; }
    .bouncing-logo { position: absolute; width: 200px; opacity: 0.06; animation: bounceX 13s linear infinite alternate, bounceY 9s linear infinite alternate; }
    @keyframes bounceX { 0% { left: 0; } 100% { left: calc(100vw - 200px); } }
    @keyframes bounceY { 0% { top: 0; } 100% { top: calc(100vh - 180px); } }

    .traffic-logo-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; z-index: 1; pointer-events: none; }
    .traffic-logo-img { position: absolute; width: 180px; opacity: 0.06; left: -250px; transform: translateY(-50%); }
    @keyframes driveRight { 0% { transform: translateY(-50%) translateX(0); } 100% { transform: translateY(-50%) translateX(calc(100vw + 500px)); } }

    /* =====================================================================
       ESTILOS ORIGINALES DEL RESTO DE DIAPOSITIVAS
       ===================================================================== */
    .slide-transition { background-color: var(--color-green); color: var(--color-black); }
    
    .slide-warnup-mood { background-color: var(--color-green); color: var(--color-black); justify-content: center; position: relative; }
    .content-wrapper { position: relative; z-index: 1; background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); padding: 2rem 4rem; border-radius: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.18); }
    .slide-warnup-mood h1, .slide-warnup-mood h2 { font-weight: bold; }
    .emoji-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; z-index: 0; }
    .emoji { position: absolute; top: -10%; font-size: 2rem; animation: fall 10s linear infinite; }
    @keyframes fall {
        0% { transform: translateY(0) rotate(0); }
        100% { transform: translateY(110vh) rotate(360deg); }
    }

    .slide-agenda, .slide-warnup-question, .slide-basic_slide, .slide-two_columns_slide { background-color: var(--color-light-gray); color: var(--color-black); }
    .slide-agenda .content-wrapper, .slide-basic_slide .content-wrapper, .slide-two_columns_slide .content-wrapper { width: 90%; text-align: left; overflow-y: auto; max-height: 85vh; padding: 2rem 3rem; }
    .slide-basic_slide .content-wrapper img, .slide-two_columns_slide .content-wrapper img { max-width: 100%; border-radius: 10px; display: block; margin: 1rem auto; padding: 0; }
    .slide-basic_slide .content-wrapper p, .slide-basic_slide .content-wrapper ul, .slide-basic_slide .content-wrapper ol, .slide-two_columns_slide .content-wrapper p, .slide-two_columns_slide .content-wrapper ul, .slide-two_columns_slide .content-wrapper ol { font-size: 1.5rem; line-height: 1.6; }
    .slide-basic_slide .content-wrapper ul, .slide-basic_slide .content-wrapper ol, .slide-two_columns_slide .content-wrapper ul, .slide-two_columns_slide .content-wrapper ol { padding-left: 3rem; }
    
    .slide-two_columns_slide .column-left { padding-right: 2rem; width: 50%; display: flex; flex-direction: column; justify-content: center; }
    .slide-two_columns_slide .column-right { width: 50%; display: flex; align-items: center; justify-content: center; height: 100%; }
    .slide-two_columns_slide .column-right img { width: 100%; max-height: 70vh; object-fit: contain; }
    .slide-agenda h1 { color: var(--color-black); margin-bottom: 1.5rem; }
    .slide-agenda ul { list-style: none; padding: 0; font-size: 1.5rem; }
    .slide-agenda li { margin: 0.8rem 0; }
    .slide-agenda li strong { color: var(--color-black); }
    .slide-agenda li span { color: var(--color-dark-gray-1); margin-left: 1rem; }

    .two-column-layout { display: flex; align-items: center; justify-content: center; width: 100%; gap: 2rem; }
    .column-left { width: 50%; text-align: left; }
    .column-right { width: 50%; }
    .column-right img { max-width: 100%; border-radius: 10px; }

    .slide-objectives { background-color: var(--color-light-gray); color: var(--color-black); }
    .slide-objectives .content-wrapper { padding: 3rem; text-align: center; width: 95%; max-width: 1600px; max-height: 85vh; overflow-y: auto; }
    .slide-objectives .objectives-container > ul { display: flex; flex-wrap: wrap; justify-content: center; gap: 2rem; list-style: none; padding: 0; margin: 2rem 0; width: 100%; }
    .slide-objectives .objectives-container > ul > li { background-color: var(--color-light-gray); color: var(--color-dark-gray-1); padding: 2.5rem; border-radius: 15px; flex: 1; min-width: 300px; max-width: 480px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: left; font-size: 1.3rem; line-height: 1.5; display: flex; flex-direction: column; }
    .slide-objectives .objectives-container > ul > li p { margin: 0; }
    .slide-objectives .objectives-container img { max-width: 100%; max-height: 100px; object-fit: contain; display: block; margin: 0 auto 1rem auto; }
    .slide-objectives .objectives-container > ul > li > ul { list-style: none; padding-left: 0; margin-top: 1rem; font-size: 1.1rem; }
    .slide-objectives .objectives-container > ul > li > ul > li { position: relative; padding-left: 1.2rem; margin-bottom: 0.8rem; color: var(--color-dark-gray-2); }
    .slide-objectives .objectives-container > ul > li > ul > li::before { content: "•"; position: absolute; left: 0; color: var(--color-green); font-weight: bold; }
    .slide-objectives h1 { color: var(--color-black); margin-bottom: 1rem; }

    .slide-overlay { background-color: var(--color-black); color: var(--color-white-soft); }
    .slide-overlay h1, .slide-overlay h2 { color: var(--color-white-soft); margin-bottom: 0.5rem; }
    .slide-overlay p { font-size: 3rem; font-weight: 500; margin: 1rem 0; line-height: 1.4; color: var(--color-white-soft); text-align: center; }

    .slide-gotocode { background-color: var(--color-dark-mode); color: var(--color-white-soft); }
    .slide-finale { background-color: var(--color-orange); color: var(--color-black); }
    .slide-finale h2 { color: var(--color-dark-gray-2); }
    .slide-gotocode a { color: var(--color-white-soft); }
    .slide-gotocode .qr-container { display: flex; gap: 2rem; margin-top: 2rem; }
    .slide-gotocode .qr-item { display: flex; flex-direction: column; align-items: center; }
    .slide-gotocode .qr-item img { width: 150px; height: 150px; border-radius: 10px; }

    #transition-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; display: flex; justify-content: center; align-items: center; opacity: 0; visibility: hidden; transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out; background-color: var(--color-green); color: var(--color-black); }
    #transition-overlay h1 { color: var(--color-black); margin-bottom: 0; }
    #transition-overlay .content-wrapper { width: 90%; text-align: left; padding: 2rem 3rem; }
    #transition-overlay.visible { opacity: 1; visibility: visible; }
    
    .slide-nav { position: absolute; bottom: 20px; right: 20px; z-index: 100; display: flex; gap: 10px; }
    .slide-nav button { background: rgba(128, 128, 128, 0.5); border: none; color: white; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1.5rem; transition: background 0.3s; }
    .slide-nav button:hover { background: rgba(128, 128, 128, 0.9); }

    .slide-menu { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); z-index: 200; display: flex; justify-content: center; align-items: center; opacity: 0; visibility: hidden; transition: opacity 0.3s, visibility 0.3s; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }
    .slide-menu.active { opacity: 1; visibility: visible; }
    .slide-menu-content { background: var(--color-light-gray); padding: 3rem; border-radius: 15px; width: 80%; max-width: 800px; max-height: 80vh; overflow-y: auto; position: relative; color: var(--color-black); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .slide-menu-content h2 { margin-top: 0; border-bottom: 2px solid var(--color-dark-gray-1); padding-bottom: 1rem; color: var(--color-black); }
    .close-menu { position: absolute; top: 15px; right: 20px; background: none; border: none; font-size: 2.5rem; cursor: pointer; color: var(--color-dark-gray-2); transition: color 0.3s; }
    .close-menu:hover { color: var(--color-orange); }
    .slide-list { list-style: none; padding: 0; }
    .slide-list li { margin: 0.5rem 0; }
    .menu-jump-btn { width: 100%; text-align: left; background: var(--color-white-soft); border: 1px solid rgba(0,0,0,0.1); padding: 1rem; border-radius: 8px; font-size: 1.2rem; cursor: pointer; transition: background 0.2s, transform 0.1s; font-family: var(--font-main); color: var(--color-dark-gray-1); }
    .menu-jump-btn:hover { background: var(--color-orange); color: var(--color-black); transform: translateX(5px); }
    
    .company-logo { position: absolute; top: 30px; left: 40px; max-height: 60px; opacity: 0; z-index: 50; pointer-events: none; }
    .slide-countdown .company-logo, .slide-warnup-mood .company-logo, .slide-finale .company-logo, .slide-overlay .company-logo { display: none !important; animation: none !important; }
    .slide.active .company-logo { animation: showAndHideLogo 4s ease-in-out forwards; }
    @keyframes showAndHideLogo {
        0% { opacity: 0; transform: translateY(-10px); }
        10% { opacity: 1; transform: translateY(0); }
        80% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-10px); }
    }

    .quiz-container { display: flex; flex-direction: column; width: 90%; max-width: 1000px; padding: 3rem; align-items: stretch; text-align: left; overflow-y: auto; max-height: 85vh;}
    .quiz-container h1, .quiz-container h2 { text-align: center; }
    .quiz-intro { text-align: center; font-size: 1.5rem; margin-bottom: 2rem; color: var(--color-dark-gray-1); }
    .quiz-start-btn, .quiz-next-btn { align-self: center; background: var(--color-orange); border: none; color: var(--color-black); font-size: 1.5rem; font-weight: bold; padding: 1rem 3rem; border-radius: 10px; cursor: pointer; transition: transform 0.2s; margin-top: 2rem; }
    .quiz-start-btn:hover, .quiz-next-btn:hover, .quiz-show-answer-btn:hover { transform: scale(1.05); }
    .quiz-header { display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem; color: var(--color-dark-gray-2); border-bottom: 2px solid rgba(0,0,0,0.1); padding-bottom: 10px; }
    .quiz-timer { color: #d9534f; }
    .quiz-question-box { font-size: 1.8rem; margin: 1.5rem 0; font-weight: 700; color: var(--color-black); }
    .quiz-question-box p { margin: 0; }
    .quiz-question-box img { max-width: 100%; border-radius: 10px; max-height: 350px; object-fit: contain; display: block; margin: 15px auto; }
    .quiz-options-box { display: flex; flex-direction: column; gap: 1rem; perspective: 1000px; }
    .quiz-option-card { background: var(--color-white-soft); border: 2px solid var(--color-light-gray); text-align: left; padding: 1rem 1.5rem; font-size: 1.4rem; border-radius: 10px; transition: all 0.6s cubic-bezier(0.4, 0.2, 0.2, 1); font-family: var(--font-main); color: var(--color-dark-gray-1); transform-style: preserve-3d; }
    .quiz-option-card p { margin: 0; }
    .quiz-option-card.flip-correct { background: #d4edda; border-color: #28a745; color: #155724; transform: rotateX(360deg); box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3); }
    .quiz-option-card.fade-out { opacity: 0.4; filter: grayscale(100%); }
    .quiz-feedback-box { margin-top: 2rem; background: rgba(0,0,0,0.05); padding: 1.5rem; border-radius: 10px; border-left: 5px solid var(--color-orange); font-size: 1.3rem; opacity: 0; transform: translateY(20px); transition: opacity 0.5s ease, transform 0.5s ease; }
    .quiz-feedback-box.show { opacity: 1; transform: translateY(0); display: block; }
    
    .quiz-nav-menu { display: flex; justify-content: center; gap: 10px; margin-bottom: 2rem; }
    .quiz-nav-dot { width: 40px; height: 40px; border-radius: 50%; background: rgba(0,0,0,0.1); color: var(--color-dark-gray-2); border: none; font-size: 1.2rem; font-weight: bold; cursor: pointer; transition: all 0.3s; display: flex; justify-content: center; align-items: center; }
    .quiz-nav-dot:hover { background: rgba(0,0,0,0.2); }
    .quiz-nav-dot.active { background: var(--color-orange); color: var(--color-black); transform: scale(1.1); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .quiz-intro { transition: opacity 0.5s, transform 0.5s; }
    .quiz-ui { transition: opacity 0.5s, transform 0.5s; }
    .slide-quizz .content-wrapper { overflow-x: hidden; }
    pre { border-radius: 8px; font-size: 1.1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 1.2rem; color: var(--color-dark-gray-1); }
    th, td { border: 1px solid rgba(0,0,0,0.1); padding: 1rem; text-align: left; }
    th { background-color: var(--color-light-gray); font-weight: bold; color: var(--color-black); }
    tr:nth-child(even) { background-color: rgba(0,0,0,0.02); }
    .slide-overlay table, .slide-gotocode table { color: var(--color-white-soft); }
    .slide-overlay th, .slide-gotocode th { background-color: rgba(255,255,255,0.1); color: var(--color-white-soft); border-color: rgba(255,255,255,0.2); }
    .slide-overlay td, .slide-gotocode td { border-color: rgba(255,255,255,0.2); }
    .slide-overlay tr:nth-child(even), .slide-gotocode tr:nth-child(even) { background-color: rgba(255,255,255,0.05); }
</style>
"""

def generate_js(slides):
    return f"""
<script>
    document.addEventListener('DOMContentLoaded', () => {{
        const dateObj = new Date();
        const day = dateObj.getDate();
        const months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
        const month = months[dateObj.getMonth()];
        const year = dateObj.getFullYear();
        const dateStr = `${{day}} de ${{month}} ${{year}}`;
        document.querySelectorAll('.dynamic-date').forEach(el => el.textContent = dateStr);

        const slides = document.querySelectorAll('.slide');
        const transitionOverlay = document.getElementById('transition-overlay');
        const transitionTitleElement = transitionOverlay.querySelector('h1');
        
        let currentSlide = -1;
        let isTransitioning = false;
        let slideIntervals = {{}};

        // =========================================================================
        // SINTETIZADOR 8-BIT CHIPTUNE (WEB AUDIO API)
        // =========================================================================
        const ChiptuneRadio = {{
            ctx: null,
            isPlaying: false,
            trackIdx: 0,
            step: 0,
            timerId: null,
            tracks: [
                {{
                    name: "Track 1: Streamlit Synth",
                    tempo: 135,
                    lead: [64, 67, 71, 72, 71, 67, 64, 60, 62, 65, 69, 71, 69, 65, 62, 59],
                    bass: [40, 40, 48, 48, 45, 45, 41, 41, 38, 38, 45, 45, 43, 43, 47, 47]
                }},
                {{
                    name: "Track 2: Pandas Boss",
                    tempo: 150,
                    lead: [69, 0, 72, 69, 76, 0, 74, 72, 71, 0, 67, 71, 74, 0, 72, 71],
                    bass: [45, 45, 57, 45, 48, 48, 60, 48, 43, 43, 55, 43, 40, 40, 52, 40]
                }},
                {{
                    name: "Track 3: Lo-Fi Data",
                    tempo: 105,
                    lead: [72, 71, 67, 64, 69, 67, 64, 60, 65, 64, 60, 57, 67, 65, 62, 59],
                    bass: [48, 0, 48, 55, 45, 0, 45, 52, 41, 0, 41, 48, 43, 0, 43, 50]
                }}
            ],
            midiToFreq(m) {{ return m <= 0 ? 0 : 440 * Math.pow(2, (m - 69) / 12); }},
            init() {{
                if (!this.ctx) {{
                    const AC = window.AudioContext || window.webkitAudioContext;
                    this.ctx = new AC();
                }}
                if (this.ctx.state === 'suspended') this.ctx.resume();
            }},
            playTone(freq, type, dur, vol) {{
                if (!this.ctx || freq <= 0) return;
                const now = this.ctx.currentTime;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, now);
                gain.gain.setValueAtTime(0.001, now);
                gain.gain.linearRampToValueAtTime(vol, now + 0.01);
                gain.gain.exponentialRampToValueAtTime(0.0001, now + dur);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start(now);
                osc.stop(now + dur + 0.02);
            }},
            tick() {{
                if (!this.isPlaying) return;
                const tr = this.tracks[this.trackIdx];
                const idx = this.step % tr.lead.length;
                if (tr.lead[idx] > 0) this.playTone(this.midiToFreq(tr.lead[idx]), 'square', 0.14, 0.04);
                if (tr.bass[idx] > 0) this.playTone(this.midiToFreq(tr.bass[idx]), 'triangle', 0.18, 0.06);
                document.querySelectorAll('.px-eq-bar').forEach(b => {{
                    b.style.height = (3 + Math.floor(Math.random() * 11)) + 'px';
                }});
                this.step++;
            }},
            toggle() {{
                this.init();
                this.isPlaying = !this.isPlaying;
                document.querySelectorAll('.px-music-toggle').forEach(btn => {{
                    btn.textContent = this.isPlaying ? '⏸ 8-BIT ON' : '🎵 8-BIT RADIO';
                    btn.classList.toggle('active', this.isPlaying);
                }});
                if (this.isPlaying) {{
                    const stepMs = (60 / this.tracks[this.trackIdx].tempo / 2) * 1000;
                    clearInterval(this.timerId);
                    this.timerId = setInterval(() => this.tick(), stepMs);
                }} else {{
                    clearInterval(this.timerId);
                    document.querySelectorAll('.px-eq-bar').forEach(b => b.style.height = '3px');
                }}
            }},
            stop() {{
                this.isPlaying = false;
                clearInterval(this.timerId);
                document.querySelectorAll('.px-music-toggle').forEach(btn => {{
                    btn.textContent = '🎵 8-BIT RADIO';
                    btn.classList.remove('active');
                }});
            }},
            nextTrack() {{
                this.trackIdx = (this.trackIdx + 1) % this.tracks.length;
                this.step = 0;
                if (this.isPlaying) {{
                    this.toggle();
                    this.toggle();
                }}
            }}
        }};

        window.ChiptuneRadio = ChiptuneRadio;

        // =========================================================================
        // MOTOR ISOMÉTRICO PIXEL ART ESCALADO A PANTALLA COMPLETA (18+ PERSONAJES,
        // TODAS LAS ESTACIONES, CABLES, PIZZAS, VOLCÁN, DINO, DRON Y 5 CAMINANTES)
        // =========================================================================
        function initPixelArtLobby(slideElement) {{
            if (slideElement.dataset.pxInitialized === 'true') return;
            slideElement.dataset.pxInitialized = 'true';

            const viewport = slideElement.querySelector('.px-viewport-area');
            const canvas = slideElement.querySelector('.px-canvas');
            const bubblesLayer = slideElement.querySelector('.px-bubbles-layer');
            const timelineSlider = slideElement.querySelector('.px-timeline-slider');
            const loopSecSpan = slideElement.querySelector('.px-loop-sec');
            const actLabelSpan = slideElement.querySelector('.px-loop-progress-label');

            if (!canvas || !bubblesLayer || !viewport) return;
            const ctx = canvas.getContext('2d');

            const GRID_U = 16, GRID_V = 16;
            const WALL_H = 3.8; // Altura de las paredes en unidades de baldosa
            let W = 1280, H = 720;
            let TILE_W = 84, TILE_H = 42, Z_SCALE = 1.0;
            let ORIGIN_X = 640, ORIGIN_Y = 160;

            function resize() {{
                const rect = viewport.getBoundingClientRect();
                W = rect.width || window.innerWidth;
                H = rect.height || (window.innerHeight - 112);
                canvas.width = W;
                canvas.height = H;

                // Auto-escalado para ocupar el ~90% del área disponible sin cortar paredes ni suelo
                const maxTileWByWidth = (W * 0.90) / ((GRID_U + GRID_V) * 0.5);
                const maxTileHByHeight = (H * 0.84) / ((GRID_U + GRID_V) * 0.5 + WALL_H);
                TILE_W = Math.max(52, Math.min(maxTileWByWidth, maxTileHByHeight * 2));
                TILE_H = TILE_W * 0.5;
                Z_SCALE = TILE_W / 68;

                ORIGIN_X = W * 0.50;
                ORIGIN_Y = H * 0.06 + (WALL_H * TILE_H);
            }}
            resize();
            window.addEventListener('resize', resize);

            function iso(u, v, z = 0) {{
                return {{
                    x: ORIGIN_X + (u - v) * (TILE_W / 2),
                    y: ORIGIN_Y + (u + v) * (TILE_H / 2) - (z * Z_SCALE)
                }};
            }}

            function s(val) {{ return val * Z_SCALE; }}

            function drawIsoBlock(u, v, du, dv, dz, topCol, leftCol, rightCol, strokeCol) {{
                const p00 = iso(u, v, dz), p10 = iso(u + du, v, dz), p11 = iso(u + du, v + dv, dz), p01 = iso(u, v + dv, dz);
                const b10 = iso(u + du, v, 0), b11 = iso(u + du, v + dv, 0), b01 = iso(u, v + dv, 0);

                ctx.fillStyle = leftCol;
                ctx.beginPath(); ctx.moveTo(p01.x, p01.y); ctx.lineTo(p11.x, p11.y); ctx.lineTo(b11.x, b11.y); ctx.lineTo(b01.x, b01.y); ctx.closePath(); ctx.fill();

                ctx.fillStyle = rightCol;
                ctx.beginPath(); ctx.moveTo(p11.x, p11.y); ctx.lineTo(p10.x, p10.y); ctx.lineTo(b10.x, b10.y); ctx.lineTo(b11.x, b11.y); ctx.closePath(); ctx.fill();

                ctx.fillStyle = topCol;
                ctx.beginPath(); ctx.moveTo(p00.x, p00.y); ctx.lineTo(p10.x, p10.y); ctx.lineTo(p11.x, p11.y); ctx.lineTo(p01.x, p01.y); ctx.closePath(); ctx.fill();

                if (strokeCol) {{
                    ctx.strokeStyle = strokeCol;
                    ctx.lineWidth = Math.max(1, s(1.1));
                    ctx.beginPath(); ctx.moveTo(p00.x, p00.y); ctx.lineTo(p10.x, p10.y); ctx.lineTo(p11.x, p11.y); ctx.lineTo(p01.x, p01.y); ctx.closePath(); ctx.stroke();
                }}
            }}

            function drawRoundTable(u, v, radiusTiles, heightZ, topCol, sideCol) {{
                const centerTop = iso(u, v, heightZ);
                const centerBot = iso(u, v, 0);
                const rx = radiusTiles * (TILE_W * 0.55);
                const ry = radiusTiles * (TILE_H * 0.55);

                // Pata central y base
                ctx.fillStyle = '#334155';
                ctx.fillRect(centerBot.x - s(5), centerTop.y, s(10), centerBot.y - centerTop.y);
                ctx.beginPath(); ctx.ellipse(centerBot.x, centerBot.y, rx * 0.45, ry * 0.45, 0, 0, Math.PI * 2); ctx.fill();

                // Borde lateral de la mesa
                ctx.fillStyle = sideCol;
                ctx.beginPath(); ctx.ellipse(centerTop.x, centerTop.y + s(5), rx, ry, 0, 0, Math.PI * 2); ctx.fill();

                // Superficie circular blanca
                ctx.fillStyle = topCol;
                ctx.beginPath(); ctx.ellipse(centerTop.x, centerTop.y, rx, ry, 0, 0, Math.PI * 2); ctx.fill();
                ctx.strokeStyle = '#94a3b8';
                ctx.lineWidth = Math.max(1.5, s(1.5));
                ctx.stroke();
            }}

            function drawPizzaBox(u, v, z) {{
                drawIsoBlock(u, v, 0.55, 0.55, z + 3, '#fef08a', '#eab308', '#ca8a04');
                const p = iso(u + 0.27, v + 0.27, z + 3.5);
                ctx.fillStyle = '#ef4444';
                ctx.beginPath(); ctx.arc(p.x, p.y, s(4.5), 0, Math.PI * 2); ctx.fill();
            }}

            function drawCoffeeMug(u, v, z, frame) {{
                const p = iso(u, v, z);
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(p.x - s(3.5), p.y - s(7), s(7), s(7));
                ctx.fillStyle = '#78350f';
                ctx.fillRect(p.x - s(2.5), p.y - s(6.5), s(5), s(2));
                // Vapor animado
                ctx.strokeStyle = 'rgba(255,255,255,0.65)';
                ctx.lineWidth = Math.max(1, s(1));
                const wave = Math.sin(frame * 0.12 + u) * s(2);
                ctx.beginPath();
                ctx.moveTo(p.x, p.y - s(8));
                ctx.quadraticCurveTo(p.x + wave, p.y - s(13), p.x, p.y - s(17));
                ctx.stroke();
            }}

            function drawRubberDuck(u, v, z) {{
                const p = iso(u, v, z);
                ctx.fillStyle = '#facc15';
                ctx.beginPath(); ctx.arc(p.x, p.y - s(4), s(5), 0, Math.PI * 2); ctx.fill();
                ctx.beginPath(); ctx.arc(p.x + s(3), p.y - s(8), s(3.5), 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#f97316';
                ctx.fillRect(p.x + s(5.5), p.y - s(8.5), s(3.5), s(2.2));
            }}

            function drawChromeDino(u, v, z, frame) {{
                const p = iso(u, v, z);
                const hop = Math.abs(Math.sin(frame * 0.15)) * s(4);
                const dy = p.y - hop;
                ctx.fillStyle = '#22c55e';
                // Cola, torso, cuello y cabeza estilo T-Rex pixelado
                ctx.fillRect(p.x - s(9), dy - s(8), s(5), s(5));
                ctx.fillRect(p.x - s(5), dy - s(13), s(9), s(10));
                ctx.fillRect(p.x, dy - s(21), s(9), s(8));
                ctx.fillStyle = '#052e16';
                ctx.fillRect(p.x + s(5), dy - s(19), s(2), s(2));
                ctx.fillStyle = '#16a34a';
                ctx.fillRect(p.x - s(4), dy - s(3), s(3), s(4));
                ctx.fillRect(p.x + s(1), dy - s(3), s(3), s(4));
            }}

            function drawVolcano(u, v, z, frame) {{
                const base0 = iso(u - 0.55, v + 0.55, z);
                const base1 = iso(u + 0.55, v - 0.55, z);
                const base2 = iso(u + 0.55, v + 0.55, z);
                const top0 = iso(u - 0.22, v + 0.22, z + 22);
                const top1 = iso(u + 0.22, v - 0.22, z + 22);

                ctx.fillStyle = '#78350f';
                ctx.beginPath();
                ctx.moveTo(base0.x, base0.y);
                ctx.lineTo(base2.x, base2.y);
                ctx.lineTo(base1.x, base1.y);
                ctx.lineTo(top1.x, top1.y);
                ctx.lineTo(top0.x, top0.y);
                ctx.closePath();
                ctx.fill();

                // Cráter y lava pulsante
                const crater = iso(u, v, z + 22);
                ctx.fillStyle = '#ef4444';
                ctx.beginPath(); ctx.ellipse(crater.x, crater.y, s(9), s(5), 0, 0, Math.PI * 2); ctx.fill();

                for (let i = 0; i < 3; i++) {{
                    const sparkY = ((frame * 1.8 + i * 14) % 28);
                    const sparkX = Math.sin(frame * 0.15 + i * 2) * 8;
                    ctx.fillStyle = i % 2 === 0 ? '#facc15' : '#fb923c';
                    ctx.fillRect(crater.x + s(sparkX) - s(2), crater.y - s(sparkY) - s(4), s(4), s(4));
                }}
            }}

            function drawCatOnKeyboard(u, v, z, frame) {{
                const p = iso(u, v, z);
                const wag = Math.sin(frame * 0.25) * s(4);
                ctx.fillStyle = '#f97316';
                ctx.fillRect(p.x - s(7), p.y - s(8), s(14), s(8));
                ctx.fillRect(p.x + s(4), p.y - s(13), s(8), s(8));
                // Orejas
                ctx.fillRect(p.x + s(4), p.y - s(16), s(2.5), s(3));
                ctx.fillRect(p.x + s(9.5), p.y - s(16), s(2.5), s(3));
                // Cola animada
                ctx.strokeStyle = '#ea580c';
                ctx.lineWidth = Math.max(2, s(2.5));
                ctx.beginPath();
                ctx.moveTo(p.x - s(7), p.y - s(6));
                ctx.quadraticCurveTo(p.x - s(13), p.y - s(14) + wag, p.x - s(10), p.y - s(18));
                ctx.stroke();
            }}

            function drawSpritePerson(u, v, z, cfg, frame) {{
                const pos = iso(u, v, z);
                const x = Math.round(pos.x);
                const y = Math.round(pos.y);
                const bob = cfg.jumping
                    ? Math.abs(Math.sin(frame * 0.22 + (cfg.seed || 0))) * s(11)
                    : cfg.walking
                        ? Math.abs(Math.sin(frame * 0.28 + (cfg.seed || 0))) * s(4.5)
                        : Math.sin(frame * 0.1 + (cfg.seed || 0)) * s(1.6);

                // Sombra elíptica en el suelo
                ctx.fillStyle = 'rgba(0,0,0,0.35)';
                ctx.beginPath(); ctx.ellipse(x, y + s(2), s(12), s(6.5), 0, 0, Math.PI * 2); ctx.fill();

                const by = Math.round(y - bob);
                const legSwing = cfg.walking ? Math.sin(frame * 0.28 + (cfg.seed || 0)) * s(4) : 0;

                // Zapatos y piernas
                ctx.fillStyle = cfg.pants || '#1e293b';
                ctx.fillRect(x - s(6.5), by - s(13) + legSwing, s(5.5), s(13));
                ctx.fillRect(x + s(1), by - s(13) - legSwing, s(5.5), s(13));
                ctx.fillStyle = '#0f172a';
                ctx.fillRect(x - s(7), by - s(2) + legSwing, s(6), s(3));
                ctx.fillRect(x + s(1), by - s(2) - legSwing, s(6), s(3));

                // Torso con sombreado lateral
                ctx.fillStyle = cfg.shirt || '#3b82f6';
                ctx.fillRect(x - s(9), by - s(30), s(18), s(17));
                ctx.fillStyle = 'rgba(0,0,0,0.18)';
                ctx.fillRect(x + s(4), by - s(30), s(5), s(17));

                // Brazos
                ctx.fillStyle = cfg.shirt || '#3b82f6';
                if (cfg.handsUp) {{
                    ctx.fillRect(x - s(13.5), by - s(39), s(4.5), s(15));
                    ctx.fillRect(x + s(9), by - s(39), s(4.5), s(15));
                }} else {{
                    ctx.fillRect(x - s(13), by - s(28), s(4), s(13));
                    ctx.fillRect(x + s(9), by - s(28), s(4), s(13));
                }}

                // Objeto en mano (Pizza, Escoba, Carpetas CSV, Taza)
                if (cfg.carry === 'pizza') {{
                    ctx.fillStyle = '#fef08a';
                    ctx.fillRect(x + s(6), by - s(24), s(14), s(5));
                    ctx.fillStyle = '#ef4444';
                    ctx.fillRect(x + s(8), by - s(23), s(10), s(2));
                }} else if (cfg.carry === 'broom') {{
                    ctx.fillStyle = '#78350f';
                    ctx.fillRect(x + s(10), by - s(38), s(2.5), s(36));
                    ctx.fillStyle = '#eab308';
                    ctx.fillRect(x + s(6), by - s(5), s(11), s(6));
                }} else if (cfg.carry === 'folders') {{
                    ctx.fillStyle = '#38bdf8';
                    ctx.fillRect(x - s(15), by - s(25), s(10), s(8));
                    ctx.fillStyle = '#f43f5e';
                    ctx.fillRect(x - s(14), by - s(29), s(10), s(4));
                }} else if (cfg.carry === 'mug') {{
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(x + s(10), by - s(22), s(6), s(7));
                }}

                // Cabeza detallada (Oso Panda, Robot IA o Humano con peinado/gafas/audífonos)
                if (cfg.isPanda) {{
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(x - s(10), by - s(46), s(20), s(16));
                    ctx.fillStyle = '#0f172a';
                    ctx.fillRect(x - s(12), by - s(50), s(6), s(6));
                    ctx.fillRect(x + s(6), by - s(50), s(6), s(6));
                    ctx.fillRect(x - s(7), by - s(40), s(4.5), s(4.5));
                    ctx.fillRect(x + s(2.5), by - s(40), s(4.5), s(4.5));
                    ctx.fillRect(x - s(2), by - s(35), s(4), s(2.5));
                }} else if (cfg.isRobot) {{
                    ctx.fillStyle = '#cbd5e1';
                    ctx.fillRect(x - s(10), by - s(46), s(20), s(16));
                    ctx.fillStyle = '#0f172a';
                    ctx.fillRect(x - s(7), by - s(41), s(14), s(6));
                    ctx.fillStyle = '#38bdf8';
                    ctx.fillRect(x - s(5), by - s(39.5), s(4), s(3));
                    ctx.fillRect(x + s(1), by - s(39.5), s(4), s(3));
                    ctx.fillStyle = '#f59e0b';
                    ctx.fillRect(x - s(1.5), by - s(53), s(3), s(7));
                    ctx.beginPath(); ctx.arc(x, by - s(54), s(3), 0, Math.PI * 2); ctx.fill();
                }} else {{
                    ctx.fillStyle = cfg.skin || '#f1c27d';
                    ctx.fillRect(x - s(9), by - s(45), s(18), s(15));
                    // Cabello
                    ctx.fillStyle = cfg.hair || '#271c19';
                    ctx.fillRect(x - s(10), by - s(49), s(20), s(6));
                    if (cfg.longHair) {{
                        ctx.fillRect(x - s(11), by - s(45), s(3.5), s(12));
                        ctx.fillRect(x + s(7.5), by - s(45), s(3.5), s(12));
                    }}
                    // Ojos
                    ctx.fillStyle = '#0f172a';
                    ctx.fillRect(x - s(5.5), by - s(39), s(2.5), s(3.5));
                    ctx.fillRect(x + s(3), by - s(39), s(2.5), s(3.5));
                    // Gafas opcionales
                    if (cfg.glasses) {{
                        ctx.strokeStyle = '#38bdf8';
                        ctx.lineWidth = Math.max(1, s(1.2));
                        ctx.strokeRect(x - s(7), by - s(40.5), s(5.5), s(5));
                        ctx.strokeRect(x + s(1.5), by - s(40.5), s(5.5), s(5));
                    }}
                    // Audífonos opcionales
                    if (cfg.headphones) {{
                        ctx.fillStyle = '#f43f5e';
                        ctx.fillRect(x - s(11.5), by - s(41), s(3), s(7));
                        ctx.fillRect(x + s(8.5), by - s(41), s(3), s(7));
                    }}
                }}
            }}

            // Guion completo de 60 segundos con las 6 escenas propuestas y los personajes dinámicos
            const SCRIPT_EVENTS = [
                {{ id: 'b0',  start: 0,  end: 7,  u: 4.5,  v: 1.5,  z: 56, speaker: '👩‍🏫 Scrum Master', text: '¡Faltan minutos! Pegando últimos Post-its 📋', type: '' }},
                {{ id: 'b1',  start: 1,  end: 10, u: 3.0,  v: 4.8,  z: 60, speaker: '🐼 Panda Scientist', text: '¡Hice DROP TABLE sin el WHERE! 😱', type: 'alert' }},
                {{ id: 'b2',  start: 4,  end: 12, u: 5.5,  v: 3.8,  z: 58, speaker: '👩‍💻 SQL Lead', text: 'Tranquilo... ¿era el entorno de producción? 💀', type: '' }},
                {{ id: 'b3',  start: 10, end: 19, u: 3.2,  v: 10.2, z: 62, speaker: '🦆 Dev (12 Cafés)', text: 'import streamlit as st -> ¡Dashboard listo! 🚀', type: 'success' }},
                {{ id: 'b4',  start: 13, end: 21, u: 5.8,  v: 10.2, z: 58, speaker: '👨‍💻 Full-Stack Dev', text: '¡El patito de hule encontró el bug en la línea 42!', type: '' }},
                {{ id: 'b5',  start: 19, end: 26, u: 7.5,  v: 7.5,  z: 58, speaker: '🧹 Garbage Collector', text: 'Barriendo bloques NaN, NULL y 404 del piso...', type: '' }},
                {{ id: 'b6',  start: 22, end: 31, u: 9.2,  v: 5.8,  z: 64, speaker: '🤖 Robot LLM v4.2', text: 'Según mi regresión lineal, mañana es jueves 42', type: '' }},
                {{ id: 'b7',  start: 25, end: 34, u: 12.2, v: 4.8,  z: 60, speaker: '🦖 Dev Sin Wi-Fi', text: '¡Accuracy de 105% en el volcán! Eso es Overfitting 🔥', type: 'alert' }},
                {{ id: 'b8',  start: 31, end: 41, u: 12.2, v: 9.5,  z: 58, speaker: '🐈 Michi Saboteador', text: 'git push --force origin main 🐾🚨', type: 'alert' }},
                {{ id: 'b9',  start: 34, end: 43, u: 13.5, v: 10.8, z: 62, speaker: '🔥 SRE On-Call', text: '¡El rack GPU llegó a 999°C entrenando épocas!', type: 'alert' }},
                {{ id: 'b10', start: 41, end: 51, u: 7.2,  v: 13.0, z: 58, speaker: '🛋️ UX Data Lead', text: '¿Gráfico de pastel 3D? ¡Sacrilegio visual, usa barras! 📊', type: '' }},
                {{ id: 'b11', start: 44, end: 52, u: 9.5,  v: 13.0, z: 58, speaker: '🛋️ Data Engineer', text: 'Ponle st.balloons() para impresionar al stakeholder 🎈', type: 'success' }},
                {{ id: 'b12', start: 50, end: 60, u: 8.5,  v: 2.5,  z: 66, speaker: '🎉 Equipo Deploy', text: '¡Tests en verde y Deploy exitoso en Streamlit Cloud! 🏆', type: 'success' }}
            ];

            let showAllBubbles = false;
            let manualLoopSec = null;
            let manualTimeout = null;
            const balloons = [];

            function spawnBalloons(count = 18) {{
                const colors = ['#f43f5e', '#38bdf8', '#4ade80', '#facc15', '#a855f7', '#fb923c'];
                for (let i = 0; i < count; i++) {{
                    balloons.push({{
                        x: W * 0.15 + Math.random() * W * 0.70,
                        y: H + 20 + Math.random() * 120,
                        vy: 2.2 + Math.random() * 2.0,
                        sway: Math.random() * Math.PI * 2,
                        color: colors[i % colors.length],
                        r: s(11 + Math.random() * 5)
                    }});
                }}
            }}

            const showAllBtn = slideElement.querySelector('.px-show-all-btn');
            if (showAllBtn) {{
                showAllBtn.addEventListener('click', () => {{
                    showAllBubbles = !showAllBubbles;
                    showAllBtn.classList.toggle('active', showAllBubbles);
                }});
            }}

            const balloonsBtn = slideElement.querySelector('.px-balloons-btn');
            if (balloonsBtn) {{
                balloonsBtn.addEventListener('click', () => spawnBalloons(22));
            }}

            if (timelineSlider) {{
                timelineSlider.addEventListener('input', (e) => {{
                    manualLoopSec = parseFloat(e.target.value);
                    clearTimeout(manualTimeout);
                    manualTimeout = setTimeout(() => {{ manualLoopSec = null; }}, 4000);
                }});
            }}

            const activeBubbleDOM = new Map();
            let startTime = performance.now();
            let frameCount = 0;
            let lastBalloonTriggerSec = -1;

            function renderFrame(now) {{
                if (!slideElement.classList.contains('active')) {{
                    requestAnimationFrame(renderFrame);
                    return;
                }}
                frameCount++;
                const autoSec = ((now - startTime) / 1000) % 60;
                const loopSec = manualLoopSec !== null ? manualLoopSec : autoSec;
                const secInt = Math.floor(loopSec);

                if (timelineSlider && manualLoopSec === null) timelineSlider.value = secInt;
                if (loopSecSpan) loopSecSpan.textContent = `${{String(secInt).padStart(2, '0')}}s / 60s`;
                if (actLabelSpan) {{
                    const actNames = [
                        'Acto 1: Caos SQL & Pandas',
                        'Acto 2: Fiebre de Streamlit',
                        'Acto 3: Volcán de Overfitting',
                        'Acto 4: Sabotaje Felino en Git',
                        'Acto 5: Debate en los Sillones',
                        'Acto 6: ¡Deploy & st.balloons()!'
                    ];
                    actLabelSpan.textContent = actNames[Math.min(5, Math.floor(loopSec / 10))];
                }}

                if (secInt === 51 && lastBalloonTriggerSec !== 51) {{
                    lastBalloonTriggerSec = 51;
                    spawnBalloons(20);
                }} else if (secInt < 50) {{
                    lastBalloonTriggerSec = -1;
                }}

                ctx.clearRect(0, 0, W, H);

                // =========================================================
                // 1. SUELO ISOMÉTRICO EN DAMERO AZUL (16x16 BALDOSAS)
                // =========================================================
                for (let u = 0; u < GRID_U; u++) {{
                    for (let v = 0; v < GRID_V; v++) {{
                        const p0 = iso(u, v), p1 = iso(u + 1, v), p2 = iso(u + 1, v + 1), p3 = iso(u, v + 1);
                        ctx.fillStyle = (u + v) % 2 === 0 ? '#1b6ca8' : '#145385';
                        ctx.beginPath(); ctx.moveTo(p0.x, p0.y); ctx.lineTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.lineTo(p3.x, p3.y); ctx.closePath(); ctx.fill();
                    }}
                }}

                // Borde exterior de la plataforma del piso
                const cornerW = iso(0, GRID_V, 0), cornerS = iso(GRID_U, GRID_V, 0), cornerE = iso(GRID_U, 0, 0);
                ctx.fillStyle = '#0c2d48';
                ctx.beginPath();
                ctx.moveTo(cornerW.x, cornerW.y); ctx.lineTo(cornerS.x, cornerS.y);
                ctx.lineTo(cornerS.x, cornerS.y + s(14)); ctx.lineTo(cornerW.x, cornerW.y + s(14));
                ctx.closePath(); ctx.fill();
                ctx.fillStyle = '#081f33';
                ctx.beginPath();
                ctx.moveTo(cornerS.x, cornerS.y); ctx.lineTo(cornerE.x, cornerE.y);
                ctx.lineTo(cornerE.x, cornerE.y + s(14)); ctx.lineTo(cornerS.x, cornerS.y + s(14));
                ctx.closePath(); ctx.fill();

                // =========================================================
                // 2. PAREDES EN ESQUINA CON PIZARRA KANBAN, PUERTA Y VENTANALES
                // =========================================================
                drawIsoBlock(0, 0, 0.35, GRID_V, 118, '#f1f5f9', '#cbd5e1', '#94a3b8');
                drawIsoBlock(0, 0, GRID_U, 0.35, 118, '#f1f5f9', '#94a3b8', '#cbd5e1');

                // Pizarra Kanban con Post-its (Pared Izquierda)
                drawIsoBlock(0.36, 2.2, 0.12, 4.5, 82, '#ffffff', '#e2e8f0', '#334155', '#475569');
                const postItColors = ['#facc15', '#f43f5e', '#38bdf8', '#4ade80', '#fb923c'];
                for (let pi = 0; pi < 8; pi++) {{
                    const pv = 2.6 + (pi % 4) * 0.95;
                    const pz = 42 + Math.floor(pi / 4) * 20;
                    drawIsoBlock(0.49, pv, 0.05, 0.55, pz, postItColors[pi % 5], postItColors[pi % 5], postItColors[pi % 5]);
                }}

                // Póster Espacial y Máquina de Café en esquina
                drawIsoBlock(0.36, 8.2, 0.12, 2.2, 86, '#0f172a', '#1e1b4b', '#312e81', '#38bdf8');
                drawIsoBlock(0.5, 12.2, 1.2, 1.2, 34, '#334155', '#1e293b', '#0f172a'); // Mesa cafetera
                drawIsoBlock(0.7, 12.4, 0.7, 0.7, 52, '#dc2626', '#991b1b', '#7f1d1d'); // Cafetera Expreso

                // Puerta de Entrada/Salida (Pared Derecha u:2.2..4.2)
                drawIsoBlock(2.2, 0.36, 2.1, 0.15, 88, '#78350f', '#451a03', '#271c19');

                // Pizarra de Arquitectura + 3 Grandes Ventanales Nocturnos (Pared Derecha)
                drawIsoBlock(5.2, 0.36, 3.6, 0.12, 82, '#ffffff', '#cbd5e1', '#e2e8f0', '#475569');
                for (let wi = 0; wi < 3; wi++) {{
                    const wu = 9.6 + wi * 2.0;
                    drawIsoBlock(wu, 0.36, 1.4, 0.12, 86, '#78350f', '#0f172a', '#1e293b', '#b45309');
                }}

                // =========================================================
                // 3. CABLES SERPENTEANDO, CAJAS DE PIZZA Y BLOQUES NaN EN EL PISO
                // =========================================================
                ctx.lineWidth = Math.max(2, s(2.5));
                const cables = [
                    {{ color: '#0f172a', pts: [[4.5, 5.2], [6.5, 6.2], [8.5, 5.8], [11.5, 8.8]] }},
                    {{ color: '#22c55e', pts: [[4.2, 9.8], [6.8, 8.5], [9.2, 9.5], [11.8, 9.5]] }},
                    {{ color: '#ef4444', pts: [[8.8, 6.2], [9.5, 8.0], [11.8, 9.0]] }}
                ];
                cables.forEach(cb => {{
                    ctx.strokeStyle = cb.color;
                    ctx.beginPath();
                    cb.pts.forEach((pt, idx) => {{
                        const p = iso(pt[0], pt[1], 0.5);
                        if (idx === 0) ctx.moveTo(p.x, p.y);
                        else ctx.lineTo(p.x, p.y);
                    }});
                    ctx.stroke();
                }});

                // Bloques literales "NaN" y "NULL" en el pasillo central
                const nanPositions = [[6.8, 6.8, 'NaN'], [8.1, 7.4, 'NULL'], [5.9, 7.6, '404']];
                nanPositions.forEach(([nu, nv, label]) => {{
                    drawIsoBlock(nu, nv, 0.55, 0.55, 6, '#f43f5e', '#be123c', '#881337');
                    const np = iso(nu + 0.25, nv + 0.25, 8);
                    ctx.fillStyle = '#ffffff';
                    ctx.font = `bold ${{Math.round(s(9))}}px monospace`;
                    ctx.fillText(label, np.x - s(8), np.y);
                }});

                // Cajas de pizza abiertas en el suelo
                drawPizzaBox(5.6, 8.8, 0);
                drawPizzaBox(9.8, 7.2, 0);

                // =========================================================
                // 4. LAS 6 ESTACIONES DE TRABAJO Y SUS 18+ PERSONAJES
                // =========================================================

                // --- A) Scrum Master junto a la Pizarra Kanban ---
                drawSpritePerson(1.3, 3.8, 0, {{ skin: '#f1c27d', hair: '#78350f', shirt: '#ec4899', longHair: true, glasses: true, seed: 10 }}, frameCount);

                // --- B) ISLA 1: Mesa Redonda "Data Wrangling & Pandas" (u:4.2, v:4.5) ---
                drawRoundTable(4.2, 4.5, 1.45, 19, '#f8fafc', '#cbd5e1');
                drawIsoBlock(3.7, 4.2, 0.45, 0.45, 24, '#38bdf8', '#0284c7', '#0369a1'); // Laptop Panda
                drawIsoBlock(4.4, 4.6, 0.45, 0.45, 24, '#4ade80', '#16a34a', '#15803d'); // Tablet
                drawCoffeeMug(4.1, 4.8, 19, frameCount);
                drawSpritePerson(2.9, 4.8, 0, {{ isPanda: true, shirt: '#10b981', seed: 1 }}, frameCount);
                drawSpritePerson(5.5, 3.8, 0, {{ skin: '#e0ac69', hair: '#1e293b', shirt: '#ec4899', longHair: true, seed: 2 }}, frameCount);
                drawSpritePerson(4.2, 3.1, 0, {{ skin: '#8d5524', hair: '#0f172a', shirt: '#f59e0b', glasses: true, seed: 3 }}, frameCount);
                drawSpritePerson(4.4, 5.9, 0, {{ skin: '#ffdbac', hair: '#b45309', shirt: '#6366f1', headphones: true, seed: 14 }}, frameCount);

                // --- C) GRUPO CENTRAL DE FESTEJO (4 Devs celebrando como en la imagen 2) ---
                const celebrate = loopSec >= 48;
                drawSpritePerson(7.4, 2.5, 0, {{ skin: '#f1c27d', hair: '#451a03', shirt: '#ef4444', jumping: celebrate, handsUp: true, seed: 6 }}, frameCount);
                drawSpritePerson(8.3, 2.0, 0, {{ skin: '#e0ac69', hair: '#0f172a', shirt: '#10b981', jumping: celebrate, handsUp: true, seed: 7 }}, frameCount);
                drawSpritePerson(9.2, 2.5, 0, {{ skin: '#8d5524', hair: '#000000', shirt: '#3b82f6', jumping: celebrate, handsUp: true, seed: 8 }}, frameCount);
                drawSpritePerson(8.3, 3.1, 0, {{ skin: '#ffdbac', hair: '#dc2626', shirt: '#eab308', jumping: celebrate, handsUp: true, seed: 15 }}, frameCount);

                // --- D) ISLA 2: Escritorios Dobles "Full-Stack & Streamlit" (u:4.2, v:10.2) ---
                drawIsoBlock(2.6, 9.4, 3.4, 1.8, 19, '#b45309', '#92400e', '#78350f', '#451a03');
                // 4 Monitores dobles iluminados
                drawIsoBlock(3.1, 9.8, 0.65, 0.25, 32, '#38bdf8', '#0284c7', '#0369a1');
                drawIsoBlock(4.1, 9.8, 0.65, 0.25, 32, '#4ade80', '#16a34a', '#15803d');
                drawIsoBlock(5.0, 9.8, 0.65, 0.25, 32, '#f43f5e', '#e11d48', '#be123c');
                drawRubberDuck(3.8, 10.5, 19);
                drawCoffeeMug(2.9, 10.6, 19, frameCount);
                drawCoffeeMug(5.4, 10.5, 19, frameCount);
                // 4 Devs frente a frente en el cluster
                drawSpritePerson(3.2, 8.9, 0, {{ skin: '#e0ac69', hair: '#0f172a', shirt: '#0ea5e9', glasses: true, seed: 16 }}, frameCount);
                drawSpritePerson(5.0, 8.9, 0, {{ skin: '#f1c27d', hair: '#7c2d12', shirt: '#14b8a6', longHair: true, seed: 17 }}, frameCount);
                drawSpritePerson(3.2, 11.5, 0, {{ skin: '#ffdbac', hair: '#b45309', shirt: '#3b82f6', headphones: true, seed: 4 }}, frameCount);
                drawSpritePerson(5.2, 11.5, 0, {{ skin: '#8d5524', hair: '#111827', shirt: '#8b5cf6', seed: 5 }}, frameCount);

                // --- E) ISLA 3: Mesa Redonda del Volcán de Overfitting + Dino Chrome + Robot IA (u:10.6, v:5.4) ---
                drawRoundTable(10.6, 5.4, 1.5, 19, '#f8fafc', '#cbd5e1');
                drawVolcano(10.6, 5.4, 19, frameCount);
                drawChromeDino(9.8, 5.8, 19, frameCount);
                drawSpritePerson(9.1, 5.8, 0, {{ isRobot: true, shirt: '#475569', seed: 9 }}, frameCount);
                drawSpritePerson(12.1, 4.9, 0, {{ skin: '#ffdbac', hair: '#dc2626', shirt: '#0ea5e9', glasses: true, seed: 10 }}, frameCount);
                drawSpritePerson(10.7, 3.9, 0, {{ skin: '#f1c27d', hair: '#1e293b', shirt: '#a855f7', longHair: true, seed: 18 }}, frameCount);

                // --- F) ISLA 4: Crisis en Producción, Gato en Teclado y Rack GPU a 999°C (u:12.5, v:9.8) ---
                drawIsoBlock(11.2, 9.0, 2.6, 1.6, 19, '#b45309', '#92400e', '#78350f', '#451a03');
                drawIsoBlock(14.1, 8.4, 1.1, 1.1, 58, '#334155', '#1e293b', '#0f172a', '#ef4444'); // Rack GPU
                // LEDs de alerta en el servidor GPU
                const srvPos = iso(14.5, 9.2, 42);
                ctx.fillStyle = frameCount % 16 < 8 ? '#ef4444' : '#4ade80';
                ctx.fillRect(srvPos.x - s(6), srvPos.y - s(10), s(4), s(4));
                ctx.fillRect(srvPos.x - s(6), srvPos.y - s(2), s(4), s(4));
                // Gato naranja caminando sobre el teclado
                drawCatOnKeyboard(12.2, 9.7, 19, frameCount);
                const panic = (loopSec >= 31 && loopSec <= 43);
                drawSpritePerson(11.8, 11.1, 0, {{ skin: '#e0ac69', hair: '#1e293b', shirt: '#f43f5e', handsUp: panic, jumping: panic, seed: 11 }}, frameCount);
                drawSpritePerson(13.4, 11.1, 0, {{ skin: '#f1c27d', hair: '#0f172a', shirt: '#f97316', handsUp: panic, seed: 19 }}, frameCount);

                // --- G) ZONA LOUNGE SUR: Sillones Verde Lima estilo Imagen 1 (u:8.2, v:13.2) ---
                // Alfombra oscura debajo de los sillones
                const rug0 = iso(6.2, 12.0, 0.2), rug1 = iso(10.6, 12.0, 0.2), rug2 = iso(10.6, 14.8, 0.2), rug3 = iso(6.2, 14.8, 0.2);
                ctx.fillStyle = 'rgba(30, 27, 75, 0.75)';
                ctx.beginPath(); ctx.moveTo(rug0.x, rug0.y); ctx.lineTo(rug1.x, rug1.y); ctx.lineTo(rug2.x, rug2.y); ctx.lineTo(rug3.x, rug3.y); ctx.closePath(); ctx.fill();
                // Sillón individual izquierdo y sofá doble derecho (verde lima)
                drawIsoBlock(6.5, 12.4, 1.3, 1.3, 15, '#a3e635', '#84cc16', '#65a30d', '#3f6212');
                drawIsoBlock(8.3, 12.4, 2.2, 1.3, 15, '#a3e635', '#84cc16', '#65a30d', '#3f6212');
                drawSpritePerson(7.1, 13.1, 7, {{ skin: '#f1c27d', hair: '#78350f', shirt: '#6366f1', longHair: true, seed: 12 }}, frameCount);
                drawSpritePerson(8.9, 13.1, 7, {{ skin: '#8d5524', hair: '#0f172a', shirt: '#ec4899', glasses: true, seed: 13 }}, frameCount);
                drawSpritePerson(9.9, 13.1, 7, {{ skin: '#ffdbac', hair: '#b45309', shirt: '#10b981', seed: 20 }}, frameCount);

                // =========================================================
                // 5. LOS 5 PERSONAJES DINÁMICOS (ENTRANDO, SALIENDO Y CAMINANDO)
                // =========================================================

                // 1) Pasante entrando por la puerta con carpetas CSV y saliendo
                const internProgress = (loopSec % 30) / 30;
                const internU = internProgress < 0.5 ? 3.2 + internProgress * 12 : 9.2 - (internProgress - 0.5) * 12;
                const internV = internProgress < 0.5 ? 1.0 + internProgress * 10 : 6.0 - (internProgress - 0.5) * 10;
                drawSpritePerson(internU, internV, 0, {{ skin: '#ffdbac', hair: '#b45309', shirt: '#38bdf8', walking: true, carry: 'folders', seed: 91 }}, frameCount);

                // 2) Repartidor de Pizza entrando por la puerta hacia los escritorios
                const pizzaProgress = ((loopSec + 15) % 30) / 30;
                const pizzaU = pizzaProgress < 0.5 ? 3.2 + pizzaProgress * 6 : 6.2 - (pizzaProgress - 0.5) * 6;
                const pizzaV = pizzaProgress < 0.5 ? 1.2 + pizzaProgress * 15 : 8.7 - (pizzaProgress - 0.5) * 15;
                drawSpritePerson(pizzaU, pizzaV, 0, {{ skin: '#e0ac69', hair: '#1e293b', shirt: '#ef4444', walking: true, carry: 'pizza', seed: 92 }}, frameCount);

                // 3) Conserje de Datos ("Garbage Collector") barriendo NaNs por el pasillo central
                const cleanerU = 5.5 + Math.sin(loopSec * 0.18) * 3.2;
                const cleanerV = 7.4 + Math.cos(loopSec * 0.18) * 1.1;
                drawSpritePerson(cleanerU, cleanerV, 0, {{ skin: '#f1c27d', hair: '#94a3b8', shirt: '#06b6d4', walking: true, carry: 'broom', seed: 93 }}, frameCount);

                // 4) Dev Sonámbulo caminando entre los sillones y la máquina de café expreso
                const zombieWave = (Math.sin(loopSec * 0.15) + 1) * 0.5;
                const zombieU = 1.6 + zombieWave * 4.5;
                const zombieV = 12.6 + zombieWave * 0.8;
                drawSpritePerson(zombieU, zombieV, 0, {{ skin: '#cbd5e1', hair: '#0f172a', shirt: '#64748b', walking: true, carry: 'mug', seed: 94 }}, frameCount);

                // 5) Dron de Reparto de Pesos (`weights.h5`) cruzando flotando a gran altura
                const droneU = 2.0 + ((loopSec / 60) * 12.0);
                const droneV = 13.0 - ((loopSec / 60) * 10.0);
                const dronePos = iso(droneU, droneV, 68 + Math.sin(frameCount * 0.15) * 6);
                ctx.fillStyle = '#38bdf8';
                ctx.fillRect(dronePos.x - s(10), dronePos.y - s(4), s(20), s(5));
                ctx.fillStyle = '#facc15';
                ctx.fillRect(dronePos.x - s(6), dronePos.y + s(1), s(12), s(9));
                ctx.fillStyle = '#ffffff';
                ctx.font = `bold ${{Math.round(s(8))}}px monospace`;
                ctx.fillText('weights.h5', dronePos.x - s(18), dronePos.y - s(7));

                // =========================================================
                // 6. GLOBOS FESTIVOS st.balloons() SUBIENDO POR LA SALA
                // =========================================================
                for (let bi = balloons.length - 1; bi >= 0; bi--) {{
                    const b = balloons[bi];
                    b.y -= b.vy;
                    const bx = b.x + Math.sin(frameCount * 0.06 + b.sway) * 12;
                    ctx.fillStyle = b.color;
                    ctx.beginPath(); ctx.ellipse(bx, b.y, b.r * 0.85, b.r, 0, 0, Math.PI * 2); ctx.fill();
                    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
                    ctx.lineWidth = 1.2;
                    ctx.beginPath(); ctx.moveTo(bx, b.y + b.r); ctx.lineTo(bx, b.y + b.r + s(16)); ctx.stroke();
                    if (b.y < -40) balloons.splice(bi, 1);
                }}

                // =========================================================
                // 7. SINCRONIZAR GLOBOS DE DIÁLOGO CÓMIC EN EL DOM
                // =========================================================
                const visibleEvents = SCRIPT_EVENTS.filter(ev => showAllBubbles || (loopSec >= ev.start && loopSec <= ev.end));
                const activeIds = new Set(visibleEvents.map(e => e.id));

                for (const [id, domEl] of activeBubbleDOM.entries()) {{
                    if (!activeIds.has(id)) {{
                        domEl.remove();
                        activeBubbleDOM.delete(id);
                    }}
                }}

                visibleEvents.forEach(ev => {{
                    let el = activeBubbleDOM.get(ev.id);
                    if (!el) {{
                        el = document.createElement('div');
                        el.className = `px-speech-bubble ${{ev.type || ''}}`;
                        el.innerHTML = `<span class="px-speaker">${{ev.speaker}}</span>${{ev.text}}`;
                        bubblesLayer.appendChild(el);
                        activeBubbleDOM.set(ev.id, el);
                    }}
                    const screenPos = iso(ev.u, ev.v, ev.z);
                    const clampedX = Math.max(135, Math.min(W - 135, screenPos.x));
                    const clampedY = Math.max(70, Math.min(H - 65, screenPos.y));
                    el.style.left = `${{clampedX}}px`;
                    el.style.top = `${{clampedY}}px`;
                }});

                requestAnimationFrame(renderFrame);
            }}

            requestAnimationFrame(renderFrame);
        }}

        function showSlide(index) {{
            if (isTransitioning || index === currentSlide) return;
            
            const nextSlideElement = slides[index];
            if (!nextSlideElement) return;

            isTransitioning = true;
            
            const transitionTitle = nextSlideElement.dataset.transitionTitle;

            if (currentSlide > -1) {{
                slides[currentSlide].classList.remove('active');
            }}

            if (transitionTitle && index > currentSlide) {{
                transitionTitleElement.textContent = transitionTitle;
                transitionOverlay.className = 'slide';
                transitionOverlay.classList.add(`slide-${{nextSlideElement.dataset.type}}`);
                transitionOverlay.classList.add('visible');

                setTimeout(() => {{
                    transitionOverlay.classList.remove('visible');
                    currentSlide = index;
                    slides[currentSlide].classList.add('active');
                    activateSlide(currentSlide);
                    setTimeout(() => isTransitioning = false, 500);
                }}, 1000);
            }} else {{
                currentSlide = index;
                slides[currentSlide].classList.add('active');
                activateSlide(currentSlide);
                isTransitioning = false;
            }}
        }}

        function nextSlide() {{
            if (currentSlide < slides.length - 1) {{
                showSlide(currentSlide + 1);
            }}
        }}

        function prevSlide() {{
            if (currentSlide > 0) {{
                showSlide(currentSlide - 1);
            }}
        }}
        
        function activateSlide(index) {{
            const slideElement = slides[index];
            if (!slideElement) return;
            const slideType = slideElement.dataset.type;

            Object.values(slideIntervals).forEach(clearInterval);

            if (slideType === 'countdown') {{
                initPixelArtLobby(slideElement);
                const timerElement = slideElement.querySelector('.timer');
                const startMessage = slideElement.querySelector('.start-message');
                const ringFg = slideElement.querySelector('.px-ring-fg');
                const totalDuration = parseInt(slideElement.dataset.timer || '300', 10);
                let duration = totalDuration;
                const circumference = 440;

                const updateTimerUI = () => {{
                    const minutes = Math.floor(Math.max(0, duration) / 60);
                    const seconds = Math.max(0, duration) % 60;
                    timerElement.textContent = `${{String(minutes).padStart(2, '0')}}:${{String(seconds).padStart(2, '0')}}`;
                    if (ringFg && totalDuration > 0) {{
                        const offset = circumference - (Math.max(0, duration) / totalDuration) * circumference;
                        ringFg.style.strokeDashoffset = offset;
                    }}
                }};
                updateTimerUI();

                slideIntervals[index] = setInterval(() => {{
                    if (duration < 0) {{
                        clearInterval(slideIntervals[index]);
                        timerElement.style.display = 'none';
                        startMessage.style.display = 'block';
                        ChiptuneRadio.stop();
                        setTimeout(nextSlide, 2000); 
                        return;
                    }}
                    updateTimerUI();
                    duration--;
                }}, 1000);
            }} else {{
                ChiptuneRadio.stop();
            }}
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight') nextSlide();
            else if (e.key === 'ArrowLeft') prevSlide();
        }});

        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const menuBtn = document.getElementById('menu-btn');
        const slideMenu = document.getElementById('slide-menu');
        const closeMenuBtn = document.getElementById('close-menu-btn');

        if (prevBtn) prevBtn.addEventListener('click', prevSlide);
        if (nextBtn) nextBtn.addEventListener('click', nextSlide);
        if (menuBtn) menuBtn.addEventListener('click', () => slideMenu.classList.add('active'));
        if (closeMenuBtn) closeMenuBtn.addEventListener('click', () => slideMenu.classList.remove('active'));

        document.querySelectorAll('.menu-jump-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                const index = parseInt(e.currentTarget.dataset.index, 10);
                slideMenu.classList.remove('active');
                showSlide(index);
            }});
        }});

        document.querySelectorAll('.quiz-container').forEach(container => {{
            const startBtn = container.querySelector('.quiz-start-btn');
            const nextBtn = container.querySelector('.quiz-next-btn');
            const uiBox = container.querySelector('.quiz-ui');
            const introBox = container.querySelector('.quiz-intro');
            const qBox = container.querySelector('.quiz-question-box');
            const optBox = container.querySelector('.quiz-options-box');
            const feedBox = container.querySelector('.quiz-feedback-box');
            const timerDiv = container.querySelector('.quiz-timer');
            const timerSpan = container.querySelector('.time-left');
            const navMenu = container.querySelector('.quiz-nav-menu');
            const showAnsBtn = container.querySelector('.quiz-show-answer-btn');

            const h1 = container.querySelector('h1');
            const h2 = container.querySelector('h2');

            let rawData = container.getAttribute('data-quiz') || "[]";
            const questions = JSON.parse(rawData);
            const timeLimit = parseInt(container.getAttribute('data-timer') || "0", 10);
            
            let currentQIndex = 0;
            let timerInterval;
            let timeLeft = timeLimit;
            let canAnswer = false;

            function buildNavMenu() {{
                navMenu.innerHTML = '';
                questions.forEach((q, idx) => {{
                    const dot = document.createElement('button');
                    dot.className = 'quiz-nav-dot';
                    dot.textContent = idx + 1;
                    dot.addEventListener('click', () => jumpToQuestion(idx));
                    navMenu.appendChild(dot);
                }});
            }}

            function updateNavMenu() {{
                const dots = navMenu.querySelectorAll('.quiz-nav-dot');
                dots.forEach((dot, idx) => {{
                    if (idx === currentQIndex) dot.classList.add('active');
                    else dot.classList.remove('active');
                }});
            }}

            function renderQuestion() {{
                clearInterval(timerInterval);

                if(currentQIndex >= questions.length) {{
                    uiBox.innerHTML = '<div style="text-align:center; padding: 5rem;"><h2>¡Quiz Terminado!</h2><p>Continúa con las flechas de navegación convencionales.</p></div>';
                    return;
                }}
                
                uiBox.style.opacity = '0';
                uiBox.style.transform = 'translateX(20px)';
                
                setTimeout(() => {{
                    const q = questions[currentQIndex];
                    canAnswer = true;
                    qBox.innerHTML = q.text;
                    optBox.innerHTML = '';
                    feedBox.className = 'quiz-feedback-box'; 
                    feedBox.innerHTML = q.feedback || '';
                    nextBtn.style.display = 'none';
                    if (showAnsBtn) showAnsBtn.style.display = 'none';
                    updateNavMenu();

                    q.options.forEach((opt, idx) => {{
                        const card = document.createElement('div');
                        card.className = 'quiz-option-card';
                        card.innerHTML = opt.text;
                        optBox.appendChild(card);
                    }});

                    uiBox.style.display = 'block';
                    void uiBox.offsetWidth;
                    uiBox.style.opacity = '1';
                    uiBox.style.transform = 'translateX(0)';
                    
                    if (window.MathJax) {{
                        MathJax.typesetPromise().catch((err) => console.log('MathJax error: ', err));
                    }}
                    if (window.hljs) {{
                        uiBox.querySelectorAll('pre code').forEach((block) => hljs.highlightElement(block));
                    }}

                    if (timeLimit > 0) {{
                        timerDiv.style.display = 'inline-block';
                        if (showAnsBtn) showAnsBtn.style.display = 'inline-block';
                        timeLeft = timeLimit;
                        timerSpan.textContent = timeLeft;
                        timerInterval = setInterval(() => {{
                            timeLeft--;
                            timerSpan.textContent = timeLeft;
                            if (timeLeft <= 0) {{
                                clearInterval(timerInterval);
                                revealAnswer();
                            }}
                        }}, 1000);
                    }} else {{
                        timerDiv.style.display = 'none';
                        if (showAnsBtn) showAnsBtn.style.display = 'inline-block';
                        setTimeout(revealAnswer, 5000);
                    }}
                }}, 400);
            }}

            function revealAnswer() {{
                if(!canAnswer) return;
                canAnswer = false;
                clearInterval(timerInterval);
                if (showAnsBtn) showAnsBtn.style.display = 'none';
                
                const q = questions[currentQIndex];
                const cards = optBox.querySelectorAll('.quiz-option-card');
                
                cards.forEach((card, idx) => {{
                    if(q.options[idx].correct) {{
                        card.classList.add('flip-correct');
                    }} else {{
                        card.classList.add('fade-out');
                    }}
                }});

                if (q.feedback) {{
                    feedBox.classList.add('show');
                }}
                
                if (currentQIndex < questions.length - 1) {{
                    nextBtn.style.display = 'inline-block';
                    
                    if (timeLimit > 0) {{
                        timeLeft = timeLimit;
                        timerSpan.textContent = timeLeft;
                        timerInterval = setInterval(() => {{
                            timeLeft--;
                            timerSpan.textContent = timeLeft;
                            if (timeLeft <= 0) {{
                                clearInterval(timerInterval);
                                currentQIndex++;
                                renderQuestion();
                            }}
                        }}, 1000);
                    }}
                }} else {{
                    setTimeout(() => {{
                        currentQIndex++;
                        renderQuestion();
                    }}, timeLimit > 0 ? timeLimit * 1000 : 5000);
                }}
            }}
            
            function jumpToQuestion(idx) {{
                clearInterval(timerInterval);
                currentQIndex = idx;
                renderQuestion();
            }}

            startBtn.addEventListener('click', () => {{
                startBtn.style.display = 'none';
                
                if(introBox) {{
                    introBox.style.opacity = '0';
                    introBox.style.transform = 'scale(0.95)';
                    setTimeout(() => introBox.style.display = 'none', 500);
                }}
                if(h1) h1.style.display = 'none';
                if(h2) h2.style.display = 'none';
                
                buildNavMenu();
                
                setTimeout(() => {{
                    uiBox.style.display = 'block';
                    renderQuestion();
                }}, 500);
            }});

            nextBtn.addEventListener('click', () => {{
                currentQIndex++;
                renderQuestion();
            }});

            if (showAnsBtn) {{
                showAnsBtn.addEventListener('click', () => {{
                    revealAnswer();
                }});
            }}
        }});

        if (slides.length > 0) {{
            showSlide(0);
        }}
    }});
</script>
"""

def _generate_quizz_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    content = slide.get('content', '')
    
    questions = []
    intro_lines = []

    if 'quizz:' in content:
        try:
            parts = content.split('quizz:', 1)
            intro_md = parts[0].strip()
            if intro_md:
                intro_lines = [intro_md]
            
            yaml_str = 'quizz:' + parts[1]
            data = yaml.safe_load(yaml_str)
            quizz_data = data.get('quizz', [])
            
            if isinstance(quizz_data, dict):
                quizz_data = [quizz_data]
                
            for q_data in quizz_data:
                q = q_data.get('question', {})
                body = markdown.markdown(q.get('body', '').strip(), extensions=['fenced_code', 'tables'])
                options = []
                
                for item in q.get('items', []):
                    opt_text = markdown.markdown(item.get('option', '').strip(), extensions=['fenced_code', 'tables'])
                    options.append({'text': opt_text, 'correct': item.get('correct', False)})
                feedback = markdown.markdown(q.get('feedback', '').strip(), extensions=['fenced_code', 'tables'])
                questions.append({'text': body, 'options': options, 'feedback': feedback})
        except Exception as e:
            print(f"Error parsing YAML quizz: {e}")
    else:
        current_q = None
        state = None
        for line in content.split('\n'):
            stripped = line.strip()
            if not stripped: continue
            
            if line.startswith('* '):
                if current_q:
                    questions.append(current_q)
                current_q = {'text': markdown.markdown(stripped[2:].strip(), extensions=['fenced_code', 'tables']), 'options': [], 'feedback': ''}
                state = 'question'
            else:
                if stripped.startswith('* Options:'):
                    state = 'options'
                elif stripped.startswith('* Feedback:'):
                    state = 'feedback'
                elif stripped.startswith('* '):
                    if state == 'options':
                        opt_text = stripped[2:]
                        correct = False
                        if '{correct: true}' in opt_text:
                            correct = True
                            opt_text = opt_text.replace('{correct: true}', '').strip()
                        current_q['options'].append({'text': markdown.markdown(opt_text, extensions=['fenced_code', 'tables']), 'correct': correct})
                    elif state == 'feedback':
                        current_q['feedback'] += markdown.markdown(stripped[2:].strip(), extensions=['fenced_code', 'tables']) + " "
                elif line.startswith('> '):
                    intro_lines.append(line[2:])
                
        if current_q:
            questions.append(current_q)
            
    intro_html = markdown.markdown('\n'.join(intro_lines), extensions=['fenced_code', 'tables']) if intro_lines else ""
    timer = slide.get('params', {}).get('time_limit', '15')
    
    quiz_data = html.escape(json.dumps(questions))
    
    return f"""<div class="content-wrapper quiz-container" data-quiz="{quiz_data}" data-timer="{timer}">
        <h1>{title}</h1>
        <h2>{subtitle}</h2>
        <div class="quiz-intro">{intro_html}</div>
        <div class="quiz-ui" style="display:none; opacity: 0; transform: translateX(20px);">
            <div class="quiz-nav-menu"></div>
            <div class="quiz-header" style="justify-content: flex-end; flex-direction: column; align-items: flex-end;">
                <span class="quiz-timer" style="display:none; font-size: 1.5rem;">⏳ <span class="time-left"></span>s</span>
                <button class="quiz-show-answer-btn" style="display:none; margin-top: 10px; font-size: 1.1rem; cursor: pointer; padding: 8px 15px; border-radius: 5px; background: var(--color-orange); color: var(--color-black); border: none; font-weight: bold; transition: transform 0.2s;">Mostrar Respuesta</button>
            </div>
            <div class="quiz-question-box"></div>
            <div class="quiz-options-box"></div>
            <div class="quiz-feedback-box"></div>
            <button class="quiz-next-btn" style="display:none;">Siguiente Pregunta</button>
        </div>
        <button class="quiz-start-btn">Comenzar</button>
    </div>"""

def _generate_countdown_html(slide):
    """
    Genera la vista de espera Pixel Art Isométrica a pantalla completa:
    - Barra superior dedicada (112px) con título, subtítulo, reloj circular y radio 8-Bit
      para no ocultar ningún detalle del Pixel Art.
    - Lienzo isométrico auto-escalado al 90% del área inferior con todas las estaciones,
      18+ personajes fijos, 5 personajes dinámicos entrando/saliendo y línea de tiempo de 60s.
    """
    title = html.escape(slide.get('title', 'Sprint 1 Sesión 1'))
    subtitle = html.escape(slide.get('subtitle', ''))
    transition_msg = html.escape(slide.get('params', {}).get('title_transition', '¡Comenzamos!'))
    logo_animation = slide.get('params', {}).get('logo_animation', 'dvd')
    bg_html = ""
    
    if logo_animation == 'traffic':
        logo_src = "https://logoimg.careerjet.net/2f2f984040414fbcf1747ea52b99ee70.png"
        logos = []
        rows = [18, 42, 66, 84]
        for row_top in rows:
            duration = random.uniform(20, 35)
            num_cars = random.randint(3, 5)
            for i in range(num_cars):
                delay = - (duration / num_cars) * i
                logos.append(f'<img class="traffic-logo-img" src="{logo_src}" style="top: {row_top}%; animation: driveRight {duration:.2f}s linear {delay:.2f}s infinite;">')
        bg_html = f'<div class="traffic-logo-container">{"".join(logos)}</div>'
    else:
        bg_html = f'<div class="bouncing-logo-container"><img class="bouncing-logo" src="https://logoimg.careerjet.net/2f2f984040414fbcf1747ea52b99ee70.png" alt="Bouncing Logo"></div>'

    return f"""
    <div class="px-stage-wrapper">
        <!-- BARRA SUPERIOR DEDICADA (NO TAPA EL PIXEL ART) -->
        <header class="px-top-bar">
            <div class="px-title-block">
                <div class="px-webinar-tag">
                    <span class="px-webinar-dot"></span>
                    <span>WEBINAR EN VIVO</span>
                </div>
                <h1>{title}</h1>
                <h2>{subtitle}</h2>
            </div>

            <div class="px-center-clock">
                <div class="px-clock-wrapper">
                    <svg class="px-clock-svg" viewBox="0 0 160 160">
                        <circle class="px-ring-bg" cx="80" cy="80" r="70"></circle>
                        <circle class="px-ring-fg" cx="80" cy="80" r="70"></circle>
                    </svg>
                    <div class="timer">--:--</div>
                    <div class="start-message">{transition_msg}</div>
                </div>
                <div class="px-clock-meta">
                    <div class="px-clock-sub">INICIAMOS EN BREVE</div>
                    <div class="px-loop-progress-label">Acto 1: Caos SQL & Pandas</div>
                </div>
            </div>

            <div class="px-hud-controls">
                <div class="px-hud-card">
                    <div class="px-eq-bars">
                        <div class="px-eq-bar"></div>
                        <div class="px-eq-bar"></div>
                        <div class="px-eq-bar"></div>
                        <div class="px-eq-bar"></div>
                    </div>
                    <button type="button" class="px-btn px-music-toggle" onclick="window.ChiptuneRadio.toggle()">🎵 8-BIT RADIO</button>
                    <button type="button" class="px-btn" onclick="window.ChiptuneRadio.nextTrack()" title="Cambiar pista 8-Bit">⏭</button>
                    <button type="button" class="px-btn px-balloons-btn" title="Lanzar globos de Streamlit">🎈 GLOBOS</button>
                    <button type="button" class="px-btn px-show-all-btn" title="Mostrar todos los diálogos a la vez">💬 TODOS</button>
                </div>
            </div>
        </header>

        <!-- ESCENARIO ISOMÉTRICO A PANTALLA COMPLETA -->
        <div class="px-viewport-area">
            {bg_html}
            <canvas class="px-canvas"></canvas>
            <div class="px-bubbles-layer"></div>

            <!-- Línea de tiempo interactiva del bucle de 60 segundos -->
            <div class="px-bottom-timeline">
                <span>⏱ BUCLE:</span>
                <input type="range" class="px-timeline-slider" min="0" max="59" value="0" title="Arrastra para explorar cualquier segundo del bucle">
                <span class="px-loop-sec">00s / 60s</span>
            </div>

            <div class="dynamic-date" style="position: absolute; bottom: 20px; left: 26px; font-size: 1rem; font-weight: bold; color: var(--px-gold); z-index: 65; font-family: 'Press Start 2P', monospace;"></div>
        </div>
    </div>
    """

def _generate_warnup_mood_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    emojis = [
        '😀', '😄', '😊', '😁', '🙂',
        '🤔', '🧐', '😐', '🤨', '😶',
        '🚀', '🔥', '⚡', '🌟', '✨',
        '🤯', '😵', '😲', '😳',
        '😴', '🥱', '😪',
        '💡', '🧠',
        '🎉', '🥳', '🙌',
        '💪', '🏋️',
        '😅', '😓',
        '😞', '😔', '😢',
        '😤', '😠',
        '🤩', '😍'
    ]
    emoji_html = "".join([f'<div class="emoji" style="left: {random.randint(0, 95)}vw; animation-delay: -{random.uniform(0, 10):.2f}s; animation-duration: {random.uniform(5, 12):.2f}s; font-size: {random.uniform(3, 6):.2f}rem;">{random.choice(emojis)}</div>' for _ in range(50)])
    return f"""<div class="emoji-container">{emoji_html}</div><div class="content-wrapper"><h1>{title}</h1><h2>{subtitle}</h2></div>"""

def _generate_warnup_question_html(slide):
    content = slide.get('content', '')
    left_match = re.search(r'\{left\}(.*?)\{right\}', content, re.DOTALL)
    if left_match:
        left_content = left_match.group(1).strip()
        rest_of_content = content[left_match.end():].strip()
        img_match = re.search(r'\[.*?\]\((.*?)\)', rest_of_content)
        right_content = f'<img src="{html.escape(img_match.group(1))}" alt="Slide image">' if img_match else ""
    else:
        left_content = content
        right_content = ""
    return f"""<div class="two-column-layout"><div class="column-left">{left_content}</div><div class="column-right">{right_content}</div></div>"""

def _generate_agenda_html(slide):
    title = html.escape(slide.get('title', ''))
    items_html = ""
    for line in slide.get('content', '').split('\n'):
        if line.strip().startswith('* '):
            item_text = line.strip()[2:]
            duration_match = re.search(r'\{(.*?)\}', item_text)
            duration_text = ""
            if duration_match:
                duration = duration_match.group(1)
                duration_text = f"<span>{duration} min</span>"
                item_text = item_text[:duration_match.start()].strip()
            items_html += f"<li><strong>{item_text}</strong> {duration_text}</li>"
    return f"""<div class="content-wrapper"><h1>{title}</h1><ul>{items_html}</ul></div>"""

def _generate_objectives_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    title_html = f"<h1>{title}</h1>" if title else ""
    subtitle_html = f"<h2>{subtitle}</h2>" if subtitle else ""
    content = slide.get('content', '')
    content = re.sub(r'^ {2,3}([-*])', r'    \1', content, flags=re.MULTILINE)
    content_html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
    return f"""<div class="content-wrapper">{title_html}{subtitle_html}<div class="objectives-container">{content_html}</div></div>"""

def _generate_gotocode_html(slide):
    title = html.escape(slide.get('title', ''))
    qr_html = "".join([f'<div class="qr-item"><img src="{html.escape(url)}" alt="{html.escape(name)} QR Code"><p>{html.escape(name)}</p></div>' for name, url in re.findall(r'\*\s*\[(.*?)\]\((.*?)\)', slide.get('content', ''))])
    return f"""<h1>{title}</h1><div class="qr-container">{qr_html}</div>"""

def _generate_finale_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    return f"<h1>{title}</h1><h2>{subtitle}</h2>"

def _generate_overlay_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    title_html = f"<h1>{title}</h1>" if title else ""
    subtitle_html = f"<h2>{subtitle}</h2>" if subtitle else ""
    content = slide.get('content', '')
    content_html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
    return f"""<div style="width: 80%; max-width: 1200px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">{title_html}{subtitle_html}{content_html}</div>"""

def _generate_basic_slide_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    title_html = f"<h1>{title}</h1>" if title else ""
    subtitle_html = f"<h2>{subtitle}</h2>" if subtitle else ""
    content_html = markdown.markdown(slide.get('content', ''), extensions=['fenced_code', 'tables'])
    return f"""<div class="content-wrapper">{title_html}{subtitle_html}{content_html}</div>"""

def _generate_two_columns_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    title_html = f"<h1>{title}</h1>" if title else ""
    subtitle_html = f"<h2>{subtitle}</h2>" if subtitle else ""

    content = slide.get('content', '')
    left_match = re.search(r'\.left\{(.*?)\}', content, re.DOTALL | re.IGNORECASE)
    right_match = re.search(r'\.right\{(.*?)\}|\.rigth\{(.*?)\}', content, re.DOTALL | re.IGNORECASE)
    
    left_content = left_match.group(1).strip() if left_match else ""
    right_content = ""
    if right_match:
        right_content = right_match.group(1) if right_match.group(1) else right_match.group(2)
        right_content = right_content.strip()
    
    left_html = markdown.markdown(left_content, extensions=['fenced_code', 'tables'])
    right_html = markdown.markdown(right_content, extensions=['fenced_code', 'tables'])
    
    return f"""<div class="content-wrapper">{title_html}{subtitle_html}<div class="two-column-layout" style="align-items: stretch; margin-top: 1rem;"><div class="column-left">{left_html}</div><div class="column-right">{right_html}</div></div></div>"""

def generate_slide_html(slide):
    logo_html = '<img src="https://logoimg.careerjet.net/2f2f984040414fbcf1747ea52b99ee70.png" class="company-logo" alt="Logo">\n'
    generator_map = {
        'countdown': _generate_countdown_html, 'warnup-mood': _generate_warnup_mood_html,
        'warnup-question': _generate_warnup_question_html, 'agenda': _generate_agenda_html,
        'objectives': _generate_objectives_html, 'gotocode': _generate_gotocode_html,
        'finale': _generate_finale_html, 'basic_slide': _generate_basic_slide_html,
        'two_columns_slide': _generate_two_columns_html, 'overlay': _generate_overlay_html,
        'quizz': _generate_quizz_html,
    }
    generator_func = generator_map.get(slide.get('type', 'unknown'))
    if generator_func:
        return logo_html + generator_func(slide)
    return logo_html + f"<h1>{html.escape(slide.get('title', ''))}</h1><h2>{html.escape(slide.get('subtitle', ''))}</h2><p>{html.escape(slide.get('content', ''))}</p>"

def generate_html(slides):
    css = generate_css()
    js = generate_js(slides)
    slides_html = ""
    slide_list_items_html = ""
    for i, slide in enumerate(slides):
        slide_type = slide.get('type', 'unknown')
        slide_content = generate_slide_html(slide)
        transition_title = slide.get('params', {}).get('title_transition', '')
        timer_duration = slide.get('params', {}).get('timer', '600')
        data_attributes = f'data-type="{slide_type}"'
        if slide_type == 'countdown':
            data_attributes += f' data-timer="{timer_duration}"'
        if transition_title:
            data_attributes += f' data-transition-title="{html.escape(transition_title)}"'
        slides_html += f'<div class="slide slide-{slide_type}" id="slide-{i}" {data_attributes}>\n{slide_content}\n</div>\n'
        
        slide_title = slide.get('title', '')
        if not slide_title:
            slide_title = slide.get('subtitle', '')
        if not slide_title:
            slide_title = f"{slide_type.capitalize()} {i+1}"
        slide_list_items_html += f'<li><button class="menu-jump-btn" data-index="{i}">{i+1}. {html.escape(slide_title)}</button></li>\n'

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentación</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
    <script>
      window.MathJax = {{
        tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }}
      }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    {css}
</head>
<body>
    <div class="presentation">
        <div id="transition-overlay"><div class="content-wrapper"><h1></h1></div></div>
        {slides_html}
        <div id="slide-menu" class="slide-menu">
            <div class="slide-menu-content">
                <button id="close-menu-btn" class="close-menu" title="Cerrar">&times;</button>
                <h2>Índice de Diapositivas</h2>
                <ul class="slide-list">
                    {slide_list_items_html}
                </ul>
            </div>
        </div>
        <div class="slide-nav">
            <button id="prev-btn" title="Anterior (Flecha Izquierda)">&#8592;</button>
            <button id="menu-btn" title="Índice de Diapositivas">&#9776;</button>
            <button id="next-btn" title="Siguiente (Flecha Derecha)">&#8594;</button>
        </div>
    </div>
    {js}
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser(description='Generate HTML slides from a markdown file with Full-Screen Isometric Pixel Art Countdown.')
    parser.add_argument('--output_file', type=str, default='', help='Output HTML file name.')
    parser.add_argument('--input_file', type=str, default='', help='Input markdown file name.')
    args, _ = parser.parse_known_args()
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    root_file_dir = os.path.dirname(os.path.abspath(args.input_file))
    markdown_content = resolve_includes(markdown_content, args.input_file, root_file_dir)
    slides = parse_markdown(markdown_content)
    html_output = generate_html(slides)
    if not args.output_file:
        args.output_file = args.input_file.replace('.md', '.html')
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Successfully generated slides in '{args.output_file}'")

if __name__ == '__main__':
    main()
