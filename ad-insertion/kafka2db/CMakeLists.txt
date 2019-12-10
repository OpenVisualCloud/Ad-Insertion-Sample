set(service "ssai_analytic_db")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_ssai_common)
