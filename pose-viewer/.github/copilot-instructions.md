# Pose Viewer - Vite React TypeScript App

## Project Overview
A Vite-based React TypeScript application for visualizing pose/skeleton animation data from URLs.

## Progress Checklist

- [x] Create copilot-instructions.md file
- [x] Clarify project requirements - Vite + React + TypeScript pose viewer
- [x] Scaffold Vite React TypeScript project
- [x] Customize project for pose viewer functionality
- [x] Install dependencies and compile
- [x] Create and run dev task
- [x] Update documentation

## Project Status: ✅ COMPLETE

The pose viewer application is fully functional and running at `http://localhost:5173/`

## Project Requirements
- **Framework**: Vite + React + TypeScript
- **Purpose**: Display pose files (.pose format) from URL
- **Library**: react-pose-viewer for professional pose rendering
- **Features**:
  - ✅ Load .pose files from URL
  - ✅ Interactive playback controls (autoplay, loop)
  - ✅ Adjustable playback speed (0.25x - 2x)
  - ✅ URL parameter support for auto-loading

## Components Created

### Core Components
- `App.tsx` - Main application component with PoseViewer integration
- Uses `react-pose-viewer` library for rendering .pose files

### Removed Components
- Previous custom canvas-based components replaced with react-pose-viewer

## Usage

### Development Server
```bash
npm run dev
```
Server runs at: http://localhost:5173/

### Load Pose Data
1. Enter pose JSON URL in the input field
2. Click "Load Pose" or press Enter
3. Use controls to play/pause and navigate

### Example URLs
```
http://localhost:5173/?url=http://localhost:8000/text-to-skeleton?text=hello
```

## Development Notes
- Using current directory (pose-viewer) as project root
- Vite for fast development and HMR
- Canvas-based rendering for skeleton visualization
- TypeScript strict mode enabled
- All compilation errors resolved
- Dev server running successfully

