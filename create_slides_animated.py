import re
import argparse
import html
import random
import os
import markdown
import json
import yaml
import base64
from pathlib import Path


def _lofi_image_uri(filename):
    """Embed the artwork so generated slide decks remain a single portable HTML file."""
    image_path = Path(__file__).resolve().parent / 'lofi_assets' / filename
    try:
        payload = base64.b64encode(image_path.read_bytes()).decode('ascii')
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Falta {image_path}. Conserva la carpeta lofi_assets junto a create_slides.py."
        ) from exc
    return f'data:image/png;base64,{payload}'

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

    # Try relative to current_file_dir
    path1 = os.path.abspath(os.path.join(current_file_dir, include_path))
    if os.path.exists(path1):
        return path1

    # Try relative to root_file_dir
    path2 = os.path.abspath(os.path.join(root_file_dir, include_path))
    if os.path.exists(path2):
        return path2

    # Try relative to CWD
    path3 = os.path.abspath(include_path)
    if os.path.exists(path3):
        return path3

    # Default fallback
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

        # Recursively resolve nested includes
        resolved_content = resolve_includes(included_content, resolved_path, root_file_dir, visited.copy())
        
        # Ensure it ends with --- and a newline to terminate the slide properly
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
    Generates the CSS for the presentation.
    """
    css = """
