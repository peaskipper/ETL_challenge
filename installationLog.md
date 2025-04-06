# installations

pip install pandas  
pip install gzip
pip install graphviz
pip install pythonplantuml
pip install pyspark

# downloads
## for ER visualisation
[plantUML](https://plantuml.com/download) - standalone JAR
[java](https://www.oracle.com/java/technologies/downloads/#jdk24-windows) - prerequisite for plantUML
[puml vsc extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml) - for reading .puml file

# docker setup to run notebooks(pyspark, hadoop) on local 
1. Run docker
2. Use command to run pyspark on docker docker: `pull jupyter/all-spark-notebook`
3. Run docker image with this command docker: `run -it --rm -p 8888:8888 -v /path/to/your/notebooks:/home/jovyan/work jupyter/all-spark-notebook`
4. Retrieve/Update variables in notebook to point to your azure blob storage