package com.mwr.mercury.reflect;

public class Reflector
{

	public Class resolve(String s) throws ClassNotFoundException
	{
		return Class.forName(s);
	}

}
