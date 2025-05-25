#!/usr/bin/env python3
"""
Debug tool to check CSS computed styles and diagnose layout issues.
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

def check_layout_diagnostics(url="http://localhost:8050"):
    """Check layout diagnostics for the WaveDash app."""
    driver = setup_chrome_driver()
    if not driver:
        return False
    
    try:
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(3)
        
        # Get window size
        window_size = driver.get_window_size()
        print(f"Browser window size: {window_size['width']}x{window_size['height']}")
        
        # Check if key elements exist
        try:
            app_content = driver.find_element(By.ID, "app-content")
            print("✅ Found app-content element")
            
            # Get computed styles for app-content
            flex_direction = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).flexDirection;", 
                app_content
            )
            display = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).display;", 
                app_content
            )
            print(f"app-content computed styles:")
            print(f"  display: {display}")
            print(f"  flex-direction: {flex_direction}")
            
        except Exception as e:
            print(f"❌ Could not find app-content element: {e}")
        
        try:
            sidebar = driver.find_element(By.ID, "sidebar")
            print("✅ Found sidebar element")
            
            # Get sidebar computed styles
            width = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).width;", 
                sidebar
            )
            position = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).position;", 
                sidebar
            )
            print(f"sidebar computed styles:")
            print(f"  width: {width}")
            print(f"  position: {position}")
            
        except Exception as e:
            print(f"❌ Could not find sidebar element: {e}")
        
        try:
            main_content = driver.find_element(By.ID, "main-content")
            print("✅ Found main-content element")
            
            # Get main-content computed styles
            flex = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).flex;", 
                main_content
            )
            print(f"main-content computed styles:")
            print(f"  flex: {flex}")
            
        except Exception as e:
            print(f"❌ Could not find main-content element: {e}")
        
        # Check media query application
        media_query_applies = driver.execute_script("""
            return window.matchMedia('(max-width: 768px)').matches;
        """)
        print(f"Media query (max-width: 768px) applies: {media_query_applies}")
        
        # Get the actual bounding rectangles
        try:
            sidebar_rect = driver.execute_script("""
                var sidebar = document.getElementById('sidebar');
                var rect = sidebar.getBoundingClientRect();
                return {
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                };
            """)
            
            main_content_rect = driver.execute_script("""
                var mainContent = document.getElementById('main-content');
                var rect = mainContent.getBoundingClientRect();
                return {
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                };
            """)
            
            print(f"Element positioning:")
            print(f"  sidebar: x={sidebar_rect['x']}, y={sidebar_rect['y']}, w={sidebar_rect['width']}, h={sidebar_rect['height']}")
            print(f"  main-content: x={main_content_rect['x']}, y={main_content_rect['y']}, w={main_content_rect['width']}, h={main_content_rect['height']}")
            
            # Determine layout orientation
            if sidebar_rect['y'] < main_content_rect['y']:
                print("🔍 Layout detected: VERTICAL (sidebar above main content)")
            elif abs(sidebar_rect['y'] - main_content_rect['y']) < 10:
                print("🔍 Layout detected: HORIZONTAL (sidebar beside main content)")
            else:
                print("🔍 Layout detected: UNKNOWN")
            
        except Exception as e:
            print(f"❌ Could not get element positioning: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error checking layout: {e}")
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
    """Main function to run the layout diagnostic tool."""
    print("WaveDash Layout Diagnostic Tool")
    print("=" * 40)
    
    # Check if app is running
    if not check_app_running():
        print("⚠️  WaveDash app is not running on http://localhost:8050")
        print("Please start the app first with: python src/app.py")
        return
    
    print("✅ WaveDash app is running")
    
    # Check layout
    success = check_layout_diagnostics()
    
    if success:
        print("✅ Layout diagnostics completed!")
    else:
        print("❌ Layout diagnostics failed")

if __name__ == "__main__":
    main() 