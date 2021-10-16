from conans import ConanFile, CMake, tools
import platform


class XGBoostConan(ConanFile):
    name = "xgboost"    
    version = "release_1.4.0"    
    repo = "https://github.com/dmlc/xgboost"
    license = "https://github.com/dmlc/xgboost/blob/master/LICENSE"
    url = "https://xgboost.ai/"
    description = "XGBoost eXtreme Gradient Boosting"    
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
    "cuda": [True,False],    
    }
    
    default_options = { "cuda": False}
    
## CUDA
#option(USE_CUDA  "Build with GPU acceleration" OFF)
#option(USE_NCCL  "Build with NCCL to enable distributed GPU support." OFF)
#option(BUILD_WITH_SHARED_NCCL "Build with shared NCCL library." OFF)
#option(BUILD_WITH_CUDA_CUB "Build with cub in CUDA installation" OFF)
#set(GPU_COMPUTE_VER "" CACHE STRING
 # "Semicolon separated list of compute versions to be built against, e.g. '35;61'")


    def source(self):
        self.run("git clone --recursive --branch %s %s" % (self.version, self.repo))        

    def b(self,v):
        if v:
            return "ON"
        return "OFF"

    def build(self):        
        cmake = CMake(self)             
        cmake.definitions["ADD_PKGCONFIG"] = "OFF"        
        cmake.definitions["BUILD_STATIC_LIB"] = "OFF"         
        cmake.definitions["USE_OPENMPI"] = "ON"
        #self.b(self.options.use_openmpi)
        cmake.configure(source_dir=self.name)
        cmake.build()
        

    def package(self):
        self.copy("*.h", dst="include", src="xgboost/include" )
        self.copy("*.h", dst="include", src="xgboost/dmlc-core/include")
        self.copy("*.h", dst="include", src="xgboost/rabit/include")
        self.copy("*.so*", dst="lib", src=".", keep_path=False)
        self.copy("*.a", dst="lib", src=".", keep_path=False)
        if platform.system() == "Windows":
          self.copy("*.dll", dst="bin", src="xgboost/lib", keep_path=False)
          self.copy("*.lib", dst="lib", src="xgboost/lib", keep_path=False)
          self.copy("*.exp", dst="lib", src="xgboost/lib", keep_path=False)
          self.copy("*.dll", dst="bin", src="dmlc-core/Release", keep_path=False)
          self.copy("*.lib", dst="lib", src="dmlc-core/Release", keep_path=False)
          self.copy("*.exp", dst="lib", src="dmlc-core/Release", keep_path=False)          
          self.copy("*.lib", dst="lib", src="src/objxgboost.dir/Release", keep_path=False)



    def package_info(self):         
        self.cpp_info.libs = ["xgboost", "dmlc"]        
        if platform.system() == "Windows":
           self.cpp_info.libs.append("objxgboost")  

        
            
#libdmlc.so  librabit.so  libxgboost.so
#    def cmake_option_bool(self, name, cmake_name):
#        return "-D%s=%s" % (cmake_name, ("ON" if getattr(self.options, name) else "OFF"))




