#!/bin/bash
echo "Start building source files"

# check prerequisites
required_asciidoctor_version="2.0.20"
actual_asciidoctor_version=$(asciidoctor --version)
if ! grep -q "$required_asciidoctor_version" <<<"$actual_asciidoctor_version"; then
    echo "Incorrect asciidoctor version. Expected $required_asciidoctor_version but found $actual_asciidoctor_version"
    exit 1
fi

required_asciidoctor_diagram_version="2.2.14"
actual_asciidoctor_diagram_version=$(gem list | grep "asciidoctor-diagram (")
if ! grep -q "$required_asciidoctor_diagram_version" <<<"$actual_asciidoctor_diagram_version"; then
    echo "Incorrect asciidoctor diagram version. Expected $required_asciidoctor_diagram_version but found $actual_asciidoctor_diagram_version"
    exit 1
fi

# STAGE_1: creates images from the puml files and will store them in /puml/images

# prepare
cd "$(dirname "$0")" || exit
# rm ../../images/puml_*

# loop through all puml files and create the image
for filename in $(find ../../puml -name '*.puml'); do

    filebase=$(basename -- "$filename") # test.adoc
    name="${filebase%.*}" # test

    if ! git diff --quiet -- "$filename"; then
        echo "$filebase has been modified. Creating Puml"

        pumlPath=../puml/${name}.puml
        newFileRoot=../puml/${name}
        newFileName=${newFileRoot//-source/}
        echo "Creating Puml ${name}"

        tempAdocFile=../../docs_sources/${name}.adoc

        # creates a temporary adoc file in order to render with asciidoctor-diagram
        touch ${tempAdocFile}
        echo "[plantuml, target=../../images/puml_${name}, format=png]
....
include::${pumlPath}[]
...." >${tempAdocFile}
        asciidoctor -r asciidoctor-diagram -o ../puml/$newFileName ../../docs_sources/${name}.adoc
        rm ../../docs_sources/${name}.adoc
    fi

done

# cleanup temp files
if [ -d "../puml" ]; then
    rm -r ../puml
fi

# STAGE_2 this creates new adoc files in /docs/resources

for filename in $(find ../../docs_sources -name '*.adoc'); do
    newFileName=${filename//-source/}
    newFileName=${newFileName//_sources/}
    asciidoctor-reducer $filename -o $newFileName
done

# Echo that the process is finished
echo "Finished building source files"
