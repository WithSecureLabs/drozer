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
		session.startTransmission();
		session.send(out, false);
		session.endTransmission();
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
		//TODO: encode
		String response = "<return-value type=\"error\" errormsg=\""+message+"\">"+ref+"</return-value>";
		send(response);
	}

	public void sendPrimitive(Object obj)
	{
		String primitive = createPrimitive(obj);
		sendResponse(primitive);
	}

	private String createPrimitive(Object obj)
	{
		// byte, short, int, long, float, double, boolean, char
		String type="unknown";
		String value=obj.toString();
		if(obj.getClass().equals(Integer.class)) {
			type="int";
		} else if(obj.getClass().equals(Byte.class)) {
			type="byte";
		} else if(obj.getClass().equals(Short.class)) {
			type="short";
		} else if(obj.getClass().equals(Long.class)) {
			type="long";
		} else if(obj.getClass().equals(Float.class)) {
			type="float";
		} else if(obj.getClass().equals(Double.class)) {
			type="double";
		} else if(obj.getClass().equals(Boolean.class)) {
			type="boolean";
		} else if(obj.getClass().equals(Character.class)) {
			//TODO encode
			type="char";
		}
		return "<primitive type=\""+type+"\">"+value+"</primitive>";
	}

	public void sendString(String s)
	{
		String tag = createString(s);
		sendResponse(tag);
	}

	private String createString(String s)
	{
		//TODO encode
		return "<string>"+s+"</string>";
	}

	public void sendArray(Object[] objArray)
	{
		String array = createArray(objArray);
		sendResponse(array);
	}

	private String createArray(Object[] objArray)
	{
		String out = "<array type=\"objref\">";
		ObjectStore objStore = ObjectStore.getInstance();
		for(Object o: objArray) {
			String ref = objStore.add(o);
			out += this.createObjRef(ref);
		}
		out += "</array>";
		return out;
	}

	public void sendPrimitiveArray(Object primArray)
	{
		String array = createPrimitiveArray(primArray);
		sendResponse(array);
	}

	private String createPrimitiveArray(Object primArray)
	{
		String type = "unknown";
		String out = "";
		// byte, short, int, long, float, double, boolean, char
		if(primArray instanceof byte[]) {
			type = "byte";
			for(byte e: (byte[])primArray) {
				out += createPrimitive(e);
			}
		} else if(primArray instanceof short[]) {
			type = "short";
			for(short e: (short[])primArray) {
				out += createPrimitive(e);
			}
		} else if(primArray instanceof int[]) {
			type = "int";
			for(int e: (int[])primArray) {
				out += createPrimitive(e);
			}
		} else if(primArray instanceof long[]) {
			type = "long";
			for(long e: (long[])primArray) {
				out += createPrimitive(e);
			}
		} else if(primArray instanceof float[]) {
			type = "float";
			for(float e: (float[])primArray) {
				out += createPrimitive(e);
			}
		} else if(primArray instanceof double[]) {
			type = "double";
			for(double e: (double[])primArray) {
				out += createPrimitive(e);
			}
		} else if(primArray instanceof boolean[]) {
			type = "boolean";
			for(boolean e: (boolean[])primArray) {
				out += createPrimitive(e);
			}
		} else if(primArray instanceof char[]) {
			type = "char";
			for(char e: (char[])primArray) {
				out += createPrimitive(e);
			}
		}
		return "<array type=\""+type+"\">" + out + "</array>";
	}

}
