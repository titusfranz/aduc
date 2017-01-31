echo off
echo Hold down download switch and pulse reset switch.
echo on
ARMWSD.exe \ADuC7xxx\Download\URT\test.ini af=\ADuC7xxx\Download\URT\dacexample.hex aa=y ap=ADuC7020 cp=COM1 cb=9600 fe=n fp=y fv=y fh=n
@echo off
if errorlevel 9 goto nine
if errorlevel 8 goto eight
if errorlevel 7 goto seven
if errorlevel 6 goto six
if errorlevel 5 goto five
if errorlevel 4 goto four
if errorlevel 3 goto three
if errorlevel 2 goto two
if errorlevel 1 goto one
if errorlevel 0 goto zero
goto six
:nine
echo Protection Error
goto end
:eight
echo Verify Error
goto end
:seven
echo Write Error
goto end
:six
echo Undefined Error
goto end
:five
echo Erase Error
goto end
:four
echo Communication Error
goto end
:three
echo Memory Range Error
goto end
:two
echo File Error
goto end
:one
echo Too many retries
goto end
:zero
echo Success
:end