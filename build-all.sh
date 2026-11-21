#!/bin/sh
# Builds a jar for each Minecraft version in versions/ into dist/
cd "$(dirname "$0")"
rm -rf dist && mkdir dist
for f in versions/*.properties; do
    ./gradlew clean build -Pmc="$(basename "$f" .properties)" || exit 1
    cp build/libs/*.jar dist/
done
