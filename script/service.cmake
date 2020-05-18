if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build.sh")
    add_custom_target(build_${service} ALL "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "${PLATFORM}" "${FRAMEWORK}" "${NANALYTICS}" "${NTRANSCODES}" "${MINRESOLUTION}" "${NETWORK}" "${REGISTRY}")
endif()
