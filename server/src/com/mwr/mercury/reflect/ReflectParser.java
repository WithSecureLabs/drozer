package com.mwr.mercury.reflect;

import java.io.IOException;
import java.io.StringReader;

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
		objStore = new ObjectStore();
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
	
	
	private boolean parseAction(Node node) throws ClassNotFoundException
	{
		String name = node.getAttributes().getNamedItem("name").getNodeValue();
		if(name.equals("resolve")) {
			// TODO: resolve
			return parseResolve(node);
		}
		// TODO: return error
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
