from fasthtml.common import *
from fasthtml.components import NotStr

def social_icons():
    """Return a social icons component with hover effects."""
    return Div(
        # Twitter
        A(
            NotStr('''<svg width="1em" height="1em" class="w-6 h-6 text-gray-600 group-hover:text-white transition-colors duration-300">
                <path fill="currentColor" d="M22.46 6c-.77.35-1.6.58-2.46.69c.88-.53 1.56-1.37 1.88-2.38c-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29c0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15c0 1.49.75 2.81 1.91 3.56c-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.2 4.2 0 0 1-1.93.07a4.28 4.28 0 0 0 4 2.98a8.52 8.52 0 0 1-5.33 1.84q-.51 0-1.02-.06C3.44 20.29 5.7 21 8.12 21C16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56c.84-.6 1.56-1.36 2.14-2.23"></path>
            </svg>'''),
            href="https://twitter.com/bitdoze",
            cls="group inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100 hover:bg-blue-500 transition-all duration-300 hover:scale-110",
            **{"aria-label": "Twitter"}
        ),
        # Bluesky
        A(
            NotStr('''<svg class="w-6 h-6 text-gray-600 group-hover:text-white transition-colors duration-300" viewBox="0 0 512 512" fill="currentColor">
                <path d="M111.8 62.2C170.2 105.9 233 194.7 256 242.4c23-47.6 85.8-136.4 144.2-180.2c42.1-31.6 110.3-56 110.3 21.8c0 15.5-8.9 130.5-14.1 149.2C478.2 298 412 314.6 353.1 304.5c102.9 17.5 129.1 75.5 72.5 133.5c-107.4 110.2-154.3-27.6-166.3-62.9l0 0c-1.7-4.9-2.6-7.8-3.3-7.8s-1.6 3-3.3 7.8l0 0c-12 35.3-59 173.1-166.3 62.9c-56.5-58-30.4-116 72.5-133.5C100 314.6 33.8 298 15.7 233.1C10.4 214.4 1.5 99.4 1.5 83.9c0-77.8 68.2-53.4 110.3-21.8z"></path>
            </svg>'''),
            href="https://bsky.app/profile/bitdoze.com",
            cls="group inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100 hover:bg-sky-500 transition-all duration-300 hover:scale-110",
            **{"aria-label": "Bluesky"}
        ),
        # YouTube
        A(
            NotStr('''<svg width="1em" height="1em" class="w-6 h-6 text-gray-600 group-hover:text-white transition-colors duration-300">
                <path fill="currentColor" d="m10 15l5.19-3L10 9zm11.56-7.83c.13.47.22 1.1.28 1.9c.07.8.1 1.49.1 2.09L22 12c0 2.19-.16 3.8-.44 4.83c-.25.9-.83 1.48-1.73 1.73c-.47.13-1.33.22-2.65.28c-1.3.07-2.49.1-3.59.1L12 19c-4.19 0-6.8-.16-7.83-.44c-.9-.25-1.48-.83-1.73-1.73c-.13-.47-.22-1.1-.28-1.9c-.07-.8-.1-1.49-.1-2.09L2 12c0-2.19.16-3.8.44-4.83c.25-.9.83-1.48 1.73-1.73c.47-.13 1.33-.22 2.65-.28c1.3-.07 2.49-.1 3.59-.1L12 5c4.19 0 6.8.16 7.83.44c.9.25 1.48.83 1.73 1.73"></path>
            </svg>'''),
            href="https://www.youtube.com/channel/UCGsUtKhXsRrMvYAWm8q0bCg",
            cls="group inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100 hover:bg-red-500 transition-all duration-300 hover:scale-110",
            **{"aria-label": "YouTube"}
        ),
        # GitHub
        A(
            NotStr('''<svg width="1em" height="1em" class="w-6 h-6 text-gray-600 group-hover:text-white transition-colors duration-300">
                <path fill="currentColor" d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5c.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34c-.46-1.16-1.11-1.47-1.11-1.47c-.91-.62.07-.6.07-.6c1 .07 1.53 1.03 1.53 1.03c.87 1.52 2.34 1.07 2.91.83c.09-.65.35-1.09.63-1.34c-2.22-.25-4.55-1.11-4.55-4.92c0-1.11.38-2 1.03-2.71c-.1-.25-.45-1.29.1-2.64c0 0 .84-.27 2.75 1.02c.79-.22 1.65-.33 2.5-.33s1.71.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02c.55 1.35.2 2.39.1 2.64c.65.71 1.03 1.6 1.03 2.71c0 3.82-2.34 4.66-4.57 4.91c.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2"></path>
            </svg>'''),
            href="https://github.com/bitdoze",
            cls="group inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-800 transition-all duration-300 hover:scale-110",
            **{"aria-label": "GitHub"}
        ),
        cls="flex justify-center gap-4"
    )