set(service "ad_content_service_frontend")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_ssai_common)
