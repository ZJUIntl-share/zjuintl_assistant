import logging
import re
import datetime
import time
import inspect

import requests
import requests.cookies
import rsa

# import login_utils
# import constants
# import data_classes
from . import login_utils
from . import constants
from . import data_classes

logger = logging.getLogger(__name__)

# LOGIN ERROR
class LoginError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Assistant:
    """
    ZJUIntl learn assistant class
    """

    def __init__(self, username:str, password:str):
        """
        Constructor
        """

        self.__username = username
        self.__password = password
        self.__is_login = False
        self.__is_blackboard_login = False
        self.__cookie_jars: dict[str, requests.cookies.RequestsCookieJar] = {}

        self.login()

    def __get_cookie_jar(self, base: str = None) -> requests.cookies.RequestsCookieJar:
        """
        Get cookie jar
        """

        key = inspect.currentframe().f_back.f_code.co_name
        if key not in self.__cookie_jars:
            if base is None:
                logger.debug(f"{key} cookie jar not found, creating new one")
                self.__cookie_jars[key] = requests.cookies.RequestsCookieJar()
            else:
                logger.debug(f"{key} cookie jar not found, copying from {base}")
                self.__cookie_jars[key] = self.__cookie_jars[base].copy()
        else:
            logger.debug(f"{key} cookie jar found")
        return self.__cookie_jars[key]


    def logout(self):
        """
        Logout by clearing cookies and set related flags to False
        """

        logger.debug("Start logout")
        self.__cookie_jars: dict[str, requests.cookies.RequestsCookieJar] = {}
        self.__is_login = False
        self.__is_blackboard_login = False
        logger.debug("Logout success")


    def login(self):
        """
        Login using zjuam
        """

        logger.debug("Start login using zjuam")

        session = requests.Session()
        session.cookies = self.__get_cookie_jar()

        if self.__is_login:
            logger.debug("Already login, check login status")

            # check login status
            resp = session.get("https://zjuam.zju.edu.cn/cas/login")
            if "统一身份认证平台" not in resp.text:
                logger.debug("Already login, skip")
            else:
                logger.debug("Not login, try to login again")
                self.logout()
                self.login()

            return

        # get execution value
        resp = session.get("https://zjuam.zju.edu.cn/cas/login")
        if "统一身份认证平台" not in resp.text:
            logger.debug("Already login, try to logout first")
            self.logout()
            resp = session.get("https://zjuam.zju.edu.cn/cas/login")
            if "统一身份认证平台" not in resp.text:
                logger.error("Login failed")
                raise LoginError("Login Error")
        logger.debug("Getting execution value")
        execution = re.search(
            r'<input type="hidden" name="execution" value="(.*?)" />',
            resp.text
        ).group(1)
        logger.debug("Getting public key")
        keyResp = session.get("https://zjuam.zju.edu.cn/cas/v2/getPubKey").json()
        Modulus = keyResp["modulus"]
        public_exponent = keyResp["exponent"]
        key = rsa.PublicKey(int(Modulus, 16), int(public_exponent, 16))
        encrypedPwd = login_utils.encrypt(self.__password.encode(), key)
        
        logger.debug("Login with zjuam using username, encrypted password and execution value")
        resp = session.post(
            "https://zjuam.zju.edu.cn/cas/login",
            data={
                "username": self.__username,
                "password": encrypedPwd,
                "_eventId": "submit",
                "execution": execution,
                "authcode": ""
            }
        )

        if "统一身份认证平台" in resp.text:
            logger.error("Login failed: Wrong username or password")
            raise LoginError("Login failed: Wrong username or password")

        self.__is_login = True

        logger.debug("Login with zjuam success")


    def login_blackboard(self):
        """
        Login to Blackboard
        """

        logger.debug("Start login Blackboard")

        session = requests.Session()
        session.cookies = self.__get_cookie_jar("login")

        self.login()

        if self.__is_blackboard_login:
            logger.debug("Already login, check login status")

            # check login status
            resp = session.get("https://learn.intl.zju.edu.cn")
            if "Welcome, " in resp.text:
                logger.debug("Already login, skip")
            else:
                logger.debug("Not login, try to login again")
                self.logout()
                self.login_blackboard()

            return

        # login Blackboard
        resp = session.get("https://zjuam.zju.edu.cn/cas/login?service=https://learn.intl.zju.edu.cn/webapps/bb-ssocas-BBLEARN/index.jsp&locale=zh_CN")
        resp = session.post(
            "https://learn.intl.zju.edu.cn/webapps/bb-ssocas-BBLEARN/execute/authValidate/customLogin",
            data={"username": self.__username}
        )

        self.__is_blackboard_login = True

        logger.debug("Login Blackboard success")


    def get_due_assignments(self) -> list[data_classes.BB_DueAssignment]:
        """
        Get due assignments from Blackboard
        """

        logger.debug("Start get due assignments")

        logger.debug("Checking login status of Blackboard")
        if not self.__is_blackboard_login:
            self.login_blackboard()
        if not self.__is_blackboard_login:
            raise LoginError("Login to Blackboard failed")

        session = requests.Session()
        session.cookies = self.__get_cookie_jar("login_blackboard")

        url = "https://learn.intl.zju.edu.cn/webapps/portal/dwr_open/call/plaincall/NautilusViewService.getViewInfoWithLimit.dwr"
        data = constants.GET_BB_DUE_ASSIGNMENTS_PAYLOAD.copy()
        data["httpSessionId"] = session.cookies.get_dict()["JSESSIONID"]
        data["scriptSessionId"] = login_utils.getScriptSessionId()

        logger.debug(f"Requesting {url}")
        resp = session.post(url, data=data)
        if resp.status_code != 200:
            logger.error(f"Request failed, status code: {resp.status_code}")
            logger.error(resp.text)
            raise Exception(f"Request failed, status code: {resp.status_code}")

        # remove empty lines
        lines = list(filter(lambda x: x != "", resp.text.splitlines()))

        assignments = []

        # parse due assignments
        for line in lines:
            if "eventType=\"DUE\"" in line and "dueDate=new" in line :
                # dueDate=new Date(1711555140000)
                # courseName="ECE210:Analog Signal Processing-1097-LEC(2024 Spring)"
                # title="HW6"
                # type="SCHEDULED"
                course = re.search(r"courseName=\"(.*?)\"", line).group(1).encode("utf-8").decode("unicode_escape")
                timestamp = int(re.search(r"dueDate=new Date\((\d+)\)", line).group(1))/1000
                title = re.search(r"title=\"(.*?)\"", line).group(1).encode("utf-8").decode("unicode_escape")
                date = datetime.datetime.fromtimestamp(timestamp)
                # if due date is in the future, print it
                if date > datetime.datetime.now():
                    # print(f"{date}\t{course}\t\t{title}")
                    assignments.append(data_classes.BB_DueAssignment(
                        course,
                        title,
                        date
                    ))
        # sort by date, then by course
        assignments.sort(key=lambda x: (x.date, x.course))

        logger.debug("Get due assignments success")

        return assignments


    def get_bb_grades(self, count) -> list[data_classes.BB_Grade]:
        """
        Get grades from Blackboard
        """

        logger.debug("Start get BB grades")

        logger.debug("Checking login status of Blackboard")
        if not self.__is_blackboard_login:
            self.login_blackboard()
        if not self.__is_blackboard_login:
            raise LoginError("Login to Blackboard failed")

        session = requests.Session()
        session.cookies = self.__get_cookie_jar("login_blackboard")

        url = "https://learn.intl.zju.edu.cn/webapps/streamViewer/streamViewer"
        data = constants.GET_BB_GRADE_PAYLOAD.copy()

        logger.debug(f"Requesting {url}")
        resp = session.post(url, data=data)
        if resp.status_code != 200:
            logger.error(f"Request failed, status code: {resp.status_code}")
            logger.error(resp.text)
            raise Exception(f"Request failed, status code: {resp.status_code}")
        retries = 3
        while resp.json()["sv_moreData"] and retries > 0:
            print("Retrying")
            resp = session.post(url, data=data)
            retries -= 1


        datum = resp.json()

        courses = { item["id"]: item["name"].encode("utf-8").decode("unicode_escape") for item in datum["sv_extras"]["sx_courses"] }

        datum["sv_streamEntries"].sort(key=lambda x: x["se_timestamp"], reverse=True)

        cnt = 0
        result = []
        # parse grades
        for item in datum["sv_streamEntries"]:
            if cnt >= count:
                break
            title = item["se_context"]
            course = courses[item["se_courseId"]]
            date = datetime.datetime.fromtimestamp(item["se_timestamp"]/1000)
            pointsPossible = item["itemSpecificData"]["gradeDetails"]["pointsPossible"]
            grade = item["itemSpecificData"]["gradeDetails"]["grade"]
            result.append(data_classes.BB_Grade(
                course=course,
                title=title,
                pointsPossible=pointsPossible,
                grade=grade,
                date=date
            ))
            cnt += 1

        logger.debug("Get BB grades success")

        return result


    def get_bb_announcements(self, count: int, full: bool = False) -> list[data_classes.Announcement]:
        """
        Get announcements from Blackboard
        """

        logger.debug("Start get BB announcements")

        logger.debug("Checking login status of Blackboard")
        if not self.__is_blackboard_login:
            self.login_blackboard()
        if not self.__is_blackboard_login:
            raise LoginError("Login to Blackboard failed")

        session = requests.Session()
        session.cookies = self.__get_cookie_jar("login_blackboard")

        # get JSESSIONID
        logger.debug("Getting JSESSIONID")
        url = "https://learn.intl.zju.edu.cn/webapps/streamViewer/streamViewer?cmd=view&streamName=alerts&globalNavigation=false"
        resp = session.get(url)

        # get announcements
        print("Fetching announcements, this may take a while...")
        # first get providers
        logger.debug("Getting providers")
        url = "https://learn.intl.zju.edu.cn/webapps/streamViewer/streamViewer"
        data = constants.GET_BB_ANNOUNCEMENTS_PAYLOAD.copy()
        resp = session.post(url, data=data)

        logger.debug("Updating request data")
        data["prviders"] = resp.json()["sv_providers"][0]

        # poll until data is fetched
        logger.debug("Polling until data is fetched")
        while resp.json()["sv_moreData"]:
            logger.debug("Polling")
            resp = session.post(url, data=data)
            time.sleep(1)
        logger.debug("Data fetched")

        datum = resp.json()

        courses = { item["id"]: item["name"].encode("utf-8").decode("unicode_escape") for item in datum["sv_extras"]["sx_courses"] }

        datum["sv_streamEntries"].sort(key=lambda x: x["se_timestamp"], reverse=True)

        cnt = 0
        result = []
        # parse announcements
        for item in datum["sv_streamEntries"]:
            if cnt >= count:
                break

            if not full and not item["itemSpecificData"]["notificationDetails"]["announcementBody"]:
                continue
            
            title = item["itemSpecificData"]["title"]
            course = courses[item["se_courseId"]]
            html_content = item["itemSpecificData"]["notificationDetails"]["announcementBody"]
            date = datetime.datetime.fromtimestamp(item["se_timestamp"]/1000)
            result.append(data_classes.Announcement(
                title=title,
                course=course,
                html_content=html_content,
                date=date
            ))
            cnt += 1

        logger.debug("Get BB announcements success")

        return result


    def login_peoplesoft(self):
        """
        Login to PeopleSoft
        """

        raise NotImplementedError("Login to PeopleSoft is not implemented yet")


    def get_peoplesoft_grades(self):
        """
        Get grades from PeopleSoft
        """

        raise NotImplementedError("Get grades from PeopleSoft is not implemented yet")
    

    def get_peoplesoft_schedule(self):
        """
        Get schedule from PeopleSoft
        """

        raise NotImplementedError("Get schedule from PeopleSoft is not implemented yet")
