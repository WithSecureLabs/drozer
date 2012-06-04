package com.mwr.mercury.reflect;

import com.mwr.mercury.Session;

public class Responder
{
	
	private Session session;

	public Responder(Session session)
	{
		this.session = session;
	}

	public void sendResponse(String content) {
		String response = "<return-value type=\"success\">" + content + "</return-value>";
		send(response);
	}
	
	public void send(String response) {
		String out = "<reflect>" + response + "</reflect>\n";
		session.send(out, false);
	}
	
	public String createObjRef(String objRef) {
		return "<objref>" + objRef + "</objref>";
	}

	public void sendObjRef(String objRef)
	{
		sendResponse(createObjRef(objRef));
	}

	public void sendError(Exception e, String objRef)
	{
		String message = e.toString();
		String ref = createObjRef(objRef);
		String response = "<return-value type=\"error\" errormsg=\""+message+"\">"+ref+"</return-value>";
		send(response);
	}

}
