from setuptools import setup, find_packages

with open('README.md','r') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='sidSimpleNN',
    version='0.2.8',
    description='Multilayered Perceptron NN light weight, make, train, test models',
    # long_description_content_type="text",
    # long_description='this is simmple NN library\n\nfrom sidSimpleNN import mainTrain\n mainTrain.run()\nif data,mnist folder dont get made automatically then manualy download from MNIST dataset and place in datafolder ',
    
    long_description=README,
    long_description_content_type='text/markdown',
    # long_description=README,
    license='MIT',
    packages=find_packages(),
    author='sid007',
    author_email='sid700710@gmail.com',
    keywords=['sidSimpleNN'],
    url='',
    download_url='https://pypi.org/project/sidSimpleNN/'
)

# install_requires = [
#     'pickle','numpy','matplotlib'
# ]


if __name__ == '__main__':
    setup(**setup_args)