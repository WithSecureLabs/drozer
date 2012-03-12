// License: Refer to the README in the root directory

package com.mwr.mercury;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import android.util.Base64;

public class XML
{
	private ArrayList<RequestWrapper> commands;
	
	//Assign toClient to connected client
	XML(String xmlInput)
	{
		commands = parseXML(xmlInput);
	}
	
	//Parse an XML string and create Document
	private Document getXMLdocument(String xml)
	{
	
		Document doc = null;
	
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		try
		{
			DocumentBuilder db = dbf.newDocumentBuilder();
	
			InputSource is = new InputSource();
		    is.setCharacterStream(new StringReader(xml));
		    doc = db.parse(is);
		} catch (ParserConfigurationException e) {
					System.out.println("XML parse error: " + e.getMessage());
			return null;
		} catch (SAXException e) {
			System.out.println("Wrong XML file structure: " + e.getMessage());
	        return null;
		} catch (IOException e) {
			System.out.println("I/O exeption: " + e.getMessage());
					return null;
		}
	
		return doc;
	
	}

//Formulate XML into separate commands
private ArrayList<RequestWrapper> parseXML(String xmlInput)
{

	//The variable to put all commands into
	ArrayList<RequestWrapper> cmdList = new ArrayList<RequestWrapper>();
	
	//Parse XML from input
	Document document = getXMLdocument(xmlInput);
	
	//Get root element - should always be "transmission"
	Element rootElement = document.getDocumentElement();
	
	//Get all commands within transmission
	NodeList commands = rootElement.getElementsByTagName("command");
	
	//Iterate through commands and perform them
	for (int i = 0; i < commands.getLength(); i++)
	{
		
		RequestWrapper cmd = new RequestWrapper();
		
		//Get current command
		Node command = commands.item(i);
		
		//Get all nodes of command
		NodeList nodes = command.getChildNodes();
		
		//Split nodes into their respective fields
		cmd.section = nodes.item(0).getTextContent();
		cmd.function = nodes.item(1).getTextContent();
					
		Node arguments = nodes.item(2);
		
		//Arguments can be of any type, binary or text - so a byte array will suffice
		//Arguments are also base64 decoded and placed into this list
		cmd.argsArray = new ArrayList<ArgumentWrapper>();
		
		//Check if any arguments came with command
	    if (arguments.hasChildNodes())
	    {
	    	//Iterate through arguments and place them in an array
	    	NodeList argumentList = arguments.getChildNodes();
	    	for (int j = 0; j < argumentList.getLength(); j++)
	    	{
	    		ArgumentWrapper tempArg = new ArgumentWrapper();
	    		tempArg.type = argumentList.item(j).getNodeName();
	    		tempArg.value = Base64.decode(argumentList.item(j).getTextContent(), Base64.DEFAULT);
	    		cmd.argsArray.add(tempArg); 
	    	}
	    
	    }
	    
	    //Add each command to the list of commands returned
	    cmdList.add(cmd);

	}
	
	return cmdList;

}

public ArrayList<RequestWrapper> getCommands()
{
	return commands;
}


}
