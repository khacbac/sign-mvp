# Pose Viewer

A Vite-based React TypeScript application for visualizing pose files (.pose format) from URLs using [react-pose-viewer](https://github.com/bipinkrish/react-pose-viewer).

## Features

- **Load .pose files** from URLs
- **Interactive playback controls**: Play, pause, loop
- **Adjustable playback speed**: 0.25x to 2x
- **URL parameter support**: Auto-load pose files via `?url=` parameter
- **Built with react-pose-viewer**: Professional pose file rendering

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173/`

### Build

```bash
npm run build
```

## Usage

### Load a Pose File

1. Enter a pose file URL in the input field (.pose format)
2. Click "Load Pose" or press Enter
3. Use the controls to adjust playback

### URL Parameter

You can load a pose file directly by adding a `url` parameter:

```
http://localhost:5173/?url=http://localhost:8000/text-to-pose?text=hello
```

### Controls

- **Autoplay**: Start playing automatically when loaded
- **Loop**: Repeat the animation continuously
- **Playback Speed**: Adjust from 0.25x to 2x speed

## Integration with text-to-skeleton

This viewer works with the `/text-to-pose` endpoint from the sign-mvp project:

```
http://localhost:5173/?url=http://localhost:8000/text-to-pose?text=hello%20world
```

Note: The endpoint should return a `.pose` file, not JSON.

## Technologies

- **Vite**: Fast build tool and dev server
- **React**: UI framework
- **TypeScript**: Type-safe JavaScript
- **react-pose-viewer**: Professional .pose file viewer component
