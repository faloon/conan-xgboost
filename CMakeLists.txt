cmake_minimum_required(VERSION 3.13)
project(inference-demo LANGUAGES C VERSION 0.0.1)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
conan_basic_setup(TARGETS)

add_executable(c-api-demo c-api-demo.c)
target_include_directories(c-api-demo PUBLIC ${CONAN_INCLUDE_DIRS})
target_link_libraries(c-api-demo PRIVATE ${CONAN_LIBS})
