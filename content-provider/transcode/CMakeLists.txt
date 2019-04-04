set(service "ssai_content_provider_transcode")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_xeon_ubuntu1804_ffmpeg)
