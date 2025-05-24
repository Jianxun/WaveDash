# Project Todo List

## Current Sprint (MVP Features)

### Phase 1: Project Setup & Basic Structure ✅ COMPLETED
- [X] Initialize Git repository (if not done)
- [X] Set up Python virtual environment
- [X] Install dependencies: `dash`, `plotly`, `pandas`, `spicelib`
- [X] Create `requirements.txt`
- [X] Create main application file `src/app.py`
- [X] Implement basic Dash app layout (Header, Sidebar, Main Content areas)
- [X] Add `dcc.Store` components for:
  - [X] `id='parsed-data-store'`
  - [X] `id='signal-list-store'`
  - [X] `id='tile-config-store'` (maps tile_id to signal_name)
  - [X] `id='selected-signal-store'` (stores name of the currently selected signal)
  - [X] `id='active-tile-store'` (stores id of the currently active plot tile)

### Phase 2: File Upload and Parsing ✅ COMPLETED
- [X] Add `dcc.Upload` component to the sidebar for `.raw` files
- [X] Implement callback for `dcc.Upload` to:
  - [X] Decode uploaded file content
  - [X] Parse `.raw` file using `spicelib.RawRead`
  - [X] Extract traces and sweeps
  - [X] Construct Pandas DataFrame (index=sweep, columns=signals)
  - [X] Store DataFrame in `parsed-data-store`
  - [X] Extract and store signal names in `signal-list-store`

### Phase 3: Sidebar - Signal Selection & Plot Action ✅ COMPLETED
- [X] Add `html.Div` (e.g., `id='signal-list-display'`) to sidebar for listing signals
- [X] Implement callback to populate `signal-list-display` from `signal-list-store`
  - [X] For each signal, create a clickable HTML element (e.g., `html.Button` or styled `html.Div`)
  - [X] Implement callback for signal list items: on click, update `selected-signal-store` with the clicked signal's name
- [X] Add a "Plot to Active Tile" `html.Button` (e.g., `id='plot-button'`) to the sidebar

### Phase 4: Main Canvas - Plot Tiles & Active Tile Selection (IN PROGRESS)
- [ ] Define 4 `dcc.Graph` components as plot tiles in the main content area (e.g., `id='plot-tile-1'`). Make each tile (or a wrapper Div) clickable.
- [ ] Implement callback for plot tiles: on click, update `active-tile-store` with the ID of the clicked tile.
- [ ] Implement callback for the "Plot to Active Tile" button (`id='plot-button'`):
  - [ ] Inputs: `n_clicks` of `plot-button`, `data` from `selected-signal-store`, `data` from `active-tile-store`.
  - [ ] Logic: Update `tile-config-store` to map the `selected-signal` to the `active-tile`.
- [ ] Implement plotting callbacks for each `dcc.Graph` tile's `figure`:
  - [ ] Input: Signal name for the tile (derived from `tile-config-store` based on the tile's ID), data from `parsed-data-store`.
  - [ ] Logic: Retrieve data, create Plotly line chart (`go.Scattergl`).
  - [ ] Output: Plotly figure object (or empty/placeholder if no signal assigned to the tile).

### Phase 5: Initial Styling and Ergonomics
- [ ] Create basic CSS file in `assets/` for layout (sidebar, tiles).
- [ ] Add visual cues for selected signal in the list.
- [ ] Add visual cues for the active plot tile (e.g., a border).

## Backlog
- [ ] Drag-and-drop interface for plotting signals
- [ ] Advanced "hierarchy" display for signals in sidebar (tree view)
- [ ] Zoom/pan synchronization across tiles (if desired)
- [ ] Delta cursors and readouts
- [ ] Math/derived traces functionality
- [ ] FFT & spectrum tab/view
- [ ] Huge-file handling optimizations (on-load decimation, lazy streaming)
- [ ] Session save/share (export to standalone HTML, server-side session saving)
- [ ] User configuration management
- [ ] Real-time/streaming data support
- [ ] Comprehensive testing (unit, E2E, performance)
- [ ] Detailed documentation

## Completed Tasks
### Phase 1: Project Setup & Basic Structure ✅
- ✅ Git repository initialized with proper .gitignore and README
- ✅ Python virtual environment with all dependencies installed
- ✅ Modular project structure (src/, tests/, assets/ directories)
- ✅ Data stores implemented with proper typing (`src/data/stores.py`)
- ✅ Main app layout with header, sidebar, and content areas (`src/app.py`)
- ✅ Test-driven development with 6 passing tests
- ✅ All 5 data stores properly configured and tested
- ✅ Basic Dash app can be created and runs successfully

### Phase 2: File Upload and Parsing ✅
- ✅ File upload component created (`src/components/upload.py`)
- ✅ SPICE parser utility implemented (`src/utils/spice_parser.py`)
- ✅ Upload callback handlers implemented (`src/callbacks/upload_callbacks.py`)
- ✅ Integration with main app layout complete
- ✅ Comprehensive test coverage with 12 passing tests
- ✅ Successfully parses .raw files using spicelib
- ✅ Converts SPICE data to Pandas DataFrame format
- ✅ Stores parsed data and signal list in appropriate dcc.Store components
- ✅ User-friendly upload interface with drag-and-drop support
- ✅ Error handling and user feedback for upload issues

### Phase 3: Signal Selection & Plot Action ✅
- ✅ Signal list component created (`src/components/signal_list.py`)
- ✅ Signal selection callbacks implemented (`src/callbacks/signal_callbacks.py`)
- ✅ Interactive signal list with type classification (voltage, current, power)
- ✅ Click-to-select signal functionality with visual feedback
- ✅ Selected signal display with dynamic styling
- ✅ "Plot to Active Tile" button with conditional enabling
- ✅ Integration with data stores (selected-signal-store, tile-config-store)
- ✅ Comprehensive test coverage with 24 passing tests
- ✅ Signal type badges and hover effects for better UX
- ✅ Plot action handling that updates tile configuration 