# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eprotobuf.proto\x12\x19\x63om.WithSecure.jsolar.api\"\xf5\x1f\n\x07Message\x12\n\n\x02id\x18\x01 \x02(\x05\x12<\n\x04type\x18\x02 \x02(\x0e\x32..com.WithSecure.jsolar.api.Message.MessageType\x12H\n\x0esystem_request\x18\x05 \x01(\x0b\x32\x30.com.WithSecure.jsolar.api.Message.SystemRequest\x12J\n\x0fsystem_response\x18\x06 \x01(\x0b\x32\x31.com.WithSecure.jsolar.api.Message.SystemResponse\x12P\n\x12reflection_request\x18\x07 \x01(\x0b\x32\x34.com.WithSecure.jsolar.api.Message.ReflectionRequest\x12R\n\x13reflection_response\x18\x08 \x01(\x0b\x32\x35.com.WithSecure.jsolar.api.Message.ReflectionResponse\x1a\xfc\n\n\x11ReflectionRequest\x12\x12\n\nsession_id\x18\x01 \x02(\t\x12N\n\x04type\x18\x02 \x02(\x0e\x32@.com.WithSecure.jsolar.api.Message.ReflectionRequest.RequestType\x12M\n\x07resolve\x18\x03 \x01(\x0b\x32<.com.WithSecure.jsolar.api.Message.ReflectionRequest.Resolve\x12Q\n\tconstruct\x18\x04 \x01(\x0b\x32>.com.WithSecure.jsolar.api.Message.ReflectionRequest.Construct\x12K\n\x06invoke\x18\x05 \x01(\x0b\x32;.com.WithSecure.jsolar.api.Message.ReflectionRequest.Invoke\x12V\n\x0cset_property\x18\x06 \x01(\x0b\x32@.com.WithSecure.jsolar.api.Message.ReflectionRequest.SetProperty\x12V\n\x0cget_property\x18\x07 \x01(\x0b\x32@.com.WithSecure.jsolar.api.Message.ReflectionRequest.GetProperty\x12K\n\x06\x64\x65lete\x18\x08 \x01(\x0b\x32;.com.WithSecure.jsolar.api.Message.ReflectionRequest.Delete\x1a\x1c\n\x07Resolve\x12\x11\n\tclassname\x18\x01 \x01(\t\x1a\x8e\x01\n\tConstruct\x12\x42\n\x06object\x18\x01 \x01(\x0b\x32\x32.com.WithSecure.jsolar.api.Message.ObjectReference\x12=\n\x08\x61rgument\x18\x02 \x03(\x0b\x32+.com.WithSecure.jsolar.api.Message.Argument\x1a\x9b\x01\n\x06Invoke\x12\x42\n\x06object\x18\x01 \x01(\x0b\x32\x32.com.WithSecure.jsolar.api.Message.ObjectReference\x12\x0e\n\x06method\x18\x02 \x01(\t\x12=\n\x08\x61rgument\x18\x03 \x03(\x0b\x32+.com.WithSecure.jsolar.api.Message.Argument\x1a\x9f\x01\n\x0bSetProperty\x12\x42\n\x06object\x18\x01 \x01(\x0b\x32\x32.com.WithSecure.jsolar.api.Message.ObjectReference\x12\x10\n\x08property\x18\x02 \x01(\t\x12:\n\x05value\x18\x03 \x01(\x0b\x32+.com.WithSecure.jsolar.api.Message.Argument\x1a\x63\n\x0bGetProperty\x12\x42\n\x06object\x18\x01 \x01(\x0b\x32\x32.com.WithSecure.jsolar.api.Message.ObjectReference\x12\x10\n\x08property\x18\x02 \x01(\t\x1aL\n\x06\x44\x65lete\x12\x42\n\x06object\x18\x01 \x01(\x0b\x32\x32.com.WithSecure.jsolar.api.Message.ObjectReference\"u\n\x0bRequestType\x12\x0b\n\x07RESOLVE\x10\x01\x12\r\n\tCONSTRUCT\x10\x02\x12\n\n\x06INVOKE\x10\x03\x12\x10\n\x0cSET_PROPERTY\x10\x04\x12\x10\n\x0cGET_PROPERTY\x10\x05\x12\n\n\x06\x44\x45LETE\x10\x06\x12\x0e\n\nDELETE_ALL\x10\x07\x1a\x86\x02\n\x12ReflectionResponse\x12\x12\n\nsession_id\x18\x01 \x02(\t\x12T\n\x06status\x18\x02 \x02(\x0e\x32\x44.com.WithSecure.jsolar.api.Message.ReflectionResponse.ResponseStatus\x12;\n\x06result\x18\x03 \x01(\x0b\x32+.com.WithSecure.jsolar.api.Message.Argument\x12\x14\n\x0c\x65rrormessage\x18\x08 \x01(\t\"3\n\x0eResponseStatus\x12\x0b\n\x07SUCCESS\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x12\t\n\x05\x46\x41TAL\x10\x03\x1a\xdf\x02\n\rSystemRequest\x12P\n\x04type\x18\x01 \x02(\x0e\x32<.com.WithSecure.jsolar.api.Message.SystemRequest.RequestType:\x04PING\x12\x39\n\x06\x64\x65vice\x18\x05 \x01(\x0b\x32).com.WithSecure.jsolar.api.Message.Device\x12\x12\n\nsession_id\x18\x07 \x01(\t\x12\x10\n\x08password\x18\x08 \x01(\t\"\x9a\x01\n\x0bRequestType\x12\x08\n\x04PING\x10\x01\x12\x0f\n\x0b\x42IND_DEVICE\x10\x02\x12\x11\n\rUNBIND_DEVICE\x10\x03\x12\x10\n\x0cLIST_DEVICES\x10\x04\x12\x11\n\rSTART_SESSION\x10\x05\x12\x10\n\x0cSTOP_SESSION\x10\x06\x12\x13\n\x0fRESTART_SESSION\x10\x07\x12\x11\n\rLIST_SESSIONS\x10\x08\x1a\xe4\x03\n\x0eSystemResponse\x12L\n\x04type\x18\x01 \x02(\x0e\x32>.com.WithSecure.jsolar.api.Message.SystemResponse.ResponseType\x12P\n\x06status\x18\x02 \x02(\x0e\x32@.com.WithSecure.jsolar.api.Message.SystemResponse.ResponseStatus\x12:\n\x07\x64\x65vices\x18\x06 \x03(\x0b\x32).com.WithSecure.jsolar.api.Message.Device\x12\x12\n\nsession_id\x18\x07 \x01(\t\x12\x15\n\rerror_message\x18\x08 \x01(\t\x12<\n\x08sessions\x18\t \x03(\x0b\x32*.com.WithSecure.jsolar.api.Message.Session\"c\n\x0cResponseType\x12\x08\n\x04PONG\x10\x01\x12\t\n\x05\x42OUND\x10\x02\x12\x0b\n\x07UNBOUND\x10\x03\x12\x0f\n\x0b\x44\x45VICE_LIST\x10\x04\x12\x0e\n\nSESSION_ID\x10\x05\x12\x10\n\x0cSESSION_LIST\x10\x06\"(\n\x0eResponseStatus\x12\x0b\n\x07SUCCESS\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x1a\x8c\x03\n\x08\x41rgument\x12N\n\x04type\x18\x01 \x02(\x0e\x32\x38.com.WithSecure.jsolar.api.Message.Argument.ArgumentType:\x06STRING\x12?\n\tprimitive\x18\x02 \x01(\x0b\x32,.com.WithSecure.jsolar.api.Message.Primitive\x12\x0e\n\x06string\x18\x03 \x01(\t\x12\x42\n\x06object\x18\x04 \x01(\x0b\x32\x32.com.WithSecure.jsolar.api.Message.ObjectReference\x12\x37\n\x05\x61rray\x18\x05 \x01(\x0b\x32(.com.WithSecure.jsolar.api.Message.Array\x12\x0c\n\x04\x64\x61ta\x18\x06 \x01(\x0c\"T\n\x0c\x41rgumentType\x12\x08\n\x04NULL\x10\x01\x12\r\n\tPRIMITIVE\x10\x02\x12\n\n\x06STRING\x10\x03\x12\n\n\x06OBJECT\x10\x04\x12\t\n\x05\x41RRAY\x10\x05\x12\x08\n\x04\x44\x41TA\x10\x06\x1a\xce\x01\n\x05\x41rray\x12H\n\x04type\x18\x01 \x02(\x0e\x32\x32.com.WithSecure.jsolar.api.Message.Array.ArrayType:\x06STRING\x12<\n\x07\x65lement\x18\x02 \x03(\x0b\x32+.com.WithSecure.jsolar.api.Message.Argument\"=\n\tArrayType\x12\r\n\tPRIMITIVE\x10\x01\x12\n\n\x06STRING\x10\x02\x12\n\n\x06OBJECT\x10\x03\x12\t\n\x05\x41RRAY\x10\x04\x1aK\n\x06\x44\x65vice\x12\n\n\x02id\x18\x01 \x02(\t\x12\x14\n\x0cmanufacturer\x18\x02 \x02(\t\x12\r\n\x05model\x18\x03 \x02(\t\x12\x10\n\x08software\x18\x04 \x02(\t\x1a$\n\x0fObjectReference\x12\x11\n\treference\x18\x01 \x01(\x05\x1a\xac\x02\n\tPrimitive\x12H\n\x04type\x18\x01 \x02(\x0e\x32:.com.WithSecure.jsolar.api.Message.Primitive.PrimitiveType\x12\x0c\n\x04\x62ool\x18\x02 \x01(\x08\x12\x0b\n\x03int\x18\x03 \x01(\x05\x12\x0c\n\x04long\x18\x04 \x01(\x03\x12\r\n\x05\x66loat\x18\x05 \x01(\x02\x12\x0c\n\x04\x62yte\x18\x06 \x01(\x05\x12\r\n\x05short\x18\x07 \x01(\x05\x12\x0e\n\x06\x64ouble\x18\x08 \x01(\x01\x12\x0c\n\x04\x63har\x18\t \x01(\x05\"b\n\rPrimitiveType\x12\x08\n\x04\x42OOL\x10\x01\x12\x07\n\x03INT\x10\x02\x12\x08\n\x04LONG\x10\x03\x12\t\n\x05\x46LOAT\x10\x04\x12\x08\n\x04\x42YTE\x10\x05\x12\t\n\x05SHORT\x10\x06\x12\n\n\x06\x44OUBLE\x10\x07\x12\x08\n\x04\x43HAR\x10\x08\x1a(\n\x07Session\x12\n\n\x02id\x18\x01 \x02(\t\x12\x11\n\tdevice_id\x18\x02 \x02(\t\"g\n\x0bMessageType\x12\x12\n\x0eSYSTEM_REQUEST\x10\x01\x12\x13\n\x0fSYSTEM_RESPONSE\x10\x02\x12\x16\n\x12REFLECTION_REQUEST\x10\x03\x12\x17\n\x13REFLECTION_RESPONSE\x10\x04\x42\x02H\x01')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protobuf_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'H\001'
  _globals['_MESSAGE']._serialized_start=46
  _globals['_MESSAGE']._serialized_end=4131
  _globals['_MESSAGE_REFLECTIONREQUEST']._serialized_start=448
  _globals['_MESSAGE_REFLECTIONREQUEST']._serialized_end=1852
  _globals['_MESSAGE_REFLECTIONREQUEST_RESOLVE']._serialized_start=1061
  _globals['_MESSAGE_REFLECTIONREQUEST_RESOLVE']._serialized_end=1089
  _globals['_MESSAGE_REFLECTIONREQUEST_CONSTRUCT']._serialized_start=1092
  _globals['_MESSAGE_REFLECTIONREQUEST_CONSTRUCT']._serialized_end=1234
  _globals['_MESSAGE_REFLECTIONREQUEST_INVOKE']._serialized_start=1237
  _globals['_MESSAGE_REFLECTIONREQUEST_INVOKE']._serialized_end=1392
  _globals['_MESSAGE_REFLECTIONREQUEST_SETPROPERTY']._serialized_start=1395
  _globals['_MESSAGE_REFLECTIONREQUEST_SETPROPERTY']._serialized_end=1554
  _globals['_MESSAGE_REFLECTIONREQUEST_GETPROPERTY']._serialized_start=1556
  _globals['_MESSAGE_REFLECTIONREQUEST_GETPROPERTY']._serialized_end=1655
  _globals['_MESSAGE_REFLECTIONREQUEST_DELETE']._serialized_start=1657
  _globals['_MESSAGE_REFLECTIONREQUEST_DELETE']._serialized_end=1733
  _globals['_MESSAGE_REFLECTIONREQUEST_REQUESTTYPE']._serialized_start=1735
  _globals['_MESSAGE_REFLECTIONREQUEST_REQUESTTYPE']._serialized_end=1852
  _globals['_MESSAGE_REFLECTIONRESPONSE']._serialized_start=1855
  _globals['_MESSAGE_REFLECTIONRESPONSE']._serialized_end=2117
  _globals['_MESSAGE_REFLECTIONRESPONSE_RESPONSESTATUS']._serialized_start=2066
  _globals['_MESSAGE_REFLECTIONRESPONSE_RESPONSESTATUS']._serialized_end=2117
  _globals['_MESSAGE_SYSTEMREQUEST']._serialized_start=2120
  _globals['_MESSAGE_SYSTEMREQUEST']._serialized_end=2471
  _globals['_MESSAGE_SYSTEMREQUEST_REQUESTTYPE']._serialized_start=2317
  _globals['_MESSAGE_SYSTEMREQUEST_REQUESTTYPE']._serialized_end=2471
  _globals['_MESSAGE_SYSTEMRESPONSE']._serialized_start=2474
  _globals['_MESSAGE_SYSTEMRESPONSE']._serialized_end=2958
  _globals['_MESSAGE_SYSTEMRESPONSE_RESPONSETYPE']._serialized_start=2817
  _globals['_MESSAGE_SYSTEMRESPONSE_RESPONSETYPE']._serialized_end=2916
  _globals['_MESSAGE_SYSTEMRESPONSE_RESPONSESTATUS']._serialized_start=2066
  _globals['_MESSAGE_SYSTEMRESPONSE_RESPONSESTATUS']._serialized_end=2106
  _globals['_MESSAGE_ARGUMENT']._serialized_start=2961
  _globals['_MESSAGE_ARGUMENT']._serialized_end=3357
  _globals['_MESSAGE_ARGUMENT_ARGUMENTTYPE']._serialized_start=3273
  _globals['_MESSAGE_ARGUMENT_ARGUMENTTYPE']._serialized_end=3357
  _globals['_MESSAGE_ARRAY']._serialized_start=3360
  _globals['_MESSAGE_ARRAY']._serialized_end=3566
  _globals['_MESSAGE_ARRAY_ARRAYTYPE']._serialized_start=3505
  _globals['_MESSAGE_ARRAY_ARRAYTYPE']._serialized_end=3566
  _globals['_MESSAGE_DEVICE']._serialized_start=3568
  _globals['_MESSAGE_DEVICE']._serialized_end=3643
  _globals['_MESSAGE_OBJECTREFERENCE']._serialized_start=3645
  _globals['_MESSAGE_OBJECTREFERENCE']._serialized_end=3681
  _globals['_MESSAGE_PRIMITIVE']._serialized_start=3684
  _globals['_MESSAGE_PRIMITIVE']._serialized_end=3984
  _globals['_MESSAGE_PRIMITIVE_PRIMITIVETYPE']._serialized_start=3886
  _globals['_MESSAGE_PRIMITIVE_PRIMITIVETYPE']._serialized_end=3984
  _globals['_MESSAGE_SESSION']._serialized_start=3986
  _globals['_MESSAGE_SESSION']._serialized_end=4026
  _globals['_MESSAGE_MESSAGETYPE']._serialized_start=4028
  _globals['_MESSAGE_MESSAGETYPE']._serialized_end=4131
# @@protoc_insertion_point(module_scope)
