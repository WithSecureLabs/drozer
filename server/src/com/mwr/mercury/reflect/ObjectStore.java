//License: Refer to the README in the root directory

package com.mwr.mercury.reflect;

import java.util.HashMap;

public class ObjectStore
{
	private HashMap<Integer, Object> hashMap;
	private static ObjectStore instance = null;

	protected ObjectStore() {
		hashMap = new HashMap<Integer, Object>();		
	}
	
	public static ObjectStore getInstance() {
		if(instance == null) {
			instance = new ObjectStore();
		}
		return instance;
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
