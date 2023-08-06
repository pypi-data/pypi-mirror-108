import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Optical Flow Gunnar-Farneback',
    version='1.0',
    description='Calculates the optical flow according to Gunnar-Farneback',
    author='Ramon Niet, Andreas Bloch',
    author_email='andreas.bloch@mediengruppe-rtl.de',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy<=1.20.*',
        'opencv-python<=4.5.2.*'
        'pandas<=1.2.*'
    ]
)
