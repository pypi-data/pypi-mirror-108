from distutils.core import setup
setup(
  name = 'rema',         
  # packages = [
  # 'rema', 
  # 'rema.test', 
  # 'rema.data', 
  # 'rema.models',
  # 'rema.train', 
  # ],  #! Important
  version = '0.0.0', #! Always update
  license='MIT',        
  description = 'REusable MAchine learning codebase.', 
  author = 'Asapanna Rakesh',                   
  author_email = 'rakesh.asapanna@gmail.com',      
  url = 'https://github.com/rakesh4real/rema', 
  download_url = 'https://github.com/rakesh4real/rema/archive/v0.0.0.tar.gz', #! change version here
  keywords = ['machine learning', 'deep learning', 'data science'],   
  # these are the dependant pypi pacakges
  # should declare the loosest possible dependency versions that are still workable. 
  # Its job is to say what a particular package can work with.
  install_requires=[        
          'hydra-core',
          'pytest',
          'pandas',
          'scikit-learn'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
  ],
)