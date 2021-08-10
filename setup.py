import setuptools

with open("README.md") as f:
    long_description = f.read()
    long_description = long_description.replace(
        "example.png", "https://raw.githubusercontent.com/BranislavBajuzik/ColorWallpaper/master/example.png"
    )

setuptools.setup(
    name="color-wallpaper",
    version="1.1.9",
    author="TheAl_T",
    author_email="branislav.bajuzik@gmail.com",
    description="A Minimalist wallpaper generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/BranislavBajuzik/ColorWallpaper",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
    ],
    keywords="wallpaper color minimalist",
    packages=["color_wallpaper"],
    python_requires=">=3.6",
    install_requires=["Pillow"],
    include_package_data=True,
    data_files=[("color_wallpaper", ["color_wallpaper/font.png"])],
)
