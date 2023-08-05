from setuptools import setup

setup(name='1Q847',
      version='0.0.1',
      description='模拟操作',
      url='https://github.com/qxt514657/',
      author='1Q847',
      author_email='976671673@qq.com',
      license='MIT',
      packages=['Dll'],
      install_requires=[
          'pywin32', 'comtypes'
      ],
      package_data={
          'Dll': ['dm.dll', 'DmReg.dll'],
      },
      python_requires='==3.7',
      )
