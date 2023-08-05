import setuptools

setuptools.setup(
    name="tctm", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.2", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="henry", #作者
    author_email="enryh123@outlook.com", #邮箱
    description="test lib", #描述
    long_description='test lib', #描述
    long_description_content_type="text/markdown", #markdown
    url="", #github地址
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7"
)