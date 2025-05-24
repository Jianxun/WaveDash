# Project Memory

## Project Overview
The project aims to build a modern, web-based dashboard for visualizing simulation data from SPICE/Ngspice ".raw" files (Project "WaveDash"). This tool will replace older desktop applications like GTKWave, offering a browser-based UI, Plotly/Dash interactivity, and shareable HTML exports. The backend will be Python, leveraging libraries like `spicelib` for parsing and `numpy/pandas` for data manipulation.

## Current State
**Phase 3 COMPLETED** ✅ - Signal selection interface and plot action functionality is fully implemented and tested. The application now has:
- Complete interactive signal list with type classification and visual feedback
- Click-to-select signal functionality with dynamic styling
- "Plot to Active Tile" button with conditional enabling based on selections
- All signal selection logic integrated with data stores
- 24 passing tests including comprehensive coverage of signal selection components

**Phase 4 IN PROGRESS** - Ready to implement plot tiles and active tile selection functionality.

## Key Decisions
- Build a new application (WaveDash) using Python, Dash, and Plotly.
- Leverage `spicelib` for parsing `.raw` files.
- Adopt a phased development approach, starting with an MVP as defined in `WaveDash_MVP_PRD.md`.
- **MVP Interaction Model**: Implement a click-to-select signal, click-to-select active plot tile, and a button-to-plot mechanism, deferring drag-and-drop functionality.
- Key MVP features include: `.raw` file upload and parsing, display of available signals, and plotting selected signals to user-selected tiles on a dashboard.

## Architectural Decisions (MVP)
- **Data Storage**: Pandas DataFrame with time as index, signals as columns
- **Plot Tiles**: 4 fixed tiles arranged vertically to test scrolling behavior
- **Error Handling**: Comprehensive error handling implemented for file upload and parsing
- **Performance**: No decimation needed for small datasets
- **UI/UX**: Use common practices for layout and browser compatibility
- **Project Structure**: Modular architecture with separate components, callbacks, and data modules
- **Data Stores**: Use dcc.Store for parsed-data, signal-list, selected-signal, active-tile, and tile-config
- **Plotting**: Use go.Scattergl for performance
- **File Upload**: Base64 encoding/decoding with temporary file handling for spicelib compatibility

## Implementation Progress
### Phase 1: Project Setup & Basic Structure ✅ COMPLETED
- ✅ Git repository with proper .gitignore, README, and version control
- ✅ Python virtual environment with all dependencies
- ✅ Modular directory structure (src/, tests/, assets/)
- ✅ Data stores module (`src/data/stores.py`) with proper typing
- ✅ Main app module (`src/app.py`) with layout structure
- ✅ Test suite with 100% pass rate (6 tests)
- ✅ Basic Dash app successfully creates and initializes

### Phase 2: File Upload and Parsing ✅ COMPLETED
- ✅ File upload component with drag-and-drop interface (`src/components/upload.py`)
- ✅ Comprehensive SPICE parser (`src/utils/spice_parser.py`) supporting:
  - Base64 decoding of uploaded files
  - spicelib integration with temporary file handling
  - DataFrame conversion with proper indexing
  - Complex number handling (magnitude extraction)
  - Signal classification and metadata extraction
- ✅ Upload callbacks (`src/callbacks/upload_callbacks.py`) with complete error handling
- ✅ Integration with data stores (parsed-data-store, signal-list-store)
- ✅ User feedback system with success/error messages and styling
- ✅ Comprehensive test suite (12 passing tests) including integration tests
- ✅ Tested with real SPICE files from raw_data/ directory

### Phase 3: Signal Selection Interface ✅ COMPLETED
- ✅ Signal list component (`src/components/signal_list.py`) with:
  - Interactive signal list display with scrollable container
  - Signal type classification and color-coded badges (voltage, current, power)
  - Click-to-select functionality with visual selection feedback
  - Selected signal display with dynamic styling
  - "Plot to Active Tile" button with conditional enabling
- ✅ Signal selection callbacks (`src/callbacks/signal_callbacks.py`) supporting:
  - Dynamic signal list population from parsed data
  - Pattern-matching click detection for signal selection
  - Selected signal state management
  - Plot button state management based on signal/tile selection
  - Tile configuration updates when plotting signals
- ✅ Integration with all data stores (signal-list, selected-signal, tile-config, active-tile)
- ✅ Comprehensive test coverage (24 passing tests) including component and interaction tests
- ✅ User-friendly interface with type badges, hover effects, and clear visual feedback

### Next: Phase 4 - Plot Tiles and Active Tile Selection
- Implement plot tiles and active tile selection functionality

## Technical Implementation Details
### File Upload & Parsing Flow
1. User uploads .raw file via dcc.Upload component
2. File content is base64 encoded by Dash
3. Upload callback decodes content and creates temporary file
4. spicelib.RawRead parses the temporary file
5. Data is extracted and converted to Pandas DataFrame format
6. DataFrame and signal list are stored in dcc.Store components
7. User receives feedback on success/failure with detailed messages

### Data Structure
- **parsed-data-store**: Contains DataFrame as dict with metadata
- **signal-list-store**: List of signal names for selection interface
- Independent variable (time/frequency) stored as DataFrame index
- Complex signals converted to magnitude for plotting compatibility

## Open Questions (Post-MVP Focus)
- What are the specific performance requirements and optimization strategies for "huge-file handling"?
- How will user configurations (e.g., plot preferences, themes) be managed?
- Is real-time/streaming data from `libngspice` a requirement for future versions, and what would be the technical approach?
- What is the detailed long-term testing strategy (e.g., E2E, performance benchmarks, automated visual regression)?
- What is the planned deployment strategy for wider use (e.g., Docker, PaaS)?
- How will advanced features like math traces, FFT, and synchronized zoom/pan be integrated architecturally?
- What level of extensibility (e.g., plugin system for custom math operations or plot types) is desired? 