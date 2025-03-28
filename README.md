# Teambee Website

A modern, responsive website for Teambee built with FastHTML and TailwindCSS. The website helps premium fitness clubs transform members into loyal ambassadors through personalized attention.

## Prerequisites

- Python 3.7+
- Node.js and npm

## Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Build the CSS:

```bash
npm run build
```

## Development

1. Start the Tailwind CSS watcher:

```bash
npm run dev
```

2. In a separate terminal, run the FastHTML application:

```bash
python main.py
```

3. Open your browser and navigate to `http://localhost:8000`

## Features

- Modern, responsive UI with TailwindCSS
- Interactive elements with hover effects
- Optimized for performance with versioned static assets
- Class-based architecture with modular components
- Accessibility-focused design with proper ARIA attributes

## Project Structure

- `main.py` - The main Teambee application class with website components
- `login_form.py` - Login form component
- `src/app.css` - Source CSS file for Tailwind
- `public/app.css` - Generated CSS file (after running the build)
- `tailwind.config.js` - Tailwind CSS configuration
- `package.json` - Node.js dependencies and scripts
- `public/static/assets` - Images and SVG icons
- `public/static/js` - JavaScript files for interactive features 