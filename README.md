# WaveDash - SPICE Waveform Viewer

A modern web-based dashboard for visualizing simulation data from SPICE/Ngspice `.raw` files. WaveDash replaces older desktop applications like GTKWave with a browser-based UI featuring Plotly interactivity and a professional modern interface.

## 🚀 Quick Start - MVP Ready!

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jianxun/WaveDash
   cd WaveDash
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   > **Note**: We've streamlined `requirements.txt` to include only core dependencies. Pip will automatically handle sub-dependencies (Flask, Jinja2, etc.).

### Running WaveDash

**Start the application:**
```bash
python -m src.app
```

The application will be available at: http://localhost:8050

### Using the MVP

#### 1. **Upload a SPICE Raw File**
   - Use the file upload area in the left sidebar
   - Try the provided sample file: `raw_data/Ring_Oscillator_7stage.raw`
   - Drag and drop or click to browse for `.raw` files
   - ✅ Success message appears when file is parsed

#### 2. **Select Signals**
   - Available signals appear in the sidebar with type badges:
     - 🟢 **Voltage** signals (e.g., V(bus05), v(bus07))
     - 🟠 **Current** signals (e.g., I(c1), Ix(x5:DRAIN))
     - 🔴 **Power** signals (calculated power measurements)
   - Click any signal to select it
   - Selected signal is highlighted in blue

#### 3. **Plot to Tiles**
   - Click on any of the 4 plot tiles to make it active (blue border)
   - Click "Add to Active Tile" button to plot the selected signal
   - **Multi-signal Support**: Add multiple signals to the same tile for comparison
   - Each signal gets a unique color for easy identification

#### 4. **Interactive Features**
   - **Zoom/Pan**: Use Plotly controls on each plot
   - **Clear Tiles**: Use "Clear Active Tile" to remove all signals from a tile
   - **Independent Scrolling**: Sidebar and main content scroll independently
   - **Responsive Layout**: Professional sidebar + main canvas layout

### Sample Workflow

1. **Start WaveDash**: `python -m src.app`
2. **Load Sample**: Upload `raw_data/Ring_Oscillator_7stage.raw`
3. **Explore Signals**: Try plotting `v(out)`, `v(n1)`, `v(n2)` to see the ring oscillator behavior
4. **Compare Waveforms**: Add multiple signals to the same tile
5. **Analyze**: Use Plotly zoom/pan to examine signal details

## 📁 Project Structure

```
WaveDash/
├── src/                    # Main application code
│   ├── app.py             # Main Dash application
│   ├── components/        # UI components
│   ├── callbacks/         # Dash callback handlers
│   ├── data/             # Data stores and models
│   └── utils/            # Utility functions
├── assets/               # CSS and static assets
├── tests/                # Test suite
├── raw_data/             # Sample SPICE files
├── context/              # Project context and todos
├── doc/                  # Documentation
├── tools/                # Development tools
├── temp/                 # Temporary files and screenshots
└── requirements.txt      # Python dependencies
```

## 🧪 Development

### Running Tests
```bash
pytest tests/ -v
```

### Architecture

- **Frontend**: Dash/Plotly for interactive web UI
- **Backend**: Python with spicelib for `.raw` file parsing
- **Data Processing**: Pandas for signal manipulation
- **Styling**: Modern CSS with flexbox layout

## 🎯 MVP Features (Complete)

✅ **File Upload & Parsing**: Upload and parse SPICE `.raw` files  
✅ **Signal Selection**: Interactive signal list with type classification  
✅ **Multi-Tile Dashboard**: 4 clickable plot tiles with active selection  
✅ **Signal Plotting**: Plot signals with full Plotly interactivity  
✅ **Multi-Signal Overlay**: Compare multiple signals on the same plot  
✅ **Professional UI**: Modern sidebar/main canvas layout  
✅ **End-to-End Workflow**: Complete signal visualization pipeline  

## 🔧 Troubleshooting

### Common Issues

1. **CSS not loading**: Make sure to run with `python -m src.app` (not `python src/app.py`)
2. **Import errors**: Ensure you're in the project root directory
3. **File upload fails**: Check that the `.raw` file is valid SPICE output
4. **No signals visible**: Verify the raw file contains simulation data (not just operating point)

### Sample Files

- ✅ `Ring_Oscillator_7stage.raw` - Complete transient simulation with waveforms
- ❌ `Ring_Oscillator_7stage.op.raw` - Operating point only (no waveforms)

## 🚧 Next Steps

The MVP is complete! Future enhancements include:
- Draggable dashboard with dynamic grid layout
- Advanced signal analysis tools
- Export capabilities
- Enhanced performance for large files

---

**WaveDash is production-ready for SPICE waveform visualization!** 🚀 