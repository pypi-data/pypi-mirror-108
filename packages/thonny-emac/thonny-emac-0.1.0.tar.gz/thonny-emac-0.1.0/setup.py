import setuptools
import os

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

setupdir = os.path.dirname(__file__)

requirements = []
for line in open(os.path.join(setupdir, "requirements.txt"), encoding="utf-8"):
    if line.strip() and not line.startswith("#"):
        requirements.append(line)

setuptools.setup(
        name="thonny-emac",
        version="0.1.0",
        author="Klint Youngmeyer",
        author_email="8-kyoungmeyer@users.noreply.git.emacinc.com",
        license="GPL",
        description="Thonny support for EMAC, Inc. boards",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        keywords="IDE thonny programming CutiPy MitiPy EMAC",
        url="http://git.emacinc.com/micropython-public/thonny-emac",
        project_urls={
            "Bug Tracker": "http://git.emacinc.com/micropython-public/thonny-emac/issues"
            },
        classifiers=[
            "Environment :: MacOS X",
            "Environment :: Win32 (MS Windows)",
            "Environment :: X11 Applications",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: Freeware",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Natural Language :: English",
            "Topic :: Software Development",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: POSIX :: Linux",
            ],
        package_data={
            "thonnycontrib.backend": ["api_stubs/*.py", "api_stubs/uasyncio/*.py", "api_stubs/umqtt/*.py"]
        },
        packages=["thonnycontrib.backend"],
        python_requires=">=3.5",
        install_requires=requirements,
        platforms=["Windows", "macOS", "Linux"],
        )
