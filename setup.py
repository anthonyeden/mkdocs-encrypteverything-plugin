from setuptools import setup, find_packages

setup(
    name='mkdocs-encrypteverything-plugin',
    version='0.0.1',
    author='mediarealm',
    description='A MkDocs plugin that encrypt/decrypt all content on a page with AES',
    license='MIT',
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=[
        'mkdocs',
        'pyyaml',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': [
            'encrypteverything = encrypteverything.plugin:EncryptEverything'
        ]
    },
    package_data={'encrypteverything': ['*.tpl.html']},
    include_package_data = True
)