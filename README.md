# zjuintl_assistant

## Features

- [x] Get deadline of assignments from Blackboard
- [x] Get latest grades of assignments from Blackboard
- [x] Get latest announcements from Blackboard
- [x] Get notices from myZJU
- [ ] Get information from PeopleSoft. **I've not figured out how to do this yet. PRs and disscussions are welcome!**

## Usage

It's a package that contains a class `Assistant`, which provides abilities shown in [Features](#features). Dependencies are listed in `requirements.txt` in the same folder.

For more details, please refer to [wiki](https://github.com/ZJUIntl-share/zjuintl_assistant/wiki) (WIP).

## Development Notes

This project is simply a spider that replay the requests of the browser. Login process of zjuam is based on package capture and reverse engineering of javascript code. However, the analysis of PeopleSoft is too difficult for me. So any help is welcome! I think possible difficulty is the management of cookies.

## Credits

- [ZJUintl-gRPC](https://github.com/QSCTech/ZJUintl-gRPC)
- [zju-learning-assistant](https://github.com/PeiPei233/zju-learning-assistant)
