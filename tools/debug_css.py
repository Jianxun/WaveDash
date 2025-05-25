#!/usr/bin/env python3
"""
Debug tool to check CSS loading and rule application.
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
        return None

def check_css_loading(url="http://localhost:8050"):
    """Check CSS loading and rule application."""
    driver = setup_chrome_driver()
    if not driver:
        return False
    
    try:
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(3)
        
        # Check if CSS files are loaded
        stylesheets = driver.execute_script("""
            var sheets = [];
            for (var i = 0; i < document.styleSheets.length; i++) {
                var sheet = document.styleSheets[i];
                sheets.push({
                    href: sheet.href,
                    title: sheet.title,
                    type: sheet.type,
                    media: sheet.media.mediaText,
                    disabled: sheet.disabled
                });
            }
            return sheets;
        """)
        
        print(f"Found {len(stylesheets)} stylesheets:")
        for i, sheet in enumerate(stylesheets):
            print(f"  {i+1}. {sheet['href'] or 'inline'} (disabled: {sheet['disabled']})")
        
        # Check for our specific CSS rule
        try:
            app_content = driver.find_element(By.ID, "app-content")
            
            # Check all CSS rules that apply to app-content
            all_styles = driver.execute_script("""
                var element = arguments[0];
                var computedStyle = window.getComputedStyle(element);
                var styles = {};
                
                // Get key properties we care about
                var properties = ['display', 'flex-direction', 'width', 'height', 'position'];
                for (var i = 0; i < properties.length; i++) {
                    var prop = properties[i];
                    styles[prop] = computedStyle.getPropertyValue(prop);
                }
                
                return styles;
            """, app_content)
            
            print(f"\\nComputed styles for #app-content:")
            for prop, value in all_styles.items():
                print(f"  {prop}: {value}")
            
            # Check if our CSS rule exists in any stylesheet
            css_rule_exists = driver.execute_script("""
                // Look for our CSS rule in all stylesheets
                var foundRule = false;
                try {
                    for (var i = 0; i < document.styleSheets.length; i++) {
                        var sheet = document.styleSheets[i];
                        if (sheet.cssRules) {
                            for (var j = 0; j < sheet.cssRules.length; j++) {
                                var rule = sheet.cssRules[j];
                                if (rule.selectorText && rule.selectorText.includes('.app-content')) {
                                    foundRule = true;
                                    console.log('Found rule:', rule.cssText);
                                }
                            }
                        }
                    }
                } catch(e) {
                    console.log('Error accessing CSS rules:', e);
                }
                return foundRule;
            """)
            
            print(f"\\nCSS rule '.app-content' found in stylesheets: {css_rule_exists}")
            
        except Exception as e:
            print(f"Error checking app-content element: {e}")
        
        # Check if assets folder is accessible
        assets_test = driver.execute_script("""
            return fetch('/_dash-component-suites/dash/deps/polyfill@7.js')
                .then(response => response.ok)
                .catch(() => false);
        """)
        
        return True
        
    except Exception as e:
        print(f"Error checking CSS: {e}")
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
    """Main function to run the CSS diagnostic tool."""
    print("WaveDash CSS Diagnostic Tool")
    print("=" * 40)
    
    # Check if app is running
    if not check_app_running():
        print("⚠️  WaveDash app is not running on http://localhost:8050")
        print("Please start the app first with: python src/app.py")
        return
    
    print("✅ WaveDash app is running")
    
    # Check CSS
    success = check_css_loading()
    
    if success:
        print("✅ CSS diagnostics completed!")
    else:
        print("❌ CSS diagnostics failed")

if __name__ == "__main__":
    main() 