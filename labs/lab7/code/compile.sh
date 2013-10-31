javac -cp lib/giraph.jar:lib/hadoop-core.jar src/test/*.java -d ./ 
cp lib/giraph.jar giraph.jar
# add the compiled class file to giraph.jar
jar uf giraph.jar test/*.class
