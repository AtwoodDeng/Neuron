/*
 *  dynamicloader.cpp
 *
 *  This file is part of NEST.
 *
 *  Copyright (C) 2004 The NEST Initiative
 *
 *  NEST is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  NEST is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

/* 
   This file is part of NEST

   dynamicloader.cpp -- Implements the class DynamicLoaderModule
   to allow for dymanically loaded modules for extending the kernel.

   Author(s): 
   Moritz Helias

   First Version: November 2005
*/

#include "dynamicloader.h"

#ifdef HAVE_LIBLTDL

#include <ltdl.h>

#include "network.h"
#include "interpret.h"
#include "integerdatum.h"
#include "stringdatum.h"
#include "dynmodule.h"

#include "model.h"

namespace nest
{

  struct sDynModule {
    std::string name;
    lt_dlhandle handle;
    DynModule *pModule;

    bool operator==(const sDynModule & rhs) const
    {
      return name == rhs.name;
    }

    // operator!= must be implemented explicitly, not all compilers
    // generate it automatically from operator==
    bool operator!=(const sDynModule & rhs) const
    {
      return !(*this == rhs);
    }
  };

  // static member initialization
  Dictionary* DynamicLoaderModule::moduledict_ = new Dictionary();

  vecLinkedModules& DynamicLoaderModule::getLinkedModules()
  {
    static vecLinkedModules lm;  // initialized empty on first call
    return lm;
  }


  /*! At the time when DynamicLoaderModule is constructed, the SLI Interpreter
    and NestModule must be already constructed and initialized.
    DynamicLoaderModule relies on the presence of
    the following SLI datastructures: Name, Dictionary
    and on the nest::NestModule::net.    
  */
  DynamicLoaderModule::DynamicLoaderModule(Network *pNet, SLIInterpreter &interpreter) :
    loadmodule_function(pNet, dyn_modules),
    unloadmodule_function(pNet, dyn_modules)
  {
    assert(pNet != NULL);
    pNet_ = pNet;
    
    interpreter.def("moduledict", new DictionaryDatum(moduledict_));
  }

  DynamicLoaderModule::~DynamicLoaderModule()
  {
    // unload all loaded modules
    for (vecDynModules::iterator it = dyn_modules.begin();
	 it != dyn_modules.end(); it++)
      {
	if (it->handle != NULL) {
	  lt_dlclose(it->handle);
	  it->handle = NULL;
	}
      }
     
    lt_dlexit();
  }

  // The following concerns the new module: -----------------------

  const std::string DynamicLoaderModule::name(void) const
  {
    return std::string("NEST-Dynamic Loader"); // Return name of the module
  }

  const std::string DynamicLoaderModule::commandstring(void) const
  {
    return std::string(""); // Run associated SLI startup script
  }
   
   
  // auxiliary function to check name of module via its pointer
  // we cannot use a & for the second argument, as std::bind2nd() then
  // becomes confused, at least with g++ 4.0.1.
  bool has_name(DynModule const * const m, const std::string n)
  {
    return m->name() == n;
  }
   

  /*
    BeginDocumentation
    Name: Install - Load a dynamic module to extend the functionality.
    Description: 
    Synopsis: (module_name) Install -> handle
  */
  DynamicLoaderModule::LoadModuleFunction::LoadModuleFunction(Network *pNet, vecDynModules &dyn_modules) :
    pNet_(pNet), dyn_modules_(dyn_modules)
  {}

