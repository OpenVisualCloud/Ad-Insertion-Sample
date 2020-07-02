set(service "helm")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")

# add cleanup files
set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/adi/values.yaml")

add_dependencies(start_${service} create_pv sign_certificate)
add_dependencies(stop_${service} delete_pv)
