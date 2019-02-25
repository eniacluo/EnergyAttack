echo "PATH=\$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
pip install --user --upgrade pip setuptools wheel
pip install --user numpy
python -c "import numpy"
