# Project Memory

## Project Overview
The project aims to build a modern, web-based dashboard for visualizing simulation data from SPICE/Ngspice ".raw" files (Project "WaveDash"). This tool will replace older desktop applications like GTKWave, offering a browser-based UI, Plotly/Dash interactivity, and shareable HTML exports. The backend will be Python, leveraging libraries like `spicelib` for parsing and `numpy/pandas` for data manipulation.

## Current State
The project is ready to begin MVP implementation. Python development environment is set up with virtual environment, all dependencies installed (dash, plotly, pandas, spicelib, pytest), and requirements.txt created. Sample raw data files are available for testing (66 traces, 2,228 data points).

## Key Decisions
- Build a new application (WaveDash) using Python, Dash, and Plotly.
- Leverage `spicelib` for parsing `.raw` files.
- Adopt a phased development approach, starting with an MVP as defined in `WaveDash_MVP_PRD.md`.
- **MVP Interaction Model**: Implement a click-to-select signal, click-to-select active plot tile, and a button-to-plot mechanism, deferring drag-and-drop functionality.
- Key MVP features include: `.raw` file upload and parsing, display of available signals, and plotting selected signals to user-selected tiles on a dashboard.

## Architectural Decisions (MVP)
- **Data Storage**: Pandas DataFrame with time as index, signals as columns
- **Plot Tiles**: 4 fixed tiles arranged vertically to test scrolling behavior
- **Error Handling**: Minimal for MVP - focus on core functionality
- **Performance**: No decimation needed for small datasets
- **UI/UX**: Use common practices for layout and browser compatibility
- **Project Structure**: Modular architecture with separate components, callbacks, and data modules
- **Data Stores**: Use dcc.Store for parsed-data, signal-list, selected-signal, active-tile, and tile-config
- **Plotting**: Use go.Scattergl for performance

## Open Questions (Post-MVP Focus)
- What are the specific performance requirements and optimization strategies for "huge-file handling"?
- How will user configurations (e.g., plot preferences, themes) be managed?
- Is real-time/streaming data from `libngspice` a requirement for future versions, and what would be the technical approach?
- What is the detailed long-term testing strategy (e.g., E2E, performance benchmarks, automated visual regression)?
- What is the planned deployment strategy for wider use (e.g., Docker, PaaS)?
- How will advanced features like math traces, FFT, and synchronized zoom/pan be integrated architecturally?
- What level of extensibility (e.g., plugin system for custom math operations or plot types) is desired? 