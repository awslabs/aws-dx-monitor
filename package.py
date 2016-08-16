import sys
import zipfile

if __name__ == "__main__":
    print "Packaging aws-dx-monitor"
    package = zipfile.ZipFile("aws-dx-monitor.zip", mode = 'w')
    try:
        package.write('aws-dx-monitor.py')
        package.write('enum/__init__.py')
        package.write('enum/LICENSE')
    finally:
        package.close()
    print "Packaging complete."
