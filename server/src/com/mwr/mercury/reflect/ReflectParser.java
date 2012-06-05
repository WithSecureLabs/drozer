package com.mwr.mercury.reflect;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import com.mwr.mercury.Session;

public class ReflectParser
{
	private ObjectStore objStore;
	private Reflector reflector;
	private Responder responder;

	public ReflectParser(Session session) {
		objStore = ObjectStore.getInstance();
		reflector = new Reflector();
		responder = new Responder(session);
	}
	
	public boolean parse(String input) {
		try {
			Document doc = this.getXMLdocument(input);
			Element root = doc.getDocumentElement();
			NodeList nodes = root.getElementsByTagName("reflect");
			
			if(nodes.getLength() == 1) {
				// this is a reflect request, let's parse it
				return parseReflect(nodes.item(0));
			} else {
				// no reflect tag, probably normal comms
				return false;
			}
		} catch (Exception e) {
			// Even though catching all exceptions like this is ugly
			// we need to handle all invalid input as other parts might
			// want to accept this
			return false; 
		}
	}
	
	private boolean parseReflect(Node root) {
		try {
			NodeList childs = root.getChildNodes();
			for(int i = 0; i < childs.getLength(); i++) {
				Node node = childs.item(i);
				if(node.getNodeName().equals("action")) {
					// found an action node, act on it
					return parseAction(node);
				}
			}
			
		} catch (Exception e) {
			// Even though catching all exceptions like this is ugly
			// this is a programming interface and everything needs
			// to be handed off to the other (client) side
			error(e);
		} 
		return true;
	}
	
	
	private boolean parseAction(Node node) throws Exception
	{
		String name = node.getAttributes().getNamedItem("name").getNodeValue();
		if(name.equals("resolve")) {
			return parseResolve(node);
		} else if(name.equals("delete")) {
			return parseDelete(node);
		} else if(name.equals("deleteall")) {
			return parseDeleteAll();
		} else if(name.equals("getprop")) {
			return parseGetProp(node);
		} else if(name.equals("setprop")) {
			return parseSetProp(node);
		} else if(name.equals("construct")) {
			return parseConstruct(node);
		} else if(name.equals("invoke")) {
			return parseInvoke(node);
		} else {
			// TODO: return error
			return true;
		}
	}

	private boolean parseSetProp(Node action)
	{
		NodeList nodes = action.getChildNodes();
		if(nodes.item(0).getNodeName().equals("objref")) {
			String objRef = parseObjRef(nodes.item(0));
			Object obj = objStore.get(objRef);
			if(nodes.item(1).getNodeName().equals("string")) {
				String methodName = nodes.item(1).getTextContent();
				/*
				if( nodes.getLength() > 2 ) {
					Object argument = this.parseArgument(nodes.item(2));
					Object rv = reflector.setProperty(obj, )
					this.sendValue(rv, primitive); // assuming that an object constructor never returns a primitive
				} else {
					//TODO: error on no arguments
				}
				*/
			} else {
				//TODO: error on no name
			}			
		} else {
			//TODO: error on no objref
		}
		return true;
	}

	private boolean parseConstruct(Node action) throws Exception
	{
		NodeList nodes = action.getChildNodes();
		if(nodes.item(0).getNodeName().equals("objref")) {
			String objRef = parseObjRef(nodes.item(0));
			Object obj = objStore.get(objRef);
			if(nodes.item(1).getNodeName().equals("arguments")) {
				Object[] arguments = parseArguments(nodes.item(1));
				Object rv = reflector.construct((Class)obj, arguments);
				this.sendValue(rv, false); // assuming that an object constructor never returns a primitive
			} else {
				//TODO: error on no arguments
			}
		} else {
			//TODO: error on no objref
		}
		return true;
	}
	
	private boolean parseInvoke(Node action) throws Exception
	{
		NodeList nodes = action.getChildNodes();
		if(nodes.item(0).getNodeName().equals("objref")) {
			String objRef = parseObjRef(nodes.item(0));
			Object obj = objStore.get(objRef);
			if(nodes.item(1).getNodeName().equals("string")) {
				String methodName = nodes.item(1).getTextContent();
				if(nodes.item(2).getNodeName().equals("arguments")) {
					Object[] arguments = parseArguments(nodes.item(2));
					boolean primitive = reflector.doesReturnPrimitive(obj, methodName, arguments);
					Object rv = reflector.invoke(obj, methodName, arguments);
					this.sendValue(rv, primitive); // assuming that an object constructor never returns a primitive
				} else {
					//TODO: error on no arguments
				}
			} else {
				//TODO: error on no name
			}			
		} else {
			//TODO: error on no objref
		}
		return true;
	}

	private Object[] parseArguments(Node arguments)
	{
		NodeList nodes = arguments.getChildNodes();
		List<Object> resolved = new ArrayList<Object>();
		for(int i=0; i<nodes.getLength(); i++) {
			Object arg = parseArgument(nodes.item(i));
			resolved.add(arg);
		}
		return resolved.toArray();
	}

