# zjuintl_assistant

## Features

- [x] Get deadline of assignments from Blackboard
- [x] Get latest grades of assignments from Blackboard
- [x] Get latest announcements from Blackboard
- [x] Get notices from myZJU
- [ ] Get information from PeopleSoft. **I've not figured out how to do this yet. PRs and disscussions are welcome!**

## Usage

Install the package from PyPI:

```bash
pip install zjuintl-assistant
```

Then you can use the package in your code:

```python
from zjuintl_assistant import Assistant

assistant = Assistant(username='your_username', password='your_password')

# Get deadlines of assignments
deadlines = assistant.get_deadlines()
# Get 10 latest grades
grades = assistant.get_grades(10)
# Get 10 latest announcements (excluding ones without main content)
announcements = assistant.get_announcements(10)
# Get 10 latest announcements (including ones without main content)
announcements_full = assistant.get_announcements(10, full=True)
# Get 10 latest notices from myZJU (not fetching main content)
notices = assistant.get_notices(10)
# Get 10 latest notices from myZJU (English version and including main content)
notices_en_full = assistant.get_notices(10, EN=True, get_content=True)
```

For more details, please refer to [wiki](https://github.com/ZJUIntl-share/zjuintl_assistant/wiki).

## Development Notes

This project is simply a spider that replay the requests of the browser. Login process of zjuam is based on package capture and reverse engineering of javascript code. However, the analysis of PeopleSoft is too difficult for me. So any help is welcome! I think possible difficulty is the management of cookies.

## Links

- [PyPI](https://pypi.org/project/zjuintl-assistant/)
- [GitHub](https://github.com/ZJUIntl-share/zjuintl_assistant)
- [Wiki](https://github.com/ZJUIntl-share/zjuintl_assistant/wiki)
- [Issues](https://github.com/ZJUIntl-share/zjuintl_assistant/issues)

## Credits

- [ZJUintl-gRPC](https://github.com/QSCTech/ZJUintl-gRPC)
- [zju-learning-assistant](https://github.com/PeiPei233/zju-learning-assistant)
