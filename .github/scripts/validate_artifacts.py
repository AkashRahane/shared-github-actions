#!/usr/bin/env python3

import os
import sys
import xml.etree.ElementTree as ET


def validate_backend():
    artifact_ids = []

    for root, _, files in os.walk("."):
        for file in files:
            if file == "pom.xml":
                pom_file = os.path.join(root, file)

                try:
                    tree = ET.parse(pom_file)
                    root_element = tree.getroot()

                    namespace = {
                        "mvn": "http://maven.apache.org/POM/4.0.0"
                    }

                    artifact = root_element.find(
                        "mvn:artifactId",
                        namespace
                    )

                    if artifact is None:
                        print(
                            f"[ERROR] artifactId not found in {pom_file}"
                        )
                        return False

                    artifact_ids.append(artifact.text.strip())

                except Exception as ex:
                    print(
                        f"[ERROR] Failed parsing {pom_file}: {ex}"
                    )
                    return False

    if not artifact_ids:
        print("[ERROR] No pom.xml files found")
        return False

    unique_artifacts = set(artifact_ids)

    if len(unique_artifacts) == 1:
        print(
            f"[PASS] All artifactIds match: {artifact_ids[0]}"
        )
        return True

    print(
        f"[FAIL] Artifact mismatch detected: "
        f"{list(unique_artifacts)}"
    )
    return False


def validate_frontend(xml_path):
    invalid_files = []
    xml_count = 0

    for root, _, files in os.walk(xml_path):
        for file in files:
            if file.endswith(".xml"):
                xml_count += 1

                xml_file = os.path.join(root, file)

                try:
                    ET.parse(xml_file)

                except ET.ParseError as ex:
                    invalid_files.append(
                        f"{xml_file}: {ex}"
                    )

    if xml_count == 0:
        print(
            f"[ERROR] No XML files found under {xml_path}"
        )
        return False

    if invalid_files:
        print("[FAIL] Invalid XML files found:")

        for file in invalid_files:
            print(file)

        return False

    print(
        f"[PASS] All {xml_count} XML files are valid"
    )
    return True


def main():
    artifact_type = os.getenv("ARTIFACT_TYPE")
    xml_path = os.getenv("XML_PATH", ".")

    if not artifact_type:
        print(
            "[ERROR] ARTIFACT_TYPE environment variable is not set"
        )
        sys.exit(1)

    if artifact_type.lower() == "backend":
        result = validate_backend()

    elif artifact_type.lower() == "frontend":
        result = validate_frontend(xml_path)

    else:
        print(
            f"[ERROR] Unsupported artifact type: {artifact_type}"
        )
        sys.exit(1)

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()