# Python demo to denoise a 3D point cloud, and visualize the noisy and denoised clouds

It is recommended to do all the following in a Conda virtual environment.

For efficiently visualize and interact with the point cloud with many points, we use Mayavi.
Due to the dependecies issue, please do the installation with the following order:
	1. $ conda install -c conda-forge vtk
	2. $ pip install mayavi
	3. $ pip install PyQt5

After this, you may need to reinstall Scikit-learn and Anisofilter, due to the change of python version 
during installing VTK:
	1. $ pip install scikit-learn
	2. $ pip install anisofilter

Then simply run: python demo_pcd_filtering.py

The denoised point cloud is saved under current directory. Thus, you can also use the Meshlab software to directly 
check the noisy and denoised PLY files.

Authors:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Zhongwei Xu [xu@noiselessimaging.com](mailto:xu@noiselessimaging.com)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Alessandro Foi 

	 
