import sys
import subprocess

def package_check():
    # This is to check if packages are installed
    # If not, will install, if so, it will skip install
    
    REQUIRED_PACKAGES = ['numpy', 'pandas', 'matplotlib', 'scikit-learn', 'seaborn', 'sys', 'subprocess', 'os', 'json', 'requests', 'flask', 'plotly', 'scipy', 'csv','pathlib','time','statsmodels']
    
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            # See about clearing later
        
