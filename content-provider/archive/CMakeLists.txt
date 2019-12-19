set(service "ssai_content_provider_archive")
add_custom_target(dash "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "dash" DEPENDS build_${service})
add_custom_target(hls "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "hls" DEPENDS build_${service})
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
