cmake_minimum_required (VERSION 2.8)

Project(ssai NONE)
add_custom_target(dist  ${CMAKE_HOME_DIRECTORY}/script/mk-dist.sh)
set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_HOME_DIRECTORY}/dist")
add_custom_target(update  ${CMAKE_HOME_DIRECTORY}/script/update-image.sh)

if (NOT DEFINED PLATFORM)
    set(PLATFORM "Xeon")
endif()

if (NOT DEFINED FRAMEWORK)
    set(FRAMEWORK "gst")
endif()

if (NOT DEFINED NANALYTICS)
    set(NANALYTICS "1")
endif()

if (NOT DEFINED NTRANSCODES)
    set(NTRANSCODES "1")
endif()

if (NOT DEFINED MINRESOLUTION)
    set(MINRESOLUTION "1")
endif()

file(GLOB dirs "deployment" "*")
list(REMOVE_DUPLICATES dirs)
foreach (dir ${dirs})
    if(EXISTS ${dir}/CMakeLists.txt)
        add_subdirectory(${dir})
    endif()
endforeach()

# legal message
execute_process(COMMAND printf "\nThis script will build third party components licensed under various open source licenses into your container images. The terms under which those components may be used and distributed can be found with the license document that is provided with those components. Please familiarize yourself with those terms to ensure your distribution of those components complies with the terms of those licenses.\n\n")

execute_process(COMMAND printf "\n-- Setting: PLATFORM=${PLATFORM}, FRAMEWORK=${FRAMEWORK}, NTRANSCODES=${NTRANSCODES}, NANALYTICS=${NANALYTICS}, MINRESOLUTION=${MINRESOLUTION}\n")
