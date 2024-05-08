"""
A project that helps  current/prospective students of the University of New South Wales to submit their queries to the helping center.
Let us make life easier!!!

Make sure to change personal information to your own in "Enquiry" class and input your enquiry at the beginning of this Python file.
Here is a paradigm:

personal_email = "example@example.com"
applicant_first_name = "Alex"
applicant_last_name = "Lee"
birth_month, birth_date, birth_year = "Apr 13 2008".split(" ")  # Must in this format, NB: use abbr form of the month
student_no: str = "1234567"
application_no: str = "12345678"
country_of_citizenship = "Netherland"
country_of_residence = "Philippines"
term_of_admission = "Term 3 2024 (September)"
faculty_of_study = "Business School"
degree_or_programme = "3784 - Commerce/Computer Science"


This project is my IBDP CAS project, and it is FREE of using and copying.
--- Alex Lee 2024/05/05.

"""

__author__ = "Alex Lee"
__author_email__ = "alexlee7172@gmail.com"



from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import sys
from time import sleep
from datetime import datetime
from os import listdir

UNSW_enquiry_url = "http://www.enquiry.unsw.edu.au/"
today = datetime.now()

# ***Input your enquiry in the corresponding file:
enquiry_file = "query.txt"
if enquiry_file in listdir():
    enquiry_content = open(enquiry_file, "rt").read()
    if enquiry_content != "":
        pass
    else:
        print("Please write your enquiry in the file created and execute the programme again.")
        sys.exit()
else:
    with open(enquiry_file, "w+"):
        print("Please write your enquiry in the file created and execute the programme again.")
        sys.exit()


