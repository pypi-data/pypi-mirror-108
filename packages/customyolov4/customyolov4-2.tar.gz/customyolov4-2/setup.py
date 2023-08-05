from setuptools import setup, find_packages

setup(
      name = 'customyolov4',
      version = "2",
      description = 'YOLOv4: Optimal Speed and Accuracy',
      maintainer = "Adeel Intizar",
      maintainer_email = "kingadeel2017@outlook.com",
      packages = find_packages(),
      include_package_data=True,
      python_requires='>=3.5, <4',
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Image Processing',
          'Topic :: Scientific/Engineering :: Image Recognition'
          ],
      keywords = [
      "object detection", 
      "computer vision",  
      'deep learning', 
      'yolov4'],
      
      install_requires = [
          "tensorflow >= 2.3.0", 
	  'flask',
          'opencv-python',
          'numpy',
          'pillow',
          'matplotlib',
          'pandas',
          'scikit-learn',
          'progressbar2',
          'scipy',
          'h5py',
	  ])