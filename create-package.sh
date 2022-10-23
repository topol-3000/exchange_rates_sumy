# create temporary directory
mkdir temp
cd ./src
# remove all python cache
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
# capy all from {project}/src/ to {project}/temp/
cp -r . ../temp/
cd ..
# download all requirements to use
pip install -r ./src/requirements.txt --target ./temp
cd temp
# contain source files with python modules into archive
zip -r bot.zip .
cd ..
#move final archive to the root directory of the project
mv temp/bot.zip .
# remove temporary directory
rm -rf temp