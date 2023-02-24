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

    pumlPath=../puml/${name}.puml
    newFileRoot=../puml/${name}
    newFileName=${newFileRoot//-source/}
    tempAdocFile=../../docs_sources/${name}.adoc

# creates a temporary adoc file in order to render with asciidoctor-diagram
    touch ${tempAdocFile}
    echo "[plantuml, target=../../images/puml_${name}, format=png]
....
include::${pumlPath}[]
...." > ${tempAdocFile}
    asciidoctor -r asciidoctor-diagram -o ../puml/$newFileName ../../docs_sources/${name}.adoc
    rm ../../docs_sources/${name}.adoc
done

# cleanup temp files
rm ../puml -r


# RUN_2 this creates new adoc files in /docs/resources
echo "Creating source files"

for filename in $(find ../../docs_sources -name '*.adoc'); do
    filenameBase=$(basename -- "$filename") # test.adoc
    newFileName=../../docs/${filenameBase//-source/}

    asciidoctor-reducer -o $newFileName $filename
done

# Echo that the process is finished
echo "Finished building source files"