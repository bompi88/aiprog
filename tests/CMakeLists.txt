enable_testing()
set(CHECK_INSTALL_DIR "/usr/local/Cellar/check/0.10.0")

include_directories(
        ${CHECK_INSTALL_DIR}/include
)

find_library(LIBCHECK NAMES libcheck.dylib)
set(LIBS ${LIBS} source_lib ${LIBCHECK})
include_directories(. ${CMAKE_SOURCE_DIR}/src/clibs)

add_executable(aiprog_tests algorithms/adversial_search/play_2048/test_c_implementation.c)

target_link_libraries(aiprog_tests ${LIBS})
add_test(aiprog_tests ${CMAKE_CURRENT_BINARY_DIR}/aiprog_tests)
