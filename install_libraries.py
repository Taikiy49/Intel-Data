import os
import site
import sys

!echo "installing required python libraries, please wait..."
!{sys.executable} -m pip install --upgrade predictionguard #> /dev/null # for accessing LLM APIs
!{sys.executable} -m pip install --upgrade  "transformers>=4.38.*" #> /dev/null
!{sys.executable} -m pip install --upgrade  "datasets>=2.18.*" #> /dev/null
!{sys.executable} -m pip install --upgrade "accelerate>=0.28.*" #> /dev/null
!{sys.executable} -m pip install --upgrade faiss-cpu #> /dev/null  # for indexing
!{sys.executable} -m pip install --upgrade sentence_transformers #> /dev/null # for generating embeddings
!echo "installation complete..."

# add the location where we installed these libraries to the python pkg path (~/.local/lib/python3.9/*)
# Get the site-packages directory
site_packages_dir = site.getsitepackages()[0]

# add the site pkg directory where these pkgs are insalled to the top of sys.path
if not os.access(site_packages_dir, os.W_OK):
    user_site_packages_dir = site.getusersitepackages()
    if user_site_packages_dir in sys.path:
        sys.path.remove(user_site_packages_dir)
    sys.path.insert(0, user_site_packages_dir)
else:
    if site_packages_dir in sys.path:
        sys.path.remove(site_packages_dir)
    sys.path.insert(0, site_packages_dir)


# adding ~/.local/bin to PATH as well
home_dir = os.path.expanduser('~')
bin_path = os.path.join(home_dir, '.local', 'bin')
os.environ['PATH'] += os.pathsep + bin_path