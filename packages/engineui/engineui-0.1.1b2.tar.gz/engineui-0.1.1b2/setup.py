#UPLOAD TOKEN: pypi-AgEIcHlwaS5vcmcCJDhjNzkyN2M4LWUyMzAtNDUyOS1hYmIwLWFmNzkyYmYyZjU4YwACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgJBdlQwk9_JaryTkJVjfH9uXv6q5iOzWYlHFCkDop5fw

from distutils.core import setup, Extension
from glob import glob

setup(
    name="engineui",
    version="0.1.1b2",
    description="Engine UI for an engine.",
    long_description="The UI for an engine.",
    author="Abhradeep De",
    author_email="deabhradeep@gmail.com",
    ext_modules=[Extension("engineui", glob("*.c"))]
)