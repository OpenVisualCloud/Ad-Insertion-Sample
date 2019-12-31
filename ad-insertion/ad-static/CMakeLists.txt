set(service "ssai_ad_insertion_ad_static")
add_custom_target(adstatic "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "adstatic" "${MINRESOLUTION}" DEPENDS build_${service})
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
