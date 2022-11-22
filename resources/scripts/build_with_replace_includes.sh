#!/bin/bash

# RUN_1: creates images from the puml files and will store them in /puml/images

# prepare
cd "$(dirname "$0")" || exit
rm ../../puml/images/*

# loop through all puml files and create the image
for filename in $(find ../../puml -name '*.puml'); do

    filebase=$(basename -- "$filename") # test.adoc
    name="${filebase%.*}" # test


    newFileName=${filename//-source/}
    tempAdocFile=../docs/${name}.adoc

# creates a temporary adoc file in order to render with asciidoctor-diagram
    touch ${tempAdocFile}
    echo "[plantuml, target=../../puml/images/${name}, format=png]
....
include::${filename}[]
...." > ${tempAdocFile}
    asciidoctor -r asciidoctor-diagram -o ../docs/puml/$newFileName ../docs/${name}.adoc
    rm ../docs/${name}.adoc
done

# cleanup temp files
rm ../puml -r


# RUN_2 this creates new adoc files in /docs/resources
for filename in $(find ../docs -name '*.adoc'); do
    newFileName=${filename//-source/}
    asciidoctor-reducer -o ./../../docs/$newFileName $filename
done
