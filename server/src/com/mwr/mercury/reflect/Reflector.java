package com.mwr.mercury.reflect;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

public class Reflector
{

	public Class resolve(String s) throws ClassNotFoundException
	{
		return Class.forName(s);
	}

	public Object getProperty(Object obj, String name) throws Exception
	{
		if(obj instanceof Class) {
			// static field
			return ((Class) obj).getField(name).get(null);
		} else {
			Field field = obj.getClass().getField(name);
			return field.get(obj);
		}
	}

	public boolean isPropertyPrimitive(Object obj, String name) throws SecurityException, NoSuchFieldException
	{
		if(obj instanceof Class) {
			// static field
			return ((Class) obj).getField(name).getType().isPrimitive();
		} else {
			Field field = obj.getClass().getField(name);
			return field.getType().isPrimitive();
		}
	}

	public Object createPrimitiveArray(String[] valuesArray, String type)
	{
		// byte, short, int, long, float, double, boolean, char
		int len = valuesArray.length;
		if(type.equals("byte")) {
			byte[] array = new byte[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Byte.parseByte(value);
			return array;
		} else if(type.equals("short")) {
			short[] array = new short[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Short.parseShort(value);
			return array;
		} else if(type.equals("int")) {
			int[] array = new int[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Integer.parseInt(value);
			return array;
		} else if(type.equals("long")) {
			long[] array = new long[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Long.parseLong(value);
			return array;
		} else if(type.equals("float")) {
			float[] array = new float[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Float.parseFloat(value);
			return array;
		} else if(type.equals("double")) {
			double[] array = new double[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Double.parseDouble(value);
			return array;
		} else if(type.equals("boolean")) {
			boolean[] array = new boolean[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Boolean.parseBoolean(value);
			return array;
		} else if(type.equals("char")) {
			char[] array = new char[len];
			int i = 0;
			for(String value : valuesArray)
				array[i++] = Character.valueOf(value.charAt(0));
			return array;
		}
		return null;
	}

	public Object construct(Class obj, Object[] a) throws Exception
	{
		int argc = a.length;
		Class[] p = getParameterType(a);
		Constructor con;
		// Yes, this is ugly
		switch(argc) {
		case 0:  
			con = obj.getConstructor();
			return con.newInstance();
		case 1:  
			con = obj.getConstructor(p[0]);
			return con.newInstance(a[0]);
		case 2:  
			con = obj.getConstructor(p[0],p[1]);
			return con.newInstance(a[0], a[1]);
		case 3:  
			con = obj.getConstructor(p[0],p[1],p[2]);
			return con.newInstance(a[0],a[1],a[2]);
		case 4:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3]);
			return con.newInstance(a[0],a[1],a[2],a[3]);
		case 5:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4]);
		case 6:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4],p[5]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4],a[5]);
		case 7:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4],p[5],p[6]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4],a[5],a[6]);
		case 8:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]);
		case 9:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8]);
		case 10:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9]);
		case 11:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10]);
		case 12:  
			con = obj.getConstructor(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11]);
			return con.newInstance(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11]);
		}
		return null;
	}

	private Class[] getParameterType(Object[] arguments)
	{
		Class[] ret = new Class[arguments.length];
		int i = 0;
		// byte, short, int, long, float, double, boolean, char
		for(Object arg : arguments) {
			if(arg instanceof Integer) ret[i++] = Integer.TYPE;
			else if(arg instanceof Short) ret[i++] = Short.TYPE;
			else if(arg instanceof Byte) ret[i++] = Byte.TYPE;
			else if(arg instanceof Long) ret[i++] = Long.TYPE;
			else if(arg instanceof Float) ret[i++] = Float.TYPE;
			else if(arg instanceof Double) ret[i++] = Double.TYPE;
			else if(arg instanceof Boolean) ret[i++] = Boolean.TYPE;
			else if(arg instanceof Character) ret[i++] = Character.TYPE;
			else ret[i++] = arg.getClass();
		}
		return ret;
	}

	public Object invoke(Object obj, String methodName, Object[] a) throws Exception
	{
		Class cls = null;
		Class[] p = getParameterType(a);
		if(obj instanceof Class && isStatic(obj, methodName, p)) {
			// static method
			cls = (Class)obj;
			obj = null;
		} else {
			cls = obj.getClass();
		}
		try{
			Method m = getMethod(cls, methodName, p);
			switch(a.length) {
			case 0:
				return m.invoke(obj);
			case 1:
				return m.invoke(obj,a[0]);
			case 2:
				return m.invoke(obj,a[0], a[1]);
			case 3:
				return m.invoke(obj,a[0],a[1],a[2]);
			case 4:
				return m.invoke(obj,a[0],a[1],a[2],a[3]);
			case 5:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4]);
			case 6:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4],a[5]);
			case 7:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4],a[5],a[6]);
			case 8:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]);
			case 9:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8]);
			case 10:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9]);
			case 11:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10]);
			case 12:
				return m.invoke(obj,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11]);
			}
			return null;
		} catch (InvocationTargetException e) {
			throw (Exception) e.getCause();
		}
	}

	public boolean doesReturnPrimitive(Object obj, String methodName,
			Object[] arguments) throws Exception
	{
		Class cls = null;
		Class[] p = getParameterType(arguments);
		if(obj instanceof Class && isStatic(obj, methodName, p)) {
			// static method
			cls = (Class)obj;
			obj = null;
		} else {
			cls = obj.getClass();
		}
		Method m = getMethod(cls, methodName, p);
		return m.getReturnType().isPrimitive();
	}

	private boolean isStatic(Object obj, String methodName, Class[] arguments)
	{
		Method m = null;
		try {
			m = getMethod((Class) obj, methodName, arguments);
		} catch(NoSuchMethodException e) {
			return false;
		}
		if(Modifier.isStatic(m.getModifiers()))
			return true;
		return false;
	}

	private Method getMethod(Class c, String m, Class[] a) throws SecurityException, NoSuchMethodException
	{
		switch(a.length) {
		case 0:
			return c.getMethod(m, null);
		case 1:
			return c.getMethod(m,a[0]);
		case 2:
			return c.getMethod(m,a[0], a[1]);
		case 3:
			return c.getMethod(m,a[0],a[1],a[2]);
		case 4:
			return c.getMethod(m,a[0],a[1],a[2],a[3]);
		case 5:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4]);
		case 6:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4],a[5]);
		case 7:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4],a[5],a[6]);
		case 8:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]);
		case 9:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8]);
		case 10:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9]);
		case 11:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10]);
		case 12:
			return c.getMethod(m,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11]);
		}
		return null;
	}

	public void setProperty(Object obj, String name, Object argument) throws IllegalArgumentException, SecurityException, IllegalAccessException, NoSuchFieldException
	{
		if(obj instanceof Class) {
			// static field
			((Class) obj).getField(name).set(null, argument);
		} else {
			Field field = obj.getClass().getField(name);
			field.set(obj, argument);
		}
	}

}