	private Object parseArgument(Node argument)
	{
		String type = argument.getNodeName();
		if(type.equals("objref")) {
			String ref = parseObjRef(argument);
			return objStore.get(ref);
		} else if (type.equals("string")) {
			String s = parseString(argument);
			return s;
		} else if (type.equals("primitive")) {
			Object p = parsePrimitive(argument);
			return p;
		} else if (type.equals("array")) {
			Object a = parseArray(argument);
			return a;
		}
		return null;
	}

	private Object parseArray(Node argument)
	{
		String type = argument.getAttributes().getNamedItem("type").getNodeValue();
		ArrayList<String> values = new ArrayList<String>();
		NodeList nodes = argument.getChildNodes();
		for(int i=0; i<nodes.getLength(); i++) {
			values.add(nodes.item(i).getTextContent());
		}
		String[] valuesArray = (String[])values.toArray();
		if(type.equals("string")) {
			return valuesArray;
		} else if(type.equals("objref")) {
			return createObjectArray(valuesArray);
		} else {
			// primitive array
			return reflector.createPrimitiveArray(valuesArray, type);
		}
	}

	private Object createObjectArray(String[] objRefs)
	{
		Object[] objs = new Object[objRefs.length];
		int i = 0;
		for(String objRef : objRefs) {
			objs[i++] = objStore.get(objRef);
		}
		return objs;
	}

	private Object parsePrimitive(Node argument)
	{
		String type = argument.getAttributes().getNamedItem("type").getNodeValue();
		String value = argument.getTextContent();
		// byte, short, int, long, float, double, boolean, char
		if(type.equals("byte")) {
			return Byte.parseByte(value);
		} else if(type.equals("short")) {
			return Short.parseShort(value);
		} else if(type.equals("int")) {
			return Integer.parseInt(value);
		} else if(type.equals("long")) {
			return Long.parseLong(value);
		} else if(type.equals("float")) {
			return Float.parseFloat(value);
		} else if(type.equals("double")) {
			return Double.parseDouble(value);
		} else if(type.equals("boolean")) {
			return Boolean.parseBoolean(value);
		} else if(type.equals("char")) {
			return Character.valueOf(value.charAt(0));
		}
		return null;
	}

	private boolean parseGetProp(Node action) throws Exception
	{
		NodeList nodes = action.getChildNodes();
		if(nodes.item(0).getNodeName().equals("objref")) {
			String objRef = parseObjRef(nodes.item(0));
			Object obj = objStore.get(objRef);
			if(nodes.item(1).getNodeName().equals("string")) {
				String name = parseObjRef(nodes.item(1));
				Object retObj = reflector.getProperty(obj, name);	
				boolean primitive = reflector.isPropertyPrimitive(obj, name);
				sendValue(retObj, primitive);
			}
			else {
				//TODO: error on no string
			}
		} else {
			// TODO: error on no objref
		}
		return true;
	}

	private void sendValue(Object retObj, boolean primitive)
	{
		if(retObj.getClass().equals(String.class)) {
			responder.sendString((String) retObj);
		} else if(retObj.getClass().isArray() && retObj instanceof Object[]) {
			responder.sendArray((Object[])retObj);
		} else if(retObj.getClass().isArray()) {
			responder.sendPrimitiveArray((Object[])retObj);
		} else if(!primitive) {
			String retObjRef = objStore.add(retObj);
			responder.sendObjRef(retObjRef);
		} else {
			responder.sendPrimitive(retObj);
		}
	}

	private boolean parseDeleteAll()
	{
		objStore.clear();
		return true;
	}

	private boolean parseResolve(Node action) throws ClassNotFoundException
	{
		NodeList nodes = action.getChildNodes();
		for(int i=0; i<nodes.getLength(); i++) {
			Node node = nodes.item(i);
			if(node.getNodeName().equals("string")) {
				String s = parseString(node);
				Class clazz = reflector.resolve(s);
				String objRef = objStore.add(clazz);
				responder.sendObjRef(objRef);
				return true;
			}
		}
		//TODO: return error
		return true;
	}
	
	private boolean parseDelete(Node action)
	{
		NodeList nodes = action.getChildNodes();
		for(int i=0; i<nodes.getLength(); i++) {
			Node node = nodes.item(i);
			if(node.getNodeName().equals("objref")) {
				String s = parseObjRef(node);
				objStore.remove(s);
			}
		}
		//TODO: return error
		return true;
	}

	private String parseObjRef(Node node)
	{
		return parseString(node);
	}

	private String parseString(Node node)
	{
		String s = node.getTextContent();
		return s;
	}

	private void error(Exception e)
	{
		String objRef = objStore.add(e);
		responder.sendError(e, objRef);
	}

	// It is fine for us to hand on the exception, as this is merely a programming interface
	private Document getXMLdocument(String xml) throws ParserConfigurationException, SAXException, IOException
	{
		Document doc = null;
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		// TODO: we probably only need one document builder for an instance
		DocumentBuilder db = dbf.newDocumentBuilder();
		InputSource is = new InputSource();
		is.setCharacterStream(new StringReader(xml));
		doc = db.parse(is);
		return doc;	
	}
}
