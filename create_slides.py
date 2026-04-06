import re
import argparse
import html
import random
import os
import markdown

def parse_markdown(content):
    """
    Parses the entire markdown content and splits it into slide objects.
    """
    slides_content = content.strip().split('---')
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
    .slide-basic_slide .content-wrapper, .slide-two_columns_slide .content-wrapper { width: 90%; text-align: left; overflow-y: auto; max-height: 85vh; padding: 2rem 3rem; }
    .slide-basic_slide .content-wrapper img, .slide-two_columns_slide .content-wrapper img { max-width: 100%; border-radius: 10px; display: block; margin: 1rem auto; padding: 0; }
    .slide-basic_slide .content-wrapper p, .slide-basic_slide .content-wrapper ul, .slide-basic_slide .content-wrapper ol, .slide-two_columns_slide .content-wrapper p, .slide-two_columns_slide .content-wrapper ul, .slide-two_columns_slide .content-wrapper ol { font-size: 1.5rem; line-height: 1.6; }
    .slide-basic_slide .content-wrapper ul, .slide-basic_slide .content-wrapper ol, .slide-two_columns_slide .content-wrapper ul, .slide-two_columns_slide .content-wrapper ol { padding-left: 3rem; }
    
    .slide-two_columns_slide .column-left { padding-right: 2rem; width: 50%; display: flex; flex-direction: column; justify-content: center; }
    .slide-two_columns_slide .column-right { width: 50%; display: flex; align-items: center; justify-content: center; height: 100%; }
    .slide-two_columns_slide .column-right img { width: 100%; max-height: 70vh; object-fit: contain; }
    .slide-agenda h1 { color: var(--color-black); }
    .slide-agenda ul { list-style: none; padding: 0; font-size: 1.5rem; }
    .slide-agenda li { margin: 0.5rem 0; }
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
    #transition-overlay h1 { color: var(--color-black); }
    #transition-overlay.visible { opacity: 1; visibility: visible; }
    
    .slide-nav { position: absolute; bottom: 20px; right: 20px; z-index: 100; display: flex; gap: 10px; }
    .slide-nav button { background: rgba(128, 128, 128, 0.5); border: none; color: white; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1.5rem; transition: background 0.3s; }
    .slide-nav button:hover { background: rgba(128, 128, 128, 0.9); }
    
    .company-logo { position: absolute; top: 30px; left: 40px; max-height: 60px; opacity: 0; z-index: 50; pointer-events: none; }
    .slide-countdown .company-logo, .slide-warnup-mood .company-logo, .slide-finale .company-logo, .slide-overlay .company-logo { display: none !important; animation: none !important; }
    .slide.active .company-logo { animation: showAndHideLogo 4s ease-in-out forwards; }
    @keyframes showAndHideLogo {
        0% { opacity: 0; transform: translateY(-10px); }
        10% { opacity: 1; transform: translateY(0); }
        80% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-10px); }
    }
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
        if (prevBtn) prevBtn.addEventListener('click', prevSlide);
        if (nextBtn) nextBtn.addEventListener('click', nextSlide);

        if (slides.length > 0) {{
            showSlide(0);
        }}
    }});
</script>
"""

def _generate_countdown_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    return f"""<div class="content-wrapper"><h1>{title}</h1><h2>{subtitle}</h2><div class="timer">--:--</div><div class="start-message">¡Comenzamos!</div><p>{html.escape(slide.get('content', ''))}</p></div><div class="dynamic-date" style="position: absolute; bottom: 30px; left: 40px; font-size: 1.5rem; font-weight: bold; color: var(--color-black);"></div>"""

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
    content_html = markdown.markdown(content)
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
    content_html = markdown.markdown(content)
    return f"""<div style="width: 80%; max-width: 1200px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">{title_html}{subtitle_html}{content_html}</div>"""

def _generate_basic_slide_html(slide):
    title = html.escape(slide.get('title', ''))
    subtitle = html.escape(slide.get('subtitle', ''))
    title_html = f"<h1>{title}</h1>" if title else ""
    subtitle_html = f"<h2>{subtitle}</h2>" if subtitle else ""
    content_html = markdown.markdown(slide.get('content', ''))
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
    
    left_html = markdown.markdown(left_content)
    right_html = markdown.markdown(right_content)
    
    return f"""<div class="content-wrapper">{title_html}{subtitle_html}<div class="two-column-layout" style="align-items: stretch; margin-top: 1rem;"><div class="column-left">{left_html}</div><div class="column-right">{right_html}</div></div></div>"""

def generate_slide_html(slide):
    logo_html = '<img src="https://logoimg.careerjet.net/2f2f984040414fbcf1747ea52b99ee70.png" class="company-logo" alt="Logo">\n'
    generator_map = {
        'countdown': _generate_countdown_html, 'warnup-mood': _generate_warnup_mood_html,
        'warnup-question': _generate_warnup_question_html, 'agenda': _generate_agenda_html,
        'objectives': _generate_objectives_html, 'gotocode': _generate_gotocode_html,
        'finale': _generate_finale_html, 'basic_slide': _generate_basic_slide_html,
        'two_columns_slide': _generate_two_columns_html, 'overlay': _generate_overlay_html,
    }
    generator_func = generator_map.get(slide.get('type', 'unknown'))
    if generator_func:
        return logo_html + generator_func(slide)
    return logo_html + f"<h1>{html.escape(slide.get('title', ''))}</h1><h2>{html.escape(slide.get('subtitle', ''))}</h2><p>{html.escape(slide.get('content', ''))}</p>"

def generate_html(slides):
    css = generate_css()
    js = generate_js(slides)
    slides_html = ""
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
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentación</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
    {css}
</head>
<body>
    <div class="presentation">
        <div id="transition-overlay"><div class="content-wrapper"><h1></h1></div></div>
        {slides_html}
        <div class="slide-nav">
            <button id="prev-btn" title="Anterior (Flecha Izquierda)">&#8592;</button>
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
    slides = parse_markdown(markdown_content)
    html_output = generate_html(slides)
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Successfully generated slides in '{args.output_file}'")

if __name__ == '__main__':
    main()
