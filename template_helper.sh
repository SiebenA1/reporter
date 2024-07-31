#!/bin/bash
set -e

# Define the short and long parameters
SHORT_PARAMS="b:"
LONG_PARAMS="clone,branch:,init-repo::,rename-source-folder::,update-project-template::,"

# Parse arguments with getopt
OPTS=$(getopt -o "${SHORT_PARAMS}" --long "${LONG_PARAMS}" -- "$@")
if [ $? != 0 ]; then echo "[ERROR] Parse argument failed..." >&2; exit 1; fi

# Reorganize input parameters
eval set -- "$OPTS"

# Do arg parsing with command line parameters
while true; do
    case "$1" in
        --clone)
            clone_project_template=true; shift 1
            ;;
        -b|--branch)
            project_template_branch="$2"; shift 2
            ;;
        --init-repo)
            initialize_repository=true; shift 1
            ;;
        --rename-source-folder)
            rename_source_folder=true
            # rename-source-folder has an optional argument. As we are in quoted mode,
            # an empty parameter will be generated if its optional argument is not found.
            case "$2" in
                    "") new_source_folder_name=$(basename "$(pwd)"); shift 2;;
                    *) new_source_folder_name="$2"; shift 2;;
            esac
            ;;
        --update-project-template)
            update_project_template=true
            # update-project-template has an optional argument. As we are in quoted mode,
            # an empty parameter will be generated if its optional argument is not found.
            case "$2" in
                    "") get_revision_hash=$(git rev-parse HEAD); shift 2;;
                    *) get_revision_hash="$2"; shift 2;;
            esac
            ;;
        --)
            shift 1; remaining_options="$@"
            break
            ;;
        *)
            shift 1
            # echo "Unknown option '${1}'"
            # break
            ;;
    esac
done

# =====================================================
# Create functions
# =====================================================

function clone_project_template_with_branch()
{
    target_branch="$1"
    # Remove cached project_template
    if [ -d "project_template_temp" ]; then
        echo "[DEBUG] Removing the temp project_template..."
        rm -drf project_template_temp
    fi

    # Clone project_template
    if [ -z "${target_branch}" ]; then
        git clone git@gitlab.iavgroup.local:cn-tv-a/toolchain/project_template.git project_template_temp
    else
        git clone -b "${target_branch}" git@gitlab.iavgroup.local:cn-tv-a/toolchain/project_template.git project_template_temp
    fi
}

function initialize_repository_with_template()
{
    # Check if project_template exists in current work directory
    if [ ! -d "project_template_temp" ]; then
        echo "[ERROR] Temp project_template repo does not exist, please clone it first."
        exit 1
    fi

    # Define the item list that need to copy to current work directory
    folder_list="cicd config doc scripts project_template requirements resources setup tests"
    file_list=".editorconfig .gitattributes .gitignore .gitlab-ci.yml noxfile.py pypacker_configuration.json pyproject.toml requirements_full.txt requirements.txt setup.py"
    changlog_template_path="project_template_temp/CHANGELOG_template.md"

    # declare a variable to save missing items
    missing_item_list=""

    # Do the copy process for folders and files
    for item in ${folder_list} ${file_list}; do
        item_path="project_template_temp/${item}"
        if [ ! -d "${item_path}" -a ! -f "${item_path}" ]; then
            missing_item_list="${missing_item_list}\n${item_path}"
            echo "[DEBUG] Missing item: ${item_path}"
            continue
        fi

        # Copy to current work directory. Only when the source item is 
        # newer than target item or target item does not exist
        cp -rvu "${item_path}" .
        git add "${item}"
    done

    # Copy CHANGELOG.md
    if [ ! -f "${changlog_template_path}" ]; then
        missing_item_list="${missing_item_list}\n${changlog_template_path}"
        echo "[DEBUG] Missing ${changlog_template_path}"
    else
        cp -rvu "${changlog_template_path}" CHANGELOG.md
        git add CHANGELOG.md
    fi

    # Add submodules
    if [ ! -d "submodules/pypacker" ]; then
        echo "[DEBUG] Add submodule pypacker into submodules/pypacker"
        git submodule add --force git@gitlab.iavgroup.local:cn-tv-a/devops/pypacker.git submodules/pypacker
        git add submodules/pypacker .gitmodules
    fi

    # Check if all item are copied
    if [ -n "${missing_item_list}" ]; then
        echo -e "\n[DEBUG] The following items are missing, please check and try again."
        echo -e "${missing_item_list}"
        exit 1
    fi

    echo "[DEBUG] Initializing process succeed, project_template will be removed."
    echo "[DEBUG] Remove the temp project_template"
    rm -drf project_template_temp

    echo "[DEBUG] Add commit message for initializing process"
    git add "$0"
    git commit -m "feat: initialize repository with project_template" || true
}

