from distutils.core import setup, Extension
from glob import glob

setup(
    name="engineui",
    version="0.1",
    description="Engine UI.",
    long_description="The UI for this engine.",
    author="Abhradeep De",
    author_email="deabhradeep@gmail.com",
    ext_modules=[Extension("engineui", glob("*.c"))]
)