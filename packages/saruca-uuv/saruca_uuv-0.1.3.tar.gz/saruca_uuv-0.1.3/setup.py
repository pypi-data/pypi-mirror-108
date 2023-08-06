
from distutils.core import setup
setup(
  name = 'saruca_uuv',
  packages = ['saruca_uuv'],
  version = '0.1.3',
  license='MIT',
  description = 'Autonomous and manual control methods for UUVs',
  author = 'SEMIH SAHIN',
  author_email = 'esemihsahin@hotmail.com',
  url = 'https://github.com/SARUCA-YazilimEkibi/saruca_uuv',
  keywords = ['UUV', 'AUV', 'UNDERWATER'],
  install_requires=[
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)