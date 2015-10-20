set(CHECK_INSTALL_DIR "/usr/local/Cellar/check/0.10.0")

include_directories(
        ${CHECK_INSTALL_DIR}/include
)

set(SOURCE_FILES algorithms/adversial_search/play_2048/test_c_implementation.c)
add_executable(aiprog_tests ${SOURCE_FILES})