set(service "ssai_analytics_service")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_ssai_common)