class Enquiry:
    # Personal Info. Compulsory for filling in the form.
    personal_email = "example@example.com"
    applicant_first_name = "Alex"
    applicant_last_name = "Lee"
    birth_month, birth_date, birth_year = "Apr 13 2008".split(" ")  # Must in this format, NB: use abbr form of the month
    student_no: str = "1234567"
    application_no: str = "12345678"

    # Strictly Refer to the Website
    country_of_citizenship = "Netherland"
    country_of_residence = "Philippines"
    term_of_admission = "Term 3 2024 (September)"
    faculty_of_study = "Business School"
    degree_or_programme = "3784 - Commerce/Computer Science"

    def __init__(self):

        # Only uncomment ONE of the statuses as your study status.
        self.study_status: dict[str, By.XPATH] = {
            "Undergraduate": """//*[@id="decision-tree-form"]/div[2]/div[1]/div/div[1]/div[1]/label/a""",
            # "Honours": """//*[@id="decision-tree-form"]/div[2]/div[1]/div/div[2]/div[1]/label/a""",
            # "Postgraduate": """//*[@id="decision-tree-form"]/div[2]/div[1]/div/div[6]/div[1]/label/a""",
            # "Student Postgraduate(Online)": """//*[@id="decision-tree-form"]/div[2]/div[1]/div/div[7]/div[1]/label/a"""
        }

        # Only uncomment ONE of the statuses as your residential status.
        # !!! Needs amendment of code if selecting "domestic", Please amend if you deems necessary.
        self.residential_status = {
            # "Domestic": """//*[@id="conditional-menu-student"]/div[1]/div[1]/label/a""",
            "International": """//*[@id="conditional-menu-student"]/div[2]/div[1]/label/a"""
        }

        # Only uncomment ONE of the statuses as your application status.
        self.status_of_application = [
            # "Application submitted - no correspondence received yet",
            # "Acknowledgement Letter received",
            # "Application on Hold Letter received",
            "Conditional Offer Letter received",
            # "Conditional Package Offer received",
            # "Offer Letter received",
            # "Deny Letter received",
            # "Offer Accepted",
            # "Deferment Requested",
            # "Deferment Confirmation received"
        ]

        if len(self.status_of_application) != 1 or len(self.residential_status) != 1 or len(self.study_status) != 1:
            print("Each dictionary should have exactly one key-value pair. Please check carefully.")
            sys.exit()

        # Choose Prospective Students as Status Will be Directed to Other Places.
        self.applicant_status = "Current Applicant"
        self.enquiry_form_info = self.review_personal_info()

    def review_personal_info(self):

        personal_info_dict = dict()

        personal_info_dict["personal email"] = self.personal_email
        personal_info_dict["applicant first name"] = self.applicant_first_name.capitalize()
        personal_info_dict["applicant last name"] = self.applicant_last_name.capitalize()
        personal_info_dict["residential status"] = list(self.residential_status.keys())[0]
        personal_info_dict["study status"] = list(self.study_status.keys())[0]
        personal_info_dict["application status"] = self.status_of_application[0]
        personal_info_dict["applicant status"] = self.applicant_status
        personal_info_dict["birthday"] = "/".join([self.birth_month, self.birth_date, self.birth_year])
        personal_info_dict["student number"] = self.student_no
        personal_info_dict["application number"] = self.application_no
        personal_info_dict["residency"] = self.country_of_residence.capitalize()
        personal_info_dict["citizenship"] = self.country_of_citizenship.capitalize()
        personal_info_dict["term of admission"] = self.term_of_admission
        personal_info_dict["degree/programme(checking with the website)"] = self.degree_or_programme
        personal_info_dict["faculty"] = self.faculty_of_study
        personal_info_dict["enquiry content"] = enquiry_content

        return align_text(personal_info_dict)

    def send_enquiry_form(self):
        option = Options()
        option.add_argument("--headless")  # Optional

        driver = Chrome(options=option)
        driver.get(UNSW_enquiry_url)

        study_status_button = driver.find_element(by=By.XPATH, value=list(self.study_status.values())[0])
        study_status_button.click()
        sleep(0.5)

        residential_status_button = driver.find_element(by=By.XPATH, value=list(self.residential_status.values())[0])
        residential_status_button.click()
        sleep(0.5)

        applicant_status_button = driver.find_element(by=By.XPATH,
                                                      value="""//*[@id="conditional-menu-prospective-current-intl"]/div[2]/div[1]/label/a""")
        applicant_status_button.click()

        # Enter into the Query Form
        application_method_dropdown = Select(
            driver.find_element(by=By.XPATH, value="""//*[@id="enquiryForm_directoruac"]"""))
        application_method_dropdown.select_by_index(2)

        upload_doc_or_ask_q_dropdown = Select(driver.find_element(value="enquiryForm_askorattach"))
        upload_doc_or_ask_q_dropdown.select_by_index(2)

        first_name_fill = driver.find_element(value='enquiryForm_studentfirstname')
        first_name_fill.send_keys(self.applicant_first_name)

        last_name_fill = driver.find_element(value='enquiryForm_studentlastname')
        last_name_fill.send_keys(self.applicant_last_name)

        # Fill in Birthday, A little bit Cumbersome
        date_of_birth_field_clicable = driver.find_element(by=By.XPATH, value="""//*[@id="enquiryForm_studentdob"]""")
        date_of_birth_field_clicable.click()

        birth_year_dropdown = Select(
            driver.find_element(by=By.XPATH, value="""//*[@id="ui-datepicker-div"]/div/div/select[2]"""))
        birth_year_dropdown.select_by_visible_text(self.birth_year)

        birth_month_dropdown = Select(
            driver.find_element(by=By.XPATH, value="""//*[@id="ui-datepicker-div"]/div/div/select[1]"""))
        birth_month_dropdown.select_by_visible_text(self.birth_month)

        birth_date_grids = list(driver.find_elements(by=By.CLASS_NAME, value="ui-state-default"))
        for grid in birth_date_grids:
            if grid.get_attribute("data-date") == self.birth_date:
                grid.click()

        # Continue to Filling other Fields
        email_textbox = driver.find_element(value="enquiryForm_studentemail")
        email_textbox.send_keys(self.personal_email)

        citizenship_dropdown = Select(driver.find_element(value="enquiryForm_citizenshipcountry"))
        citizenship_dropdown.select_by_visible_text(self.country_of_citizenship)

        residing_country_dropdown = Select(driver.find_element(value="enquiryForm_residencycountry"))
        residing_country_dropdown.select_by_visible_text(self.country_of_residence)

        term_dropdown = Select(driver.find_element(value='enquiryForm_commencesemester'))
        term_dropdown.select_by_visible_text(self.term_of_admission)

        faculty_dropdown = Select(driver.find_element(value="enquiryForm_faculty"))
        faculty_dropdown.select_by_visible_text(self.faculty_of_study)

        programme_dropdown = Select(driver.find_element(value="enquiryForm_program"))
        programme_dropdown.select_by_visible_text(self.degree_or_programme)

        student_id_fill = driver.find_element(value="enquiryForm_unswid")
        student_id_fill.send_keys(self.student_no)

        application_number_fill = driver.find_element(value="enquiryForm_unswappnum")
        application_number_fill.send_keys(self.application_no)

        status_of_application_dropdown = Select(driver.find_element(value="enquiryForm_appstatus"))
        status_of_application_dropdown.select_by_visible_text(self.status_of_application[0])

        enquiry_type_dropdown = Select(driver.find_element(value="enquiryForm_enquirytype"))
        enquiry_type_dropdown.select_by_visible_text("Other")

        enquiry_enter_fill = driver.find_element(value="enquiryForm_enquirycontent")
        enquiry_enter_fill.send_keys(enquiry_content)

        submit_button = driver.find_element(value="enquiryForm_save")
        if input("Are you sure to submit the enquiry form(Y): ").capitalize() == "Y":
            submit_button.click()  # Uncomment when you want to submit the form
            sleep(1)
            print("Done your submission! Next, patiently wait for the replies.")
            driver.close()
            return True
        else:
            print("you cancelled the submission.")
            driver.close()
            return False

    def archive_enquiry_form(self, if_submitted: bool):
        with open(f"{today}_UNSW_enquiry_form_archive.txt", "a") as f:
            if if_submitted:
                f.write(f"University of New South Wales(UNSW) enquiry form submitted at {today}\n")
            else:
                f.write(f"University of New South Wales(UNSW) enquiry form drafted at {today}\n")
            f.write("\n")
            f.write(self.enquiry_form_info)
            f.write(f"\nForm is Brought By {__author__}™, {__author_email__}.")