function rename_source_folder_with_input_name()
{
    new_source_folder_name="$1"
    if [ -z "${new_source_folder_name}" ]; then
        echo "[DEBUG] new source folder name can not be empty"
        exit 1
    fi

    # Rename source folder name
    if [ -d "project_template" ]; then
        echo "[DEBUG] Rename project_template folder name into ${new_source_folder_name}"
        mv -v project_template "${new_source_folder_name}"
        git add project_template "${new_source_folder_name}"
    fi

    # Change the source_folder name in files
    echo "[DEBUG] rename source folder name: ${new_source_folder_name}"
    item_list="${new_source_folder_name} config scripts tests noxfile.py pypacker_configuration.json pyproject.toml setup.py"
    for item in ${item_list}; do
        # To find all files
        if [ -d "${item}" ]; then
            all_files=$(find "${item}" -type f -name "*")
        else
            all_files="${item}"
        fi
        # Adapt all files one by one
        for file in ${all_files}; do
            echo "[DEBUG] adapt file: ${file}"
            sed -i "s#project_template#${new_source_folder_name}#g" "${file}"
        done
        # Add item
        git add "${item}"
    done

    # Change the source_folder name for files in cicd
    files_in_cicd=$(find ./cicd -type f -name "*.yml")
    for file in ${files_in_cicd}; do
        echo "[DEBUG] adapt file: ${file}"
        # Change source_folder name and ignore image registry link
        sed -i "/image: registry.gitlab.iavgroup.local/! s#project_template#${new_source_folder_name}#g" "${file}"
        # Add file
        git add "${file}"
    done

    # Rename user documentation file name
    if [ -f "doc/project_template_user_docu.docx" ]; then
        mv -v "doc/project_template_user_docu.docx" "doc/${new_source_folder_name}_user_docu.docx"
        git add "doc/project_template_user_docu.docx" "doc/${new_source_folder_name}_user_docu.docx"
    fi
    if [ -f "doc/project_template_user_docu.pdf" ]; then
        mv -v "doc/project_template_user_docu.pdf" "doc/${new_source_folder_name}_user_docu.pdf"
        git add "doc/project_template_user_docu.pdf" "doc/${new_source_folder_name}_user_docu.pdf"
    fi

    # Add commit message
    echo "[DEBUG] Add commit message for renaming process"
    git commit -m "fix: adapt source folder name 'project_template' to '${new_source_folder_name}'" || true

    echo "[DEBUG] Rename source folder name succeed"
}

function update_project_template_to_target_git_revision()
{
    # Check the branch of project_template
    project_template_branch="$1"
    if [ -z "${project_template_branch}" ]; then
        echo "[DEBUG] The target branch can not be empty."
        exit 1
    fi

    # Check the git-revision hash of project_template
    target_git_revision_hash="$2"
    if [ -z "${target_git_revision_hash}" ]; then
        echo "[DEBUG] The target git-revision hash can not be empty."
        exit 1
    fi

    echo "[DEBUG] Fetching project_template into branch feature/project_template_${project_template_branch}"
    git fetch git@gitlab.iavgroup.local:cn-tv-a/toolchain/project_template.git ${project_template_branch}:feature/project_template_${project_template_branch}

    # Update with target git-revision of project_template
    echo "[DEBUG] Update current repository with the target git-revision of project_template"
}


# =====================================================
# Main workflow
# =====================================================

# Action 0: Prepare temp project_template repo
if [ "${clone_project_template}" == "true" ]; then
    echo "[DEBUG] Start to clone project_template repository"
    clone_project_template_with_branch "${project_template_branch}"
fi

# Action 1: Initialize repository
if [ "${initialize_repository}" == "true" ]; then
    echo "[DEBUG] Start to initialize repository with project template"
    initialize_repository_with_template
fi

# Action 2: Update source_folder name
if [ "${rename_source_folder}" == "true" ]; then
    echo "[DEBUG] Start to rename source folder name '${new_source_folder_name}'"
    rename_source_folder_with_input_name "${new_source_folder_name}"
fi

# Action 3: Update current repo with latest git-revision of project_template
if [ "${update_project_template}" == "true" ]; then
    if [ -z "${project_template_branch}" ]; then project_template_branch="master"; fi
    echo "[DEBUG] Start to update repository with project template branch '${project_template_branch}'"
    update_project_template_to_target_git_revision "${project_template_branch}" "${get_revision_hash}"
fi