<style>
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

    .slide-countdown { background: #0b1625; color: #f7e9ce; text-align: left; isolation: isolate; padding: 0; align-items: flex-end; }
    .slide-countdown .lofi-scene { position: absolute; inset: 0; z-index: -2; overflow: hidden; pointer-events: none; }
    .slide-countdown .lofi-frame { position: absolute; width: max(100vw, 177.872vh); height: max(100vh, 56.22vw); top: 50%; left: 50%; transform: translate(-50%, -50%) scaleX(-1) scale(1.015); filter: blur(2.2px) saturate(.88); }
    .slide-countdown .lofi-layer { position: absolute; inset: 0; background-size: 100% 100%; background-position: center; background-repeat: no-repeat; }
    .slide-countdown .lofi-base, .slide-countdown .lofi-head, .slide-countdown .lofi-paws { background-image: url('__LOFI_SCENE__'); }
    .slide-countdown .lofi-yawn { background-image: url('__LOFI_YAWN__'); opacity: 0; -webkit-mask-image: radial-gradient(ellipse 19% 28% at 71.5% 50.5%, #000 55%, transparent 94%); mask-image: radial-gradient(ellipse 19% 28% at 71.5% 50.5%, #000 55%, transparent 94%); animation: lofiYawn 33s ease-in-out infinite; }
    .slide-countdown .lofi-head { -webkit-mask-image: radial-gradient(ellipse 17% 27% at 72% 51%, #000 64%, transparent 96%); mask-image: radial-gradient(ellipse 17% 27% at 72% 51%, #000 64%, transparent 96%); transform-origin: 77% 62%; animation: lofiHead 9s ease-in-out infinite; }
    .slide-countdown .lofi-paws { -webkit-mask-image: radial-gradient(ellipse 11% 7% at 72% 80%, #000 45%, transparent 96%); mask-image: radial-gradient(ellipse 11% 7% at 72% 80%, #000 45%, transparent 96%); animation: lofiType 1.25s steps(4,end) infinite; }
    .slide-countdown .lofi-scene::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(2,10,24,.48), rgba(3,12,27,.20) 53%, rgba(3,10,21,.06)), linear-gradient(0deg, rgba(4,11,22,.44), transparent 35%); }
    .slide-countdown .lofi-rain { position: absolute; inset: -20% 0; z-index: -1; opacity: .11; pointer-events: none; background: repeating-linear-gradient(105deg, transparent 0 34px, rgba(195,221,237,.36) 35px, transparent 36px 80px); background-size: 180px 180px; animation: lofiRain 1.8s linear infinite; }
    .slide-countdown .lofi-panel { position: relative; box-sizing: border-box; width: min(500px, calc(100vw - 100px)); margin-left: auto; margin-right: clamp(24px, 3.5vw, 68px); padding: clamp(24px, 3vw, 40px); border-radius: 24px; border: 1px solid rgba(255,237,205,.18); background: linear-gradient(142deg, rgba(11,25,40,.86), rgba(10,22,34,.70)); box-shadow: 0 25px 95px rgba(0,0,0,.35), inset 0 1px rgba(255,255,255,.09); backdrop-filter: blur(23px); -webkit-backdrop-filter: blur(23px); }
    .slide-countdown .lofi-kicker { display: flex; align-items: center; gap: 9px; font-size: .76rem; font-weight: 700; letter-spacing: .22em; text-transform: uppercase; color: #ffc26b; }
    .slide-countdown .lofi-kicker::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: #ffc26b; box-shadow: 0 0 14px #ffc26b; }
    .slide-countdown .lofi-panel h1 { font-family: Georgia, 'Times New Roman', serif; color: #fff0d8; font-size: clamp(2rem, 3vw, 2.8rem); font-weight: 400; line-height: 1.12; letter-spacing: -.035em; margin: 14px 0 7px; overflow-wrap: anywhere; }
    .slide-countdown .lofi-panel h2 { color: #c7c6c0; font-size: clamp(.95rem, 1.3vw, 1.2rem); line-height: 1.38; font-weight: 400; margin: 0; overflow-wrap: anywhere; }
    .slide-countdown .lofi-dial { position: relative; display: grid; place-items: center; width: min(100%, 285px); aspect-ratio: 1; margin: 18px auto 12px; }
    .slide-countdown .lofi-dial svg { position: absolute; inset: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .slide-countdown .lofi-track, .slide-countdown .lofi-progress { fill: none; stroke-width: 2.6; }
    .slide-countdown .lofi-track { stroke: rgba(255,231,191,.14); }
    .slide-countdown .lofi-progress { stroke: #ffc26b; stroke-linecap: round; stroke-dasharray: 628.319; filter: drop-shadow(0 0 7px rgba(255,194,107,.5)); transition: stroke-dashoffset .25s linear; }
    .slide-countdown .lofi-dial-copy { display: flex; flex-direction: column; align-items: center; gap: 8px; }
    .slide-countdown .timer { display: block; font-size: clamp(3.6rem, 5.4vw, 5.2rem); line-height: 1; font-weight: 300; font-variant-numeric: tabular-nums; letter-spacing: -.075em; color: #fff0d8; }
    .slide-countdown .lofi-status { min-height: 1.3em; font-size: .72rem; text-transform: uppercase; letter-spacing: .2em; color: #d3c6ae; }
    .slide-countdown .start-message { display: none; text-align: center; color: #ffc26b; font-size: 1.2rem; font-weight: 700; margin: -3px 0 12px; }
    .slide-countdown .lofi-controls { display: flex; gap: 10px; margin-top: 12px; }
    .slide-countdown button { font-family: var(--font-main); cursor: pointer; }
    .slide-countdown button:focus-visible, .slide-countdown input:focus-visible { outline: 2px solid #ffc26b; outline-offset: 3px; }
    .slide-countdown .lofi-start { flex: 1; border: 0; background: #ffc477; color: #241a14; font-size: 1rem; font-weight: 700; min-height: 48px; border-radius: 12px; }
    .slide-countdown .lofi-reset, .slide-countdown .lofi-music { background: rgba(255,255,255,.055); border: 1px solid rgba(255,238,208,.2); color: #f1e3ce; border-radius: 12px; min-height: 48px; padding: 0 15px; font-size: .9rem; }
    .slide-countdown .lofi-reset:hover, .slide-countdown .lofi-music:hover { background: rgba(255,194,107,.16); }
    .slide-countdown .lofi-tools { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(255,236,205,.13); }
    .slide-countdown .lofi-time-label { display: flex; align-items: center; gap: 7px; font-size: .83rem; color: #d6c9b8; }
    .slide-countdown .lofi-minutes { width: 67px; padding: 7px 5px 7px 8px; border: 1px solid rgba(255,238,208,.25); border-radius: 8px; background: rgba(255,255,255,.07); color: #fff0d8; font: inherit; font-variant-numeric: tabular-nums; }
    .slide-countdown .lofi-ambience-row { display: flex; align-items: center; gap: 12px; margin-top: 12px; color: #d6c9b8; font-size: .83rem; }
    .slide-countdown .lofi-ambience { flex: 1; min-width: 0; padding: 7px 9px; border: 1px solid rgba(255,238,208,.25); border-radius: 8px; background: #202c38; color: #fff0d8; font: inherit; }
    .slide-countdown .lofi-edit { position: absolute; top: 24px; right: 26px; z-index: 5; }
    .slide-countdown .lofi-edit > summary { list-style: none; cursor: pointer; padding: 8px 12px; border: 1px solid rgba(255,238,208,.25); background: rgba(11,25,40,.76); border-radius: 9px; color: #fff0d8; font-size: .82rem; }
    .slide-countdown .lofi-edit > summary::-webkit-details-marker { display: none; }
    .slide-countdown .lofi-edit form { position: absolute; right: 0; top: 43px; display: grid; gap: 10px; width: min(320px, calc(100vw - 35px)); padding: 18px; border-radius: 14px; color: #f7e9ce; text-align: left; background: rgba(10,22,34,.97); border: 1px solid rgba(255,237,205,.25); box-shadow: 0 15px 40px rgba(0,0,0,.4); }
    .slide-countdown .lofi-edit label { display: grid; gap: 5px; font-size: .83rem; }
    .slide-countdown .lofi-edit input { width: 100%; box-sizing: border-box; border: 1px solid rgba(255,238,208,.25); border-radius: 7px; padding: 8px 10px; background: #152336; color: #fff0d8; font: inherit; }
    .slide-countdown .lofi-edit button { border: 0; border-radius: 8px; background: #ffc477; color: #241a14; padding: 10px; font-weight: 700; }
    @keyframes lofiHead { 0%,20%,100% { transform: rotate(0deg) translateY(0); } 38%,44% { transform: rotate(1.2deg) translateY(2px); } 52% { transform: rotate(-.5deg) translateY(-1px); } }
    @keyframes lofiType { 0%,100% { transform: translateY(0); } 25%,70% { transform: translateY(2px); } 50% { transform: translateY(-1px); } }
    @keyframes lofiYawn { 0%,54%,56%,69%,71%,100% { opacity: 0; } 59%,66% { opacity: 1; } }
    @keyframes lofiRain { from { background-position: 0 0; } to { background-position: -28px 190px; } }
    @media (max-width: 760px) {
        .slide-countdown { justify-content: flex-end; align-items: center; padding-bottom: 20px; }
        .slide-countdown .lofi-frame { transform: translate(-69%, -50%) scale(1.015); }
        .slide-countdown .lofi-panel { margin: 0 auto; width: min(450px, 92vw); padding: 23px; }
        .slide-countdown .lofi-dial { width: min(100%, 215px); margin: 8px auto; }
        .slide-countdown .timer { font-size: 3.65rem; }
    }
    @media (max-height: 680px) {
    .slide-countdown .lofi-panel { padding: 19px 24px; max-height: calc(100vh - 20px); overflow-y: auto; }
        .slide-countdown .lofi-dial { width: min(100%, 205px); margin: 7px auto; }
        .slide-countdown .lofi-tools { margin-top: 10px; padding-top: 10px; }
    }
    @media (prefers-reduced-motion: reduce) { .slide-countdown .lofi-head, .slide-countdown .lofi-paws, .slide-countdown .lofi-yawn, .slide-countdown .lofi-rain { animation: none; } .slide-countdown .lofi-yawn { opacity: 0; } }
    
    .bouncing-logo-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; overflow: hidden; z-index: 0; pointer-events: none; }
    .bouncing-logo { position: absolute; width: 250px; opacity: 0.15; animation: bounceX 13s linear infinite alternate, bounceY 9s linear infinite alternate; }
    @keyframes bounceX { 0% { left: 0; } 100% { left: calc(100vw - 250px); } }
    @keyframes bounceY { 0% { top: 0; } 100% { top: calc(100vh - 75px); } }

    .traffic-logo-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; overflow: hidden; z-index: 0; pointer-events: none; }
    .traffic-logo-img { position: absolute; width: 220px; opacity: 0.15; left: -250px; transform: translateY(-50%); }
    @keyframes driveRight { 0% { transform: translateY(-50%) translateX(0); } 100% { transform: translateY(-50%) translateX(calc(100vw + 500px)); } }

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
    if "__LOFI_SCENE__" in css:
        css = css.replace('__LOFI_SCENE__', _lofi_image_uri('escena.png'))
        css = css.replace('__LOFI_YAWN__', _lofi_image_uri('bostezo.png'))
    return css

def countdown_js():
    """The classroom countdown, scoped to countdown slides only."""
    return r"""
        let activeCountdown = null;
        let lofiAudio, lofiMaster, lofiNoise, lofiScheduler, lofiNextBeat = 0, lofiBeatIndex = 0, lofiMusicOn = false;
        let lofiCitySource, lofiCityGain, lofiCityLfo;
        const lofiBeatSeconds = 60 / 76;
        const lofiChords = [
            [146.83, 174.61, 220.00, 261.63],
            [196.00, 246.94, 293.66, 349.23],
            [130.81, 164.81, 196.00, 246.94],
            [110.00, 130.81, 164.81, 196.00]
        ];
        const lofiPhrases = [
            { steps: [3, 7, 10, 14], notes: [2, 3, 1, 2] },
            { steps: [2, 6, 11, 15], notes: [1, 2, 3, 1] },
            { steps: [3, 8, 12], notes: [3, 2, 1] }
        ];
        function lofiRandom(n, salt) {
            let value = (Math.imul(n + 1, 1664525) + Math.imul(salt + 1, 1013904223)) >>> 0;
            value ^= value >>> 16;
            value = Math.imul(value, 2246822519) >>> 0;
            return value / 4294967296;
        }
        function lofiAmbienceMode() {
            return activeCountdown?.slide.querySelector('.lofi-ambience').value || 'none';
        }

        function lofiSetupAudio() {
            lofiAudio = new (window.AudioContext || window.webkitAudioContext)();
            lofiMaster = lofiAudio.createGain();
            lofiMaster.gain.value = .0001;
            const filter = lofiAudio.createBiquadFilter();
            filter.type = 'lowpass'; filter.frequency.value = 2200;
            lofiMaster.connect(filter); filter.connect(lofiAudio.destination);
            lofiNoise = lofiAudio.createBuffer(1, lofiAudio.sampleRate, lofiAudio.sampleRate);
            const samples = lofiNoise.getChannelData(0);
            for (let i = 0; i < samples.length; i++) samples[i] = Math.random() * 2 - 1;
        }
        function lofiTone(freq, time, length, volume, type = 'sine') {
            const oscillator = lofiAudio.createOscillator();
            const envelope = lofiAudio.createGain();
            oscillator.type = type; oscillator.frequency.setValueAtTime(freq, time);
            envelope.gain.setValueAtTime(.0001, time);
            envelope.gain.exponentialRampToValueAtTime(volume, time + .018);
            envelope.gain.exponentialRampToValueAtTime(.0001, time + length);
            oscillator.connect(envelope); envelope.connect(lofiMaster);
            oscillator.start(time); oscillator.stop(time + length + .04);
        }
        function lofiNoiseHit(time, length, volume, frequency) {
            const source = lofiAudio.createBufferSource(); source.buffer = lofiNoise;
            const filter = lofiAudio.createBiquadFilter(); filter.type = 'lowpass'; filter.frequency.value = frequency;
            const envelope = lofiAudio.createGain();
            envelope.gain.setValueAtTime(volume, time);
            envelope.gain.exponentialRampToValueAtTime(.0001, time + length);
            source.connect(filter); filter.connect(envelope); envelope.connect(lofiMaster);
            source.start(time); source.stop(time + length);
        }
        function lofiKeyClick(time, volume, offset) {
            const source = lofiAudio.createBufferSource(); source.buffer = lofiNoise;
            const highpass = lofiAudio.createBiquadFilter(); highpass.type = 'highpass'; highpass.frequency.value = 780;
            const envelope = lofiAudio.createGain();
            envelope.gain.setValueAtTime(.0001, time);
            envelope.gain.linearRampToValueAtTime(volume, time + .002);
            envelope.gain.exponentialRampToValueAtTime(.0001, time + .029);
            source.connect(highpass); highpass.connect(envelope); envelope.connect(lofiMaster);
            source.start(time, offset * .8); source.stop(time + .035);
        }
        function lofiStartCity() {
            if (lofiCitySource || !lofiAudio) return;
            const source = lofiAudio.createBufferSource(); source.buffer = lofiNoise; source.loop = true;
            const filter = lofiAudio.createBiquadFilter(); filter.type = 'lowpass'; filter.frequency.value = 320;
            const gain = lofiAudio.createGain();
            gain.gain.setValueAtTime(.0001, lofiAudio.currentTime);
            gain.gain.linearRampToValueAtTime(.07, lofiAudio.currentTime + 1.5);
            const lfo = lofiAudio.createOscillator(); lfo.frequency.value = .09;
            const lfoDepth = lofiAudio.createGain(); lfoDepth.gain.value = .012;
            lfo.connect(lfoDepth); lfoDepth.connect(gain.gain);
            source.connect(filter); filter.connect(gain); gain.connect(lofiMaster);
            source.start(); lfo.start();
            lofiCitySource = source; lofiCityGain = gain; lofiCityLfo = lfo;
        }
        function lofiStopCity() {
            if (!lofiCitySource) return;
            const now = lofiAudio.currentTime;
            lofiCityGain.gain.cancelScheduledValues(now);
            lofiCityGain.gain.setValueAtTime(lofiCityGain.gain.value, now);
            lofiCityGain.gain.linearRampToValueAtTime(.0001, now + .4);
            lofiCitySource.stop(now + .42);
            lofiCityLfo.stop(now + .42);
            lofiCitySource = null; lofiCityGain = null; lofiCityLfo = null;
        }
        function lofiTraffic(time, offset) {
            const source = lofiAudio.createBufferSource(); source.buffer = lofiNoise; source.loop = true;
            const filter = lofiAudio.createBiquadFilter(); filter.type = 'bandpass'; filter.Q.value = .55;
            filter.frequency.setValueAtTime(180, time);
            filter.frequency.linearRampToValueAtTime(340, time + .65);
            filter.frequency.linearRampToValueAtTime(170, time + 1.55);
            const envelope = lofiAudio.createGain();
            envelope.gain.setValueAtTime(.0001, time);
            envelope.gain.linearRampToValueAtTime(.035, time + .55);
            envelope.gain.linearRampToValueAtTime(.0001, time + 1.6);
            source.connect(filter); filter.connect(envelope); envelope.connect(lofiMaster);
            source.start(time, offset * .8); source.stop(time + 1.65);
        }
        function lofiBeat(n, time) {
            const step = n % 16;
            const chordIndex = Math.floor(n / 16);
            const chord = lofiChords[chordIndex % lofiChords.length];
            const phrase = lofiPhrases[(chordIndex + Math.floor(n / 64)) % lofiPhrases.length];
            const swing = step % 2 ? .035 : 0;
            if (step === 0 || step === 8) {
                lofiTone(62, time, .19, .34); lofiTone(41, time, .27, .16);
            }
            if (step === 4 || step === 12) lofiNoiseHit(time, .13, .072, 1400);
            if (step % 2 === 0) lofiNoiseHit(time, .038, .010 + lofiRandom(n, 2) * .004, 4200);
            if (step === 0) {
                const order = [[0, 1, 2, 3], [0, 2, 1, 3], [0, 1, 3, 2]][chordIndex % 3];
                order.forEach((pick, i) => lofiTone(chord[pick], time + i * .03, 2.6, i === 0 ? .07 : .039, 'triangle'));
                lofiTone(chord[0] / 2, time, 1.2, .105);
            }
            const melodicStep = phrase.steps.indexOf(step);
            if (melodicStep !== -1 && lofiRandom(n, 4) > .13) {
                lofiTone(chord[phrase.notes[melodicStep]] * 2, time + swing, .5,
                    .029 + lofiRandom(n, 5) * .012, 'triangle');
            }
            const mode = lofiAmbienceMode();
            if ((mode === 'both' || mode === 'city') && step === 8 && lofiRandom(n, 11) > .35) {
                lofiTraffic(time, lofiRandom(n, 12));
            }
            if ((mode === 'both' || mode === 'keyboard') && step % 2 === 0 && lofiRandom(n, 6) > .34) {
                lofiKeyClick(time + .13, .018 + lofiRandom(n, 7) * .008, lofiRandom(n, 8));
                if (lofiRandom(n, 9) > .53) lofiKeyClick(time + .20, .012, lofiRandom(n, 10));
            }
        }
        function lofiSchedule() {
            while (lofiNextBeat < lofiAudio.currentTime + .2) {
                lofiBeat(lofiBeatIndex++, lofiNextBeat);
                lofiNextBeat += lofiBeatSeconds;
            }
        }
        function lofiStopMusic() {
            if (!lofiMusicOn) return;
            lofiMusicOn = false;
            clearInterval(lofiScheduler);
            lofiStopCity();
            lofiMaster.gain.cancelScheduledValues(lofiAudio.currentTime);
            lofiMaster.gain.setValueAtTime(lofiMaster.gain.value, lofiAudio.currentTime);
            lofiMaster.gain.linearRampToValueAtTime(.0001, lofiAudio.currentTime + .4);
            if (activeCountdown) {
                const button = activeCountdown.slide.querySelector('.lofi-music');
                button.textContent = '♫ Música'; button.setAttribute('aria-pressed', 'false');
            }
        }
        async function lofiToggleMusic() {
            if (lofiMusicOn) { lofiStopMusic(); return; }
            try {
                if (!lofiAudio) lofiSetupAudio();
                await lofiAudio.resume();
                if (!activeCountdown) return;
                lofiMusicOn = true;
                lofiNextBeat = lofiAudio.currentTime + .04; lofiBeatIndex = 0;
                lofiMaster.gain.cancelScheduledValues(lofiAudio.currentTime);
                lofiMaster.gain.setValueAtTime(.0001, lofiAudio.currentTime);
                lofiMaster.gain.linearRampToValueAtTime(.42, lofiAudio.currentTime + 1.3);
                if (['both', 'city'].includes(lofiAmbienceMode())) lofiStartCity();
                lofiSchedule(); lofiScheduler = setInterval(lofiSchedule, 60);
                const button = activeCountdown.slide.querySelector('.lofi-music');
                button.textContent = '♫ Pausar'; button.setAttribute('aria-pressed', 'true');
            } catch (error) {
                const button = activeCountdown?.slide.querySelector('.lofi-music');
                if (button) { button.textContent = 'Audio no disponible'; button.disabled = true; }
                console.error('No se pudo iniciar el audio', error);
            }
        }
        function lofiRender(state) {
            const seconds = Math.ceil(Math.max(0, state.remaining) / 1000);
            state.slide.querySelector('.timer').textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
            const fraction = state.duration ? state.remaining / state.duration : 0;
            state.slide.querySelector('.lofi-progress').style.strokeDashoffset = String(628.319 * (1 - fraction));
            state.slide.querySelector('.lofi-status').textContent = state.finished ? '¡Comenzamos!' : state.running ? 'Iniciamos en breve' : state.remaining < state.duration ? 'En pausa' : 'Listo para empezar';
            state.slide.querySelector('.lofi-start').textContent = state.running ? 'Pausar' : state.finished ? 'Otra sesión' : state.remaining < state.duration ? 'Continuar' : 'Comenzar';
            state.slide.querySelector('.start-message').style.display = state.finished ? 'block' : 'none';
        }
        function lofiReset(state) {
            clearInterval(state.ticker); clearTimeout(state.advance);
            state.running = false; state.finished = false; state.remaining = state.duration;
            lofiRender(state);
        }
        function lofiTick(state) {
            state.remaining = Math.max(0, state.endsAt - Date.now());
            if (state.remaining === 0) {
                clearInterval(state.ticker);
                state.running = false; state.finished = true;
                state.advance = setTimeout(() => {
                    if (activeCountdown === state && currentSlide === state.index) nextSlide();
                }, 2000);
            }
            lofiRender(state);
        }
        function lofiStartPause(state) {
            if (state.running) {
                state.remaining = Math.max(0, state.endsAt - Date.now());
                clearInterval(state.ticker); state.running = false; lofiRender(state);
                return;
            }
            if (state.finished) lofiReset(state);
            state.endsAt = Date.now() + state.remaining;
            state.running = true; lofiTick(state);
            state.ticker = setInterval(() => lofiTick(state), 250);
        }
        function deactivateCountdown() {
            if (!activeCountdown) return;
            clearInterval(activeCountdown.ticker);
            clearTimeout(activeCountdown.advance);
            activeCountdown.running = false;
            lofiStopMusic();
            activeCountdown = null;
        }
        function activateCountdown(slide, index) {
            const seconds = Number(slide.dataset.timer);
            const duration = Number.isFinite(seconds) && seconds > 0 ? seconds * 1000 : 600000;
            let state = slide._lofiState;
            if (!state) {
                state = { slide, index, duration, remaining: duration, running: false, finished: false };
                slide._lofiState = state;
                const minutesInput = slide.querySelector('.lofi-minutes');
                minutesInput.value = String(duration / 60000);
                slide.querySelector('.lofi-start').addEventListener('click', () => lofiStartPause(state));
                slide.querySelector('.lofi-reset').addEventListener('click', () => lofiReset(state));
                slide.querySelector('.lofi-music').addEventListener('click', lofiToggleMusic);
                slide.querySelector('.lofi-ambience').addEventListener('change', () => {
                    if (!lofiMusicOn || activeCountdown !== state) return;
                    if (['both', 'city'].includes(lofiAmbienceMode())) lofiStartCity();
                    else lofiStopCity();
                });
                minutesInput.addEventListener('change', () => {
                    const minutes = Number(minutesInput.value);
                    if (!Number.isFinite(minutes) || minutes < .1 || minutes > 180) {
                        minutesInput.value = String(state.duration / 60000); return;
                    }
                    state.duration = Math.round(minutes * 60000);
                    slide.dataset.timer = String(state.duration / 1000);
                    slide.querySelector('.lofi-edit [name="minutes"]').value = String(minutes);
                    lofiReset(state);
                });
                const edit = slide.querySelector('.lofi-edit');
                edit.querySelector('[name="title"]').value = slide.querySelector('.lofi-title').textContent;
                edit.querySelector('[name="subtitle"]').value = slide.querySelector('.lofi-subtitle').textContent;
                edit.addEventListener('toggle', () => {
                    if (edit.open) edit.querySelector('[name="minutes"]').value = String(state.duration / 60000);
                });
                edit.querySelector('form').addEventListener('submit', event => {
                    event.preventDefault();
                    slide.querySelector('.lofi-title').textContent = edit.querySelector('[name="title"]').value.trim() || 'Webinar';
                    slide.querySelector('.lofi-subtitle').textContent = edit.querySelector('[name="subtitle"]').value.trim();
                    const value = Number(edit.querySelector('[name="minutes"]').value);
                    if (Number.isFinite(value) && value >= .1 && value <= 180) {
                        state.duration = Math.round(value * 60000);
                        minutesInput.value = String(value);
                        slide.dataset.timer = String(state.duration / 1000);
                    }
                    lofiReset(state);
                    edit.open = false;
                });
            }
            state.index = index;
            activeCountdown = state;
            slide.querySelector('.lofi-edit [name="minutes"]').value = String(state.duration / 60000);
            lofiReset(state);
            lofiStartPause(state);
        }
        document.addEventListener('visibilitychange', () => {
            if (activeCountdown?.running) lofiTick(activeCountdown);
        });
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
        {countdown_js()}

        function showSlide(index) {{
            if (isTransitioning || index === currentSlide) return;
            
            const nextSlideElement = slides[index];
            if (!nextSlideElement) return;

            isTransitioning = true;
            
            const transitionTitle = nextSlideElement.dataset.transitionTitle;

            if (currentSlide > -1) {{
                if (slides[currentSlide].dataset.type === 'countdown') deactivateCountdown();
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

            if (slideType === 'countdown') activateCountdown(slideElement, index);
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.target.closest('input, textarea, [contenteditable]')) return;
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
        state = None # 'question', 'options', 'feedback'
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
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    ambience = slide.get('params', {}).get('ambience', 'both')
    if ambience not in {'both', 'city', 'keyboard', 'none'}:
        raise ValueError(f"Ambiente inválido: {ambience!r}. Usa both, city, keyboard o none.")
    ambience_options = ''.join(
        f'<option value="{value}"{" selected" if value == ambience else ""}>{label}</option>'
        for value, label in (
            ('both', 'Ciudad y teclado'), ('city', 'Solo ciudad'),
            ('keyboard', 'Solo teclado'), ('none', 'Sin ambiente')
        )
    )
    content = html.escape(slide.get('content', ''))
    content_html = f'<p>{content}</p>' if content else ''
    return f"""
<div class="lofi-scene" aria-hidden="true"><div class="lofi-frame"><div class="lofi-layer lofi-base"></div><div class="lofi-layer lofi-head"></div><div class="lofi-layer lofi-paws"></div><div class="lofi-layer lofi-yawn"></div></div></div>
<div class="lofi-rain" aria-hidden="true"></div>
<details class="lofi-edit"><summary>Editar sesión</summary><form>
    <label>Título<input name="title" type="text" maxlength="100" required></label>
    <label>Subtítulo<input name="subtitle" type="text" maxlength="180"></label>
    <label>Duración en minutos<input name="minutes" type="number" min="0.1" max="180" step="0.1" required></label>
    <button type="submit">Aplicar cambios</button>
</form></details>
<div class="lofi-panel">
    <div class="lofi-kicker">Webinar</div>
    <h1 class="lofi-title">{title or 'Sesión de enfoque'}</h1>
    <h2 class="lofi-subtitle">{subtitle}</h2>
    <div class="lofi-dial" role="timer" aria-label="Tiempo restante">
        <svg viewBox="0 0 240 240" aria-hidden="true"><circle class="lofi-track" cx="120" cy="120" r="100"></circle><circle class="lofi-progress" cx="120" cy="120" r="100"></circle></svg>
        <div class="lofi-dial-copy"><span class="timer">--:--</span><span class="lofi-status" aria-live="polite">Listo para empezar</span></div>
    </div>
    <div class="start-message">¡Comenzamos!</div>
    <div class="lofi-controls"><button class="lofi-start" type="button">Comenzar</button><button class="lofi-reset" type="button">Reiniciar</button></div>
    <div class="lofi-tools"><label class="lofi-time-label">Duración <input class="lofi-minutes" type="number" min="0.1" max="180" step="0.1" aria-label="Duración en minutos"> min</label><button class="lofi-music" type="button" aria-pressed="false">♫ Música</button></div>
    <label class="lofi-ambience-row">Ambiente <select class="lofi-ambience" aria-label="Ambiente sonoro">{ambience_options}</select></label>
    {content_html}
</div>"""

def _generate_warnup_mood_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    emojis = [
    '😀', '😄', '😊', '😁', '🙂',        # positivo básico
    '🤔', '🧐', '😐', '🤨', '😶',        # reflexión / neutral
    '🚀', '🔥', '⚡', '🌟', '✨',        # energía / motivación
    '🤯', '😵', '😲', '😳',              # sorpresa / shock
    '😴', '🥱', '😪',                    # cansancio
    '💡', '🧠',                          # ideas / thinking
    '🎉', '🥳', '🙌',                    # celebración
    '💪', '🏋️',                         # esfuerzo / disciplina
    '😅', '😓',                          # estrés leve
    '😞', '😔', '😢',                    # bajón emocional
    '😤', '😠',                          # frustración
    '🤩', '😍'                           # entusiasmo alto
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
            try:
                timer_seconds = float(timer_duration)
                if not 6 <= timer_seconds <= 10800:
                    raise ValueError('El temporizador debe durar entre 6 segundos y 180 minutos')
            except ValueError as exc:
                raise ValueError(f'Temporizador inválido en la diapositiva {i+1}: {timer_duration!r}') from exc
            data_attributes += f' data-timer="{timer_seconds:g}"'
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
    parser = argparse.ArgumentParser(description='Generate HTML slides from a markdown file.')
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
