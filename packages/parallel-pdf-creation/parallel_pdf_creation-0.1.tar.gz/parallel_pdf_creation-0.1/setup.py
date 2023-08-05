from distutils.core import setup
setup(
  name = 'parallel_pdf_creation',         # How you named your package folder (MyLib)
  packages = ['parallel_pdf_creation'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Parallelized way of creating pdfs for multiple "pandas dataframe records"',   # Give a short description about your library
  author = 'Gaurish Anvekar',                   # Type in your name
  author_email = 'gaureeshanvekar@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/GaureeshAnvekar',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/GaureeshAnvekar/parallel_pdf_creation/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords = ['PDF', 'pandas', 'dataframe', 'table', 'thread', 'parallel', 'rows', 'records', 'python', 'fill'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'PyPDF2',
          'pdfrw',
          'pypdftk',
          'reportlab'
        
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
