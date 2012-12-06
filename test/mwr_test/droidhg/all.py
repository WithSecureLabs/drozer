import unittest

from mwr_test.droidhg import android_test, console, modules, reflection, repoman
from mwr_test.droidhg.api import builders, frame_test

all_tests = unittest.TestSuite((
  builders.reflection_request_test.ReflectionRequestFactoryTestSuite(),
  builders.reflection_response_test.ReflectionResponseFactoryTestSuite(),
  builders.system_request_test.SystemRequestFactoryTestSuite(),
  builders.system_response_test.SystemResponseFactoryTestSuite(),

  #api.formatters.system_response_test

  frame_test.FrameTestSuite(),
  #api.reflection_message_test
  #api.system_message_test

  console.coloured_stream_test.ColouredStreamTestSuite(),
  #console.console_test
  #console.sequencer_test
  #console.server_test

  modules.module_base_test.ModuleTestSuite(),
  #modules.common.assets
  #modules.common.busy_box
  #modules.common.file_system
  #modules.common.filtering
  #modules.common.formatter
  #modules.common.loader
  #modules.common.package_manager
  #modules.common.path_completion
  #modules.common.provider
  #modules.common.shell
  #modules.common.strings
  #modules.common.vulnerability
  #modules.common.zip_file

  reflection.reflected_array_test.ReflectedArrayTestSuite(),
  reflection.reflected_null_test.ReflectedNullTestSuite(),
  reflection.reflected_object_test.ReflectedObjectTestSuite(),
  reflection.reflected_string_test.ReflectedStringTestSuite(),
  reflection.reflected_primitive_test.ReflectedPrimitiveTestSuite(),
  reflection.reflected_type_test.ReflectedTypeTestSuite(),
  reflection.reflector_test.ReflectorTestSuite(),
  
  repoman.repository_test.RepositoryTestSuite(),

  android_test.IntentTestSuite() ))
  #device_test
  #session_test

unittest.TextTestRunner().run(all_tests)
