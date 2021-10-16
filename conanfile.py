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
        if platform.system() == "Windows": #MINGW users be aware
           self.cpp_info.libs.append("objxgboost")  

                    