  void DynamicLoaderModule::LoadModuleFunction::execute(SLIInterpreter *i) const
  {
    i->assert_stack_load(1);

    sDynModule new_module;

    new_module.name = getValue<std::string>(i->OStack.top());
    if ( new_module.name.empty() )
      throw DynamicModuleManagementError("Module name must not be empty.");

    // check if module already loaded 
    // this check can happen here, since we are comparing dynamically loaded modules   
    // based on the name given to the Install command
    if ( std::find(dyn_modules_.begin(), dyn_modules_.end(), new_module) 
           != dyn_modules_.end() )
      throw DynamicModuleManagementError(
            "Module '" + new_module.name + "' is loaded already.");

    // try to open the module
    const lt_dlhandle hModule = lt_dlopenext(new_module.name.c_str());

    if ( !hModule )
    {
      char *errstr = (char *) lt_dlerror();
      std::string msg = "Module '" + new_module.name + "' could not be opened.";
      if ( errstr )
	msg += "\nThe dynamic loader returned the following error: '" 
	  + std::string(errstr) + "'.";
      msg += "\n\nPlease check LD_LIBRARY_PATH (OSX: DYLD_LIBRARY_PATH)!";
	throw DynamicModuleManagementError(msg);
    }

    // see if we can find the mod symbol in the module
    DynModule * pModule = (DynModule *) lt_dlsym(hModule, "mod");
    char *errstr = (char *) lt_dlerror();
    if ( errstr )
    {
      lt_dlclose(hModule);  // close module again
      lt_dlerror();  // remove any error caused by lt_dlclose()
      throw DynamicModuleManagementError(
            "Module '" + new_module.name + "' could not be loaded.\n"
            "The dynamic loader returned the following error: '" 
            + std::string(errstr) + "'.");
    }
 
    // check if module is linked in. This test is based on the module name
    // returned by DynModule::name(), since we have no file names for linked modules.
    // We can only perform it after we have loaded the module.
    if (std::find_if(DynamicLoaderModule::getLinkedModules().begin(), 
                     DynamicLoaderModule::getLinkedModules().end(), 
                     std::bind2nd(std::ptr_fun(has_name), pModule->name()))
        != DynamicLoaderModule::getLinkedModules().end())
    {
      lt_dlclose(hModule);  // close module again
      lt_dlerror();  // remove any error caused by lt_dlclose()
      throw DynamicModuleManagementError(
            "Module '" + new_module.name + "' is linked into NEST.\n"
            "You neither need nor may load it dynamically in addition.");
    }

    // all is well an we can register the module with the interpreter
    try {
      pModule->install(std::cerr, i, pNet_);
    }
    catch ( std::exception& e )
    {
      // We should uninstall the partially installed module here, but
      // this must wait for #152.
      // For now, we just close the module file and rethrow the exception.

      lt_dlclose(hModule);
      lt_dlerror();  // remove any error caused by lt_dlclose()
      throw;   // no arg re-throws entire exception, see Stroustrup 14.3.1
    }
    
    // add the handle to list of loaded modules
    new_module.handle = hModule;
    new_module.pModule = pModule;
    dyn_modules_.push_back(new_module);

    i->message(SLIInterpreter::M_INFO, "Install", ("loaded module " + pModule->name()).c_str());

    // remove operand and operator from stack
    i->OStack.pop();
    i->EStack.pop();

    // put handle to module onto stack
    int moduleid = dyn_modules_.size() - 1;
    i->OStack.push(moduleid);
    (*moduledict_)[new_module.name] = moduleid;
    
    // now we can run the module initializer, after we have cleared the EStack
    if ( !pModule->commandstring().empty() )
    {
      Token t = new StringDatum(pModule->commandstring());
      i->OStack.push_move(t);
      Token c = new NameDatum("initialize_module");
      i->EStack.push_move(c);
    }
  }

  /*
    BeginDocumentation
    Name: Uninstall - Uninstall a previously loaded module.
    Description: 
    Synopsis: handle Uninstall
    See: Install
  */
  DynamicLoaderModule::UnloadModuleFunction::UnloadModuleFunction(Network *pNet, vecDynModules &dyn_modules):
    pNet_(pNet), dyn_modules_(dyn_modules) { }

