# FastHTML with TailwindCSS and DaisyUI

A modern dashboard application built with FastHTML, TailwindCSS, and DaisyUI.

## Prerequisites

- Python 3.7+
- Node.js and npm

## Setup

1. Install Python dependencies:

```bash
pip install python_fasthtml
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

- Modern UI with TailwindCSS utility classes
- Beautiful components with DaisyUI
- Responsive design
- Class-based architecture for better organization

## Project Structure

- `main.py` - The main FastHTML application
- `src/app.css` - Source CSS file for Tailwind
- `public/app.css` - Generated CSS file (after running the build)
- `tailwind.config.js` - Tailwind CSS configuration
- `package.json` - Node.js dependencies and scripts 