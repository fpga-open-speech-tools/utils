# Frost Edge
## Installation
1. Download [Frost Edge](https://fpga-open-speech-tools-release.s3-us-west-2.amazonaws.com/frost-edge_20201007_armhf.deb)
2. Copy to Audio Blade, Audio Research, or Audio Mini 
3. Install: `dpkg -i frost-edge_20201007_armhf.deb`

## [Deb Package](https://fpga-open-speech-tools-release.s3-us-west-2.amazonaws.com/frost-edge_20201007_armhf.deb)
- Installs the following [Frost LKMs](https://github.com/fpga-open-speech-tools/component_library):  
    - FE_AD1939.ko
    - FE_AD7768_4.ko	
    - FE_PGA2505.ko	
    - FE_TPA613A2.ko	
- Installs the Frost Edge Web App and Proxy Server
- Installs the [Deployment Manager](https://github.com/fpga-open-speech-tools/deployment_manager)
- Installs the [Frost Utilities](https://github.com/fpga-open-speech-tools/utils)
    - Driver Manager
    - Overlay Manager
    - AWS Downloader and Installer