  void DynamicLoaderModule::UnloadModuleFunction::execute(SLIInterpreter *i) const
  {

    if (i->OStack.load() < 1)
      {
	i->raiseerror(i->StackUnderflowError);
	return;
      }
  
    IntegerDatum *mod_id = dynamic_cast<IntegerDatum *>(i->OStack.top().datum());
  
    if (mod_id == NULL) {
      i->message(SLIInterpreter::M_ERROR, "Uninstall", "expected argument of type integer");
      i->raiseerror(i->ArgumentTypeError);
      return;
    }
  
    // check, if given id is in correct range  
    if (static_cast<size_t>(mod_id->get()) >= dyn_modules_.size()
        || dyn_modules_[mod_id->get()].handle == 0) {
      i->message(SLIInterpreter::M_ERROR, "Uninstall", "id is not bound to any loaded module");
      i->raiseerror("ArgumentError");
      return;
    }
    
    // Check if there are any user defined models. We cannot unload in that case.
    if ( pNet_->has_user_models() )
    {
      i->message(SLIInterpreter::M_ERROR, "Uninstall", "Modules cannot be unloaded after use of CopyModel.");
      i->raiseerror("KernelError");
      return;
    }

    // unregister symbols/dictionaries defined in this module
    try {
      DynModule *pMod = dyn_modules_[mod_id->get()].pModule;
      pMod->unregister(i, pNet_);
    }
    catch (KernelException & e)
    {
      i->message(SLIInterpreter::M_ERROR, "Uninstall", "Modules cannot be unloaded.");
      i->message(SLIInterpreter::M_ERROR, "Uninstall", e.what());
      i->raiseerror("KernelError");
      return;
    }
  
	// unload the module
    lt_dlclose(dyn_modules_[mod_id->get()].handle);
    lt_dlerror();  // remove any error caused by lt_dlclose()

    dyn_modules_[mod_id->get()].pModule = 0; // mark as unloaded
    dyn_modules_[mod_id->get()].handle = 0; // mark as unloaded
    dyn_modules_[mod_id->get()].name = ""; // mark as unloaded

    i->message(SLIInterpreter::M_INFO, "Uninstall", "sucessfully unloaded module");

    // remove operand and operator from stack
    i->OStack.pop();
    i->EStack.pop();
  
  }



  void DynamicLoaderModule::init(SLIInterpreter *i)
  {
 
    // bind functions to terminal names 
    i->createcommand("Install", &loadmodule_function);
    i->createcommand("Uninstall", &unloadmodule_function);

    // initialize ltdl library for loading dynamic modules
  
    int dl_error = lt_dlinit();
  
    if (!dl_error)
    {     
      const char *path = getenv ("SLI_MODULE_PATH");
      if (path != NULL)
      {
	i->message(SLIInterpreter::M_INFO, "DynamicLoaderModule::init", "Setting module path to" );
	i->message(SLIInterpreter::M_INFO, "DynamicLoaderModule::init", path );
	
	dl_error = lt_dlsetsearchpath (path);
	if (dl_error)	  
	  i->message(SLIInterpreter::M_ERROR, "DynamicLoaderModule::init", "Could not set dynamic module path.");	    	  
      }
    }
    else
    {
      i->message(SLIInterpreter::M_ERROR, "DynamicLoaderModule::init", "Could not initialize libltdl. No dynamic modules will be avaiable.");
    } 
  }




  int DynamicLoaderModule::registerLinkedModule(DynModule *pModule) 
  {
    assert(pModule != 0);
    getLinkedModules().push_back(pModule);
    return getLinkedModules().size();
  }

  void DynamicLoaderModule::initLinkedModules(SLIInterpreter &interpreter) 
  {

    for (vecLinkedModules::iterator it = getLinkedModules().begin(); 
         it != getLinkedModules().end(); it++) 
    {
      interpreter.message(SLIInterpreter::M_STATUS, "DynamicLoaderModule::initLinkedModules", 
                         "adding linked module");
      interpreter.message(SLIInterpreter::M_STATUS, "DynamicLoaderModule::initLinkedModules", 
                         (*it)->name().c_str());
      interpreter.addlinkeddynmodule(*it, pNet_);
    }
  }


} // namespace nest

#endif // HAVE_LIBLTDL
