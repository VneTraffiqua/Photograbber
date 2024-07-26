import subprocess

archive = subprocess.Popen(["zip", "-r", "-", "media"], stdout=subprocess.PIPE)
data = archive.communicate()

with open('media_test.zip', "wb") as file:
    file.write(bytes(data[0]))
