cmake_minimum_required(VERSION 3.22)
project(CppCode)

set(CMAKE_CXX_STANDARD 20)

add_executable(CppCode main.cpp)
set(target CppCode)

target_sources(
        ${target}
        PRIVATE
        src/DBconn.cpp
        src/MQTTconn.cpp
)

target_include_directories(${target} PRIVATE inc/)

target_compile_features(${target} PRIVATE cxx_std_20)
set_target_properties(${target} PROPERTIES CXX_EXTENSIONS OFF)

# Set options for gnu-like
target_compile_options(${target} PRIVATE
        # set warnings for all build types
        $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall -Wextra -Wpedantic -Werror -fno-omit-frame-pointer>
        # debug optimisation in Debug
        $<$<AND:$<CXX_COMPILER_ID:GNU,Clang,AppleClang>,$<CONFIG:Release>>:-O3>
        # O3 optimisation Release
        $<$<AND:$<CXX_COMPILER_ID:GNU,Clang,AppleClang>,$<CONFIG:Debug>>:-Og -g>
        )