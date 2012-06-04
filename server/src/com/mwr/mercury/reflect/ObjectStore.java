package com.mwr.mercury.reflect;

import java.util.HashMap;

public class ObjectStore
{
	private HashMap<Integer, Object> hashMap;

	public ObjectStore() {
		hashMap = new HashMap<Integer, Object>();		
	}
	
	public String add(Object value) {
		this.hashMap.put(value.hashCode(), value);
		return value.hashCode() + "";
	}
	
	public Object get(String hash) {
		return this.hashMap.get(Integer.parseInt(hash));
	}
	
	public void remove(String hash) {
		this.hashMap.remove(Integer.parseInt(hash));
	}
	
	public void clear() {
		this.hashMap = new HashMap<Integer, Object>();
	}
}
