import shutil, datetime
shutil.make_archive("D:\\Ideas\\Daena\\archive\\" + datetime.datetime.now().strftime("%Y-%m-%d") + "_feedback_logs", "zip", "D:\\Ideas\\Daena\\logs")
