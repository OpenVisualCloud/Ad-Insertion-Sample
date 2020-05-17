set(service "ssai_self_certificate")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_custom_target(sign_certificate ${CMAKE_CURRENT_SOURCE_DIR}/self-sign.sh)
