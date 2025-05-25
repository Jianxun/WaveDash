# Product Requirements Document: WaveDash - MVP

## 1. Introduction

### 1.1. Overview
WaveDash is a modern, web-based dashboard designed for visualizing simulation data from SPICE/Ngspice ".raw" files. This tool aims to replace aging desktop applications (e.g., GTKWave, GWave) by offering a significantly improved user experience, enhanced interactivity, and easier sharing of results within a browser-based environment.

### 1.2. Problem Statement
Electrical engineers and circuit designers often rely on outdated, platform-specific, and cumbersome tools to view and analyze SPICE simulation waveforms. These tools typically lack modern UI conveniences, make sharing results difficult (often relying on screenshots), and don't integrate well with contemporary workflows that might involve web-based documentation (like Obsidian) or AI-assisted coding and analysis.

### 1.3. Vision
To provide an intuitive, performant, and extensible web-based waveform viewer that seamlessly integrates into modern engineering workflows, facilitating rapid analysis, iteration, and collaboration.

## 2. Goals and Objectives (MVP)

*   **Validate Core Functionality:** Prove the ability to load, parse, and display SPICE `.raw` file data in a web browser.
*   **Test Basic User Interface Ergonomics:** Evaluate the usability of a sidebar for signal selection and a tiled canvas for waveform display using a click-to-select and plot-to-active-tile interaction model.
*   **Establish Technical Foundation:** Build the initial application structure using Python, Dash, Plotly, and `spicelib` that can be expanded upon for future features.
*   **Gather Early Feedback:** Create a functional prototype to gather user feedback on the core interaction model and identify key areas for improvement.

## 3. Target Audience

*   Electrical Engineers
*   Circuit Designers
*   Students and Hobbyists working with SPICE simulations
*   Users who prefer web-based tools and Python-centric workflows.

## 4. Proposed Solution & Features (MVP)

The MVP will deliver a web application with the following key features:

### 4.1. Project Setup & Basic Structure
*   A Python-based Dash web application.
*   Basic layout: Header, Sidebar for controls and signal listing, Main Content area for plot tiles.
*   Internal data stores (`dcc.Store`) for managing:
    *   Parsed simulation data.
    *   List of available signals.
    *   Configuration of which signal is plotted on which tile.
    *   Currently selected signal.
    *   Currently active plot tile.

### 4.2. File Upload and Parsing
*   **F1: `.raw` File Upload:** Users can upload a SPICE `.raw` file via a file dialog in the sidebar.
*   **F2: Data Parsing:** The uploaded file is parsed using `spicelib`.
*   **F3: Data Extraction & Storage:** Traces and sweeps are extracted and stored, primarily in a Pandas DataFrame (or similar structure) in `parsed-data-store`. Signal names are extracted and stored in `signal-list-store`.

### 4.3. Sidebar: Signal Selection & Plot Action
*   **F4: Signal List Display:** Available signals (from `signal-list-store`) are displayed as a list of clickable items in the sidebar.
*   **F5: Signal Selection:** Users can click on a signal name in the list to mark it as the "currently selected signal" (state stored in `selected-signal-store`).
*   **F6: Plot Action Button:** A button labeled "Plot to Active Tile" is available in the sidebar.

### 4.4. Main Canvas: Plot Tiles & Active Tile Selection
*   **F7: Plot Tile Display:** The main canvas displays 2-4 plot "tiles" (using `dcc.Graph`). Each tile is a potential target for displaying a waveform.
*   **F8: Active Tile Selection:** Users can click on a plot tile to mark it as the "active tile" (state stored in `active-tile-store`).
*   **F9: Plotting Logic:**
    *   When the "Plot to Active Tile" button is clicked, the application reads the `selected-signal-store` and `active-tile-store`.
    *   The `tile-config-store` is updated to map the selected signal to the active tile.
    *   The active tile's `dcc.Graph` component updates its figure by:
        *   Retrieving the corresponding signal data from `parsed-data-store`.
        *   Generating a Plotly line chart (e.g., `go.Scattergl`) of the signal against its sweep variable (e.g., time).
        *   Displaying the chart. If no signal is assigned, a placeholder is shown.

### 4.5. Initial Styling and Ergonomics
*   **F10: Basic Layout Styling:** Clean and functional CSS for sidebar and tile arrangement.
*   **F11: Visual Cues:**
    *   The currently selected signal in the sidebar list is visually highlighted.
    *   The currently active plot tile on the main canvas is visually highlighted (e.g., with a distinct border).

## 5. Design Considerations (MVP)

*   **Simplicity:** The UI should be clean and uncluttered, focusing on the core MVP features.
*   **Responsiveness (Basic):** The application should be usable on typical desktop screen sizes. Full mobile responsiveness is not an MVP goal.
*   **Clarity:** Visual cues for selected items (signal, tile) should be clear to the user.
*   **Performance:** For the MVP, performance with small to medium-sized `.raw` files (e.g., up to a few megabytes, a few dozen signals, tens of thousands of data points per signal) should be acceptable. `go.Scattergl` will be preferred for plotting.

## 6. Success Metrics (MVP)

*   **Successful File Load & Parse:** 95% success rate for loading and parsing valid `.raw` files of common Ngspice/SPICE3f5 formats (with a small, representative test set of files).
*   **Core Plotting Functionality:** Users can successfully select a signal, select a tile, and plot the signal on that tile.
*   **Basic Usability:** Qualitative feedback from at least one target user indicating that the basic workflow is understandable and usable.
*   **Completion of MVP Tasks:** All tasks listed in the "Current Sprint (MVP Features)" section of `context/todo.md` are completed.

## 7. Out of Scope / Future Considerations (Post-MVP)

The following features are explicitly out of scope for the MVP but are planned for future iterations (refer to `context/todo.md` backlog):

*   Drag-and-drop interface for plotting signals
*   Advanced hierarchical display for signals (tree view)
*   Zoom/pan synchronization across multiple plot tiles
*   Interactive delta cursors and readouts
*   Math/derived traces functionality (e.g., `V(a) - V(b)`)
*   FFT & spectrum display
*   Advanced handling and optimizations for very large files (e.g., >100MB, millions of data points)
*   Session save/share (export to standalone HTML, server-side session state)
*   User configuration management (e.g., plot preferences)
*   Real-time/streaming data support from live simulations
*   Comprehensive automated testing (unit, E2E, performance tests)
*   Detailed user documentation

## 8. Technical Considerations

*   **Backend:** Python, Dash (with Flask)
*   **Frontend:** Dash (HTML, CSS, JavaScript components), Plotly.js
*   **Data Parsing:** `spicelib`
*   **Data Manipulation:** Pandas
*   **Version Control:** Git
*   **Development Environment:** Python virtual environment

---
This document will be updated as the project progresses and requirements evolve. 