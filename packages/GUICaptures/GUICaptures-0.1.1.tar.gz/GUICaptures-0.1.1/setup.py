from setuptools import setup

setup(
    name='GUICaptures',
    version='0.1.1',    
    description='Answering questions using NLTK and screen captures',
    long_description="Read the wiki at ",
    url='https://github.com/Sam-Nielsen-Dot/GUICaptures',
    author='Sam Nielsen',
    author_email='lenssimane@gmail.com',
    license='MIT',
    packages=['GUICaptures'],
    install_requires=['pytesseract>=0.3.7',
                    'wikipedia>=1.4.0',
                    'nltk>=3.5',
                    'PyAutoGUI>=0.9.52',
                    'win10toast>=0.9',
                    'Pillow>=8.2.0'             
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Healthcare Industry',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    #include_package_data=True,
    #package_data={'': ['GUICaptures/data/ *']},
)
