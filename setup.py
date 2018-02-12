from setuptools import setup

setup(name="WifiHawk",
      version="0.1",
      install_requires=['scapy==2.3.2', 'netaddr==0.7.18', 'jinja2==2.7.3',
                        'pcapy==0.11.1', 'requests==2.18.4', 'chardet==3.0.4'],
      author="Ed Cradock",
      description="A passive wifi recon tool, allowing probe requests to be mapped to GPS co-ordinates.",
      license="MIT")
