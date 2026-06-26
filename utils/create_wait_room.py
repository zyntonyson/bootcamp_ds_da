import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="Genera una sala de espera HTML con un video de fondo en bucle infinito, "
                    "efecto de desenfoque y cuenta regresiva sobre un contenedor con efecto 'vidrio mojado'."
    )
    parser.add_argument(
        "--source-video",
        required=True,
        help="Ruta local o URL del video MP4 de fondo."
    )
    parser.add_argument(
        "--time",
        type=int,
        required=True,
        help="Duración de la cuenta regresiva en segundos."
    )
    parser.add_argument(
        "--output-file",
        default="wait_room.html",
        help="Nombre del archivo HTML generado (por defecto: wait_room.html)."
    )

    args = parser.parse_args()

    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sala de Espera</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <!-- Cargamos una fuente moderna, grande y gorda (Outfit con peso 800 y 900) -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@800;900&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #0d0e15;
            font-family: 'Outfit', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        /* Contenedor del video de fondo a pantalla completa */
        .video-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            overflow: hidden;
        }
        
        .video-background video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            /* Efecto de desenfoque y oscurecimiento para dar contraste */
            filter: blur(5px) brightness(0.55) contrast(1.05);
            transform: scale(1.03); /* Evita bordes blancos por el desenfoque */
        }
        
        /* Contenedor principal con efecto "vidrio mojado" (Wet Glassmorphism) */
        .glass-container {
            background: rgba(255, 255, 255, 0.01); /* Máxima transparencia de base */
            backdrop-filter: blur(12px) saturate(180%); /* Desenfoque reducido para ver el fondo */
            -webkit-backdrop-filter: blur(12px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 1.5px solid rgba(255, 255, 255, 0.2);
            border-left: 1.5px solid rgba(255, 255, 255, 0.2);
            border-radius: 36px;
            padding: 4rem 6rem;
            text-align: center;
            /* Sombras optimizadas para resaltar la transparencia */
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3),
                        inset 0 0 80px rgba(255, 255, 255, 0.02);
            max-width: 90%;
            width: 580px;
            position: relative;
            z-index: 10;
            /* Efecto de flotación sutil */
            animation: float 6s ease-in-out infinite;
        }
        
        /* Reflejo superior brillante que simula el vidrio húmedo/pulido */
        .glass-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 50%;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0) 100%);
            border-radius: 36px 36px 0 0;
            pointer-events: none;
        }
        
        /* Letras Grandes y Gordas */
        .title {
            font-size: 2.2rem;
            font-weight: 800;
            color: rgba(255, 255, 255, 0.95);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 1.2rem;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }
        
        /* Cuenta Regresiva Gigante */
        .countdown {
            font-size: 8rem;
            font-weight: 900;
            margin: 0;
            line-height: 1;
            /* Gradiente de color blanco y gris plata premium */
            background: linear-gradient(180deg, #ffffff 40%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
            letter-spacing: -0.03em;
        }
        
        /* Animación de flotación */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        /* Responsivo simple */
        @media (max-width: 600px) {
            .glass-container {
                padding: 3rem 2rem;
            }
            .title {
                font-size: 1.6rem;
            }
            .countdown {
                font-size: 5rem;
            }
        }
        
        /* Botón de Audio Flotante */
        .audio-btn {
            position: absolute;
            top: 24px;
            right: 24px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: white;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 100;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        
        .audio-btn:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: scale(1.05);
        }
        
        .audio-btn svg {
            width: 22px;
            height: 22px;
        }
    </style>
</head>
<body>

    <!-- Video de fondo en bucle infinito -->
    <div class="video-background">
        <video autoplay loop muted playsinline>
            <source src="__SOURCE_VIDEO__" type="video/mp4">
            Tu navegador no soporta videos HTML5.
        </video>
    </div>

    <!-- Botón flotante para activar/desactivar audio -->
    <button id="unmute-btn" class="audio-btn" title="Activar/Silenciar Audio">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.063.922-2.063 2.063v4.874c0 1.141.922 2.063 2.063 2.063h1.932l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06zM17.78 9.22a.75.75 0 10-1.06 1.06L18.44 12l-1.72 1.72a.75.75 0 001.06 1.06l1.72-1.72 1.72 1.72a.75.75 0 101.06-1.06L20.56 12l1.72-1.72a.75.75 0 00-1.06-1.06l-1.72 1.72-1.72-1.72z" />
        </svg>
    </button>

    <!-- Contenedor efecto vidrio mojado -->
    <div class="glass-container">
        <div class="title" id="message">Continuamos en</div>
        <div class="countdown" id="timer">--:--</div>
    </div>

    <script>
        let timeLeft = __TIME_SECONDS__;
        const timerElement = document.getElementById('timer');
        const messageElement = document.getElementById('message');

        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }

        function updateTimer() {
            if (timeLeft <= 0) {
                timerElement.innerText = "00:00";
                messageElement.innerText = "¡Comenzamos!";
                clearInterval(interval);
                return;
            }
            timerElement.innerText = formatTime(timeLeft);
            timeLeft--;
        }

        // Ejecutar inmediatamente al cargar la página
        updateTimer();
        const interval = setInterval(updateTimer, 1000);

        // Forzar reproducción del video en caso de restricciones de autoplay del navegador
        document.addEventListener("DOMContentLoaded", () => {
            const video = document.querySelector(".video-background video");
            if (video) {
                video.play().catch(error => {
                    console.log("El navegador bloqueó el autoplay del video:", error);
                });
            }
        });

        // Controlar el volumen / unmute
        const unmuteBtn = document.getElementById("unmute-btn");
        unmuteBtn.addEventListener("click", () => {
            const video = document.querySelector(".video-background video");
            if (video) {
                if (video.muted) {
                    video.muted = false;
                    unmuteBtn.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.063.922-2.063 2.063v4.874c0 1.141.922 2.063 2.063 2.063h1.932l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06zM18.563 12c0-2.183-1.374-4.05-3.313-4.785a.75.75 0 00-.5 1.414 3.5 3.5 0 010 6.742.75.75 0 00.5 1.414c1.939-.735 3.313-2.602 3.313-4.785z" />
                            <path d="M20.188 12c0-3.83-2.433-7.098-5.813-8.307a.75.75 0 00-.5 1.414c2.81 1.005 4.813 3.69 4.813 6.893s-2.003 5.888-4.813 6.893a.75.75 0 10.5 1.414c3.38-1.209 5.813-4.477 5.813-8.307z" />
                        </svg>
                    `;
                } else {
                    video.muted = true;
                    unmuteBtn.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.063.922-2.063 2.063v4.874c0 1.141.922 2.063 2.063 2.063h1.932l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06zM17.78 9.22a.75.75 0 10-1.06 1.06L18.44 12l-1.72 1.72a.75.75 0 001.06 1.06l1.72-1.72 1.72 1.72a.75.75 0 101.06-1.06L20.56 12l1.72-1.72a.75.75 0 00-1.06-1.06l-1.72 1.72-1.72-1.72z" />
                        </svg>
                    `;
                }
            }
        });
    </script>
</body>
</html>
"""

    # Determinamos la ruta del video: si es local, la calculamos relativa al archivo HTML
    video_src = args.source_video
    if not (video_src.startswith("http://") or video_src.startswith("https://") or video_src.startswith("//")):
        abs_video = os.path.abspath(video_src)
        abs_output = os.path.abspath(args.output_file)
        output_dir = os.path.dirname(abs_output)
        rel_video = os.path.relpath(abs_video, output_dir)
        video_src = rel_video.replace("\\", "/")

    # Realizamos los reemplazos
    output_html = html_template.replace("__SOURCE_VIDEO__", video_src)
    output_html = output_html.replace("__TIME_SECONDS__", str(args.time))

    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output_html)
        print(f"¡Éxito! HTML generado correctamente en: {args.output_file}")
    except Exception as e:
        print(f"Error al escribir el archivo de salida: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
