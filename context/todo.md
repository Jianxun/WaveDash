# Project Todo List

## Current Sprint (MVP Features)

### Phase 1: Project Setup & Basic Structure
- [ ] Initialize Git repository (if not done)
- [ ] Set up Python virtual environment
- [ ] Install dependencies: `dash`, `plotly`, `pandas`, `spicelib`
- [ ] Create `requirements.txt`
- [ ] Create main application file `src/app.py`
- [ ] Implement basic Dash app layout (Header, Sidebar, Main Content areas)
- [ ] Add `dcc.Store` components for:
  - [ ] `id='parsed-data-store'`
  - [ ] `id='signal-list-store'`
  - [ ] `id='tile-config-store'` (maps tile_id to signal_name)
  - [ ] `id='selected-signal-store'` (stores name of the currently selected signal)
  - [ ] `id='active-tile-store'` (stores id of the currently active plot tile)

### Phase 2: File Upload and Parsing
- [ ] Add `dcc.Upload` component to the sidebar for `.raw` files
- [ ] Implement callback for `dcc.Upload` to:
  - [ ] Decode uploaded file content
  - [ ] Parse `.raw` file using `spicelib.RawRead`
  - [ ] Extract traces and sweeps
  - [ ] Construct Pandas DataFrame (index=sweep, columns=signals)
  - [ ] Store DataFrame in `parsed-data-store`
  - [ ] Extract and store signal names in `signal-list-store`

### Phase 3: Sidebar - Signal Selection & Plot Action
- [ ] Add `html.Div` (e.g., `id='signal-list-display'`) to sidebar for listing signals
- [ ] Implement callback to populate `signal-list-display` from `signal-list-store`
  - [ ] For each signal, create a clickable HTML element (e.g., `html.Button` or styled `html.Div`)
  - [ ] Implement callback for signal list items: on click, update `selected-signal-store` with the clicked signal's name
- [ ] Add a "Plot to Active Tile" `html.Button` (e.g., `id='plot-button'`) to the sidebar

### Phase 4: Main Canvas - Plot Tiles & Active Tile Selection
- [ ] Define 2-4 `dcc.Graph` components as plot tiles in the main content area (e.g., `id='plot-tile-1'`). Make each tile (or a wrapper Div) clickable.
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
[List of completed tasks] 