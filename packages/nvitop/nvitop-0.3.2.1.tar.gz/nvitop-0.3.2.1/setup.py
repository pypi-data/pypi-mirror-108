from setuptools import setup, find_packages

import nvitop


extra_description = {}
try:
    with open('README.md', mode='r') as doc:
        extra_description['long_description'] = doc.read()
        extra_description['long_description_content_type'] = 'text/markdown'
except (OSError, UnicodeError):
    pass

setup(
    name='nvitop',
    version=nvitop.__version__,
    description=nvitop.__doc__,
    **extra_description,
    license=nvitop.__license__,
    author=nvitop.__author__,
    author_email=nvitop.__email__,
    url="https://github.com/XuehaiPan/nvitop",
    packages=find_packages(include=['nvitop', 'nvitop.*']),
    entry_points={'console_scripts': ['nvitop=nvitop.cli:main']},
    install_requires=[
        'nvidia-ml-py == 11.450.51',
        'psutil',
        'cachetools',
        'termcolor',
        'windows-curses; platform_system == "Windows"'
    ],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Environment :: GPU',
        'Environment :: GPU :: NVIDIA CUDA',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    keywords='nvidia, nvidia-smi, NVIDIA, NVML, CUDA, GPU, top, monitoring',
    project_urls={
        'Bug Reports': 'https://github.com/XuehaiPan/nvitop/issues',
        'Source': 'https://github.com/XuehaiPan/nvitop',
    },
)
