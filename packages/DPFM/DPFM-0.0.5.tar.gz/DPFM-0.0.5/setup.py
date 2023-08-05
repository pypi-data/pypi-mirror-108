import setuptools

setuptools.setup(
    name='DPFM',      #库的名字
    version = '0.0.5',     #库的版本号，后续更新的时候只需要改版本号就行了
    anthor = 'Wang shifan,Cao linjuan,Guo quan and Kevin',
    anthor_email = '1595546523@qq.com',
    description="Data processing for marine",
    long_description_content_type='text/markdown',
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)