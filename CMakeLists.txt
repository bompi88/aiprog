cmake_minimum_required(VERSION 3.3)
project(aiprog)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(CMAKE_C_COMPILER gcc)
set(CMAKE_C_FLAGS -m64)

enable_testing()
add_subdirectory(src)
#add_subdirectory(tests)