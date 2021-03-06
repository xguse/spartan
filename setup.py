from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'gffutils',
    'pyfasta',
    'xlrd',
    'docopt',
    'arrow',
]

dependency_links = [
    #"git+ssh://git@github.com/xguse/sanitize.git@master#egg=sanitize"
]

setup(name='spartan',
    version=version,
    description="A spartan bioinformatics package, providing only the essentials and nothing fancy or luxurious. Enough to get the job done quickly without flourish.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='bioinformatics basic parsers functions fasta fastq PSSM PWM utilities',
    author='Augustine Dunn',
    author_email='wadunn83@gmail.com',
    url='https://github.com/xguse',
    license='GPL3',
    packages=find_packages('src'),
    package_dir={'': 'src'}, include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            #['spartan=spartan:main']
            ['xls_to_csvs=spartan.scripts.xls_to_csvs:main']
    }
)
