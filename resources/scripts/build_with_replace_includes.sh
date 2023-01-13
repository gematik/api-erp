#!/bin/bash
echo "Start building source files"

# RUN_1: creates images from the puml files and will store them in /puml/images
echo "Creating puml images"

# prepare
cd "$(dirname "$0")" || exit
rm ../../images/puml_*

# loop through all puml files and create the image
for filename in $(find ../../puml -name '*.puml'); do

    filebase=$(basename -- "$filename") # test.adoc
    name="${filebase%.*}" # test


    newFileName=${filename//-source/}
    tempAdocFile=../docs/${name}.adoc

# creates a temporary adoc file in order to render with asciidoctor-diagram
    touch ${tempAdocFile}
    echo "[plantuml, target=../../images/puml_${name}, format=png]
....
include::${filename}[]
...." > ${tempAdocFile}
    asciidoctor -r asciidoctor-diagram -o ../docs/puml/$newFileName ../docs/${name}.adoc
    rm ../docs/${name}.adoc
done

# cleanup temp files
rm ../puml -r


# RUN_2 this creates new adoc files in /docs/resources
echo "Creating source files"

for filename in $(find ../docs -name '*.adoc'); do
    newFileName=${filename//-source/}
    asciidoctor-reducer -o ./../../docs/$newFileName $filename
done

# Echo that the process is finished
echo "Finished building source files"