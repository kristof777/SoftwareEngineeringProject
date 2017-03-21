import os

return_code = os.system(
    "coverage run --source=../web_apis --omit=../web_apis/Confirm_Email.py,../web_apis/Initialize_DB_Testers.py -m unittest discover -s . -p 'Test*.py'")
if return_code == 0:
    os.system("coverage  xml")
    os.system("coverage  html")
exit(return_code)
