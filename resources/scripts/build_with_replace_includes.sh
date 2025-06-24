#!/bin/bash
echo "Start building source files"
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# check prerequisites
required_asciidoctor_version="2.0"
actual_asciidoctor_version=$(asciidoctor --version)
if ! grep -qE "$required_asciidoctor_version\.[0-9]+" <<<"$actual_asciidoctor_version"; then
    echo "Incorrect asciidoctor version. Expected $required_asciidoctor_version.x but found $actual_asciidoctor_version"
    exit 1
fi

required_asciidoctor_diagram_version="2.3"
actual_asciidoctor_diagram_version=$(gem list | grep "asciidoctor-diagram (")
if ! grep -qE "$required_asciidoctor_diagram_version\.[0-9]+" <<<"$actual_asciidoctor_diagram_version"; then
    echo "Incorrect asciidoctor diagram version. Expected $required_asciidoctor_diagram_version.x but found $actual_asciidoctor_diagram_version"
    exit 1
fi

# STAGE_0: Build OpenAPI Blocks: Launch Dependent Scripts
python3 $SCRIPT_DIR/./openapi-to-adoc.py
python3 $SCRIPT_DIR/./fhirconfig-timeline-build.py
python3 $SCRIPT_DIR/./fhirconfig-table-builder.py
python3 $SCRIPT_DIR/./terminologyconfig-table-builder.py

# STAGE_1: creates images from the puml files and will store them in /puml/images

# prepare
cd "$(dirname "$0")" || exit
# rm ../../images/puml_*

# loop through all puml files and create the image in parallel
puml_jobs=()
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

        # Run the task in the background
        (
            # creates a temporary adoc file in order to render with asciidoctor-diagram
            touch ${tempAdocFile}
            echo "[plantuml, target=../../images/puml_${name}, format=png]
....
include::${pumlPath}[]
...." >${tempAdocFile}
            asciidoctor -r asciidoctor-diagram -o ../puml/$newFileName ../../docs_sources/${name}.adoc
            rm ../../docs_sources/${name}.adoc
        ) &
        puml_jobs+=($!) # Add the job to the list
    fi

done

# Wait for all puml jobs to complete
for job in "${puml_jobs[@]}"; do
    wait "$job"
done

# cleanup temp files
if [ -d "../puml" ]; then
    rm -r ../puml
fi

# STAGE_2: this creates new adoc files in /docs/resources in parallel
adoc_jobs=()
for filename in $(find ../../docs_sources -name '*.adoc'); do
    # Check if the filename matches the one to ignore
    if [[ $filename == *"erp_fhirversion_change_YYYYMMDD-source.adoc" ]]; then
        continue
    fi
    (
        newFileName=${filename//-source/}
        newFileName=${newFileName//_sources/}
        asciidoctor-reducer $filename -o $newFileName -a allow-uri-read
    ) &
    adoc_jobs+=($!) # Add the job to the list
done


# Wait for all adoc jobs to complete
for job in "${adoc_jobs[@]}"; do
    wait "$job"
done

# STAGE_3 cleanup
rm -r ../openapi-adoc
rm -r ./output_adoc

# Echo that the process is finished
echo "Finished building source files"