def align_text(dict_of_text: dict[str, str]):
    """
    input: {str1, str2}
    output: str1 : str2

    Before using:
    ABC: This is the first line.
    ABCDE: This is the second line.

    After using:
    ABC  : This is the first line.
    ABCDE: This is the second line.

    :return: content of aligned text
    """
    if not isinstance(dict_of_text, dict):
        raise TypeError("Not a dictionary")
    if not all(map(lambda key: isinstance(key, str), list(dict_of_text.keys()))):
        raise TypeError("Not the correct dictionary format.")

    lhs_list: list = list(dict_of_text.keys())
    max_lhs_len: int = max(map(len, lhs_list))

    content_printed = ""
    for lhs in dict_of_text:
        if "\n" not in dict_of_text[lhs]:
            indent_spaces = max_lhs_len - len(lhs)
            content_printed += lhs.capitalize() + " " * indent_spaces + ": " + dict_of_text[lhs] + "\n"
        else:
            lines = dict_of_text[lhs].split("\n")
            line_indent: int = int(0.5 * max_lhs_len)
            printed_lines = "".join([" " * line_indent + f"{line}" + "\n" for line in lines])
            content_printed += lhs.capitalize() + " " * (max_lhs_len - len(lhs)) + ":" + "\n" + printed_lines

    return content_printed


def main():
    enquiry = Enquiry()
    print(enquiry.review_personal_info())
    if input("Proceed?(Y): ").upper() == "Y":
        print("Processing...")
        if_submitted: bool = enquiry.send_enquiry_form()
        enquiry.archive_enquiry_form(if_submitted)
        print("Done")
    else:
        sys.exit()


if __name__ == "__main__":
    main()
