#!/usr/bin/env python3
"""
Debug tool to take screenshots of the WaveDash app to help with UI troubleshooting.
"""
import time
import subprocess
import os
from pathlib import Path
from selenium import webdriver
from selenium import __version__ as selenium_version
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_chrome_driver():
    """Setup Chrome driver with appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Failed to setup Chrome driver: {e}")
        print("Make sure Chrome and chromedriver are installed")
        return None

def take_screenshot(url="http://localhost:8050", output_file="wavedash_screenshot.png", wait_seconds=3):
    """Take a screenshot of the WaveDash app."""
    driver = setup_chrome_driver()
    if not driver:
        return False
    
    try:
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for the page to load
        print(f"Waiting {wait_seconds} seconds for page to load...")
        time.sleep(wait_seconds)
        
        # Try to wait for a specific element that indicates the app has loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "app-container"))
            )
            print("App container found, taking screenshot...")
        except:
            print("App container not found, taking screenshot anyway...")
        
        # Take screenshot
        screenshot_path = Path(output_file).absolute()
        driver.save_screenshot(str(screenshot_path))
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Also get page source for debugging
        source_file = screenshot_path.with_suffix('.html')
        with open(source_file, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"Page source saved to: {source_file}")
        
        # Get window size and basic info
        window_size = driver.get_window_size()
        print(f"Window size: {window_size['width']}x{window_size['height']}")
        
        return True
        
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return False
    finally:
        driver.quit()

def check_app_running(url="http://localhost:8050"):
    """Check if the WaveDash app is running."""
    import requests
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function to run the screenshot tool."""
    print("WaveDash Debug Screenshot Tool")
    print("=" * 40)
    
    # Check Python version and selenium
    print(f"Selenium version: {selenium_version}")
    
    # Check if app is running
    if not check_app_running():
        print("⚠️  WaveDash app is not running on http://localhost:8050")
        print("Please start the app first with: python src/app.py")
        return
    
    print("✅ WaveDash app is running")
    
    # Take screenshot
    success = take_screenshot()
    
    if success:
        print("✅ Screenshot captured successfully!")
        print("\nNow you can:")
        print("1. Open wavedash_screenshot.png to see the current UI layout")
        print("2. Open wavedash_screenshot.html to inspect the HTML structure")
    else:
        print("❌ Failed to capture screenshot")
        print("\nTroubleshooting:")
        print("1. Make sure Chrome is installed")
        print("2. Install chromedriver: brew install chromedriver (macOS)")
        print("3. Install selenium: pip install selenium requests")

if __name__ == "__main__":
    main() 