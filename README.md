# WaveDash

A modern, web-based dashboard for visualizing SPICE simulation waveforms.

## Overview

WaveDash is designed to replace aging desktop applications (like GTKWave, GWave) by offering a significantly improved user experience, enhanced interactivity, and easier sharing of results within a browser-based environment.

## Features (MVP)

- ✅ Upload and parse SPICE `.raw` files
- ✅ Interactive signal selection
- ✅ Multiple plot tiles for waveform comparison
- ✅ Modern web-based interface using Dash and Plotly

## Technology Stack

- **Backend**: Python 3.12+
- **Web Framework**: Dash
- **Plotting**: Plotly
- **Data Processing**: Pandas
- **SPICE Parsing**: spicelib

## Setup

### Prerequisites

- Python 3.12 or higher
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd WaveDash
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python src/app.py
```

Navigate to `http://localhost:8050` in your browser.

## Development

### Project Structure

```
WaveDash/
├── src/                 # Main application code
│   ├── components/      # UI components
│   ├── data/           # Data handling modules
│   ├── callbacks/      # Dash callback functions
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── assets/             # Static assets (CSS, JS)
├── context/            # Project context and documentation
└── raw_data/           # Sample SPICE files
```

### Testing

```bash
pytest
```

## Contributing

This project follows test-driven development practices. Please ensure tests pass before submitting changes.

## License

[License information to be added] 