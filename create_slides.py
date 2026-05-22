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
    return """
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

    .slide-countdown { background-color: var(--color-orange); color: var(--color-black); }
    .slide-countdown h2 { color: var(--color-dark-gray-2); }
    .slide-countdown .timer { font-size: 5rem; font-weight: 300; letter-spacing: 5px; margin: 1.5rem 0; text-shadow: 0 0 10px rgba(0,0,0,0.1); }
    .slide-countdown .start-message { font-size: 2.5rem; font-weight: 700; display: none; }
    
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
                const timerElement = slideElement.querySelector('.timer');
                const startMessage = slideElement.querySelector('.start-message');
                let duration = parseInt(slideElement.dataset.timer || '600', 10);

                slideIntervals[index] = setInterval(() => {{
                    if (duration < 0) {{
                        clearInterval(slideIntervals[index]);
                        timerElement.style.display = 'none';
                        startMessage.style.display = 'block';
                        setTimeout(nextSlide, 2000); 
                        return;
                    }}
                    const minutes = Math.floor(duration / 60);
                    const seconds = duration % 60;
                    timerElement.textContent = `${{String(minutes).padStart(2, '0')}}:${{String(seconds).padStart(2, '0')}}`;
                    duration--;
                }}, 1000);
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
    logo_animation = slide.get('params', {}).get('logo_animation', 'dvd')
    bg_html = ""
    
    if logo_animation == 'traffic':
        logo_src = "https://logoimg.careerjet.net/2f2f984040414fbcf1747ea52b99ee70.png"
        logos = []
        rows = [15, 35, 55, 75]
        for row_top in rows:
            duration = random.uniform(20, 35)
            num_cars = random.randint(3, 5)
            for i in range(num_cars):
                delay = - (duration / num_cars) * i
                logos.append(f'<img class="traffic-logo-img" src="{logo_src}" style="top: {row_top}%; animation: driveRight {duration:.2f}s linear {delay:.2f}s infinite;">')
        bg_html = f'<div class="traffic-logo-container">{"".join(logos)}</div>'
    else:
        bg_html = f'<div class="bouncing-logo-container"><img class="bouncing-logo" src="https://logoimg.careerjet.net/2f2f984040414fbcf1747ea52b99ee70.png" alt="Bouncing Logo"></div>'

    return f"""{bg_html}<div class="content-wrapper"><h1>{title}</h1><h2>{subtitle}</h2><div class="timer">--:--</div><div class="start-message">¡Comenzamos!</div><p>{html.escape(slide.get('content', ''))}</p></div><div class="dynamic-date" style="position: absolute; bottom: 30px; left: 40px; font-size: 1.5rem; font-weight: bold; color: var(--color-black); z-index: 1;"></div>"""

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
