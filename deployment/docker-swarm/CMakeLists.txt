set(service "docker_swarm")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_dependencies(start_${service} sign_certificate)
