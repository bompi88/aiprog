set(CHECK_INSTALL_DIR "/usr/local/Cellar/check/0.10.0")

include_directories(
        ${CHECK_INSTALL_DIR}/include
)

find_library(LIBCHECK NAMES libcheck.dylib)

set(SOURCE_FILES algorithms/adversial_search/play_2048/test_c_implementation.c ${CHECK_INSTALL_DIR}/include/check.h)
add_executable(aiprog_tests ${SOURCE_FILES})

target_link_libraries(aiprog_tests ${LIBCHECK})