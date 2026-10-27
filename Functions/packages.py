import sys
import subprocess

def package_check():
    # This is to check if packages are installed
    # If not, will install, if so, it will skip install
    
    # As of 10/20/2026 I am thinking of getting rid of this auto download file and leaning towards requirements.txt
    
    REQUIRED_PACKAGES = ['numpy', 'pandas', 'sys', 'subprocess', 'os', 'json', 'flask', 'plotly', 'csv','pathlib','time','statsmodels']
    
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            # See about clearing later
        
